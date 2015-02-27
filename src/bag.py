import os

from src.package import Package

class Bag:

  def __init__(self, root):
    self.__root = root
    self.__package_name = "package.unicorn"

  def __available_packages(self):
    return os.listdir(self.__root)

  def __build_package_data(self, name):
    pkg_dir = os.path.join(self.__root, name)
    pkg_file = os.path.join(pkg_dir, self.__package_name)
    return (pkg_dir, pkg_file)

  def fetch_all(self):
    packs = []
    notifications = []
    available = self.__available_packages()
    for name in available:
      (pkg_dir, pkg_file) = self.__build_package_data(name)

      if os.path.exists(pkg_file):
        pack = Package()
        if pack.load(open(pkg_file), pkg_dir):
          packs.append(pack)
        else:
          notifications.append("{:s} failed to load! Possibly mallformated package definition.".format(name))

    return (packs, notifications)

  def fetch(self, name):
    available = self.__available_packages()
    if name in available:
      (pkg_dir, pkg_file) = self.__build_package_data(name)

      if not os.path.exists(pkg_file):
        return None

      pack = Package()
      if pack.load(open(pkg_file), pkg_dir):
        return pack

    return None

