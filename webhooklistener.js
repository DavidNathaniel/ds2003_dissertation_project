// Authored by: David Smith
// Date: 2024-03-15


require('dotenv').config();
// Access the API key from the environment variables
const secretKey = process.env.SONAR_API_KEY; 

const express = require('express');
const bodyParser = require('body-parser');
const crypto = require('crypto');

const app = express();
const port = 5353;

// Middleware to parse JSON
app.use(bodyParser.json());

app.post('/webhook-endpoint', (req, res) => {
  const sonarCloudPayload = req.body;
  console.log('Received SonarCloud webhook:', sonarCloudPayload);
  
  /*
   * Perform actions based on the payload:
   * is the payload from SonarCloud? check the signature
   * was scan completed successfully? 
   * is there a new issue / hotspot?
   *
   * Can also use this webserver to activate the pipeline:
   * find objects in cairis (vulnerabilities, assets, etc)
   * create objects in cairis
   */

  res.status(200).send('Webhook received successfully');
  // Check if the request has a valid signature (using SC hmac)
  /*if (isValidSignature(req)) {
    // Signature is valid, process the payload
    const sonarCloudPayload = req.body;
    console.log('Received SonarCloud webhook:', sonarCloudPayload);

    // Perform actions based on the payload
    // (Is scan completed successfuklly? is there a new issue? )

    res.status(200).send('Webhook received successfully');
  } else {
    // Invalid signature, reject the request
    console.error('Invalid signature. Request rejected.');
    res.status(403).send('Invalid signature');
  }*/
});

app.listen(port, () => {
  console.log(`Web server listening at http://localhost:${port}`);
});

// Function to validate the request signature
function isValidSignature(req) {
  const receivedSignature = req.get('X-Sonar-Webhook-HMAC-SHA256');
  console.log('Received Signature:', receivedSignature);

  const expectedSignature = calculateHmac(req.rawBody || '', secretKey);
  console.log('Expected Signature:', expectedSignature);
  
  return receivedSignature === expectedSignature;
}

// Function to calculate HMAC with SHA-256
function calculateHmac(data, key) {
  const hmac = crypto.createHmac('sha256', key);
  hmac.update(data);
  return hmac.digest('hex');
}
