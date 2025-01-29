
# CSV Formats

Describes the input formats as observed from CSV exports. Used to automatically decide the provider.

* Headers in different languages

## Provider 01

* Fields: 11

* Date: DD.MM.YYYY


```python
provider_01_header_fi = [
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
]
```

```python
provider_01_header_sv = [
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
]
```


## Provider 02

* Fields: 10 (actual 9 - ends csv rows with ; which causes last to be empty)

```python
provider_02_header_en = [
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
]
```

```python
provider_02_header_fi = [
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
]

```

```python

provider_02_header_sv = [
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
]
```
