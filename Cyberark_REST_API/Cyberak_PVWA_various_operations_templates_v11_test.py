#
# do: pip install pyopenssl in cmd as administrator!
#

import json
import ssl
import time
from builtins import str
from typing import Dict

import requests
import urllib3
urllib3.disable_warnings() # SSL warnings disabled

# Global variables ------------------------------------------
PVWA     = "https://mytestv11.com" # <-- test v11
username = "myuser"
password = "mypassword"

# Connect to Cyberark/Vault/PVWA
# use this in case your environment doesn't "like" the certification and this helps override them
# Try always to avoid this! Consult your admin or whoever can provide with the credentials and other resources!
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python w/o verify HTTPS certifies
    pass
else:
    # Handle environments w/o HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# ------------- To Conn to Cyberark v11 ---------------
url = PVWA + "/PasswordVault/API/Auth/CyberArk/Logon"
#url = PVWA + "/PasswordVault/API/auth/RADIUS/Logon" # <-- if ypu need radius for v9 & v11
body = '{"username": "' + username + '", "password": "' + password + '"}' # unlike other body's contents, user must uphold this (quoted) format
headers = { 'Content-Type': 'application/json' }
response = requests.post(url, headers=headers, data=body, verify=False)
sessionID=response.json()
print(" · Connecting... Status_code:" , response.status_code , "= Connection established:", response.ok ,"; SessionID =" , sessionID[0:30] , "...")
print("   >>>> Sleeping for 1 sec before moving on! <<<<") # just if you would like to pause for a bit :) 
time.sleep(1) 

# ------------ To Create Safe to Cyberark v11 -------------
sf = "mynewsafev11"
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Safes"
body = '{"safe": {"SafeName":"'+sf+'","Description":"'+sf+' from batchrecon","ManagingCPM":"PasswordManager","NumberOfDaysRetention":1}}'
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("POST", url, headers=headers, data=body, verify=False)

# ------------ To Create Account to Cyberark v11 -------------
ac = "mynewaccountv11"
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Account"
body = '{"account": {"safe":"'+sf+'","Description":"'+ac+' from batchrecon","platformID":"CyberarkTest","address":"1.2.3.4","accountName":"'+ac+'", "password":"Test123", "username":"'+ac+'"}}'
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("POST", url, headers=headers, data=body, verify=False)
r.ok

# ------------ To Update Account to Cyberark v11 -------------
sf = "mynewsavev11"
ac = "mynewaccountv11"
id = "199_4" # this must be a number (known) for Cyberark to update the desired account
url = PVWA + "/PasswordVault/api/Accounts/" + id
body = '[{"op":"replace", "path":"address", "value":"010.010.010.00100"}]'
headers = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request('PATCH', url, headers=headers, data=body, verify=False)
r.ok

# -------------- To Query Safe Cyberark v11 ----------------
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Safes"
body = {}
headers = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("GET", url, headers=headers, data=body, verify=False)
response = r.json()
for resp_ in response['GetSafesResult']:
    sfn = resp_['SafeName']
    dsc = resp_['Description']
    print (resp_['ManagingCPM'])
    print (resp_['NumberOfDaysRetention'])
    print (resp_['NumberOfVersionsRetention'])
    print ("Safename: " + sfn + " ; Description: " + dsc)

# reviewing some of the details in GetSafesResult
j = 0
for i in response['GetSafesResult']:
    j += 1
    sfn = i['SafeName']
    dsc = i['Description']
    print ("Safename: [" + str(j) + "] " + sfn + " ; Description: " + dsc)

# -------------- To Query All Accounts in Safe Cyberark v11 ----------------
sf = "mysafev11"
# Use any of the following examples of URL variable
url = PVWA + "/PasswordVault/api/Accounts?limit=1000&filter=safeName eq " + sf # this yields all of the related records
url = PVWA + "/PasswordVault/api/Accounts?limit=1000&offset=500&filter=safeName eq " + sf # this yields all of the related records
url = PVWA + "/PasswordVault/api/Accounts?search="+sf+"&limit=1000"
url = PVWA + "/PasswordVault/api/Accounts?search="+sf+"&limit=10&offset=170&sort=name" # this yields all account which names matches string == '_Py' good version provides id, name, safe)
r = requests.request("GET", url, headers=headers, data=body, verify=False)
response_ = r.json()

# reviewing some of the details in GetSafesResult
for i in response_['GetSafesResult']:
    print(i['SafeName'])

# reviewing some of the details in value
j = 0
for i in response_['value']:
    #print(str(j) +" "+ i['name'])
    print (i['name'])
    j+=1

# reviewing some of other details
x=0
mat = [['id','name','address','userName','platformId','safeName','secretType']]
for response in response_['GetSafesResult']:
    x += 1
    id_ = response['id']
    nam = response['name']
    # optional fields
    #add = response['address']
    #usr = response['userName']
    #plt = response['platformId']
    #saf = response['safeName']
    #sec = response['secretType']
    print("Id: [ "+str(x)+" ] " + str(id_) + " : ") # + str(usr))
    mat.append([id_, nam])
for i in mat:
    print(i[1]) # printing account name only column

