#!/usr/bin/python
# -*- coding=UTF-8 -*-

import sys
import os

len_argv=len(sys.argv)
#print '传参数量',len_argv-1

if   len_argv <  4:
    print '参数错误：python '+sys.argv[0]+' 需要编辑的文件 被替换的字符串 提成成的字符串 [另存成的文件]'

elif len_argv >  5:
    print '参数错误：python '+sys.argv[0]+' 需要编辑的文件 被替换的字符串 提成成的字符串 [另存成的文件]'

else:
    if not os.path.isfile(sys.argv[1]):
        print '文件不存在'
        sys.exit()
    s_file  = file(sys.argv[1],'r+')
    old_str = sys.argv[2]
    new_str = sys.argv[3]
    d_file  = file(sys.argv[1]+'.tmp','w')
    for line in s_file.readlines():
        d_file.writelines(line.replace(old_str,new_str))
    s_file.close()
    d_file.close()

    if len_argv == 4:
        os.rename(sys.argv[1]+'.tmp',sys.argv[1])
    else:
        os.rename(sys.argv[1]+'.tmp',sys.argv[4])
