# Copyright (c) Matt Haggard.
# See LICENSE for details.

import lxml


class OFXTransactionParser(object):
    """
    I parse OFX files for transaction data.
    """

    def parseFile(self, fh):
        """
        Parse an OFX file for transaction data.
        """