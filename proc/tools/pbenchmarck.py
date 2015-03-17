#! coding: utf-8

#
# Benchmarck between SciELO CitedBy RESTFull API and Tirgramas Bireme.
#
# More about SciELO CitedBy RESTFull API docs: http://docs.scielo.org/projects/citedby/en/latest/
#
# More about Trigramas Bireme: http://trigramas.bireme.br/
#

import time
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

url_tri = 'http://trigramas.bireme.br/cgi-bin/mx/cgi=@scielo/cited?pid='
url_sci = 'http://citedby.scielo.org/api/v1/pid/?q='


# pid_lst = ['S0100-41582005000300006', 'S0798-04692002000100019',
#            'S0102-09352005000400022', 'S0034-89101985000100002',
#            'S0100-204X2005000800003', 'S0034-89101981000300009',
#            'S0034-89102005000300007', 'S1516-35982002000500021',
#            'S0034-89101985000600002', 'S0071-17132003003800004']

pid_lst = []
pids = open('500.pid', 'r').readlines()

for pid in pids:
    pid_lst.append(pid.split('|')[0])

#Start time
start = time.time()

for pid in pid_lst:
    res = requests.get(url_tri + pid)
    res.text

end = time.time()
#End time

print "Duration Trigramas: %s" % str(end-start)


#Start time
start = time.time()

for pid in pid_lst:
    res = requests.get(url_sci + pid)
    res.text

end = time.time()
#End time

print "Duration SciELO: %s" % str(end-start)