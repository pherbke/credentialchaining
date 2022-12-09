import requests
import json
import time
#install everything mentioned here: https://github.com/hyperledger/aries-cloudagent-python/blob/main/demo/AliceWantsAJsonCredential.md
#especially installation of aries-cloudagent-python in local is important + to run script IDE or python on terminal

#start up FABER in a local GIT Terminal with - (Have docker installed)
#ge --aip 20 --cred-type json-ldght.bcovrin.vonx.io ./run_demo faber --did-exchang

#start up alice in a local GIT Terminal with
#LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo alice



headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

params = {
    'alias': 'Hello alice 1',
}

json_data = {}

#Faber sends connection invitation
response = requests.post('http://localhost:8021/connections/create-invitation', params=params, headers=headers, json=json_data)
print("Faber Sends Connection Invitation")
print(response.content)
print("")


json_response = json.loads(response.content)
#print(json_response['invitation'])
#assign inventation to receive-inviation
json_data = json_response['invitation']

#Alice accepts connection
response2 = requests.post('http://localhost:8031/connections/receive-invitation', headers=headers, json=json_data)
print("Alice Accepts Connection")
print(response2.content)
print("")
json_response2 = json.loads(response2.content)
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.

connection_id_faber = json_response['connection_id']
print(connection_id_faber)
connection_id_alice = json_response2['connection_id']
print(connection_id_alice)
print("")

#TEST SEND BASIC MESSAGE
json_data = {
    'content': 'Alice accept connection failing - probably due to connection auto accept'
}

url = "http://localhost:8021/connections/" + connection_id_faber + "/send-message"
time.sleep(0.1)
print(url)
responseM = requests.post(url, headers=headers, json=json_data)


print("Message Sent")
print(responseM.content)
print("")

#response = requests.post('http://localhost:8021/connections/create-invitation', params=params, headers=headers, data=data)


#prep to issue credential

response3 = requests.get('http://localhost:8021/connections', headers=headers, json=json_data)
json_response3 = json.loads(response3.content)
#print(json_response3['results'][1]['connection_id'])


print("Alice accept connection")
#this is failing due to auto accept
time.sleep(0.4)
#response4 = requests.post('http://localhost:8031/connections/' + connection_id_alice + '/accept-request', headers=headers, json=json_data)

#print(response4.content)
print("")


#DID FABER
did = {
  "method": "key",
  "options": {
    "key_type": "bls12381g2"
  }
}
json_data = did
time.sleep(0.1)
response5 = requests.post('http://localhost:8021/wallet/did/create', headers=headers, json=json_data)
print("Faber DID")
json_response5 = json.loads(response5.content)
print(json_response5['result']['did'])
print("")

#DID alice
json_data = did
time.sleep(0.1)
responsea = requests.post('http://localhost:8031/wallet/did/create', headers=headers, json=json_data)
json_responsea = json.loads(responsea.content)
print("Alice DID")
print(responsea.content)
print(json_responsea['result']['did'])
print("")
#Example credential to be issued
cred = {
  "connection_id": connection_id_faber,
  "filter": {
    "ld_proof": {
      "credential": {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          "https://www.w3.org/2018/credentials/examples/v1"
        ],
        "type": ["VerifiableCredential", "UniversityDegreeCredential"],
        "issuer": json_response5['result']['did'],
        "issuanceDate": "2020-01-01T12:00:00Z",
        "credentialSubject": {
          "degree": {
            "type": "BachelorDegree",
            "name": "Bachelor of Science and Arts"
          },
          "college": "Faber College"
        }
      },
      "options": {
        "proofType": "BbsBlsSignature2020"
      }
    }
  }
}
cred2 = {
    "connection_id": connection_id_faber,
    "filter": {
        "ld_proof": {
            "credential": {
                "@context": [
                    "https://www.w3.org/2018/credentials/v1",
                    "https://w3id.org/citizenship/v1"
                ],
                "type": [
                    "VerifiableCredential",
                    "PermanentResident"
                ],
                "id": "https://credential.example.com/residents/1234567890",
                "issuer": json_response5['result']['did'],
                "issuanceDate": "2020-01-01T12:00:00Z",
                "credentialSubject": {
                    "type": [
                        "PermanentResident"
                    ],
                    "id": json_responsea['result']['did'],
                    "givenName": "ALICE",
                    "familyName": "SMITH",
                    "gender": "Female",
                    "birthCountry": "Bahamas",
                    "birthDate": "1958-07-17"
                }
            },
            "options": {
                "proofType": "BbsBlsSignature2020"
            }
        }
    }
}
chained_cred = {
  "connection_id": connection_id_faber,
  "filter": {
    "ld_proof": {
      "credential": {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          "https://www.w3.org/2018/credentials/examples/v1"
        ],
        "type": ["VerifiableCredential", "UniversityDegreeCredential"],
        "issuer": json_response5['result']['did'],
        "issuanceDate": "2020-01-01T12:00:00Z",
        "credentialSubject": {
          "degree": {
            "type": "BachelorDegree",
            "name": "Bachelor of Science and Arts"
          },
          "college": "Faber College"
        }
      },
      "options": {
        "proofType": "BbsBlsSignature2020"
      }
    }
  }
}

