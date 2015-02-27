class Application(object):

  def __init__(self, bag, message, args):
    self.__bag = bag
    self.__message = message

  def list(self, verbose=0):
    (all_packages, notifications) = self.__bag.fetch_all()
    if len(all_packages) == 0:
      self.__message.minor("No packages found")
      if verbose > 0:
        self.__message.minor("The princess is in another castle!")
      if verbose > 1:
        self.__message.minor("No, seriously... she is!")
      return 0

    for p in all_packages:
      self.__message.minor("{:<12} {:s}: {:s}".format(p.identification(), p.name(), p.description()));

    if len(notifications) > 0:
      self.__message.major("Errors occured:")
      for n in notifications:
        self.__message.warning(n)

    if verbose > 0:
      self.__message.major("Found %s packages" % len(all_packages))

    return 0

  def query(self, name, target):
    package = self.__bag.fetch(name)
    if package is None:
      self.__message.info("No such package: %s" % name)
      return 0

    self.__message.info("Info for package {:s}".format(package.identification()))
    self.__message.info("Name.......: {:s} ".format(package.name()))
    self.__message.info("Description: {:s} ".format(package.description()))
    self.__message.info("Author.....: {:s} ".format(package.author()))

    if package.has_dependency():
      self.__message.info("Depends....: %s" % len(package.depends()))
      for dep in package.depends():
        self.__message.minor(dep)
    else:
      self.__message.info("Depends....: none")

    tasks = package.tasks()
    self.__message.info("Tasks......: {:d}".format(len(tasks)))
    for task in tasks:
      self.__message.minor(task.present(target))

    return 0

  def install(self, name, target, dryrun):
    if dryrun:
      self.__message.alert("Test mode - nothing is installed...")

    if target is not None:
      self.__message.minor("Target dir is: " + target)

    package = self.__bag.fetch(name)
    if package is None:
      self.__message.info("No package specified")
      return 0

    self.__message.major("Installing: {:s} - {:s} ".format(package.identification(), package.name()))

    (successes, total) = package.install(self.__message, target, dryrun)
    if total == 0:
      self.__message.warning("Nothing to install")
    else:
      self.__message.major("{:d} of {:d} tasks executed ({:.0f}%)".format(successes, total, (successes / total) * 100))

    return 0

