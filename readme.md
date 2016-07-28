#Cloudflare API

<pre>
usage: cloudflareapi.py [-h] [--domain DOMAIN] [--action ACTION]
                        [--content CONTENT] [--record RECORD] [--host HOST]
                        [--id ID]

optional arguments:
  -h, --help            show this help message and exit
  --domain DOMAIN, -d DOMAIN
                        Domain name to perform an action on
  --action ACTION, -a ACTION
                        Action to perform
  --content CONTENT, -c CONTENT
                        Content of DNS Record (IP / FQDN)
  --record RECORD, -r RECORD
                        Type of DNS Record to perform an action on
  --host HOST, -H HOST  Domain name to perform an action on
  --id ID, -i ID        Record ID to perform an action on


Basic Commands:<br>
<strong>Lists Zones you Control</strong> 
	#python cloudflareapi.py -a list
<strong>Create a new Zone</strong>
	#python cloudflareapi.py -d example.xyz -a create
<strong>List DNS For a Zone</strong> 
	#python cloudflareapi.py -d example.xyz -a list
<strong>Create a New DNS Record For a Zone</strong> 
	#python cloudflareapi.py -d example.xyz -a add -r <RECORD_TYPE> -H <HOST> -c <RECORD_CONTENT>
<strong>Edit an Existing DNS Record For a Zone</strong> 
	#python cloudflareapi.py -d example.xyz -a modify -r <RECORD_TYPE> -H <HOST> -c <RECORD_CONTENT>
<strong>Delete an Existing DNS Record From a Zone</strong> 
	#python cloudflareapi.py -d example.xyz -a delete -H <HOST>


Requirements:
	* Python requests library (https://pypi.python.org/pypi/requests#downloads)
	* Cloudflare API Credentials
 
</pre>