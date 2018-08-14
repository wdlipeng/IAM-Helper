#!/usr/bin/python
#coding=utf-8

from ssh_sub_process import remote_cmd, local_cmd
from unit_func import *
import time


def inital_all():
    global _args
    _args=get_args().parse_args()
    global timeRange
    timeRange=_args.time*60+8
    print "#"*103+"\n\n"
    global configPara
    global nodesInfo
    global currentLogPath
    print "starting IAM Helper********************************************";
    configPara=getConfiguration()
    currentLogPath = mkLogPath( configPara.get('logPath'))
    print "Destination folder for collected logs:%s"%currentLogPath;
    nodesInfo = get_nodes_info( configPara.get('ClusterNodesInfoPath'));


def collectNodesLogs():
    global timeRange
    print "#"*100
    for node in nodesInfo:
        time_start=time.time()
        print "start collecting logs on %s,this could take a few minutes"%node['hostname'];
        print "*"*80
        print "Below ERRORs are found in logs on %s:"%node['hostname'];
        print "*"*80
        nodeLogDir = currentLogPath+r"/"+node['hostname']+r"/"
        local_cmd("sudo mkdir -p "+nodeLogDir);time.sleep(1)
        cmdCollectServerLog =r'''sudo find /var/exposure/serverlog/DP*/ -mmin -'''+str(timeRange/60)+r''' -name "Server.log*" |awk -F / '{print "tac "$0"|awk -F '\''[<>]'\'' '\''BEGIN{c=systime();timerange='''+str(timeRange)+r'''}{a=\$2;gsub(/[^0-9]/,\" \",a);b=mktime(a);d=c-b;if(b!=-1 && d>timerange){exit}else print \$0}'\''|tac |tee -a "$5"-"$6"|grep ERROR |awk '\''{print $0\"'''+node['hostname']+r'''-"$0"\";}'\''"}'|bash|sudo tee -a ../summary.log;'''
        cmdcollectLaBgLog =r'''sudo find /var/lib/modules/DP-*/ -mmin -'''+str(timeRange/60)+r''' -name "*.log.*.log" |awk -F / '{print "tac "$0"|awk  '\''BEGIN{c=systime();timerange='''+str(timeRange)+r'''}{a=\$1\" \"\$2;gsub(/[^0-9]/,\" \",a);b=mktime(a);d=c-b;if(b!=-1 && d>timerange){exit}else print \"####<\"\$0}'\''|tac |tee -a "$NF"|grep ERROR |awk '\''{print $0\"'''+node['hostname']+r'''-"$0"\";}'\''"}'|bash|sudo tee -a ../summary.log;'''
        cmdCollectServerLog="sudo mkdir -p "+nodeLogDir+" && "+"cd "+nodeLogDir+";"+cmdCollectServerLog
        cmdcollectLaBgLog="sudo mkdir -p "+nodeLogDir+" && "+"cd "+nodeLogDir+";"+cmdcollectLaBgLog
        remote_cmd(node['hostname'],node['internal_ip'], _args.user, _args.passwd,cmdCollectServerLog+cmdcollectLaBgLog)
        timeRange+=int(time.time()-time_start)

def packAllInfo():
    print "#"*100
    print "start packing the logs files";
    cmd_sort_summ="sudo sort "+currentLogPath+r"/summary.log -o "+currentLogPath+r"/summary.log;"
    local_cmd(cmd_sort_summ)
    cmdPackLogs = "sudo tar -czf "+currentLogPath+r".tar.gz"+" "+currentLogPath+r"/* &>/dev/null 2>&1;"
    local_cmd(cmdPackLogs)
    print "all log files has been packed into %s.tar.gz"%currentLogPath

def end_all():
    print "Logs has been collected successfully and can be found at %s"%currentLogPath
    print "\n\n"+"#"*103
    local_cmd("sudo cd "+currentLogPath)


if __name__ == '__main__':
    inital_all()
    collectNodesLogs()
    packAllInfo()
    end_all()