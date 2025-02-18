import requests
import json
import time

from get_info import get_ticket
from get_info import get_hosts

# Get path trace
def get_pathtrace(ticket, source_ip, dest_ip):
    url = 'http://localhost:58000/api/v1/flow-analysis'
    headers = {'X-Auth-Token': ticket}
    body = {'sourceIP': source_ip, 'destIP': dest_ip}
    resp = requests.post(url, headers=headers, json=body)
    resp_data = resp.json()
    flow_analysis_id = resp_data['response']['flowAnalysisId']

    url = 'http://localhost:58000/api/v1/flow-analysis/' + flow_analysis_id
    headers = {'X-Auth-Token': ticket}
    
    
    while True:
        resp = requests.get(url, headers=headers)
        resp_data = resp.json()
        #print(json.dumps(resp_data, indent=4))
        if resp_data['response']['request']['status'] != 'INPROGRESS':
            return resp_data['response']
        time.sleep(.1)
        
        
my_ticket = get_ticket('admin', 'admin')
print(my_ticket)

#my_trace = get_pathtrace(my_ticket, '10.0.2.130', '192.168.101.100')
#print(json.dumps(my_trace, indent=4))

my_hosts = get_hosts(my_ticket)
#print(json.dumps(my_hosts, indent=4))

for source in my_hosts:
    for dest in my_hosts:
        pathtrace = get_pathtrace(my_ticket, source['hostIp'], dest['hostIp'])
        print(source['hostIp'], dest['hostIp'], pathtrace['request']['status'], len(pathtrace['networkElementsInfo']))


