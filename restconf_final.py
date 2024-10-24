import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.189
api_url = "https://10.0.15.189/restconf"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
} # Add 
basicauth = ("admin", "cisco")


# check interface
def get():
    resp = requests.get(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070168",
        auth=basicauth,
        headers=headers,
        verify=False
        )
    
    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        return bool(json.dumps(response_json, indent=4))

def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070168",
            "description": "created loopback by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.168.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    check = get()
    if check == True:
        return "Can't create: Interface loopback 65070168"
    else:
        resp = requests.put(
            api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070168",
            data=json.dumps(yangConfig),
            auth=basicauth, 
            headers=headers, 
            verify=False
            )

        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface Loopback65070168 created."
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Can,t create: Interface loopback 65070168"


def delete():
    resp = requests.delete(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070168", # Add
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070168 is delete successfully>"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Can't delete: Interface loopback 65070168"


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070168",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        }
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070168",
        data=json.dumps(yangConfig),
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070168 is enable successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Can't enable: Interface loopback 65070168"


def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070168",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070168", # Add
        data=json.dumps(yangConfig),
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070168 is disable successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Can't shutdown: Interface loopback 65070168"


def status():
    api_url_status = "https://10.0.15.189/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback65070168"

    resp = requests.get(
        api_url_status,
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        print(json.dumps(response_json, indent=4))
        interface_name = response_json["ietf-interfaces:interface"]["name"]
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if(admin_status == 'up' and oper_status == 'up' and interface_name == 'Loopback65070168'):
            return "Interface loopback 65070168 is enabled"
        elif(admin_status == 'down' and oper_status == 'down' and interface_name == 'Loopback65070168'):
            return "Interface loopback 65070168 is disabled"
        elif(interface_name != 'Loopback65070168'):
            return "No Interface loopback 65070168"
        
    else:
        return "No Interface loopback 65070168"
