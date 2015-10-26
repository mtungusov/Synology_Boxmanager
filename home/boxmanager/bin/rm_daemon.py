#!/usr/bin/env python
#
# Service for removing forbidden files from folder of internal users

import os
import sys
import signal
import time
import glob
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

DEBUG = False
SIGTERM_CAUGHT = False

CONFIG_PATH = "/volume1/homes/etc/rm_forbidden_files.yaml"
PID = "/var/run/S99rmforbiddenfiles.pid"

if DEBUG:
    CONFIG_PATH = "rm_forbidden_files_debug.yaml"
    PID = "rmforbiddenfiles.pid"
    logging.basicConfig(
        filename="rm_forbidden_files_daemon.log",
        level=logging.DEBUG)
else:
    logging.basicConfig(
        filename="/volume1/homes/log/rm_forbidden_files_daemon.log",
        level=logging.INFO)

TIME = lambda: time.strftime('%Y/%m/%d %H:%M:%S')
LOG = lambda msg: '{0} === {1}'.format(TIME(), msg)

# logging.basicConfig(filename=LOG, level=logging.DEBUG)


def load_config(filename):
    err, config = None, None
    try:
        config = yaml.safe_load(file(filename, 'r'))
    except:
        err = "Error: load config"
    if not ('root_dir' in config
            and 'wildcard' in config
            and 'default_exts' in config):
        err = "Error: Not found - root_dir or wildcard or default_exts"

    return [err, config]


def user_dirs_and_exts(root_path, wildcard, users_and_exts, default_exts):
    r = {}
    for user_dir in glob.glob("%s/%s" % (root_path, wildcard)):
        username = user_dir.split('/')[-1]
        if username in users_and_exts:
            r[user_dir] = users_and_exts[username]
        else:
            r[user_dir] = default_exts
    return r


def signal_cleanup(signal, frame):
    logging.info("recived signal: %s" % signal)
    global SIGTERM_CAUGHT
    SIGTERM_CAUGHT = True


class RmEventHandler(FileSystemEventHandler):
    def __init__(self, exts=[], root_dir=""):
        FileSystemEventHandler.__init__(self)
        self.exts = exts
        self.root_dir = root_dir

    def perform_on_event(self, filename):
        if self.root_dir == "":
            return
        try:
            f = os.path.join(self.root_dir, filename)
            os.remove(f)
            logging.info(LOG("Remove file: %s" % f))
        except OSError as ex:
            logging.error(LOG("Error remove file: %s, errno: %s" % (f, ex.errno)))

    def catch_all(self, event):
        if not self.exts or event.is_directory:
            return
        if event.event_type == 'moved':
            filename = event.dest_path
        else:
            filename = event.src_path
        extension = os.path.splitext(filename)[-1][1:].lower()
        if extension in self.exts:
            if DEBUG:
                print("found filename: [%s], ext: [%s]" % (filename, extension))
            self.perform_on_event(filename)

    def on_created(self, event):
        self.catch_all(event)

    def on_moved(self, event):
        self.catch_all(event)


class Watcher(object):
    def __init__(self, user_dirs_and_exts={}, root_dir=""):
        self.user_dirs_and_exts = user_dirs_and_exts
        self.root_dir = root_dir
        self.__observers = []

    def __start_observer(self, user_dir, exts):
        observer = Observer()
        self.__observers.append(observer)
        event_handler = RmEventHandler(exts, self.root_dir)
        observer.schedule(event_handler, user_dir, recursive=True)
        logging.info("Watch dir [%s], exts: [%s]" % (user_dir, exts))
        observer.start()

    def start_all(self):
        for user_dir in self.user_dirs_and_exts.keys():
            exts = self.user_dirs_and_exts[user_dir]
            self.__start_observer(user_dir, exts)

    def stop_all(self):
        for observer in self.__observers:
            observer.stop()


def create_pidfile_or_exit(pidfile):
    pid = str(os.getpid())

    if os.path.isfile(pidfile):
        logging.error(LOG("%s already exists, exiting" % pidfile))
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_cleanup)
    signal.signal(signal.SIGTERM, signal_cleanup)
    create_pidfile_or_exit(PID)
    logging.info(LOG("Started Rm_Daemon with pid: %s" % os.getpid()))

    # Read config file
    err, config = load_config(CONFIG_PATH)
    if err:
        logging.error(err)
        sys.exit(1)

    # Get list of user dirs
    user_dirs_and_exts = user_dirs_and_exts(
        config['root_dir'],
        config['wildcard'],
        config['users'],
        config['default_exts'])

    # Start observers for user dirs
    watcher = Watcher(user_dirs_and_exts, config['root_dir'])
    watcher.start_all()

    # Infinitive loop
    while not SIGTERM_CAUGHT:
        time.sleep(2)

    watcher.stop_all()
    os.unlink(PID)
    logging.info(LOG("Stoped Rm_Daemon with pid: %s" % os.getpid()))
