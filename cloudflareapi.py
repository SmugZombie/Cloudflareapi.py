# Cloudflare Api
# Ron Egli - Github.com/smugzombie
# Version 0.7

import requests, json, argparse

auth_email = ""
auth_key = ""
api_url = "https://api.cloudflare.com/client/v4"
headers = { 'x-auth-email': auth_email, 'x-auth-key': auth_key, 'content-type': "application/json", 'cache-control': "no-cache" }

def listDNSZones(page=1):
	url = "/zones?per_page=50&page=" + str(page)
	response = requests.request("GET", api_url+url, headers=headers)

	try:
		data = json.loads(response.text)
	except:
		print "Uhoh - List Zones"

	zones = {}
	for x in xrange(len(data['result'])):
		zone = data['result'][x]
		zone_id = len(zones)
		zones[zone['name']] = {}
		zones[zone['name']]['status'] = zone['status']
		zones[zone['name']]['nameservers'] = str(zone['name_servers'][0]) + ", " + str(zone['name_servers'][1])

	zones['stats'] = {}
	zones['stats']['count'] = data['result_info']['count']
	zones['stats']['page'] = data['result_info']['page']
	zones['stats']['total_count'] = data['result_info']['total_count']
	zones['stats']['total_pages'] = data['result_info']['total_pages']

	if data['result_info']['total_pages'] > data['result_info']['page']:
		page += 1
		listDNSZones(page)

	return json.dumps(zones, sort_keys=True, indent=4, separators=(',', ': '))

def getRecordId(host, zone_id):
	url = "/zones/" + str(zone_id) + "/dns_records?name=" + host 
	response = requests.request("GET", api_url+url,  headers=headers)

	try:
		data = json.loads(response.text)
	except:
		print "Uhoh - Create Zone"
	return data['result'][0]['id']

def createZone(domain):
	url = "/zones/"
	payload = "{\"name\":\"" + str(domain) + "\"}";
	response = requests.request("POST", api_url+url, data=payload, headers=headers)

	try:
		data = json.loads(response.text)
	except:
		print "Uhoh - Create Zone"

	return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def createDNSRecord(domain, record, host, content):
	zone_id = getZoneId(domain)
	url = "/zones/" + str(zone_id) + "/dns_records"
	payload = "{\"type\":\"" + str(record) + "\",\"name\":\"" + str(host) + "." + str(domain) + "\",\"content\":\"" + str(content) + "\",\"ttl\":120}"
	response = requests.request("POST", api_url+url, data=payload, headers=headers)
	
	try:
		data = json.loads(response.text)
	except:
		print "Uhoh - Create DNS Record"
	dns_records = {}
	dns_records['id'] = data['result']['id']
	dns_records['type'] = data['result']['type']
	dns_records['name'] = data['result']['name']
	dns_records['content'] = data['result']['content']
	dns_records['success'] = data['success']
	dns_records['errors'] = data['errors']
	return json.dumps(dns_records, sort_keys=True, indent=4, separators=(',', ': '))

def deleteDNSRecord(host, domain):
	zone_id = getZoneId(domain)
	record_id = getRecordId(host+"."+domain, zone_id)
	url = "/zones/" + str(zone_id) + "/dns_records/" + str(record_id)
	response = requests.request("DELETE", api_url+url, headers=headers)

	try:
		data = json.loads(response.text)
	except:
		print "Uhoh - Delete DNS Record"
	dns_records = {}
	dns_records['success'] = data['success']
	dns_records['errors'] = data['errors']
	return json.dumps(dns_records, sort_keys=True, indent=4, separators=(',', ': '))

def listDNSRecords(domain):
	zone_id = getZoneId(domain)
	url = "/zones/" + str(zone_id) + "/dns_records" 
	response = requests.request("GET", api_url+url, headers=headers)
	
	try:
		data = json.loads(response.text)
	except:
		print "Uhoh - List DNS Records"

	dns_records = {}
	for x in xrange(len(data['result'])):
		record = data['result'][x]
		record_id = len(dns_records)
		dns_records[record_id] = {}
		dns_records[record_id]['type'] = record['type']
		dns_records[record_id]['name'] = record['name']
		dns_records[record_id]['content'] = record['content']
		dns_records[record_id]['id'] = record['id']

	return json.dumps(dns_records, sort_keys=True, indent=4, separators=(',', ': '))

def getZoneId(domain):
	url = "/zones/?name=" + str(domain)
	response = requests.request("GET", api_url+url, headers=headers)
	try:
		data = json.loads(response.text)
	except:
		print "Unable to request Zone Id for " + str(domain)
		exit()
	try:
		return data['result'][0]['id']
	except:
		print "You do not appear to have control over " + domain + "'s zone file."
		exit()

########### MAIN ###########

arguments = argparse.ArgumentParser()
arguments.add_argument('--domain','-d', help="Domain name to perform an action on", required=False, default="")
arguments.add_argument('--action','-a', help="Action to perform", required=False, default="list")
arguments.add_argument('--content','-c', help="Content of DNS Record (IP / FQDN)", required=False, default="")
arguments.add_argument('--record','-r', help="Type of DNS Record to perform an action on", required=False, default="")
arguments.add_argument('--host','-H', help="Domain name to perform an action on", required=False, default="")
arguments.add_argument('--id','-i', help="Record ID to perform an action on", required=False, default="")
args = arguments.parse_args()
domain = args.domain
action = args.action
record = args.record
content = args.content
host = args.host
record_id = args.id

if action == "list":
	if domain == "":
		print listDNSZones(1)
	else:
		print listDNSRecords(domain)
	exit()

while domain == "":
	domain = raw_input("What domain name are you looking to perform the " + action + " action on? (Example domain.tld): ").upper()
	if domain != "":
		if "." not in domain:
			print "Invalid Domain " + domain + ". Try Again."
			domain = ""

if action == "create":
	print createZone(domain)

if action == "add":
	while record == "":
		record = raw_input("What type of record are you adding? (A, AAAA, CNAME, MX, LOC, SRV, SPF, TXT, NS): ").upper()
		allowed_record_types = ["A","AAAA","CNAME","MX","LOC","SRV","SPF","TXT","NS"]
		if record not in allowed_record_types:
			record = ""
			print "Invalid Record Type. Try Again."

	# If host not provided in arguments.
	while host == "":
		host = raw_input("What host are you adding this " + record + " record for? (Example: {HOST}." + domain + "): ").upper()
		if host == "":
			print "Invalid Host. Try Again."

	while content == "":
		content = raw_input("What content are you adding to this " + record + " record for " + host + "." + domain + "? (Example: IP or FQDN): ").upper()
		if content == "":
			print "Invalid Content. Try Again."

	print createDNSRecord(domain, record, host, content)

if action == "delete":
	while host == "":
		host = raw_input("What is the host for "+ domain +" that you would like to delete? (Example: {HOST}." + domain + "): ")
		if host == "":
			host = ""
			print "Invalid Host. Try Again."

	print deleteDNSRecord(host, domain)
