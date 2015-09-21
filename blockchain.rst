blockchain spec
---------------

I'm not sure if IPFS intends to create an official blockchain spec, since that
kind of thing seems to be outside the scope of the project for now.  Here I
will be documenting an experimental blockchain spec.

My main goal with this blockchain spec is to facilitate distributed
applications.  The blockchain is composed of blocks that point to mdag objects,
where each node coordinates the head of the blockchain.

Assumptions made:

- new objects only become available at one node


the block
~~~~~~~~~

```

{
  'Data': {
    'height':       <height in blockchain>,
    'app_mhash':    <multihash bound to application>,
    'created_utc':  <unix timestamp @ creation>,
    'num_objects':  <number of objects contained in this block>,
    'previous':     <multihash of previous block>
  },
  'Links': [
    <ipfs object>,
    <ipfs object>,
    ...
  ]
}

```


gossip
~~~~~~


