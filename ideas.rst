
Blockchain Tree Merge
---------------------

In a network of nodes trying to coordinate a blockchain (a network perhaps less cohesive than the Bitcoin network itself), it would be convenient to think of the blockchain as a tree in order to reduce the number of comparisons necessary.  Therefore instead of nodes keeping track of the pointer to the head of the blockchain, they would keep track of a tree structure.  Then if the head pointers of two coordinating nodes don't match, instead of each node working linearly backwards to figure out the missing blocks, they can traverse this tree instead.

Consider that a scheme where for every 10 blocks added to the block chain, the next block is the merkle root of those 10 blocks (call it a metablock).  Then for every 100 blocks (110 including metablocks), the next block is the merkle root of the previous 10 metablocks, etc etc.  In a situation where blockchains are perhaps more volatile, this would drastically reduce the numer of comparisons necessary in order to compare blockchains.  On a blockchain that has 11153 blocks, for example, the 11,111th block would be the metablock for the first 10,000 actual blocks, then there would be 3 metablocks for the next 3 sets of 10, and then 9 actual blocks that have not been consolidated yet.  Thus, on the first level of the tree there are only 13 hashes.

note that this scheme relies on the generation of metablocks not being arbitrary.

Problems:
~~~~~~~~~
- What if two nodes have metablocks that contain overlapping but different sub-blocks?

Pseudocode:
~~~~~~~~~~~

*Variables beginning in `s_` are sets and operations are defined by [python set notation](https://docs.python.org/2/library/sets.html#set-objects).*

.. code-block:: python

    api = get_ipfs_api()
    
    def merge(self, peer):
        if self.head == peer.head:
        return
      
        # api.ls returns a list of blocks that the given
        # block points to.
        s_self = api.ls(self.head)
        s_peer = api.ls(peer.head)
      
        # The set of blocks needed by this node
        s_need = s_peer - (s_self & s_peer)

        # The set of blocks this node has but the peer doesn't.
        # Some of these blocks could be included in a metablock
        # owned by the peer.
        s_leftover = s_self - (s_self & s_peer)
      
        while len(s_need) > 0:
            block = s_need.pop()
            if not is_metablock(block):
                # self.own performs all operations necessary for this node to
                # own the given block.  Then, add this new block to the
                # leftover set incase it is included in any of the peer's
                # metablocks
                self.own(block)
                s_leftover.add(block)
            else:
                # block is a metablock and thus points to other blocks.
                s_meta = api.ls(block)
                if s_meta <= s_leftover:
                    # relinquish ownership of all blocks contained in the 
                    # metablock and assume ownership of the metablock
                    self.disown(s_meta & s_leftover)
                    self.add(block)
                else:
                    # if this node doesn't yet control all blocks in the
                    # metablock, add the metablock back into the queue and also
                    # add all the blocks this node is missing under the
                    # metablock.
                    s_need.add(block)
                    s_need.add(s_meta & leftover)
