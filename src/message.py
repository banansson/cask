class Message:

  def __init__(self, out, verbose=False):
    self.__out = out
    self.__verbose = verbose

  def __print_verbose(self, text, prefix):
    if self.__verbose:
      self.__print(text, prefix)
    else:
      self.__print(text)

  def __print(self, text, prefix=""):
    if len(prefix) > 0:
      self.__out.write("%s %s\n" % (prefix, text))
    else:
      self.__out.write("%s%s\n" % (prefix, text))

  def info(self, text):
    self.__print_verbose(text, "info:")

  def warning(self, text):
    self.__print_verbose(text, "warn:")

  def error(self, text):
    self.__print_verbose(text, "err :")

  def alert(self, text):
    self.__print_verbose(text, " >>");

  def major(self, text):
    self.__print(text, "==>")

  def minor(self, text):
    self.__print(text, " ->")

  def plain(self, text):
    self.__print(text)

  def empty(self):
    self.__print("")

