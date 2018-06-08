#!/usr/bin/env python
from pyzabbix import ZabbixAPI
from datetime import datetime
import time

# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = 'http://10.214.0.112/zabbix'

zapi = ZabbixAPI(ZABBIX_SERVER)

# Login to the Zabbix API
zapi.login('Admin', 'zabbix')

item_id = '25471'

# Create a time range
time_from = time.mktime(time.strptime("2017-05-31 18:00:00","%Y-%m-%d %H:%M:%S"))
time_till = time.mktime(time.strptime("2017-05-31 18:30:00","%Y-%m-%d %H:%M:%S"))

# Query item's history (integer) data
history = zapi.history.get(itemids=[item_id],
                           time_from=time_from,
                           time_till=time_till,
                           output='extend',
                           )

# If nothing was found, try getting it from history (float) data
if not len(history):
    history = zapi.history.get(itemids=[item_id],
                               time_from=time_from,
                               time_till=time_till,
                               output='extend',
                               history=0,
                               )

# Print out each datapoint
for point in history:
    print("{0}: {1}".format(datetime.fromtimestamp(int(point['clock']))
                            .strftime("%Y/%m/%d %X"), point['value']))
