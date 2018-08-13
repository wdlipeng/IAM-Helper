Log Collector is a tool that helps to collect logs of all IAM DPs in defined time range on all IAM nodes. It also generates a summary log that includes all ERROR information sorted by time, so that you can easily understand which DP on which node throw ERROR message first. Besides, it helps packed the log into a compressed file and 1st line support engineer can easily sent the file to 2nd line support for analyze when needed.
1, Put log-collector.tar.gz to /cluster on any one of the IAM node.
2, Uncompress log-collector.tar.gz by executing "tar -zxvf log-collector.tar.gz"
3, cd /cluster/log-collector, execute "python log-collector.py -h", you will get the help information.
4, To start collecting the log, execute "python log-collector.py -t <time interval> -u <username> -p <password>", here:
	-t: Defines the interval in minutes for log collection.
    This is a mandatory parameter.
	For example, 5 means to collect logs for the previous 5 minutes.
	-u: Username to login to other IAM nodes.
		This account must have sudo previllige. This account can be used to login all IAM nodes, in other case, this tool may not work as expected.
		If not specified, default username root will be used.
	-p: Password to login to other IAM nodes. This is a mandatory parameter.
5. Log collected can be found at /cluster/log-collector/log/, a compressed file (.tar.gz) named with the timestamp can also be found there.

Example of the command: python log-collector.py -t 10 -u admin -p adminpass