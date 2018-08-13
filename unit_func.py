#!/usr/bin/python
#coding=utf-8
from ssh_sub_process import local_cmd , remote_cmd
import subprocess
import ConfigParser
import argparse


def get_args():
    description='''Log Collector is a tool that helps to collect logs of all IAM DPs in defined time range on all IAM nodes. It also generates a summary log that includes all ERROR information sorted by time, so that you can easily understand which DP on which node throw ERROR message first. Besides, it helps packed the log into a compressed file and 1st line support engineer can easily sent the file to 2nd line support for analyze when needed. '''
    parser = argparse.ArgumentParser(description = description)
    help = '''Defines the interval in minutes for log collection.
    This is a mandatory parameter.
	For example, 5 means to collect logs for the previous 5 minutes.'''
    parser.add_argument('-t','--time', type=int,required=True,help=help)
    help = '''Username to login to other IAM nodes. This account must have sudo previllige.
    This account can be used to login all IAM nodes, in other case, this tool may not work as expected.
	If not specified, default username root will be used.'''
    parser.add_argument('-u','--user',default="root", help=help)
    help = '''Password to login to other IAM nodes. This is a mandatory parameter.'''
    parser.add_argument('-p','--passwd',required=True , help=help)
    return parser



def get_nodes_info(nodesFilePath):
    with open(nodesFilePath) as f:#从TXT文件中读出数据
        nodesInfo = []
        tmpList=[]
        dictList = {}
        line = f.readline()#   #通过for循环一行一行加载
        while line:
            if line.find('nodename:') >= 0:
                dictList[line.split(":")[0].replace("-","").strip()]=line.split(":")[1].replace("\n","").strip()
            elif line.find('hostname:') >= 0:
                dictList[line.split(":")[0].replace("-","").strip()]=line.split(":")[1].replace("\n","").strip()
            elif line.find('internal_ip:') >= 0:
                dictList[line.split(":")[0].replace("-","").strip()]=line.split(":")[1].replace("\n","").strip()
            elif line.find('external_ip:') >= 0:
                dictList[line.split(":")[0].replace("-","").strip()]=line.split(":")[1].replace("\n","").strip()
                nodesInfo.append(dictList)
                dictList = {}
            line = f.readline()
        return nodesInfo

def mkLogPath(logPath):
    obj = subprocess.Popen([r"date +%Y%m%d%H%M"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timestamp = obj.stdout.read().replace("\n","")
    local_cmd(r"sudo mkdir -p "+logPath+timestamp)
    return logPath+timestamp


def getConfiguration():
    # cf=ConfigParser.ConfigParser()
    # cf.read("config.ini")
    global logPath
    global ClusterNodesInfoPath
    cfDict={}
    # cfDict['logPath']=cf.get('baseConfig','logPath')
    cfDict['logPath']=r"/cluster/log-collector/log/"
    # cfDict['ClusterNodesInfoPath']=cf.get('baseConfig','ClusterNodesInfoPath')cfDict['logPath']=cf.get('baseConfig','logPath')
    cfDict['ClusterNodesInfoPath']=r"/boot/.clusterx.conf"
    return cfDict




if __name__ == '__main__':
    pass
