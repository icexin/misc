import sys
import os
import subprocess
from stat import ST_MTIME

local_root_dir = ''
remote_root_dir = ''
tmpfile = ''

def upload(local_file, remote_file):
    print 'upload %s to %s' %(local_file, remote_file)
    ret = subprocess.call('scp -q -r %s %s'%(local_file, remote_file), shell=True)
    return ret == 0

def is_new(f):
    tmp_mtime = os.stat(tmpfile)[ST_MTIME]
    file_mtime = os.stat(f)[ST_MTIME]
    return file_mtime > tmp_mtime

def touch(f):
    open(f, 'w').close()
   
def update_dir(curr_dir):
    for root, dirs, files in os.walk(curr_dir):
        for f in files:
            relative_path = os.path.join(curr_dir, f)
            ret = update_file(relative_path)
            if not ret: return False
    return True


def update_file(relative_path):
    local_path = os.path.join(local_root_dir, relative_path)
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

    if not os.path.exists(tmpfile):
        touch(tmpfile)

    for item in os.listdir(local_root_dir):
        full_name = os.path.join(local_root_dir, item)
        if os.path.isfile(full_name):
            ret = update_file(item)
        else:
            ret = update_dir(item)

    return ret

if __name__ == '__main__':
    if run():
        touch(tmpfile)

