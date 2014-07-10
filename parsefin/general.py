# Copyright (c) Matt Haggard.
# See LICENSE for details.

import json

from parsefin.ofx import OFXTransactionParser



def parseFile(handle):
    """
    """
    # XXX currently only support OFX
    ofx = OFXTransactionParser()
    return ofx.parseFile(handle)



class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        try:
            return obj.isoformat()
        except:
            return json.JSONEncoder.default(self, obj)


def toJson(obj, *args, **kwargs):
    """
    Convert to JSON (including dates to ISO format).
    """
    kwargs['cls'] = DateEncoder
    return json.dumps(obj, *args, **kwargs)
