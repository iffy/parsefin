# Copyright (c) Matt Haggard.
# See LICENSE for details.

import lxml.etree
import lxml.html


class OFXTransactionParser(object):
    """
    I parse OFX files for transaction data.
    """

    def parseFile(self, fh):
        """
        Parse an OFX file for transaction data.
        """
        root = lxml.html.parse(fh).getroot()
        ret = {}

        # header stuff
        fi = root.xpath('//fi[1]')[0]
        ret['fi'] = {
            'org': fi.xpath('//org[1]')[0].text.strip(),
            'fid': fi.xpath('//fid[1]')[0].text.strip(),
        }
        intus = root.xpath('//intu')
        ret['user'] = {
            'bid': intus[0].text.strip(),
            'userid': intus[1].text.strip(),
        }

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