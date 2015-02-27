from subprocess import call
from os import path

class Task:

  def __init__(self, data, pkg_dir):
    self.action = data["action"]
    self.source = data["source"]
    self.target = data["target"]
    self.pkg_dir = pkg_dir

  def run(self, command, test_mode=False):
    if test_mode:
      return False

    result = call(command)
    return result == 0

  def present(self, target):
    return "[{:s}] {:s} -> {:s}".format(self.action, self.source, self.lookup(target))

  def lookup(self, target):
    if target is None:
      return path.expanduser(self.target)
    else:
      original = self.target.strip("~/")
      return path.join(target.rstrip("/"), original.lstrip("/"))

class LinkTask(Task):

  def run(self, target, test_mode=False):
    source = path.join(path.abspath(self.pkg_dir), self.source)
    target = super(LinkTask, self).lookup(target)
    command_line = ["ln", "-s", source, target]
    return super(LinkTask, self).run(command_line, test_mode)

class MkdirTask(Task):

  def run(self, target, test_mode=False):
    target = super(MkdirTask, self).lookup(target)
    command_line = ["mkdir", "-p", target]
    return super(MkdirTask, self).run(command_line, test_mode)

