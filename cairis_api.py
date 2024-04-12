# author: David Smith
# date: 2024-01-31
# 
# This Class is used to interact with the CAIRIS API.

import requests
import os
class cairis_api():
    def __init__(self):
        self.session_id = None
        self.assets = None
    
    # get session id:
    # this should always be run prior to any other requests to CAIRIS.
    def get_session_id(self) -> str:
        url = "http://localhost:80/api/session"
        username = os.environ.get('CAIRIS_USERNAME')
        password = os.environ.get('CAIRIS_PASSWORD')
        if username is None or password is None:
            print("No username or password found." )
            print("Plase set the environment variables: CAIRIS_USERNAME and CAIRIS_PASSWORD.")
            print("Exiting.")
            exit()

        # post the request to get the session id
        response = requests.post(url, auth=(username, password))
        session_id = ''
        if response.status_code == 200:
            session_id = response.json()["session_id"]
            print("Session ID Created. POST request successful.") 
            self.session_id = session_id
            return session_id
        else:
            print(f"Session ID POST request failed with status code {response.status_code}. Response content:")
            print(response.text)

        # force exit if no session id is created
        if not session_id:
            print("No session ID found. Exiting.")
            exit()

    # get all assets from CAIRIS
    def get_assets(self, session_id):
        if self.session_id == None:
            print("No session ID found, please run 'get_session_id'. Exiting.")
            exit()

        # create the payload for GET request
        # 'localhost' bcause CAIRIS is hosted locally through Docker
        url = "http://localhost:80/api/assets"
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "session_id": session_id,
        }

        # request assets and store results
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print(f"Asset Request successful. Number of Assets found: {len(response.json())}")
            self.assets = response.json()
        else:
            print(f"Request failed with status code {response.status_code}. Response content:")
            print(response.text)
            
    # POST an asset to CAIRIS
    def post_asset(self, asset_name, 
                   asset_short_code,
                   asset_description,
                   asset_significance,
                   asset_environment,
                   asset_properties):
        '''asset_properties = [{'name': 'Confidentiality', 
            'value': 'Medium', 
            'rationale': 'testing rationale'}]'''
        if self.session_id == None:
            print("No session ID found, please run 'get_session_id'. Exiting...")
            exit()
        
        # create the payload for POST request
        url = "http://localhost:80/api/assets"
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "session_id": self.session_id,
        }

        data = {'object': 
                {
                    'theName': asset_name, 
                    'theShortCode': asset_short_code, 
                    'theDescription': asset_description, 
                    'theSignificance': asset_significance, 
                    'theType': 'Hardware', 
                    'isCritical': 0, 
                    'theCriticalRationale': '', 
                    'theTags': [], 
                    'theInterfaces': [], 
                    'theEnvironmentProperties': 
                        [ {
                            'theEnvironmentName': asset_environment, 
                            'theProperties': [ asset_properties ], # at least one property must be defined
                            'theAssociations': []
                        }]
                }
            }

        # post the asset and store results
        response = requests.post(url, headers=headers, params=params, json=data)
        if response.status_code == 200:
            print("Vulnerability POST successful. Response:")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}. Response content:")
            print(response.text)


    # get all vulnerabilities from CAIRIS
    def get_vulnerabilities(self):
        if self.session_id == None:
            print("No session ID found, please run 'get_session_id'. Exiting.")
            exit()

        # create the payload for GET request
        url = "http://localhost:80/api/vulnerabilities"
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "session_id": self.session_id,
        }

        # request vulnerabilities and store results
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print("Vulnerability Request successful. Response:")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}. Response content:")
            print(response.text)

    # post a vulnerability to CAIRIS
    def post_vulnerability(self, asset_name, 
                           vulnerability_name, 
                           vulnerability_description, 
                           vulnerability_probablity, 
                           vulnerability_sec_cat):
        if self.session_id == None:
            print("No session ID found, please run 'get_session_id'. Exiting.")
            exit()

        # Other option is 'Negligible', but security concerns aren't really negligible. 
        # This can be reviewed and altered by the CAIRIS owner if need be.
        match vulnerability_probablity:
            case 'HIGH':
                vulnerability_probablity = 'Catastrophic'
            case 'MEDIUM':
                vulnerability_probablity = 'Critical'
            case 'LOW':
                vulnerability_probablity = 'Marginal'
        print(f'new vulprob: {vulnerability_probablity}')

        # clean vulnerability name - CAIRIS has character limitations which clash with SonarCloud
        asset_name = asset_name.replace(':', ';').replace('_', '-')

        # create the payload for POST request
        url = "http://localhost:80/api/vulnerabilities" #name/" + vulnerability_name
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "session_id": self.session_id,
        }

        data = {'object': {
            'theName': vulnerability_name, 
            'theDescription': vulnerability_description,
            'theType': 'Implementation', #Design, Implementation, or Configuration
            'theTags': [vulnerability_sec_cat], 
            'theEnvironmentProperties': 
                [
                    {
                        'theEnvironmentName': 'Default', 
                        'theSeverity': vulnerability_probablity, 
                        'theAssets': [asset_name] 
                    }
                ]
            }
        }

        # post the vulnerability and print results
        response = requests.post(url, headers=headers, params=params, json=data)
        if response.status_code == 200:
            print("Vulnerability POST successful. Response:")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}. Response content:")
            print(response.text)

