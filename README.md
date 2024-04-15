# CAIRIS-Linter Integration Through DevOps Platform

## Abstract
In the realm of security analysis, CAIRIS (Computer-Aided Integrating Requirements and In-formation Security) operates as a tool developers may use to improve the security and usability of their systems. It stands as a robust platform, offering a suite of risk analysis tools to prevent security breaches. One of its integral features is threat modeling, indispensable for modern systems and organizations requiring adept security analysis. To enhance CAIRIS’s capabilities, this dissertation explores the integration of static vulnerability analysis through the use of Linters. The overarching objective is to seamlessly link CAIRIS with a modern and accessible Linter through a DevOps CI/CD (Continuous Integration / Continuous Delivery) platform. This integration project can extend to all DevOps platforms, but has a particular focus on leveraging GitHub Actions through the GitHub platform. 

## Repository Overview

This repository was used to develop the integration for ds2003's dissertation project. The other repository containing the vulnerable code file can be found [at this GitHub repository](https://github.com/DavidNathaniel/CN_CW1_Diss)

## .env
An extra .env file was created to store API keys and account details which has not been uploaded to this repository as they are unique to this project. They are loaded in the code files below using the [Python dotenv library](https://github.com/theskumar/python-dotenv).

## Code Files

1. **[sonar_api.py](sonar_api.py)**: Used to interact with the [SonarCloud web API](https://sonarcloud.io/web_api). To utilise this correctly, a user will need to create their own SonarCloud account, project, and finally token. The token is what allows user to communicate with the API, the token used for this project is stored in the repository secrets.
   
2. **[cairis_api.py](cairis_api.py)**: Used to interact with the [CAIRIS web API](https://app.swaggerhub.com/apis/failys/CAIRIS/1.0.14). To utilise this correctly, a user will need to create their own [CAIRIS environment](https://cairis.readthedocs.io/en/latest/install.html). For this project the CAIRIS environment was stored locally using a Docker container.

3. **[bulk_upload_integration.py](bulk_upload_integration.py)**: Uses the classes described above to bulk upload vulnerabilities from SonarCloud to CAIRIS.

4. **[webhooklistener.js](webhooklistener.js)**: Used to receive webhooks from SonarCloud via [NGROK](https://ngrok.com/). This aspect of the intergration could be further automated to activate the codefiles above. The current implementation uses the [bulk upload solution](bulk_upload_integration.py) as described in the dissertation.
