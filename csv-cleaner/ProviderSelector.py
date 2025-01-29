#
# Transaction CSV Cleaner
#
# Version 1.1.0
# 2025-01-29
#

from enum import Enum

from Logger import Logger
from CSVTransformer import CSVTransformer, Provider01Transformer, Provider02Transformer, EmptyTransformer

'''
## Provider Enums
'''
class Provider(Enum):
    PROVIDER01 = "provider01"
    PROVIDER02 = "provider02"
    UNKNOWN = "unknown"

'''
## Provider Selector
'''
class ProviderSelector:

    _provider_01_header_fi = (
        "Kirjauspäivä",
        "Maksupäivä",
        "Summa",
        "Tapahtumalaji",
        "Maksaja",
        "Saajan nimi",
        "Saajan tilinumero",
        "Saajan BIC-tunnus",
        "Viitenumero",
        "Viesti",
        "Arkistointitunnus"
    )

    _provider_01_header_sv = (
        "Bokningsdag",
        "Betalningsdag",
        "Belopp",
        "Betalningstyp",
        "Betalare",
        "Mottagarens namn",
        "Mottagarens kontonummer",
        "Mottagarens BIC-kod",
        "Referensnummer",
        "Meddelande",
        "Arkiveringskod"
    )

    _provider_02_header_fi = (
        "Kirjauspäivä",
        "Määrä",
        "Maksaja",
        "Maksunsaaja",
        "Nimi",
        "Otsikko",
        "Viitenumero",
        "Saldo",
        "Valuutta",
        ""
    )

    _provider_02_header_sv = (
        "Bokföringsdag",
        "Belopp",
        "Avsändare",
        "Mottagare",
        "Namn",
        "Rubrik",
        "Referensnummer",
        "Saldo",
        "Valuta",
        ""
    )

    _provider_02_header_en = (
        "Booking date",
        "Amount",
        "Sender",
        "Recipient",
        "Name",
        "Title",
        "Reference number",
        "Balance",
        "Currency",
        ""
    )

    ## Provider lists hashed as keys
    _provider_hash = {
        hash(_provider_01_header_fi): Provider.PROVIDER01,
        hash(_provider_01_header_sv): Provider.PROVIDER01,
        hash(_provider_02_header_en): Provider.PROVIDER02,
        hash(_provider_02_header_fi): Provider.PROVIDER02,
        hash(_provider_02_header_sv): Provider.PROVIDER02,
    }

    logger: Logger
    provider: Provider

    def __init__(self, logger):
        self.logger = logger
        self.provider = Provider.UNKNOWN
        return

    @staticmethod
    def get_transformer(provider: Provider) -> CSVTransformer:
        match provider:
            case Provider.PROVIDER01:
                return Provider01Transformer()
            case Provider.PROVIDER02:
                return Provider02Transformer()
            case _:
                return EmptyTransformer()

    def select_provider(self, header: list[str]) -> Provider:
        header_hash: int = hash(tuple(header))
        provider_: Provider = self._provider_hash.get(header_hash)
        if provider_ is None:
            provider_ = Provider.UNKNOWN
        self.provider = provider_
        return provider_
