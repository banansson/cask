import json
from os import path

from src.task import Task
from src.task import MkdirTask
from src.task import LinkTask
from src.dependency import Dependency

class Package():

  def __init__(self):
    self.__data = ""
    self.__tasks = []
    self.__depends = []

  def load(self, pkg_file, pkg_dir):
    try:
      self.__data = json.load(pkg_file)
    except ValueError:
      return False

    if self.has_dependency:
      for name in self.depends():
          self.__depends.append(Dependency(name))

    tasks = self.__data["tasks"]
    for task_data in tasks:
      if task_data["action"] == "link":
        self.__tasks.append(LinkTask(task_data, pkg_dir))
      if task_data["action"] == "mkdir":
        self.__tasks.append(MkdirTask(task_data, pkg_dir))

    return True

  def install(self, report, target, test_mode):
    installed_count = 0
    for depend in self.__depends:
      report.minor(depend.present())
      depend.run(test_mode)

    for task in self.__tasks:
      report.minor(task.present(target))
      installed_count += int(task.run(target, test_mode))
    return (installed_count, len(self.__tasks))

  def has_dependency(self):
    return len(self.__data["depends"]) > 0

  def identification(self):
    return self.__data["id"]

  def name(self):
    return self.__data["name"]

  def author(self):
    return self.__data["author"]

  def description(self):
    return self.__data["description"]

  def depends(self):
    return self.__data["depends"]

  def tasks(self):
    return self.__tasks