#print(cred)
#assign credential to json-data for request
json_data = cred2
#send request faber
time.sleep(0.1)
response6 = requests.post('http://localhost:8021/issue-credential-2.0/send', headers=headers, json=json_data)
print("Credential issued to alice")
print(response6)
print(response6.content)
print("")

json_data = {}
#Alice sends request to see credentials in wallet
time.sleep(0.5)
response7 = requests.post('http://localhost:8031/credentials/w3c', headers=headers, json=json_data)
print("Alice Gets her w3c credentials")
print(response7)
print(response7.content)
print("")
json_response7 = json.loads(response7.content)

#TEST MESSAGE
time.sleep(0.5)
json_data = {
    'content': 'It seems that this proof is failing:',
}
responseM = requests.post('http://localhost:8031/connections/' + connection_id_alice + '/send-message', headers=headers, json=json_data)
print("Test Message Sent")
print("")

#proof if credential valid?
json_data = {
    "comment": "string",
    "connection_id": connection_id_faber,
    "presentation_request": {
          "dif": {
              "options": {
                  "challenge": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                  "domain": "4jt78h47fh47"
              },
              "presentation_definition": {
                  "id": "32f54163-7166-48f1-93d8-ff217bdb0654",
                  "format": {
                      "ldp_vp": {
                          "proof_type": [
                              "BbsBlsSignature2020"
                          ]
                      }
                  },
                  "input_descriptors": [
                      {
                          "id": "citizenship_input_1",
                          "name": "EU Driver's License",
                          "schema": [
                              {
                                  "uri": "https://www.w3.org/2018/credentials#VerifiableCredential"
                              },
                              {
                                  "uri": "https://w3id.org/citizenship#PermanentResident"
                              }
                          ],
                          "constraints": {
                              "limit_disclosure": "required",
                              "is_holder": [
                                  {
                                      "directive": "required",
                                      "field_id": [
                                          "1f44d55f-f161-4938-a659-f8026467f126"
                                      ],
                                  }
                              ],
                              "fields": [
                                  {
                                      "id": "1f44d55f-f161-4938-a659-f8026467f126",
                                      "path": [
                                          "$.credentialSubject.familyName"
                                      ],
                                      "purpose": "The claim must be from one of the specified issuers",
                                      "filter": {
                                          "const": "SMITH"
                                      }
                                  },
                                  {
                                      "path": [
                                          "$.credentialSubject.givenName"
                                      ],
                                      "purpose": "The claim must be from one of the specified issuers"
                                  }
                            ]
                        }
                    }
                ]
            }
        }
    }
}
print(json_response7['results'])
response8 = requests.post('http://localhost:8021/request-presentation-2.0/request-proof', headers=headers, json=json_data)
print(response8)
print(response8.content)
