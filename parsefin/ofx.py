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
        fi = root.xpath('//fi[1]')[0]
        ret['fi'] = {
            'org': fi.xpath('//org[1]')[0].text.strip(),
            'fid': fi.xpath('//fid[1]')[0].text.strip(),
        }

        # Because OFX is an awesome XML-compatible (not compatible) format,
        # we resort to regex for these fields containing dots in their names.
        ret['intu'] = {}
        intus = self.r_intu.findall(guts)
        for (name, value) in intus:
            name = name.split('.')[1].lower()
            value = value.strip()
            ret['intu'][name] = value

        # accounts
        statements = root.xpath('//stmtrs')
        accounts = ret['accounts'] = []
        for statement in statements:
            account = {
                'currency': statement.xpath('//curdef[1]')[0].text.strip(),
                'bankid': statement.xpath('//bankid[1]')[0].text.strip(),
                'account_id': statement.xpath('//acctid[1]')[0].text.strip(),
                'account_type': statement.xpath('//accttype[1]')[0].text.strip(),
                'balance': statement.xpath('//ledgerbal//balamt[1]')[0].text.strip(),
                'balance_date': statement.xpath('//ledgerbal//dtasof[1]')[0].text.strip(),
                'available_balance': statement.xpath('//availbal//balamt[1]')[0].text.strip(),
                'available_balance_date': statement.xpath('//availbal//dtasof[1]')[0].text.strip(),
                'transaction_start': statement.xpath('//dtstart[1]')[0].text.strip(),
                'transaction_end': statement.xpath('//dtend[1]')[0].text.strip(),
            }
            transactions = account['transactions'] = []
            translist = statement.xpath('//banktranlist[1]//stmttrn')
            for trans in translist:
                transaction = {
                    'type': trans.xpath('//trntype[1]')[0].text.strip(),
                    'posted': trans.xpath('//dtposted[1]')[0].text.strip(),
                    'amount': trans.xpath('//trnamt[1]')[0].text.strip(),
                    'id': trans.xpath('//fitid[1]')[0].text.strip(),
                    'memo': trans.xpath('//memo[1]')[0].text.strip(),
                    'name': trans.xpath('//name[1]')[0].text.strip(),
                }
                transactions.append(transaction)
            accounts.append(account)
        return ret