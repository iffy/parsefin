# Copyright (c) Matt Haggard.
# See LICENSE for details.

import lxml.etree
import lxml.html

import re

from parsefin.error import MissingData


class OFXTransactionParser(object):
    """
    I parse OFX files for transaction data.
    """

    r_intu = re.compile('(?=<(INTU\..*?)>(.*?)<)', re.I | re.S | re.M)

    _ACCOUNT_MAP = {
        'currency': './/curdef[1]',
        'bankid': './/bankid[1]',
        'account_id': './/acctid[1]',
        'account_type': './/accttype[1]',
        'balance': './/ledgerbal//balamt[1]',
        'balance_date': './/ledgerbal//dtasof[1]',
        'available_balance': './/availbal//balamt[1]',
        'available_balance_date': './/availbal//dtasof[1]',
        'transaction_start': './/dtstart[1]',
        'transaction_end': './/dtend[1]',
    }

    _TRANS_MAP = {
        'type': './/trntype[1]',
        'posted': './/dtposted[1]',
        'amount': './/trnamt[1]',
        'id': './/fitid[1]',
        'memo': './/memo[1]',
        'name': './/name[1]',
    }

    _FI_MAP = {
        'org': './/org[1]',
        'fid': './/fid[1]',
    }

    def _getXPaths(self, root, mapping, required=None):
        """
        Get a dictionary of the text of the given xpaths.

        @param required: List of required keys.
        """
        required = set(required or [])
        # Consider combining these xpaths with | if it's faster than looping
        # through the mapping dict.
        ret = {}
        for attr,xpath in mapping.items():
            node = root.xpath(xpath)
            if node:
                ret[attr] = node[0].text.strip()
            elif attr in required:
                raise MissingData("Missing required field %s" % (attr,))
        return ret


    def parseFile(self, fh):
        """
        Parse an OFX file for transaction data.
        """
        root = lxml.html.parse(fh).getroot()

        # is it even OFX or something similar?
        if not root.xpath('//ofx[1]'):
            raise MissingData("Not a recognized OFX file")

        ret = {}

        # header stuff
        fi = root.xpath('//fi[1]')
        if fi:
            ret['fi'] = self._getXPaths(fi[0], self._FI_MAP)  

        # accounts
        statements = root.xpath('.//stmtrs')
        accounts = ret['accounts'] = []
        for statement in statements:
            account = self._getXPaths(statement, self._ACCOUNT_MAP)
            transactions = account['transactions'] = []
            translist = statement.xpath('.//banktranlist[1]//stmttrn')
            for trans in translist:
                transaction = self._getXPaths(trans, self._TRANS_MAP)
                transactions.append(transaction)
            accounts.append(account)
        return ret
