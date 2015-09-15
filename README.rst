Overlay
=======

*Tools for deploying distributed applicaions on IPFS using Python*


Planned Components
------------------

- Transport
    - ipfs daemon
        - make async python-ipfs-api
    - peers
        - each application will have a unique hash
        - use ipfsApi.Client.dht_findprovs(<APP HASH>) in order to find peers
- Blockchain
    - Blocks
        - blocks are mdag objects which link to other mdag objects
        - a node will make blocks out of new posts every N (<30) seconds
        - new blocks are added to the local block chain
    - Blockchain
        - each node manages a local copy of the blockchain
        - as new blocks are added to the local copy, a pointer to the head block will be maintained on ipns
        - gossip
            - every node will periodically (<60s) query the head of each peer’s blockchain at /ipns/<PEER ID>
            - new blocks are merged into the blockchain and a new local blockchain is generated
                - *how are blockchains merged?*
- Index
    - tool for indexing a blockchain
    - data structure which can be used to query refs and backrefs of an mdag object.
