Overlay
=======

*Tools for deploying distributed applicaions on IPFS using Python*

This library will be a set of tools for building distributed applications which depend on dynamic content and thus need the ability to coordinate an index of ipfs objects between involved nodes.  The plan is to have each node manage a local blockchain or collection of block chains for each application, which can then be indexed locally.  While this not be massively scalable, it will be a good start until I figure out a good solution for a distributed index.

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
        - a node will make blocks out of newly submitted objects every N (<30) seconds
        - new blocks are added to the local block chain
    - Blockchain
        - each node manages a local copy of the blockchain
        - as new blocks are added to the local copy, a pointer to the head block will be maintained on IPNS
        - gossip
            - every node will periodically (<30s) query the head of each peer’s blockchain at /ipns/<PEER ID>/some/path/.
            - new blocks are merged into the blockchain and a new local blockchain is generated.
- Index
    - tool for indexing a blockchain
    - data structure which can be used to query refs and backrefs of an mdag object.

Architecture
------------
Planning to use gevent to handle the large amount of i/o and periodic tasks.
