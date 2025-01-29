#
# Transaction CSV Cleaner
#
# Version 1.1.0
# 2025-01-29
#

from datetime import date, datetime
from decimal import Decimal

from Transaction import Transaction

KEYWORD_SELF = 'SELF'
KEYWORD_UNKNOWN = 'UNKNOWN'

class CSVTransformer:

    EMPTY_STRING_QUOTES = "''"

    lenient:bool = False

    def __init__(self):
        pass

    def transform(self, row: list[str]) -> Transaction:
        # return Transaction.empty_transaction()
        pass

    def _parse_amount(self, amount: str) -> Decimal:
        pass

    def _parse_date(self, date_: str) -> date:
        pass

    def _parse_sender(self, sender: str) -> str:
        pass

    def _parse_recipient(self, recipient: str) -> str:
        pass

    def _parse_message(self, msg: str) -> str:
        pass

class EmptyTransformer(CSVTransformer):
    def __init__(self):
        super().__init__()

    def transform(self, row: list[str]) -> Transaction:
        return Transaction.empty_transaction()


class Provider01Transformer(CSVTransformer):

    EMPTY_FILLER = '-'
    EMPTY_FILLER_QUOTED = "'-'"


    def __init__(self):
        super().__init__()

    def transform(self, row: list[str]) -> Transaction:
        booking_date: str = row[0]
        #payment_date: str = row[1]
        amount: str = row[2]
        #type_: str = row[3]
        sender_name: str = row[4]
        recipient_name: str = row[5]
        #recipient_account: str = row[6]
        #recipient_bic: str = row[7]
        #reference_number: str = row[8]
        message: str = row[9]
        #archival_code: str = row[10]

        parsed_date: date = self._parse_date(booking_date)
        parsed_amount = self._parse_amount(amount)
        parsed_sender = self._parse_sender(sender_name)
        parsed_recipient = self._parse_recipient(recipient_name)
        parsed_message = self._parse_message(message)

        return Transaction(parsed_date, parsed_amount, parsed_sender, parsed_recipient, parsed_message)

    def _parse_amount(self, amount_str: str) -> Decimal:
        ## TODO Improve on this conversion
        amount_str = amount_str.replace(',','.') ## TOD
        try:
            parsed_amount = Decimal(amount_str)
        except ValueError as e:
            if self.lenient:
                parsed_amount = Decimal(0)
            else:
                raise e
        return parsed_amount

    def _parse_date(self, date_str: str) -> date:
        date_ = datetime.strptime(date_str, "%d.%m.%Y").date()
        return date_

    def _parse_sender(self, counterpart: str) -> str:
        return KEYWORD_SELF if counterpart == self.EMPTY_FILLER else counterpart

    def _parse_recipient(self, counterpart: str) -> str:
        return KEYWORD_SELF if counterpart == self.EMPTY_FILLER else counterpart

    def _parse_message(self, msg: str) -> str:
        if msg == self.EMPTY_FILLER_QUOTED:
            return self.EMPTY_STRING_QUOTES
        elif msg is None:
            return self.EMPTY_STRING_QUOTES
        else:
            return msg


class Provider02Transformer(CSVTransformer):

    def __init__(self):
        super().__init__()

    def transform(self, row: list[str]) -> Transaction:
        booking_date: str = row[0]
        amount: str = row[1]
        sender_account: str = row[2]
        #recipient_account: str = row[3]
        name: str = row[4]
        title: str = row[5]
        #reference_number: str = row[6]
        #balance: str = row[7]
        #currency: str = row[8]
        #empty: str = row[9]

        parsed_date: date = self._parse_date(booking_date)
        parsed_amount = self._parse_amount(amount)
        parsed_sender = self._resolve_sender(sender_account, name, title)
        parsed_recipient = self._resolve_recipient(sender_account, name, title)

        return Transaction(parsed_date, parsed_amount, parsed_sender, parsed_recipient, self.EMPTY_STRING_QUOTES)

    @staticmethod
    def _resolve_sender(sender_account:str, name: str, title: str) -> str:
        ## Only sent transactions specify sender account number
        if sender_account:
            return KEYWORD_SELF

        ## Usually Name seems to equal Title, but is missing for some internal transactions.
        counterpart: str = title if not name else name
        if not counterpart:
            counterpart = KEYWORD_UNKNOWN
        return counterpart

    @staticmethod
    def _resolve_recipient(sender_account:str, name: str, title: str) -> str:
        ## Received transactions do not specify sender account number, meaning holder is the recipient
        if not sender_account:
            return KEYWORD_SELF

        counterpart: str = title if not name else name
        if not counterpart:
            counterpart = KEYWORD_UNKNOWN
        return counterpart

    def _parse_amount(self, amount_str: str) -> Decimal:
        ## TODO Improve on this conversion
        amount_str = amount_str.replace(',','.')
        try:
            parsed_amount = Decimal(amount_str)
        except ValueError as e:
            if self.lenient:
                parsed_amount = Decimal(0)
            else:
                raise e
        return parsed_amount

    def _parse_date(self, date_str: str) -> date:
        date_str = date_str.replace('/','-') ## Not nice but it works
        try:
            date_ = date.fromisoformat(date_str)
        except ValueError as e:
            if self.lenient:
                date_ = date.fromtimestamp(0)
            else:
                raise e
        return date_
