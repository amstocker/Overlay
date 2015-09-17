from ipfsApi.utils import make_json_buffer
from ipfsApi.exception import ipfsApiError


class BlockChain(object):

    def __init__(self, ipfs_api, head=None):

        self.api = ipfs_api
        self.id = self.api.id()

        if head:
            self.head = head
        else:
            self.head = api.object_new()
    

    def iter(self, start=None):
        """
        Iterates over the blocks in this blockchain.
        """
        cur = start or self.head
        
        try:
            res = self.api.get_json(cur)
        except ipfsApiError:
            return

        while True:
            yield res['block']
            try:
                res = self.api.get_json(res['prev'])
            except ipfsApiError:
                return


class LocalBlockChain(BlockChain):
    """
    Represents the local blockchain, the head of which is publish to IPNS.
    """
    
    def add_block(self, multihash, blockmeta):
        """
        Adds a block to this blockchain and updates the head.
        """
        block = {'Data':
                    {'block': multihash,
                     'blockmeta': blockmeta,
                     'prev': self.head
                     },
                 'Links':
                    [self.head]
                 }

        res = self.api.object_add(make_json_buffer(block))

        self.head = res['Hash']
        return self.head


    def merge(self, others):
        """
        Does a merge of this blockchain with another blockchain or set of
        blockchains from this node's peers.
        """
        pass
