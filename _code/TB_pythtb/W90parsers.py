import re
import numpy as np
import pandas as pd
from typing import List, Tuple
from ase import Atoms

# -------------------- Utility functions --------------------
def periodic_distance(r1: np.ndarray, r2: np.ndarray, cell: np.ndarray) -> float:
    """Minimum-image distance between two Cartesian points using cell (rows = a1,a2,a3)."""
    # Solve for fractional: cell^T * frac = cart  => frac = (cell^T)^{-1} * cart
    frac1 = np.linalg.solve(cell.T, r1)
    frac2 = np.linalg.solve(cell.T, r2)
    diff = frac1 - frac2
    diff -= np.round(diff)   # minimum image
    cart = cell.T @ diff
    return np.linalg.norm(cart)

def find_closest_atom(wc: np.ndarray, atom_positions: np.ndarray, cell: np.ndarray) -> int:
    """Return index of nearest atom to wc (using periodic distances)."""
    dists = [periodic_distance(wc, pos, cell) for pos in atom_positions]
    return int(np.argmin(dists))

def guess_orbital_type(element: str, spread: float) -> str:
    """Simple heuristic for orbital type (expand as needed)."""
    if element == "I":
        return "I-5p" if spread > 1.0 else "I-5s"
    if element == "Pb":
        return "Pb-6p" if spread > 1.0 else "Pb-6s"
    if element == "C":
        return "C-2p" if spread > 0.8 else "C-2s"
    if element == "N":
        return "N-2p" if spread > 0.8 else "N-2s"
    if element == "H":
        return "H-1s"
    return "unknown"

# -------------------- Parsing helpers --------------------
float_re = re.compile(r'[-+]?\d*\.\d+|\d+')  # find floats & ints (keeps sign)

def parse_lattice_from_lines(lines: List[str]) -> np.ndarray:
    """Find 'a_1 a_2 a_3' block and return 3x3 lattice (Ang)."""
    for i, line in enumerate(lines):
        if line.strip().startswith("a_1") or "a_1" in line:
            # read three consecutive lines that include a_1, a_2, a_3
            vals = []
            for j in range(3):
                parts = lines[i + j].split()
                # find numeric parts after the a_i token
                nums = [float(x) for x in parts[1:4]]
                vals.append(nums)
            return np.array(vals, dtype=float)
    raise ValueError("Lattice vectors (a_1,a_2,a_3) not found in .wout")

def parse_atoms_from_lines(lines: List[str]) -> Tuple[np.ndarray, List[str]]:
    """
    Parse the atomic table block that looks like:
    | H    1   0.00198   0.18482   0.85823   |    0.01693   2.37306   7.97296    |
    returns (N x 3 array of Cartesian coords), list of element symbols
    """
    atom_positions = []
    elements = []
    inside_table = False
    # Detect the start of the Site / Cartesian table by matching header line
    for i, line in enumerate(lines):
        if "Site" in line and "Cartesian Coordinate" in line:
            inside_table = True
            continue
        if not inside_table:
            continue
        # stop when table ends - typically a line with '*' or blank+separator
        if line.strip().startswith('*') or line.strip() == "":
            # table end
            break
        # table lines typically begin with '|'
        if not line.strip().startswith('|'):
            continue
        cols = line.split('|')
        # We expect something like ['',' H    1   0.... ','    0.01693  2.37306 7.97296   ','']
        if len(cols) < 3:
            continue
        left = cols[1].strip()
        right = cols[2].strip()
        left_tokens = left.split()
        if len(left_tokens) < 1:
            continue
        elem = left_tokens[0].capitalize()
        # extract last three floats from the right column (Cartesian)
        nums = float_re.findall(right)
        if len(nums) < 3:
            # sometimes the Cartesian coords are in the middle column (if formatting differs)
            # try to extract floats from the whole line and take last 3
            all_nums = float_re.findall(line)
            if len(all_nums) >= 3:
                coords = list(map(float, all_nums[-3:]))
            else:
                continue
        else:
            coords = list(map(float, nums[-3:]))
        atom_positions.append(coords)
        elements.append(elem)
    if len(atom_positions) == 0:
        raise ValueError("No atomic positions found in .wout — check the file format.")
    return np.array(atom_positions, dtype=float), elements

