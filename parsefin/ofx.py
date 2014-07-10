# Copyright (c) Matt Haggard.
# See LICENSE for details.

import lxml.etree
import lxml.html

import re

from datetime import datetime, timedelta

from parsefin.error import MissingData


r_ofx_timestamp = re.compile(r'''
    (?P<year>\d{4})
    (?P<month>\d{2})
    (?P<day>\d{2})
    (?:
        (?P<hour>\d{2})
        (?P<minute>\d{2})
        (?P<second>\d{2})
    )?
    (?:
        \.
        (?P<millisecond>\d\d\d)
    )?
    (?:
        \[
            (?P<offset>.*?)
            :
            .*?
        \]
    )?
    ''', re.I | re.X)

def timestamp(ofx_timestamp):
    """
    Convert an OFX timestamp into a Python C{datetime}.
    """
    m = r_ofx_timestamp.match(ofx_timestamp)
    parts = m.groupdict()
    offset = timedelta(hours=-int(parts['offset'] or 0))
    microsecond = int(parts['millisecond'] or 0) * 1000
    return datetime(
        int(parts['year']),
        int(parts['month']),
        int(parts['day']),
        int(parts['hour'] or 0),
        int(parts['minute'] or 0),
        int(parts['second'] or 0),
        microsecond,
    ) + offset



class OFXTransactionParser(object):
    """
    I parse OFX files for transaction data.
    """

    _ACCOUNT_MAP = {
        'currency': ('.//curdef[1]', unicode),
        'bankid': ('.//bankid[1]', unicode),
        'account_id': ('.//acctid[1]', unicode),
        'account_type': ('.//accttype[1]', unicode),
        'balance': ('.//ledgerbal//balamt[1]', unicode),
        'balance_date': ('.//ledgerbal//dtasof[1]', timestamp),
        'available_balance': ('.//availbal//balamt[1]', unicode),
        'available_balance_date': ('.//availbal//dtasof[1]', timestamp),
        'transaction_start': ('.//dtstart[1]', timestamp),
        'transaction_end': ('.//dtend[1]', timestamp),
    }

    _TRANS_MAP = {
        'type': ('.//trntype[1]', unicode),
        'posted': ('.//dtposted[1]', timestamp),
        'amount': ('.//trnamt[1]', unicode),
        'id': ('.//fitid[1]', unicode),
        'memo': ('.//memo[1]', unicode),
        'name': ('.//name[1]', unicode),
    }

    _FI_MAP = {
        'org': ('.//org[1]', unicode),
        'fid': ('.//fid[1]', unicode),
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
        for attr,(xpath,cast) in mapping.items():
            node = root.xpath(xpath)
            if node:
                ret[attr] = cast(node[0].text.strip())
            elif attr in required:
                raise MissingData("Missing required field %s" % (attr,))
        return ret


    def parseTimestamp(self, tstamp):
        """
        Turn an OFX timestamp into a Python C{datetime}.
        """



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
