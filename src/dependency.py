from subprocess import call
from os import path

class Dependency:

  def __init__(self, pkg_name):
    self.pkg_name = pkg_name
    self.tool = "pacman"
    self.command = ["sudo", self.tool, "-S", pkg_name]

  def run(self, test_mode=False):
    if test_mode:
      return False

    result = call(self.command)
    return result == 0

  def present(self):
    return "[{:s}] {:s} -> {:s}".format("dep", self.tool, self.pkg_name)

