

from parsefin.ofx import OFXTransactionParser

def parseFile(handle):
    """
    """
    # XXX currently only support OFX
    ofx = OFXTransactionParser()
    return ofx.parseFile(handle)