# -------------- To Query All Accounts with Paging (offset) in Safe Cyberark v11 ----------------
offs = rows = 0
i = l = 0
page = 1
while True:
    offs = (page * (i+1))
    url = PVWA + "/PasswordVault/api/Accounts?search=<acct_name_prefix>&limit="+str(page)+"&offset="+str(offs)+"&sort=name" # this yields all account which names matches string == '_Py' 8good version proveds id, name, safe)
    url = PVWA + "/PasswordVault/api/Accounts?search=Acct_XX11Py2_&limit=500&offset=500&sort=name"  # this yields all account which names matches string == '_Py' good version provides id, name, safe)
    r = requests.request("GET", url, headers=headers, data=body, verify=False)
    response_ = r.json()
    try:
        j = int(response_['count'])
        k = str(response_['count'])
    except:
        print("eof")
    print(" * total counts() : " + str(j) )
    print("k: " + k)
    for l in range(0, int(j)):
        print(str(response_['value'][l]))
        rows += 1
        print (" ···· part" + str (rows))
    i+=1
    if(j < page):
        print("eof")
        break

# or (this works better!!!!!!).....
x    = 0
offs = 1000
page = 1000
url  = PVWA + "/PasswordVault/api/Accounts?search=<acct_name_prefix>&limit="+str(page)+"&offset="+str(offs)+"&sort=name" # this yields all account which names matches string == '_Py' 8good version proveds id, name, safe)#
r    = requests.request("GET", url, headers=headers, data=body, verify=False)
l    = r.json()['value'].__len__()
for i in range(0, (l)): # there is no need to make this (var - 1). As is covers all the entries from (0 - l) without omitting a single element
    print(" - " + str(x) + " : [ " + str(r.json()['value'][x]['name']) +" ]")
    x += 1

# -------------- To Query Accounts Cyberark v11 ----------------
sf = "mysafev11"
# use one of teh following URL that fits your request 
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts?Keywords=AcctXX11_Py2_0&Safe="+sf+"&limit=100" # this only yields 1 record
url = PVWA + "/PasswordVault/api/Accounts?limit=100&filter=safeName eq RSCCMS-Read"
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts?Keywords=Acct&limit=100" # this only yields 1 record
body = {}
headers = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("GET", url, headers=headers, data=body, verify=False)
response = r.json()
print(json.dumps(response, indent=1))

""""
# InternalProperties (just 1 acct)
acct_id = response['accounts'][0]['AccountID']
cpm_stt = response['accounts'][0]['InternalProperties'][0]
con_dis = response['accounts'][0]['InternalProperties'][1]
cre_met = response['accounts'][0]['InternalProperties'][2]
cpm_err = response['accounts'][0]['InternalProperties'][3]
ret_cnt = response['accounts'][0]['InternalProperties'][4]
lst_fai = response['accounts'][0]['InternalProperties'][5]
lst_tsk = response['accounts'][0]['InternalProperties'][6]
#-- Properties (just 1 acct)
saf_nam = response['accounts'][0]['Properties'][0]['Value']
fol_nam = response['accounts'][0]['Properties'][1]['Value']
acc_nam = response['accounts'][0]['Properties'][2]['Value']
usr_nam = response['accounts'][0]['Properties'][3]['Value']
poli_id = response['accounts'][0]['Properties'][4]['Value']
res_imm = response['accounts'][0]['Properties'][5]['Value']
dev_typ = response['accounts'][0]['Properties'][6]['Value']
address = response['accounts'][0]['Properties'][7]['Value']
"""

for i in (response['accounts'][0]['InternalProperties']):
    print ("InternalProperties: [" + str(i['Key']) + "] : [" + str(i['Value']) + "] ")

for j in (response['accounts'][0]['Properties']):
    print ("Properties: [" + str (j['Key']) + "] : [" + str (j['Value']) + "] ")

# -------------- To Retrieve Credentials Cyberark v11 ----------------
acct_id = response['accounts'][0]['AccountID']
url = PVWA + "/PasswordVault/api/Accounts/" + str(acct_id) + "/Password/Retrieve"
body = {}
headers = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("POST", url, headers=headers, data=body, verify=False)
r.ok

# -------------- To Change Credentials Cyberark v11 ----------------
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts/" + str(acct_id) + "/ChangeCredentials"
body = {}
headers = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID, 'ImmediateChangeByCPM':'Yes' }
r = requests.request("PUT", url, headers=headers, data=body, verify=False)
r.ok

# -------------- To Reconcile Credentials Cyberark v11 ----------------
url = PVWA + "/PasswordVault/API/Accounts/" + str(acct_id) + "/Reconcile"
body = {}
headers = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("POST", url, headers=headers, data=body, verify=False)
r.ok

# -------------- To Change Password Cyberark v11 ----------------
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts/" + str(acct_id) + "/ChangeCredentials"
body = { "ImmediateChangeByCPM" : "Yes" , "ChangeCredsForGroup" : 'No' } # body may not be necessary as headers contains all parameters
headers = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID, "ImmediateChangeByCPM" : "Yes" } # again, what is supposed to be in the body, goes at the end in the headers
r = requests.request("PUT", url, headers=headers, data=body, verify=False)
r.ok

# ------------ To DisConn to Cyberark v11 -------------
url = PVWA + "/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logoff"
body = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
response = requests.post(url, headers=headers, data=body, verify=False)
print(response.status_code)
print(response.json())
print(" · Disconnecting...Status_code:" , response.status_code , "= Connection disengaged:" , response.ok)