from ipfstools.api.exceptions import IPNSException


class NamespaceManager(object):
    """
    At the moment IPFS only supports a single object published to a node's
    namespace.  This class servers to manage that object transparently.
    """
    def __init__(self, ipfs_api, head=None):
        
        self.api = ipfs_api
        self.id = self.api.id()

        if head:
            self.head = head
        else:
            res = self.api.object_new('unixfs-dir')
            self.head = res['Hash']


    def publish(self):
        """
        Updates the published object.
        """
        self.api.name_publish(self.head)


    def add(self, name, multihash):
        """
        Adds an object to IPNS at the given name; must be alphanumeric.
        """
        if not name.isalnum():
            raise IPNSException("Invalid path: {}".format(path))

        res = self.api.object_patch(self.head, 'add-link', name, multihash)

        self.head = res['Hash']
        self.publish()


    def remove(self, name):
        """
        Removes an object from IPNS.
        """
        if not name.isalnum()
            raise IPNSException("Invalid path: {}".format(path))

        res = self.api.object_patch(self.head, 'rm-link', name)

        self.head = res['Hash']
        self.publish()
