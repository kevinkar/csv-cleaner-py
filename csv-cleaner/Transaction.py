#
# Transaction CSV Cleaner
#
# Version 1.0.0
# 2025-01-29
#

from datetime import date
from decimal import Decimal

DEFAULT_CURRENCY = 'EUR'

'''
## Data object for transactions
'''
class Transaction:

    date_: date = date.fromtimestamp(0)
    amount: Decimal = Decimal(0)
    sender: str = ''
    recipient: str = ''
    currency: str = DEFAULT_CURRENCY

    def __init__(self, timestamp, amount, sender, recipient, currency=DEFAULT_CURRENCY):
        self.date_ = timestamp
        self.amount = amount
        self.sender = sender
        self.recipient = recipient
        self.currency = currency
        return

    def __str__(self):
        """
        Creates CSV line of the transaction
        :return:
        """
        return ';'.join([str(self.date_), str(self.amount), self.sender, self.recipient, self.currency])

    def __repr__(self):
        """
        Verbose string of the transaction.
        :return:
        """
        repr_: str = ('Transaction: [\n'
                     '\tDate: ' + str(self.date_) + '\n'
                     '\tAmount: ' + str(self.amount) + '\n'
                     '\tSender: ' + self.sender + '\n'
                     '\tRecipient: ' + self.recipient + '\n'
                     '\tCurrency: ' + self.currency + '\n'
                     ']')
        return repr_
