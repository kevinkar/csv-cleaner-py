#
# Transaction CSV Cleaner
#
# Version 1.1.0
# 2025-01-29
#

from datetime import date
from decimal import Decimal

'''
## Data object for transactions
'''
class Transaction:

    booking_date: date
    amount: Decimal
    sender: str
    recipient: str
    message: str

    def __init__(self, booking_date, amount, sender, recipient, message = ''):
        self.booking_date = booking_date
        self.amount = amount
        self.sender = sender
        self.recipient = recipient
        self.message = message
        return

    @staticmethod
    def empty_transaction():
        return Transaction(date.fromtimestamp(0), Decimal(0), '', '', '')

    def __str__(self):
        """
        Creates CSV line of the transaction
        :return:
        """
        return ';'.join([str(self.booking_date), str(self.amount), self.sender, self.recipient, self.message])

    def __repr__(self):
        """
        Verbose string of the transaction.
        :return:
        """
        repr_: str = ('Transaction: [\n'
                     '\tDate: ' + str(self.booking_date) + '\n'
                     '\tAmount: ' + str(self.amount) + '\n'
                     '\tSender: ' + self.sender + '\n'
                     '\tRecipient: ' + self.recipient + '\n'
                     '\tMessage: ' + self.message + '\n'
                     ']')
        return repr_

