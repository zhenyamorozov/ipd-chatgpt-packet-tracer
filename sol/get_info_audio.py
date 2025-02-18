import requests
import json
import base64
import tempfile

from openai import OpenAI
from playsound import playsound

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

def play_mp3_data(mp3_data):
    # Create a temporary file to write the MP3 data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(mp3_data)
        temp_file_path = temp_file.name
    # Play the MP3 file
    playsound(temp_file_path)

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
        model='gpt-4o-audio-preview',
        audio={"voice": "coral", "format": "mp3"},
        messages=[
            # {'role': 'developer', 'content': 'You keep your responses short and straight to the point. You always start your response with \'I believe,\''},
            {'role': 'user', 'content': prompt}
        ],
        modalities=['text', 'audio']
        
    )

    # analysis = completion.choices[0].message.content
    analysis = completion.choices[0].message.audio.transcript
    print(analysis)
    
    mp3_data = base64.b64decode(completion.choices[0].message.audio.data)
    play_mp3_data(mp3_data)
    
    
    
    pass

