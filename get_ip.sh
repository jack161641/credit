#!/bin/bash
localip=`ip addr|grep 'inet 10'|awk -F ' ' '{print $2}'|awk -F '/' '{print $1}'`
sed -i '/Hostname=/d'  /etc/zabbix/zabbix_agentd.conf
echo Hostname=$localip >> /etc/zabbix/zabbix_agentd.conf
