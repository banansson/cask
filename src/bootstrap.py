import sys
import os
from subprocess import Popen, PIPE
from src.message import Message

class Bootstrap(object):

  def __init__(self):
    self.__pacman_req = (4, 1, 2)
    self.__python_req = (3, 3, 2)

  def dist(self):
    os_file = open('/etc/os-release', 'r')
    data = {}
    for line in os_file:
      if line == '\n':
        continue
      entry = line.strip().replace('"', '').split('=')
      data[entry[0]] = entry[1]
    return(data)

  def verify_all(self):
    messages = []
    if not self.is_arch():
      messages.append('This is not a Arch distro :(')

    pacman = self.verify_pacman()
    if not pacman[1]:
      messages.append('Pacman: your version {:s} is too old'.format(pacman[0]))

    python = self.verify_python()
    if not python[1]:
      messages.append('Python: your version {:s} is too old'.format(python[0]))

    return (len(messages) == 0, messages)

  def is_arch(self):
    return self.dist()['ID'] == 'arch'

  def verify_pacman(self):
    pacman = Popen(['pacman', '--version'], stdout=PIPE)
    raw = pacman.communicate()[0].decode().strip().split('\n')
    version = raw[0].lstrip('.- ').split()[1].lstrip('v')

    return (version, self.__verify_version(version, self.__pacman_req))

  def verify_python(self):
    version = self.__execute(['python', '--version'])
    return (version, self.__verify_version(version, self.__python_req))

  def __verify_version(self, version, minimum):
    raw_version = version.split('.')
    found = []
    for part in raw_version:
      found.append(int(part))
    
    return tuple(found) >= minimum

  def __execute(self, command):
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    raw  = proc.communicate()
    (std, err) = tuple(raw)

    result = std if len(std) > 0 else err
    return result.decode().split()[1]

  def verbose(self, message):
    message.info('Output from this boostrap is provided as information only.')
    message.info('The unicorn application itself will use this programatically to determine if your system is supported.')
    message.empty()
    
    is_arch = 'yes' if self.is_arch() else 'no'
    message.info('Arch Linux: {:s}'.format(is_arch))

    format_output = lambda title, what: '{:s}....: {:s} [{:s}]'.format(title, what[0], self.map2readable(what[1]))

    message.info(format_output('Pacman', self.verify_pacman()))
    message.info(format_output('Python', self.verify_python()))

  def map2readable(self, condition):
    map = { True: 'ok', False: 'failed' }
    return map[condition]

