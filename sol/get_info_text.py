import requests
import json

from openai import OpenAI

# Function to obtain an authorization ticket
def get_ticket(username, password):
    url = 'http://localhost:58000/api/v1/ticket'
    body = {'username': username, 'password': password}
    resp = requests.post(url, json=body)
    resp_data = resp.json()
    ticket = resp_data['response']['serviceTicket']
    return ticket

# Function to get a list of network devices
def get_devices(ticket):
    url = 'http://localhost:58000/api/v1/network-device'
    headers = {'X-Auth-Token': ticket}
    resp = requests.get(url, headers=headers)
    return resp.json()['response']

# Function to get a list of hosts
def get_hosts(ticket):
    url = 'http://localhost:58000/api/v1/host'
    headers = {'X-Auth-Token': ticket}
    resp = requests.get(url, headers=headers)
    return resp.json()['response']

# Main application code
if __name__ == '__main__':
    admin_ticket = get_ticket('admin', 'admin')
    print(admin_ticket)

    my_devices = get_devices(admin_ticket)
    #print(json.dumps(my_devices, indent=4))

    for device in my_devices:
        print(device['id'], device['hostname'], device['type'], device['managementIpAddress'])

    my_hosts = get_hosts(admin_ticket)
    #print(json.dumps(my_hosts, indent=4))

    for host in my_hosts:
        print(host['id'], host['hostName'], host['hostType'], host['hostIp'])
        
    pass

    gpt = OpenAI()
    
    prompt = f"""
        Analyze the provided data about the network setup and generate a short description of the network. Try to be specific about the numbers and types of devices but do not invent any facts.
        
        Point out if there are any reachability issues in the network.
        
        Network devices:

        {my_devices}
        
        Network hosts:
        
        {my_hosts}
    
    """
    
    print(prompt)

    completion = gpt.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'developer', 'content': 'You are a qualified network engineer.'},
            {'role': 'user', 'content': prompt}
        ],
    )

    analysis = completion.choices[0].message.content
    print(analysis)
    
    pass

