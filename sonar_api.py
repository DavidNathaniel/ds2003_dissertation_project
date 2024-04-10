# author: David Smith
# date: 2024-01-22
# 
# This Class is used to interact with the SonarCloud Web API.

import requests, json
import os


class sonar_api():
    def __init__(self):
        # must have an auth token to access the SonarCloud API
        self.session_id = os.environ.get('SONAR_AUTH_TOKEN')
        self.project_key = os.environ.get('SONAR_PROJECT_KEY')
        self.hotspots = None
        if self.session_id is None or self.project_key is None:
            print("Please set the environment variableS: SONAR_AUTH_TOKEN, SONAR_PROJECT_KEY")
            print("Exiting.")
            exit()
    

    # retrieve all hotspots from SonarCloud
    def get_hotspots(self):
        url = 'https://sonarcloud.io/api/hotspots/search?deprecated=false&projectKey=' + self.project_key
        headers = {
            'Authorization': self.session_id,
        }   

        # Get the hotspotsfrom SonarCloud
        response = requests.get(url, headers=headers)
        if (response.status_code == 200 ):
            #print(response.json())
            self.hotspots = response.json()
        else:
            print(f"Request failed with status code {response.status_code}. Response content:")
            print(response.text)