
Blockchain TreeMerge Pseudocode
----------------------------------

The Blockchain tree structure is a tree of blocks pointing to the multihashes other blocks (metablocks), the leaves of which are raw blocks of IPFS objects, and the root of which is a single multihash (called the head).  In a network of nodes trying to coordinate a blockchain, the tree structure of the blockchain serves the reduce the number of comparisons necessary, with older blocks eventually being consolidated into metablocks.

Note that this algorithm performs best when the merged nodes are not too out of sync.  In the case that a node has been offline for a while, it should just assume the most common head node of its peers.

**Apparent Problems**

This scheme relies on the generation of metablocks out of regular blocks either not being arbitrary or being coordinated between nodes.

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
      need = s_peer - (s_self & s_peer)
    
      # The set of blocks this node has but the peer doesn't.
      # Some of these blocks could be included in a metablock
      # owned by the peer.
      leftover = s_self - (s_self & s_peer)
      
      while len(need) > 0:
        block = need.pop()
        if not is_metablock(block):
          # self.own performs all operations necessary for this node to
                # own the given block.  Then, add this new block to the leftover
          # set incase it is included in any of the peer's metablocks
          self.own(block)
          leftover.add(block)
        else:
          # block is a metablock and thus points to other blocks.
          s_meta = api.ls(block)
          if s_meta <= leftover:
            # relinquish ownership of all blocks contained in the metablock
            # and assume ownership of the metablock
            self.disown(s_meta & leftover)
            self.add(block)
          else:
            # if this node doesn't yet control all blocks in the metablock,
            # add the metablock back into the queue and also add all the
            # blocks this node is missing under the metablock.
            need.add(block)
            need.add(s_meta & leftover)
