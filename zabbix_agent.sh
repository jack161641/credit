#!/bin/bash
sed -i 's/^ServerActive=*/ServerActive=10.214.124.55,10.214.0.112/g' /etc/zabbix/zabbix_agentd.conf
sed -i 's/^Server=*/Server=10.214.124.55,10.214.0.112/g' /etc/zabbix/zabbix_agentd.conf
