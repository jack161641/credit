#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
import os
import time
import sys

source='/tmp/logs/'
target_dir=sys.argv[1]
today=target_dir+time.strftime('%Y')+'/'+time.strftime('%m')
files=os.listdir(source)
for file in files:
    if file.find('2017') != -1:
	target=today+os.sep+file+'.tar.gz'
	zip_command = "tar czf '%s' '%s' " % (target,source+file)
	print target
	print zip_command
	if os.system(zip_command) == 0:
	    print 'Successful backup to',target
	    os.remove(source+file)
	else:
	    print 'Backup FAILED'
