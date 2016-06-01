#!/bin/bash
#
# If Tomcat uses server.xml config to rotate localhost_access_log,
# the daily rotated logs will need compressing and old ones deleted to stop filling
# the log partiton. Cannot use the system logrotate command as conficts with tomcat rotate
# therefore run this script in a daily cronjob
#
# localhost_access_log.2015-09-03.txt
#
# Add this script in /etc/cron.daily/ owned by root
#

CATALINA_BASE=`ps aux | grep catalina.base | awk -F'catalina.base\\=' '{print $2}' | awk '{print $1}'`

if [ ! $CATALINA_BASE ]
then
    if [ -r /var/lib/tomcat7 ]
    then
        CATALINA_BASE=/var/lib/tomcat7
    else
        echo "Error: cannot find CATALINA_BASE"
        exit 1
    fi
fi

cd ${CATALINA_BASE}/logs

if [ $? -ne 0 ]
then
    echo "Error, cannot cd to logs directory, quitting...."
    exit 1
fi

# today's date (not to be gzipped)
DATE=`date --rfc-3339=date`
# number of days to keep
MTIME=14

# Compress all previous days uncompressed logs
for log in `ls localhost_access_log* | grep -v bz2 | grep -v $DATE`
do
    bzip2 $log
done

# delete old logs
find . -name "*.bz2" -mtime +$MTIME -exec rm {} \;

exit 0
