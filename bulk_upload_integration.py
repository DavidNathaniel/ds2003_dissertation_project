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
print(sonar.hotspots)

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
    if hotspot['component'] not in assets:
        print('Creating asset in CAIRIS')
        # create asset code ...

    else:
        print('Asset already exists in CAIRIS...adding vulnerability.')
        #add vulnerability
        CAIRIS.post_vulnerability(hotspot['component'],
                                   hotspot['key'], 
                                   hotspot['message'], 
                                   hotspot['vulnerabilityProbability'], 
                                   hotspot['securityCategory'])
        
        # future work: If the vulnerability already exists in CAIRIS, we should not create a new one.
        # future work: If the vulnerability already exists, and the review in SonarCloud has changed status, this should be represented in CAIRIS.
    