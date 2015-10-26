#!/usr/bin/env python

# 5        0        *        *        *        root        /home/boxmanager/bin/clear_usr_folders.py 2>&1 >> /volume1/homes/log/clear_usr_folders.log

import os
import glob
import datetime
import yaml
import sys


def get_items(root):
    result = {'dirs': [], 'files': []}
    for top, dirs, files in os.walk(root):
        for d in dirs:
            result['dirs'].append(os.path.join(top, d))
        for f in files:
            result['files'].append(os.path.join(top, f))
    return result


def is_older(filename, date_now, delta):
    try:
        d_f = datetime.datetime.fromtimestamp(os.path.getctime(filename))
    except OSError:
        return False
    else:
        return date_now - d_f > delta


def filter_files(files, delta_in_days):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=delta_in_days)
    # delta = datetime.timedelta(minutes=delta_in_days)
    return filter(lambda f: is_older(f, now, delta), files)


def filter_dirs(dirs, delta_in_days):
    dirs = filter_files(dirs, delta_in_days)
    return filter(lambda f: os.listdir(f) == [], dirs)


def rm_files(files):
    for f in files:
        try:
            os.remove(f)
            print "Remove file: %s" % f
        except OSError as ex:
            print "Error remove file: %s, errno: %s" % (f, ex.errno)


def rm_dirs(dirs):
    for d in dirs:
        try:
            os.rmdir(d)
            print "Remove dir: %s" % d
        except OSError as ex:
            print "Error remove dir: %s, errno: %s" % (d, ex.errno)


def get_delta(user_dir, deltas):
    username = user_dir.split('/')[-1]
    try:
        r = int(deltas[username])
    except:
        r = 7
    return r


def main():
    # Load Config
    CONFIG_PATH = "/volume1/homes/etc/clear_usr_folders.yaml"
    try:
        config = yaml.safe_load(file(CONFIG_PATH, 'r'))
    except:
        print "Error load config"
    else:
        if not ('root_dir' in config and 'wildcard' in config):
            print "Not found: root_dir or wildcard"
            sys.exit()

        user_dirs = glob.glob("%s/%s" % (config['root_dir'], config['wildcard']))

        for user_dir in user_dirs:
            delta = get_delta(user_dir, config['deltas'])
            items = get_items(user_dir)
            rm_files(filter_files(items['files'], delta))
            rm_dirs(filter_dirs(items['dirs'], delta))

if __name__ == "__main__":
    main()

