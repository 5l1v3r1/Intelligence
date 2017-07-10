import os

TIMEOUT = 30
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
DBPATH = 'mongodb://arquanum:qPuDqX2e@138.68.92.9:27017/admin'

ROOTPATH= ''

for i in os.getcwd().split('/')[1:-1]:
        ROOTPATH=ROOTPATH+'/'+i
