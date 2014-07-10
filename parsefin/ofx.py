# Copyright (c) Matt Haggard.
# See LICENSE for details.

import lxml.etree
import lxml.html

import re


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

    def _getXPaths(self, root, mapping):
        """
        Get a dictionary of the text of the given xpaths.
        """
        # Consider combining these xpaths with | if it's faster than looping
        # through the mapping dict.
        ret = {}
        for attr,xpath in mapping.items():
            node = root.xpath(xpath)
            if node:
                ret[attr] = node[0].text.strip()
        return ret


    def parseFile(self, fh):
        """
        Parse an OFX file for transaction data.
        """
        # We do this because we're gonna use regex later anyway.
        guts = fh.read()
        fh.seek(0)
        root = lxml.html.parse(fh).getroot()

        ret = {}

        # header stuff
        fi = root.xpath('//fi[1]')
        if fi:
            fi = fi[0]
            ret['fi'] = {
                'org': fi.xpath('.//org[1]')[0].text.strip(),
                'fid': fi.xpath('.//fid[1]')[0].text.strip(),
            }

        # Because OFX is an awesome XML-compatible (not compatible) format,
        # we resort to regex for these fields containing dots in their names.
        intus = self.r_intu.findall(guts)
        if intus:
            ret['intu'] = {}
            for (name, value) in intus:
                name = name.split('.')[1].lower()
                value = value.strip()
                ret['intu'][name] = value

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