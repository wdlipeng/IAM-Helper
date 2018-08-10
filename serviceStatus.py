#coding=utf-8
#!/usr/bin/python

import subprocess
import errno
import logging
import threading
import time
from ssh_sub_process import ssh2
# subprocess.Popen('check-ece-health',shell=True,cwd='/root')

# obj = subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# obj.stdin.write('print 1 \n')
# obj.stdin.write('print 2 \n')
# obj.stdin.write('print 3 \n')
# obj.stdin.write('print 4 \n')
# obj.stdin.close()
#
# cmd_out = obj.stdout.read()
# obj.stdout.close()
# cmd_error = obj.stderr.read()
# obj.stderr.close()
#
# print cmd_out
# print cmd_error

# a = subprocess.call('df -hT',shell=True)
# print a

def timeout( p):
        print "enter into timeout"
        if p.poll() is None:
            try:
                p.kill()
                print 'Error: process taking too long to complete--terminating'
            except OSError as e:
                if e.errno != errno.ESRCH:
                    raise









# obj = subprocess.Popen(["sd-cli list"], shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
obj = subprocess.Popen(["ssh 10.172.39.22"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# obj = subprocess.Popen(['ssh 10.172.39.22 "ip add"'], shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
# obj = subprocess.Popen(["check-ece-health"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
t = threading.Timer(20.0, timeout, (obj,))
t.start()
# t.join()
print "the end"
while True:
    buff = obj.stdout.readline()
    if buff == '' and obj.poll() != None:
        break
   


# sub_status = obj.poll()
# print "sub_status: ", sub_status
# cmd_out = obj.stdout.read()
# print "cmd_out: ", cmd_out
# sub_status2 = obj.poll()
# print "sub_status 2: ", sub_status2


