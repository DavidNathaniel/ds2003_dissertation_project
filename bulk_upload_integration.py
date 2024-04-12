# author: David Smith
# date: 2024-02-07
# 
# This Module is used to bulk upload concepts (Vulnerabilities) into CAIRIS.
# utilises both CAIRIS and SonarCloud APIs through the imported classes.

from dotenv import load_dotenv
from sonar_api import sonar_api
from cairis_api import cairis_api
import os

# Load environment variables from .env and access them
load_dotenv()
username = os.getenv("CAIRIS_USERNAME")
password = os.getenv("CAIRIS_PASSWORD")
auth_token = os.getenv("SONAR_AUTH_TOKEN")

# Get Hotspots from sonarcloud
sonar = sonar_api()
sonar.get_hotspots()
sonar.get_project()

# Get session ID from CAIRIS
CAIRIS = cairis_api()
assetFound = False
session = CAIRIS.get_session_id()

# find all assets in CAIRIS that match with the SonarCloud project
assets = []
CAIRIS.get_assets(session)
for asset in CAIRIS.assets:
    assets.append(asset['theName'].replace(';', ':').replace('-', '_'))
    if asset['theName'] == 'DavidNathaniel-CN-CW1-Diss;vulnerable-code.py': 
        print('Asset found')
        assetFound = True
print(assets)

if not assetFound:
    print('Asset not found')
    # Future work: If the asset does not exist in cairis, create it (Option A)
    # create_asset()
    # get sonarcloud file name and do changes:
    # assetName = fileName.replace(':', ';').replace('_', '-')
    # create_asset_in_cairis()

# Future work: If the asset does not exist in cairis, create it (Option B)
for hotspot in sonar.hotspots['hotspots']:
    # for future work, the check should be performed, and the asset should be created if it does not exist.
    # currently the asset is created manually in CAIRIS
    if hotspot['component'] not in assets and False:
        print('Creating asset in CAIRIS')
        sonar.get_project()
        CAIRIS.post_asset(sonar.project)
        
    else:
        print('Asset already exists in CAIRIS...adding vulnerability.')
        # message is an amalgamation of the hotspot message and last few characters of the key
        message =  f'''{hotspot['message']}\r\n{hotspot['key']}'''

        # future work: review status should be dynamic through SonarCloud API
        review_status = 'TO_REVIEW:' 
        name = review_status + hotspot['key'][-6:]

        # add vulnerability
        CAIRIS.post_vulnerability(hotspot['component'],
                                   name, 
                                   message, 
                                   hotspot['vulnerabilityProbability'], 
                                   hotspot['securityCategory'])
        # future work: If the vulnerability already exists in CAIRIS, we should not create a new one.
    