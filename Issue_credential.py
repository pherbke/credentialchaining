import requests
import json
import time
#start up FABER in a local GIT Terminal with - (Have docker installed)
#ge --aip 20 --cred-type json-ldght.bcovrin.vonx.io ./run_demo faber --did-exchang

#start up alice in a local GIT Terminal with
#LEDGER_URL=http://dev.greenlight.bcovrin.vonx.io ./run_demo alice



def issuefaber():
    print("test")



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
    cred_did = json_response5['result']['did']
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
    cred_not_in_use = {
   "connection_id":connection_id_faber,
   "filter":{
      "ld_proof":{
          "credential": {
              "@context": [
                  "https://www.w3.org/2018/credentials/v1",
                  "https://www.w3.org/2018/credentials/examples/v1"
              ],
              "issuer": cred_did,
              "issuanceDate": "2020-01-01T12:00:00Z",
              "credentialSubject": {
                  "degree": {
                      "type": "Promotion",
                      "name": "Doctor of Science and Arts"
                  },
                  "college": "Faber College"
              },
              "type": [
                  "VerifiableCredential", "UniversityDegreeCredential"
              ],
              "schema": "WwogICJAY29udGV4dCIsIC8vSlN... (clipped for brevity) ...ob2x",
              "provenanceProofs": [
                  [
                      [
                          "authorization"
                      ],
                      {

                      }
                  ]
              ],
              "credentialSubject.car.VIN": "1HGES26721L024785",
              "credentialSubject.holder.name": "Ur Wheelz Houston",
              "credentialSubject.holder.id": "did:example:12345",
              "credentialSubject.holder.role": "regional_office"
          },
         "options":{
            "proofType":"BbsBlsSignature2020"
         }
      }
   }
    }

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
    sample_cred2 = {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          {
            "provenanceProofs": {
              "@id": "https://www.w3.org/2018/credentials/v1",
              "@type": "@id"
            }
          },
          "https://w3id.org/security/bbs/v1"
        ],
        "type": [
          "VerifiableCredential",
          "UniversityDegreeCredential"
        ],
        "issuer": "did:key:zUC79greFef5EGb61dH6NwXsnoUXTxhp3dRLuzP8Nd92e4doQiuJXQ4KUMjPV7vo5fVmgNm5PkjSTMzCo4wihwT6v3hDWBBEVGEwkDj369pooaaRyerVoVThWpZxXbxp3zKRqTS",
        "issuanceDate": "2022-01-01T12:00:00Z",
        "credentialSubject": {
          "id": "did:key:zUC7Jv1h21wxx8VFGitEGwmYZzG7X4nm9zFgug2EsvBoH3EYasGnNdsAfM7eGxqkiUXMpx5X9rn9NdbteyTgQe6uj8U5GvSpv39Vo3GaSZya6LAi1NUuPgqTYBQGTS3cKGwN2GN"
        },
        "proof": {
          "type": "BbsBlsSignature2020",
          "proofPurpose": "assertionMethod",
          "verificationMethod": "did:key:zUC79greFef5EGb61dH6NwXsnoUXTxhp3dRLuzP8Nd92e4doQiuJXQ4KUMjPV7vo5fVmgNm5PkjSTMzCo4wihwT6v3hDWBBEVGEwkDj369pooaaRyerVoVThWpZxXbxp3zKRqTS#zUC79greFef5EGb61dH6NwXsnoUXTxhp3dRLuzP8Nd92e4doQiuJXQ4KUMjPV7vo5fVmgNm5PkjSTMzCo4wihwT6v3hDWBBEVGEwkDj369pooaaRyerVoVThWpZxXbxp3zKRqTS",
          "created": "2023-01-22T18:19:09.157596+00:00",
          "proofValue": "tzthlm5X10IkLprPBHtNKnnsucZFXfEliUGfnBM4uFERxUbbDx855d7eXtZc/TZwa3e9EaO8wmII8dw0gQ37E3w/uln9fyLu5urrxyC2ZG0myVm0aQ1ZiAlO3YgH0xGf8Pfk4+MzXRkQzvEItOXvTQ=="
        },
        "provenanceProofs": [
          {
            "proof": {
              "type": "BbsBlsSignature2020",
              "proofPurpose": "assertionMethod",
              "verificationMethod": "did:key:zUC776nyCxdnbwSaQQyLeaSgrJTzTcY9pdU1zttMhcuK22gwzaRzT8BuJ7yBtmFSVMcL46q5bGBGF9xTzmJ1Noy7BD5hHtpZXi7gPYGXwbhCY6Rg1zEbTTvXAT8AZrr6cpFQxw8#zUC776nyCxdnbwSaQQyLeaSgrJTzTcY9pdU1zttMhcuK22gwzaRzT8BuJ7yBtmFSVMcL46q5bGBGF9xTzmJ1Noy7BD5hHtpZXi7gPYGXwbhCY6Rg1zEbTTvXAT8AZrr6cpFQxw8",
              "created": "2023-01-22T16:07:50.350085+00:00",
              "proofValue": "rZ+CacHwikuXH2bmX80jtzWcU8/NLK9qUFoAdhpT6qcCClqCqOATnPNva7eI1azrcXne9xKxuQK17iPtf/FAWl5gVm2Am+w2WUkzOvjD8c0Zn4Fg8F+2AQFwIqlJkeuLhpJyaKi1ZOe+X4vyOjy1RQ=="
            }
          }
        ]
      }
    sample_cred = {
            "proof": {"type": "BbsBlsSignature2020", "proofPurpose": "assertionMethod",
                      "verificationMethod": "did:key:zUC776nyCxdnbwSaQQyLeaSgrJTzTcY9pdU1zttMhcuK22gwzaRzT8BuJ7yBtmFSVMcL46q5bGBGF9xTzmJ1Noy7BD5hHtpZXi7gPYGXwbhCY6Rg1zEbTTvXAT8AZrr6cpFQxw8#zUC776nyCxdnbwSaQQyLeaSgrJTzTcY9pdU1zttMhcuK22gwzaRzT8BuJ7yBtmFSVMcL46q5bGBGF9xTzmJ1Noy7BD5hHtpZXi7gPYGXwbhCY6Rg1zEbTTvXAT8AZrr6cpFQxw8",
                      "created": "2023-01-22T16:07:50.350085+00:00",
                      "proofValue": "rZ+CacHwikuXH2bmX80jtzWcU8/NLK9qUFoAdhpT6qcCClqCqOATnPNva7eI1azrcXne9xKxuQK17iPtf/FAWl5gVm2Am+w2WUkzOvjD8c0Zn4Fg8F+2AQFwIqlJkeuLhpJyaKi1ZOe+X4vyOjy1RQ=="}
    }
    # print(cred)
    cred_in_use = {
        "connection_id": connection_id_faber,
        "filter": {
            "ld_proof": {
                "credential": {
                    "@context": [
                        "https://www.w3.org/2018/credentials/v1",
                        {

                            "provenanceProofs": {
                                "@id": "https://www.w3.org/2018/credentials/v1",
                                "@type": "@id"


                          }}
                    ],
                    "type": ["VerifiableCredential","UniversityDegreeCredential"],
                    "issuer": json_response5['result']['did'],
                    "issuanceDate": "2022-01-01T12:00:00Z",
                    "credentialSubject": {
                        "id": json_responsea['result']['did'],
                    },
                    "provenanceProofs": [sample_cred2]
                },
                "options": {
                    "proofType": "BbsBlsSignature2020"
                }
            }
        }
    }
    cred_not_in_use = {
      "connection_id": connection_id_faber,
      "filter": {
        "ld_proof": {
    "credential": {
            "@context": [
              "https://www.w3.org/2018/credentials/v1",
              "https://www.w3.org/2018/credentials/examples/v1",
              "https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0104-chained-credentials/"
            ],
            "type": ["VerifiableCredential", "UniversityDegreeCredential"],
            "issuer": json_response5['result']['did'],
            "issuanceDate": "2020-01-01T12:00:00Z",
            "credentialSubject": {
              "degree": {
                "type": "Promotion",
                "name": "Doctor of Science and Arts"
              },
              "college": "Faber College"
            },
            "schema": "WwogICJAY29udGV4dCIsIC8vSlN... (clipped for brevity) ...ob2x"

          },
          "options": {
            "proofType": "BbsBlsSignature2020"
          }
        }
      }
    }

    #assign credential to json-data for request
    #UPDATE cred passed by function
    json_data = cred_in_use
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
    response8 = requests.post('http://localhost:8021/present-proof-2.0/send-request', headers=headers, json=json_data)
    print(response8)
    print(response8.content)
