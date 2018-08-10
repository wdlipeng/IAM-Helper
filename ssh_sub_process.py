#!/usr/bin/python
#coding=utf-8

import subprocess
import paramiko
def remote_cmd(hostname,ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        stdin,stdout,stderr = ssh.exec_command(cmd)
#           stdin.write("Y")
#         print stdout.read()
        for x in  stdout.readlines():
            print x.strip("n")
        print '%s\tdone.\n'%(hostname)
        ssh.close()
    except :
        print '%s\tconnection\tFAILED!\n'%(hostname)


def local_cmd(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    obj = subprocess.Popen(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
    while True:
        buff = obj.stdout.readline()
        if buff == '' and obj.poll() != None:
            print obj.stderr.read()
            break
        else: print buff


def local_cmd2(cmd):
    obj = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    while True:
        buff = obj.stdout.readline()
        if buff == '' and obj.poll() != None:
            break
        else: print buff


if __name__ == '__main__':
    pass