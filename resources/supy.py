import os
import pwd
import subprocess
import sys
import threading
import time
from colors import colors

def main(user_name, args, cwd = '/home'):    
    pw_record = pwd.getpwnam(user_name)
    user_name      = pw_record.pw_name
    user_home_dir  = pw_record.pw_dir
    user_uid       = pw_record.pw_uid
    user_gid       = pw_record.pw_gid
    env = os.environ.copy()
    env[ 'HOME'     ]  = user_home_dir
    env[ 'LOGNAME'  ]  = user_name
    env[ 'PWD'      ]  = cwd
    env[ 'USER'     ]  = user_name
    report_ids('starting ' + str(args))
    process = subprocess.Popen(
        args, preexec_fn=demote(user_uid, user_gid), cwd=cwd, env=env
    )
    #result = process.wait()
    
    
    thread = threading.Thread(target=get_result, args=(process, user_name))
    thread.daemon = False
    thread.start()

def get_result(process, user):
    print 'Starting', user
    time.sleep(10)
    #report_ids('finished ' + str(args))
    #print 'result', result

    if process.poll() == 1 :
        print user + ' success';
    else:
        print colors.WARNING + '[WARNING] ' + user + ' returned code ' + str(process.poll()) + colors.ENDC

def demote(user_uid, user_gid):
    def result():
#        report_ids('starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
#        report_ids('finished demotion')
    return result


def report_ids(msg):
    print 'uid, gid = %d, %d; %s' % (os.getuid(), os.getgid(), msg)


if __name__ == '__main__':
    main()
