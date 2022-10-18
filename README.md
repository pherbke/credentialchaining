# IoSL WiSe 2022 - SNET: Internet of Services Lab (Project)

**Contact and Info**

Patrick Herbke, p.herbke@tu-berlin.de \
Max. 4 Students 

**Project title**

**Establishing trust in a decentralized network with verifiable credentials**

In electronic communication, trust between network participants can be built using a Public-Key-Infrastructure (PKI). 
PKI is a set of roles, policies, and procedures needed to create, manage, distribute, use, store and revoke 
digital certificates and manage public-key encryption [[1]](#1).
One prominent example of PKI is signed certificates issued by certified authorities (CA) for websites.
A CA issues a signed certificate to a website that website visitors can prove. 
These certificates can be issued via different hierarchy levels, beginning with a root CA [[2]](#2).

In this project, students will implement a certificate chain, similar to X.509, into the Self-Sovereign Identity paradigm with verifiable credentials (VCs) [[3]](#3).
Good examples and a more detailed description can be found here: https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0104-chained-credentials/README.md
and here https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0103-indirect-identity-control/delegation-details.md 
The implementation will utilize the Hyperledger Aries Cloud Agent - Python (ACA-Py)
https://github.com/hyperledger/aries-cloudagent-python

The research questions is:
- How to adapt certificate chains, such as in X.509, into SSI, a decentralized system?

Number of Students: 4-5

Requirements:
- Good programming skills with Python
- Some front-end programming experience for visualization
- Basic docker knowledge
- Experience in interaction with APIs (swagger, postman)

Knowledge of the following areas are beneficial:
- Good understanding of Public-Key-Infrastructure and X.509
- Basic knowledge of Self-Sovereign Identity
- First look into ACA-Py demos 
(https://github.com/hyperledger/aries-cloudagent-python/tree/main/demo)

# References
<a id="1">[1]</a> 
Perlman, R. (1999). An overview of PKI trust models. IEEE network, 13(6), 38-43.

<a id="2">[2]</a> 
Welch, V., Foster, I., Kesselman, C., Mulmo, O., Pearlman, L., Tuecke, S., ... & Siebenlist, F. (2004, April). X. 509 proxy certificates for dynamic delegation. In 3rd annual PKI R&D workshop (Vol. 14).

<a id="3">[3]</a>
Tobin, A., & Reed, D. (2016). The inevitable rise of self-sovereign identity. The Sovrin Foundation, 29(2016), 18.
