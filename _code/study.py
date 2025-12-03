#Use a decorator to run a function over an entire study?

import os
import itertools

class Study():
  def __init__(self, root, files, append = '.py'):
    # mats = ['CsPbBr3_info', 'CsPbI3_info', 'CsPbBr2I_info', 'CsPbBrI2_info' ]
    self.files = [os.path.join(root, m + append) for m in mats]
    self.file_iter = itertools.cycle([self.files])

    return

  def exec(self):
    with open(next(self.file_iter)) as f:
      exec(f.read)
    return


  def runoverstudy(self):
    return


st = Study(root, files)

for mat in len(files):
  st.exec(next(file))
  
  # with open(m) as f:
  #   exec(f.read())