def parse_wannier_last_iteration(lines: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Parse only the last block of 'WF centre and spread' lines.
    Approach:
      - scan from the end, collect consecutive lines containing 'WF centre and spread'
      - stop when a non-matching line is encountered after collection starts
    Returns arrays: centers (N x 3), spreads (N,)
    """
    collected = []
    # scan reversed
    for line in reversed(lines):
        if "WF centre and spread" in line:
            collected.append(line)
        else:
            if collected:
                # we've already started collecting; the last block is finished
                break
            else:
                # still scanning for the final block
                continue
    if not collected:
        raise ValueError("No 'WF centre and spread' lines found in .wout")
    collected = collected[::-1]  # restore original order
    centers = []
    spreads = []
    for line in collected:
        # find all floats in the line and take last 4 floats: x,y,z,spread
        nums = float_re.findall(line)
        if len(nums) < 4:
            # skip malformed line
            continue
        # take last 4 numbers (index may be earlier)
        x, y, z, spread = map(float, nums[-4:])
        centers.append([x, y, z])
        spreads.append(spread)
    if len(centers) == 0:
        raise ValueError("No valid WF centre lines parsed in last iteration block.")
    return np.array(centers, dtype=float), np.array(spreads, dtype=float)

# -------------------- Main parser --------------------
def parse_wout(wout_file: str):
    with open(wout_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    lattice = parse_lattice_from_lines(lines)          # 3x3
    atom_positions, elements = parse_atoms_from_lines(lines)
    wannier_centers, spreads = parse_wannier_last_iteration(lines)

    return wannier_centers, spreads, atom_positions, elements, lattice

# -------------------- Build mapping and save --------------------
def build_and_save_mapping(wout_file: str, save_csv_prefix: str = None, verbose = False):
    """
    Parse .wout, map WFs to nearest atoms, print dicts, and save CSVs.
    save_csv_prefix: if None, uses same folder as wout_file and base name 'wannier_mapping.csv'
    """
    wannier_centers, spreads, atom_positions, elements, lattice = parse_wout(wout_file)

    n_atoms = len(atom_positions)
    n_wf = len(wannier_centers)

    if verbose: 
        print(f"Number of atoms: {n_atoms}")
        print(f"Number of Wannier centers (last iteration): {n_wf}")

    mapping = []
    for i, (wc, sp) in enumerate(zip(wannier_centers, spreads)):
        nearest = find_closest_atom(wc, atom_positions, lattice)
        elem = elements[nearest]
        # atomic number lookup (extend map if needed)
        atomic_number_map = {
            "H":1, "C":6, "N":7, "O":8, "F":9, "Na":11, "Mg":12,
            "Al":13, "Si":14, "P":15, "S":16, "Cl":17, "K":19,
            "Ca":20, "Pb":82, "I":53
        }
        Z = np.int64(atomic_number_map.get(elem, 0))
        orbital = guess_orbital_type(elem, sp)
        entry = {
            "wannier_index": int(i),
            "center": np.array(wc, dtype=float),
            "spread": np.float64(sp),
            "nearest_atom": int(nearest),
            "atomic_number": Z,
            "element": elem,
            "orbital_type": orbital
        }
        mapping.append(entry)

    # Print each mapping dict in requested format (one per line)
    if verbose:
        for entry in mapping:
            # The default print of numpy types is okay; keep format exactly similar to your example
            print({
                "wannier_index": entry["wannier_index"],
                "center": entry["center"],
                "spread": entry["spread"],
                "nearest_atom": entry["nearest_atom"],
                "atomic_number": entry["atomic_number"],
                "element": entry["element"],
                "orbital_type": entry["orbital_type"]
            })

    # Prepare CSVs
    # default save path
    import os
    base_dir = os.path.dirname(wout_file)
    base_name = os.path.splitext(os.path.basename(wout_file))[0]
    if save_csv_prefix is None:
        mapping_csv = os.path.join(base_dir, f"{base_name}_wannier_mapping.csv")
        lattice_csv = os.path.join(base_dir, f"{base_name}_lattice_vectors.csv")
    else:
        mapping_csv = os.path.join(base_dir, f"{save_csv_prefix}_wannier_mapping.csv")
        lattice_csv = os.path.join(base_dir, f"{save_csv_prefix}_lattice_vectors.csv")

    # mapping DataFrame: expand center coordinates
    df = pd.DataFrame([{
        "wannier_index": e["wannier_index"],
        "x": float(e["center"][0]),
        "y": float(e["center"][1]),
        "z": float(e["center"][2]),
        "spread": float(e["spread"]),
        "nearest_atom": e["nearest_atom"],
        "atomic_number": int(e["atomic_number"]),
        "element": e["element"],
        "orbital_type": e["orbital_type"]
    } for e in mapping])
    df.to_csv(mapping_csv, index=False)
    
    if verbose: 
      print(f"Wannier mapping saved to {mapping_csv}")

    # lattice save
    df_lat = pd.DataFrame(lattice, columns=['ax','ay','az'])
    df_lat.to_csv(lattice_csv, index=False)
    if verbose: 
      print(f"Lattice vectors saved to {lattice_csv}")

    return mapping, lattice, atom_positions, elements


def get_wannier_mappings_and_geometry(mats, file_paths):
  """
  Read wannier output files to generate mappings and ase Atoms objects. 

  file_paths = list of paths to wout files. 
  mats = list of materials names. 
  """
  mats_data = {}

  for mat, wout_file in zip(mats, file_paths):
    mapping, lattice, atom_pos, elems = build_and_save_mapping(wout_file)
    mat_geom = Atoms(''.join(elems),
                positions=atom_pos,
                cell=lattice,
                pbc=[1, 1, 1])

    mats_data[mat] = {'mapping': mapping, 
                      # 'lattice': lattice, 'atom_positions': atom_pos, 'elements': elems,
                      'ase': mat_geom}


  return mats_data


def wannier_mappings_df(mats, file_paths):
  """
  Return Wannier mappings 
  Args:
    mats: list of material names.
    file_paths: file paths for wout files
  Returns:
    mapping as dataframe and all data (including mapping, lattice, atoms, positions) in json too

  Example:
    rootdir = '../../_data/wann_tb_files/'
    mats = ['MAPbI3', 'MAPbBr2I','MAPbI2Br','MAPbBr3']
    file_paths = [rootdir + m + f'_wan/{m}.wout' for m in mats]

    mats_data = wp.get_wannier_mappings_and_geometry(mats, file_paths)
  """

  mats_data = {}
  map_df = pd.DataFrame()
  for mat, wout_file in zip(mats, file_paths):
    mapping, lattice, atom_pos, elems = build_and_save_mapping(wout_file)
    mats_data[mat] = {'mapping': mapping, 'lattice': lattice, 'atom_positions': atom_pos, 'elements': elems}
    
    mat_mapdf = pd.DataFrame(mats_data[mat]['mapping'])
    mat_mapdf['material'] = mat
    map_df = pd.concat([map_df, mat_mapdf])

  return map_df, mats_data