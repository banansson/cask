import os

def lookup_dir(directory):
  if directory is None:
    return ''

  d = ''
  if '../' in directory:
    return os.path.abspath(directory)
  else:
    return os.path.expanduser(directory)

def try_lookup_dir(directory):
  d = lookup_dir(directory) 
  if not os.path.exists(d):
    return (False, directory)

  return (d != "", d)

