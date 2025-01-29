# Transaction CSV Cleaner

A little project for doing some cleaning of bank transaction CSV file exports.


## Description

The program ingests CSV-files and outputs a cleaned and simplified CSV format to new files.

**User discretion is advised**


## Usage

Provide the program with the path of either a file or directory to process. If no argument is provided in operates on the working directory.

**Only filenames ending with .csv are considered**

Run the Python program.

### No argument - Works on all .csv-files in the current working directory
```shell
python csv-cleaner/CSV-Cleaner.py
```
### File path provided - Works on a single .csv-file
```shell
python csv-cleaner/CSV-Cleaner.py ..\samples\sample01.csv
```
### Directory path provided - Works on all .csv-files in the directory
```shell
python csv-cleaner/CSV-Cleaner.py .\samples\
```


## Output Format

**Subject To Change**

The program outputs a CSV-file named `input_file_name-CLEANED.csv` in the same directory as the input file.

CSV data with the following fields and formats. Semicolon ; is used for separator. Field contents are not escaped or enveloped at the moment.

| Fields  | 0          | 1         | 2           | 3              | 4            |
|---------|------------|-----------|-------------|----------------|--------------|
| Header  | Date       | Amount    | Sender      | Recipient      | Message      |
| Format  | YYYY-MM-DD | [-]#0.00  | Sender Name | Recipient Name | Message text |
| Policy  | Mandatory  | Mandatory | Mandatory   | Mandatory      | Empty Filler |
| Default | 1970-01-01 | 0.00      | Text        | Text           | ''           |

> Keyword `SELF` is used to indicate the account holder as Sender or Recipient.
> Keyword `UNKNOWN` is used to indicate unknown Sender or Recipient.


### Sample CSV

```csv
Date;Amount;Sender;Recipient;Message
2025-01-07;-1000.00;SELF;Apartments AB;Rent 01/2025
2025-01-02;4200.00;Employer AB;SELF;Paycheck 01/2025
```


## Supported Providers

CSV exports from the following providers are supported.

* Provider 01 
* Provider 02
* TODO: More providers


## To-Do

* Ignore already cleaned files
* Output location and name controls
* Changes to improve CSV format
  - CSV escaping strategy
