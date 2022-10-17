# IoSL WiSe 2022 - SNET: Internet of Services Lab (Project)

**Contact and Info** \
Patrick Herbke, p.herbke@tu-berlin.de \
Max. 4 Students 

**Project title** \

**Establishing trust in a decentralized network with verifiable credentials**

In electronic communication, trust between entities can be built using a Public-Key-Infrastructure (PKI). 
PKI is a set of roles, policies, and procedures needed to create, manage, distribute, use, store and revoke 
digital certificates and manage public-key encryption. 

A standard for PKI is X.509, used in different internet protocols, such as TLS and offline, for digital signatures of certificates [[1]](#1).   
Digital signed certificates enable entities to authenticate themselves or verify the identity of another entity. 
With X.509, an entity (certified authority CA) can issue a certificate to another (proxy authority) and delegate trust. 
Delegated trust means that the proxy authority can issue verifiable credentials to other entities (holder).
Verifiable credentials can be hold and presented by holders to verifier. 
Based on the hierarchy in X.509, a verifier can check if a presented credential is issued by a trustworthy proxy issuer.
To verify the credentials' authenticity, a verifier can check the signature chain from the proxy issuer to the certified authority [[2]](#2). 

In this project, students will implement the logic of X.509 in the Self-Sovereign Identity paradigm with verifiable credentials (VCs) [[3]](#3).
Self-Sovereign Identity is a paradigm and technology for digital identities and self-determination of (personal) information. 
SSI utilizes VCs as data structures that can be digitally signed, issued, held, and verified. 
The goal of this project is to implement the idea of chained credentials, as described by Glastra et al.
https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0104-chained-credentials/README.md
Furthermore, the implementation will utilize the Hyperledger Aries Cloud Agent - Python (ACA-Py)
https://github.com/hyperledger/aries-cloudagent-python

The research questions is:
- How to adapt certificate chains, such as in X.509, into SSI, a decentralized system?

Number of Students: 3-4

Requirements:
- Good programming skills with Python
- Basic knowledge of PKI, X.509 and SSI

# References
<a id="1">[1]</a> 
Perlman, R. (1999). An overview of PKI trust models. IEEE network, 13(6), 38-43.

<a id="2">[2]</a> 
Welch, V., Foster, I., Kesselman, C., Mulmo, O., Pearlman, L., Tuecke, S., ... & Siebenlist, F. (2004, April). X. 509 proxy certificates for dynamic delegation. In 3rd annual PKI R&D workshop (Vol. 14).

<a id="3">[3]</a>
Tobin, A., & Reed, D. (2016). The inevitable rise of self-sovereign identity. The Sovrin Foundation, 29(2016), 18.
