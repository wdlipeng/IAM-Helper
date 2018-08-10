'''
Created on Jul 31, 2017

@author: ezhonho
'''
import subprocess
import time

def run_cmd(cmd):
    print "excute cmd:"+ cmd
    child = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    realtime_output=child.stdout.read()
            
    if realtime_output:
        print realtime_output
        
        
def run_cmd_list(cmd_list):
    for cmd in cmd_list:
        run_cmd(cmd)
        print cmd

def run_cmd_r(cmd):
    print "excute cmd:"+ cmd
    child = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    realtime_output=child.stdout.read()

    if realtime_output:
        print realtime_output
        return realtime_output
    

if __name__ == '__main__':
    pass
    pass