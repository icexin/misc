#!/usr/bin/env python

import sys
import os
import subprocess
from stat import ST_MTIME

local_root_dir = ''
remote_root_dir = ''
tmpfile = ''

def error(msg):
	print '\033[1;33m%s\033[m' %(str)	

def upload(local_file, remote_file):
    print 'upload %s to %s' %(local_file, remote_file)
    ret = subprocess.call('scp -q -r %s %s'%(local_file, remote_file), shell=True)
    return ret == 0

def is_new(f):
    # if the tmp file does not exists force an update
    if not os.path.exists(tmpfile):
        return True

    tmp_mtime = os.stat(tmpfile)[ST_MTIME]
    file_mtime = os.stat(f)[ST_MTIME]
    return file_mtime > tmp_mtime

def touch(f):
    open(f, 'w').close()
   
def update_dir(local_path):
    for item in os.listdir(local_path):
        if item.startswith('.'):
            continue

        full_name = os.path.join(local_path, item)

        if os.path.isfile(full_name):
            if not update_file(full_name):
                return False
        else:
            if not update_dir(full_name):
                return False

    return True


def update_file(local_path):
    relative_path = os.path.relpath(local_path, local_root_dir)
    remote_path = os.path.join(remote_root_dir, relative_path)
    if is_new(local_path):
        return upload(local_path, remote_path)
    else:
        return True


def run():
    global tmpfile, local_root_dir, remote_root_dir

    if len(sys.argv) < 3 :
        print 'usage: up.py local_root_dir user@host:dir'
        return False

    local_root_dir = sys.argv[1]
    remote_root_dir = sys.argv[2]
    tmpfile = os.path.join(local_root_dir, '.lastupload.tmp')

    return update_dir(local_root_dir);

if __name__ == '__main__':
    try:
        if run():
            touch(tmpfile)
		else
			error("failed.")
    except Exception, e:
		error(e);

