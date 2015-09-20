"""
Asynchronous version of ipfsApi (all we really have to do is patch socket).
"""
from gevent.monkey import patch_all; patch_all(thread=False, select=False)
import gevent

from ipfsApi import Client


def map(requests):
    pass
