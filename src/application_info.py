class ApplicationInfo(object):

  def __init__(self):
    self.__name    = 'cask'
    self.__version = { 'major': 0, 'minor': 0, 'revision': 1, 'state': 'dev' }
    self.__terms   = 'Released under the MIT Licence. The software is provided "as is", use at you own risk.'

  def name(self):
    return '{:s} {:s}'.format(self.__name, self.version())

  def short_name(self):
    return self.__name

  def version(self):
    return '{:d}.{:d}.{:d}{:s}'.format(
        self.__version['major'],
        self.__version['minor'],
        self.__version['revision'],
        self.__version['state']
      )

  def terms(self):
    return self.__terms

