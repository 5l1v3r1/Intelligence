import os
import sys

TIMEOUT = 30
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
DBPATH = 'mongodb://arquanum:qPuDqX2e@138.68.92.9:27017/admin'
ROOTPATH = ''
RISK={0:3, 1:6, 2:10, 'low':3, 'medium':6, 'high':10}
for i in os.getcwd().split('/')[1:-1]:
        ROOTPATH = ROOTPATH+'/'+i
if ROOTPATH not in sys.path:
        sys.path.append(ROOTPATH)