issuefaber()

#alice connect to acme

def issuealice():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    params = {
        'alias': 'Hello acme 1',
    }

    json_data = {}

    #alice sends connection invitation
    response = requests.post('http://localhost:8031/connections/create-invitation', params=params, headers=headers, json=json_data)
    print("Faber Sends Connection Invitation")
    print(response.content)
    print("")


    json_response = json.loads(response.content)
    print(json_response['invitation'])
    #assign inventation to receive-inviation
    json_data = json_response['invitation']

    #Alice accepts connection
    response2 = requests.post('http://localhost:8041/connections/receive-invitation', headers=headers, json=json_data)
    print("Acme Accepts Connection")
    print(response2.content)
    print("")
    json_response2 = json.loads(response2.content)
    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.

    connection_id_alice2 = json_response['connection_id']
    print(connection_id_alice2)
    connection_id_acme = json_response2['connection_id']
    print(connection_id_acme)
    print("")


    #alice issues credential to acme -
    #DID ACME
    did = {
        "method": "key",
        "options": {
            "key_type": "bls12381g2"
        }
    }
    json_data = did
    time.sleep(0.2)
    responseac = requests.post('http://localhost:8041/wallet/did/create', headers=headers, json=json_data)
    json_responseac = json.loads(responseac.content)

    credential_in_use = {
    "@context": ["https://w3.org/2018/credentials/v1", "https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0104-delegatable-credentials"],
    "provenanceProofs": {
        [["authorization"], ]
    },
    "credentialSubject.car.VIN": "1HGES26721L024785",
    "credentialSubject.proxied.permissions": {
        "grant": ["drive", "delegate"],
        "when": { "role": "renter" }
    },

    "credentialSubject.holder.name": "Alice Jones",

    "credentialSubject.holder.id": "did:example:12345",
    "credentialSubject.holder.role": "renter",

    "credentialSubject.holder.constraints.startTime": "2020-05-20T14:00Z",
    "credentialSubject.holder.constraints.endTime": "2020-05-27T14:00Z",

    "credentialSubject.holder.constraints.boundary": "USA:TX"
    }
    chained = {
        "connection_id": connection_id_alice2,
        "filter": {
            "ld_proof": {
                "credential": {
                    "@context": [
                        "https://www.w3.org/2018/credentials/v1",
                        "https://www.w3.org/2018/credentials/examples/v1"
                    ],
                    "type": [
                        "VerifiableCredential", "UniversityDegreeCredential"
                    ],
                    "issuer": json_response['result']['did'],
                    "issuanceDate": "2022-01-01T12:00:00Z",
                    "credentialSubject": {
                        "degree": {
                            "type": "BachelorDegree",
                            "name": "Bachelor of Science and Arts"
                          },
                        "id": json_responseac['result']['did'],
                        "givenName": "ALICE",
                        "familyName": "SMITH",
                        "college": "Alice Class"
                    },
                    "proof": {
                        "type": "BbsBlsSignature2020",
                        "proofPurpose": "assertionMethod",
                        "verificationMethod": "did:key:zUC711oTkePo4NUAEkYHtT535ui8De922UspFk7xT8ussbK7f5Y3tP5bUpk3jg7Ym9EfSHdibEzExAZQQNB32e2VixnxzfnYzEujZyADcewSQrCT2EW1KAwgMxj5mGfsnzLY3FL#zUC711oTkePo4NUAEkYHtT535ui8De922UspFk7xT8ussbK7f5Y3tP5bUpk3jg7Ym9EfSHdibEzExAZQQNB32e2VixnxzfnYzEujZyADcewSQrCT2EW1KAwgMxj5mGfsnzLY3FL",
                        "created": "2022-12-11T18:07:20.775192+00:00",
                        "proofValue": "kuBH1p1HkMcFPMOTurN2o6Mcs/4yfU9M3c0K9TSN7dKPSAd7mMKpBk/vixE+I4V8IVLnnx2C+14a99L1ODpllrDi9aYwLDVRQv4l1TmF36dlCmaOrIphDpe6SeurQOlYowHdCtwDxTbDleBxCcHL8g=="
                    }
                },
                "options": {
                    "proofType": "BbsBlsSignature2020"
                }
            }
        }
    }
    #TEST MESSAGE
    time.sleep(0.5)
    json_data = {
        'content': 'It seems that this proof is failing:',
    }
    responseM = requests.post('http://localhost:8041/connections/' + connection_id_acme + '/send-message', headers=headers, json=json_data)
    print("Test Message Sent")
    print("")

    #print(cred)
    #assign credential to json-data for request
    json_data = credential_in_use
    time.sleep(0.5)
    responseacme = requests.post('http://localhost:8031/issue-credential-2.0/send-offer', headers=headers, json=json_data)
    print("Credential issued to acme")
    print(responseacme)
    print(responseacme.content)
    print("")


    time.sleep(0.2)

    time.sleep(0.2)
    #ACME accepts credential offer
    json_responseacme = json.loads(responseacme.content)
    print("")
    print("")
    print(json_responseacme["cred_ex_id"])
    print("")
    print("")
    url1 = "http://localhost:8041/issue-credential-2.0/" + json_responseacme["cred_ex_id"] + "/store"

    print(json_response7['results'])
    json_data={}
    responseacc = requests.post(url1, headers=headers, json=json_data)
    print(responseacc)
    print(responseacc.content)


    #proof if credential valid?
    json_data = {}
    #acme sends request to see credentials in wallet
    time.sleep(0.5)
    responseacme1 = requests.post('http://localhost:8041/credentials/w3c', headers=headers, json=json_data)
    print("acme Gets her w3c credentials")
    print(responseacme1)
    print(responseacme1.content)
    print("")
    json_responseacme1 = json.loads(responseacme1.content)

    #TEST MESSAGE
    time.sleep(0.5)
    json_data = {
        'content': 'It seems that this proof is failing:',
    }
    responseM = requests.post('http://localhost:8041/connections/' + connection_id_acme + '/send-message', headers=headers, json=json_data)
    print("Test Message Sent")
    print("")

    #proof if credential valid?
    json_data = {
        "comment": "string",
        "connection_id": connection_id_alice2,
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
    response8 = requests.post('http://localhost:8031/present-proof-2.0/send-request', headers=headers, json=json_data)
    print(response8)
    print(response8.content)
#issuealice()
