#!/usr/bin/env python

# 5        0        *        *        *        root        /home/boxmanager/bin/rm_forbidden_files.py 2>&1 >> /volume1/homes/log/rm_forbidden_files.log

import os
import glob
import yaml
import sys


def get_items(root, exts):
    result = []
    for top, _, files in os.walk(root):
        for f in files:
            # splitext return ['filename', '.ext']
            ext = os.path.splitext(f)[1][1:]
            if ext in exts:
                result.append(os.path.join(top, f))
    return result


def rm_files(files):
    for f in files:
        try:
            os.remove(f)
            print "Remove file: %s" % f
        except OSError as ex:
            print "Error remove file: %s, errno: %s" % (f, ex.errno)


def get_forbidden_exts(user_dir, users, defaults):
    username = user_dir.split('/')[-1]
    if username in users:
        r = users[username]
    else:
        r = defaults
    return r


def main():
    # Load Config
    CONFIG_PATH = "/volume1/homes/etc/rm_forbidden_files.yaml"
    try:
        config = yaml.safe_load(file(CONFIG_PATH, 'r'))
    except:
        print "Error load config"
    else:
        if not ('root_dir' in config and 'wildcard' in config and 'default_exts' in config):
            print "Not found: root_dir or wildcard or default_exts"
            sys.exit()

        user_dirs = glob.glob("%s/%s" % (config['root_dir'], config['wildcard']))

        for user_dir in user_dirs:
            exts = get_forbidden_exts(user_dir, config['users'], config['default_exts'])
            rm_files(get_items(user_dir, exts))

if __name__ == "__main__":
    main()

