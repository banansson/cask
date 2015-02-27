#!/usr/bin/python

import sys
import argparse
from os import path

from src.bag import Bag
from src.package import Package
from src.task import Task
from src.message import Message
from src.application import Application
from src.application_info import ApplicationInfo
from src.bootstrap import Bootstrap
from src import utils

def run(argv):
  default_packs_dir  = "~/.config/cask/packs"
  default_target_dir = "~"

  parser = argparse.ArgumentParser()

  actions = parser.add_mutually_exclusive_group()
  actions.add_argument('--version', action='store_true',
                       help='Display version')
  actions.add_argument('--bootstrap', action='store_true',
                       help='run bootstrap test')

  parser.add_argument('command', nargs='?', help='Command to run: list, query, install')

  parser.add_argument('-v', '--verbose', action='count', default=0,
                      help='be verbose')
  parser.add_argument('-d', '--dryrun', action='store_true',
                      help='run in test mode, nothing is installed')
  parser.add_argument('-s', '--source', action='store',
                      default=default_packs_dir,
                      help='override directory in which to look for packages')
  parser.add_argument('-t', '--target', action='store',
                      default=default_target_dir,
                      help='override directory in which to install packages')
  parser.add_argument('package', nargs='?', help='Name of package')

  args = parser.parse_args()
  verbose = args.verbose

  message = Message(sys.stdout, verbose > 0)

  if args.bootstrap:
    bootstrap = Bootstrap()
    if args.verbose:
      bootstrap.verbose(message)
    else:
      verifications = bootstrap.verify_all()
      if not verifications[0]:
        message.info('Boostrap verification failed! Use verbose flag for more detailed output')
        message.major('Errors:')
        for error in verifications[1]:
          message.minor(error)
      else:
        message.info('Boostrap verification succeeded')
    return 0

  appinfo = ApplicationInfo()
  
  if args.version:
    message.info(appinfo.name())
    return 0

  if not(args.command or args.package):
    message.info("No package specified, use -h or --help for help. Listing of")
    message.info("all packages can be done using the 'list' argument.")
    return 0

  (valid, source) = utils.try_lookup_dir(args.source)

  if not valid:
    message.error("No such directory: %s" % source)
    return 0

  message.plain("Looking for packages in: %s" % source) 
 
  target = utils.lookup_dir(args.target)

  bag = Bag(path.abspath(source))
  app = Application(bag, message, args)

  commands = {}
  commands['list']    = lambda bag, message, args: app.list(verbose)
  commands['query']   = lambda bag, message, args: app.query(args.package, target)
  commands['install'] = lambda bag, message, args: app.install(args.package, target, args.dryrun)

  if len(args.command) == 0:
    message.info("No action specified, use -h or --help for help.")
    return 0

  cmd = args.command
  if cmd not in commands:
    message.info('No such command: {:s}'.format(cmd))
    return 0

  commands[cmd](bag, message, args)

  return 0

if __name__ == '__main__':
  code = run(sys.argv)
  exit(code)

