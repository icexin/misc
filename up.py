import sys
import os
import subprocess
from stat import ST_MTIME

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
      
def run():
    global tmpfile
    if len(sys.argv) < 3:
        print 'usage: %s local_root_dir user@host:dir' %(sys.argv[0])
        return

    root_dir = sys.argv[1]
    remote_root_dir = sys.argv[2]
    tmpfile = '%s.upload' %(sys.argv[1])
    if not os.path.exists(tmpfile):
        touch(tmpfile)

    for root, dirs, files in os.walk(root_dir):
        for f in files:
            full_path = os.path.join(root, f)
            if is_new(full_path):
                ret = upload(full_path, os.path.join(remote_root_dir, full_path))
                if not ret:
                    return False
    return True

if __name__ == '__main__':
    if run():
        touch(tmpfile)

        
