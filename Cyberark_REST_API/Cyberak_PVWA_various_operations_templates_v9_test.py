#
# do: pip install pyopenssl in cmd as administrator!
#
import json
import ssl
import time
from builtins import str
import requests
import urllib3
urllib3.disable_warnings() # SSL warnings disabled

# Global variables ------------------------------------------
PVWA     = "https://mytestv9.com" # <-- test v9
username = "myuser"
password = "mypasword"

# Connect to Cyberark/Vault/PVWA
# use this in case your environment doesn't "like" the certification and this helps override them
# Try always to avoid this! Consult your admin or whoever can provide with the credentials and other resources!
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# ------------- To Conn to Cyberark v9 ---------------
url = PVWA + "/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logon"
body = '{"username": "' + username + '", "password": "' + password + '"}'
headers = { 'Content-Type': 'application/json' }
response = requests.post(url, headers=headers, data=body, verify=False)
sessionID=response.json()['CyberArkLogonResult']
print(" · Connecting...Status_code:" , response.status_code , "= Connection established:", response.ok ,"; SessionID =" , sessionID[0:30] , "...")
print("   >>>> Sleeping for 1 sec before moving on! <<<<")
time.sleep(1)

# ------------ To Create Safe to Cyberark v9 -------------
sf = "mynewsafe"
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Safes"
body = '{"safe": {"SafeName":"'+sf+'","Description":"'+sf+'","ManagingCPM":"PasswordManager","NumberOfDaysRetention":1}}'
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("POST", url, headers=headers, data=body, verify=False)
r.text

# ------------ To Create Account to Cyberark v9 -------------
ac = "TestAv9_Py3"
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Account"
body = '{"account": {"safe":"'+sf+'","Description":"'+ac+'","platformID":"CyberarkTesting","address":"145.168.21.68","accountName":"'+ac+'", "password":"Test1234.", "username":"'+ac+'"}}'
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("POST", url, headers=headers, data=body, verify=False)
r.ok

# ------------ To Update Account to Cyberark v9 -------------
id = '293_3' # this value must be known beforehand
ac = 'myaccountv9'
sf = 'mysafev9'
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts/" + id
body = '{ "Accounts": { "Folder":"Root", "AccountName":"'+ac+'", "DeviceType":"Application", "PlatformID":"CyberarkTesting", "Address":"0012.0034.0056.0078", "UserName":"uXXXXXX02", "GroupName":"", "GroupPlatformID":"" } }'
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request('PUT', url, headers=headers, data=body, verify=False)
r.text

# -------------- To Query Safe Cyberark v9 ----------------
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Safes"
body = {} # just a quick var cre : it might not be used here!
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("GET", url, headers=headers, data=body, verify=False)
response = r.json()
for response in response['GetSafesResult']:
    sfn = response['SafeName']
    dsc = response['Description']
    """
    print (response['SafeName'])
    print (response['Description'])
    print (response['ManagingCPM'])
    print (response['NumberOfDaysRetention'])
    print (response['NumberOfVersionsRetention'])
    """
    print ("Safename: " + sfn + " ; Description: " + dsc)

# or
response = r.json()
j = 0
for i in response['GetSafesResult']:
    j += 1
    sfn = i['SafeName']
    dsc = i['Description']
    print ("Safename: [" + str(j) + "] " + sfn + " ; Description: " + dsc)

# -------------- To Query Accounts Cyberark v9 ----------------
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts?Keywords=Acctv9_Py1&Safe=TestAv9_Py1"
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts?Keywords="+ac+""
body = {} # just a quick var cre! it may not be used here!
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("GET", url, headers=headers, data=body, verify=False)
response = r.json()
# Important!!! with this query, addressing InternalProperties, information on File Categories (e.g. CPMStatus) can be queried with no activity log query
j = 0
for i in response['accounts']:
    j += 1
    # InternalProperties
    acct_id = response['accounts'][0]['AccountID']
    cpm_stt = response['accounts'][0]['InternalProperties'][0]
    con_dis = response['accounts'][0]['InternalProperties'][1]
    cre_met = response['accounts'][0]['InternalProperties'][2]
    cpm_err = response['accounts'][0]['InternalProperties'][3]
    ret_cnt = response['accounts'][0]['InternalProperties'][4]
    lst_fai = response['accounts'][0]['InternalProperties'][5]
    lst_tsk = response['accounts'][0]['InternalProperties'][6]
    # Properties
    saf_nam = response['accounts'][0]['Properties'][0]['Value']
    fol_nam = response['accounts'][0]['Properties'][1]['Value']
    acc_nam = response['accounts'][0]['Properties'][2]['Value']
    usr_nam = response['accounts'][0]['Properties'][3]['Value']
    poli_id = response['accounts'][0]['Properties'][4]['Value']
    res_imm = response['accounts'][0]['Properties'][5]['Value']
    dev_typ = response['accounts'][0]['Properties'][6]['Value']
    address = response['accounts'][0]['Properties'][7]['Value']
    print ("AccountID: [" + str(j) + "] " + str(acct_id) + " ; UserName: " + str(acc_nam))

# ------------ To Query Password To Cyberark v9 -------------
# acct_id is taken from above operations!
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts/" + str(acct_id) + "/Credentials"
body = {} # just a quick var cre! it may not be used here!
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("GET", url, headers=headers, data=body, verify=False)
r.ok

# ------------ To Change/ImmediateChangeByCPM Credentials to Cyberark v9 -------------
# acct_id is taken from above operations!
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts/" + str(acct_id) + "/ChangeCredentials"
body = {} # just a quick var cre! it may not be used here!
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID, 'ImmediateChangeByCPM':'Yes' } # again, what is supposed to be in the body, goes at the end in the headers
r = requests.request("PUT", url, headers=headers, data=body, verify=False)
r.ok

# ------------ To Verify Credentials to Cyberark v9 -------------
# acct_id is taken from above operations!
url = PVWA + "/PasswordVault/WebServices/PIMServices.svc/Accounts/" + str(acct_id) + "/VerifyCredentials"
body = {} # just a quick var cre! it may not be used here!
headers = {} # just a quick var cre
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
r = requests.request("PUT", url, headers=headers, data=body, verify=False)
r.ok

# ------------ To DisConn to Cyberark v9 -------------
url = PVWA + "/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logoff"
body = {}
headers = { 'Content-Type': 'application/json', 'Authorization': sessionID }
response = requests.post(url, headers=headers, data=body, verify=False)
#print(response.status_code)
#print(response.json())
print(" · Disconnecting...Status_code:" , response.status_code , "= Connection disengaged:" , response.ok)