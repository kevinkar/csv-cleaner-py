#
# Transaction CSV Cleaner
#
# Version 1.0.0
# 2025-01-29
#

import csv
import glob
import os
import sys
import typing
from datetime import date
from decimal import Decimal
from pathlib import Path

from Logger import Logger
from Transaction import Transaction

'''
## Change this to enable/disable debug logging
'''
debug: bool = True
#debug: bool = False
logger: Logger

FILE_SUFFIX: str = '.csv'
DELIMITER: str = ';'
## Source data ends lines with an empty field (extra delimiter), making it 10 fields.
FIELD_COUNT: int = 10

def write_file(path_output: str, text_output: str):
    """
    Write provided string to the specified file.
    :param path_output:
    :param text_output:
    :return:
    """
    logger.info('Writing file ' + path_output)
    try:
        outfile: typing.IO = open(path_output, mode='xt')
        outfile.write(text_output)
        outfile.close()
        logger.debug('The output file ' + path_output + ' has been written.')
    except FileExistsError as e:
        logger.error('Failed already exists: ' + path_output)
        logger.debug('Encountered an exception.  ' + repr(e))
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error('Failed to write file ' + path_output)
        logger.debug('Encountered an exception.  ' + repr(e))
        sys.exit(1)
    return

def parse_transaction_row(row: list[str], lenient = False) -> Transaction:
    """
    Parse the row data into a transaction object.
    :param lenient: Use default values when failing to parse, or raises ValueError
    :param row:
    :return:
    """
    if len(row) != FIELD_COUNT:
        raise ValueError('The row must have ' + str(FIELD_COUNT) + ' fields, had ' + str(len(row)))

    ## Data as strings
    date_str: str = row[0].replace('/','-') ## Not nice but it works
    amount_str: str = row[1].replace(',','.') ## Not nice but it works
    sender_acc: str = row[2]
    recipient_acc: str = row[3]
    name: str = row[4]
    title: str = row[5]
    #reference_number: str = row[6]
    currency: str = row[8]

    ## Next, attempt to populate the following fields:
    parsed_date: date
    parsed_amount: Decimal
    parsed_counterpart: str
    parsed_sender: str
    parsed_recipient: str

    try:
        parsed_date = date.fromisoformat(date_str)
    except ValueError as e:
        if lenient:
            parsed_date = date.fromtimestamp(0)
        else:
            raise e
    try:
        parsed_amount = Decimal(amount_str)
    except ValueError as e:
        if lenient:
            parsed_amount = Decimal(0)
        else:
            raise e

    ## Name is always the counterpart, whether receiving or sending transaction
    ## Name might be omitted, then use Title. Usually Name seems to equal Title
    if not name:
        name = title

    parsed_counterpart = title if not name else name
    if not parsed_counterpart:
        ## Unexpected that Name and Title would be missing. Sender account probably not defined either.
        if lenient:
            parsed_counterpart = 'UNKNOWN'
        else:
            raise ValueError('No Name or Title exists for transaction.')

    ## Case 1: Sender account not defined, holder is receiving
    ## Case 2: In other cases, holder is sending
    if not sender_acc:
        parsed_sender = parsed_counterpart
        parsed_recipient = 'SELF'
    else:
        parsed_sender = 'SELF'
        parsed_recipient = parsed_counterpart

    if not recipient_acc:
        ## Unexpected that recipient account is missing.
        if lenient:
            pass
        else:
            raise ValueError('No Recipient Account exists for transaction.')

    tr = Transaction(parsed_date,parsed_amount, parsed_sender, parsed_recipient, currency)
    return tr

def parse_file(path_input: str) -> list[Transaction]:
    """
    Reads and parses given file to a list of transactions.
    :param path_input:
    :return:
    """
    logger.info('Parsing contents of ' + path_input)

    transactions: list[Transaction] = []
    try:
        with open(path_input, mode='rt', newline='') as csvfile:
            csvfile.readline() ## Skip the first row with header
            row_num: int = 1
            failed_num = 0
            logger.debug('Skipped header on row ' + str(row_num))
            csvreader = csv.reader(csvfile, delimiter=DELIMITER)
            for row in csvreader:
                row_num = row_num + 1
                try:
                    tr: Transaction = parse_transaction_row(row)
                    transactions.append(tr)
                    logger.debug('Parsed transaction on row ' + str(row_num))
                except ValueError as e:
                    failed_num = failed_num + 1
                    logger.warning('Ignored row ' + str(row_num) + ' due to parsing failure.')
                    logger.debug('Exception parsing row ' + str(row_num) + '\n' +  repr(e))

            logger.info('Parsed ' + str(row_num - 1) + ' rows into ' + str(len(transactions)) + ' transactions, failing on ' + str(failed_num) + ' transactions.')

    except IOError as e:
        logger.error('Failed to process the file ' + path_input)
        logger.debug('Encountered an exception.  ' + repr(e))
        sys.exit(1)

    return transactions

def process_source_file(path_input: str):
    """
    Process provided file.
    :param path_input: File path to process
    :return:
    """
    logger.info('Processing file: ' + path_input)
    transactions: list[Transaction] = parse_file(path_input)

    ## Data has been transformed into transactions.

    ## Next, create an output string of clean CSV
    data_list: list[str] = []
    for tr in transactions:
        data_list.append(str(tr))
    data_str: str = '\n'.join(data_list)

    ## Output path is same folder as input file
    path: Path = Path(path_input)
    parent: str = str(path.parent.absolute())
    filename: str = os.path.basename(path_input)
    path_output_a: str = parent + os.sep + filename[:-len(FILE_SUFFIX)] + '-CLEANED' + FILE_SUFFIX

    ## Write the output data to a file
    write_file(path_output_a, data_str)

    return

def process_directory(path_input: str):
    """
    Processes files in directory
    :param path_input:
    :return:
    """
    logger.info('Starting processing of directory ' + path_input)
    file_paths: list[str] = glob.glob(path_input + os.sep + '*' + FILE_SUFFIX)
    if len(file_paths) == 0:
        logger.error('Directory does not contain a single  ' + FILE_SUFFIX + path_input)
        sys.exit(1)
    ## Iterate through the provided files
    for path_file in file_paths:
        ## Process each individual file
        process_source_file(path_file)
    return

def process_file(path_input: str):
    """
    Checks if given file path suffix matches and continues processing.
    :param path_input:
    :return:
    """
    logger.debug('Starting processing of file ' + path_input)
    file_name = path_input.split(os.sep)[-1]
    if not file_name.lower().endswith(FILE_SUFFIX):
        logger.error('Provided file is not a ' + FILE_SUFFIX + '  file.')
        sys.exit(1)
    process_source_file(path_input)
    return

def read_args() -> str:
    """
    Helper. Parses the command line input.
    :rtype: str
    :return: Input argument
    """
    logger.debug('Number of command line arguments provided: ' + str(len(sys.argv)))
    i: int = 0
    for arg in sys.argv:
        logger.debug('Argument ' + str(i) + ' : ' + arg)
        i = i + 1
    return sys.argv[1] if len(sys.argv) == 2 else None

def main():
    """
    Main method, entry point of the analyzer.
    Does some checking and continues execution.
    :return:
    """
    ## Per our contract, argument can be none, folder or file. If none, do CWD.
    if len(sys.argv) > 2:
        logger.error(f'Usage: {sys.argv[0]} [source] Where source is a directory or a file.'
                         f'If no argument is provided, the program will operate on the current directory.')
        sys.exit(1)

    path_input: str = read_args()
    if path_input is None:
        path_input = os.path.dirname(os.path.realpath(__file__))
        logger.info('No input path provided. Assuming current directory: ' + path_input)

    if not os.path.exists(path_input):
        sys.exit('Provided input path does not exist. Exiting.')

    ## Call the actual business logic to get things done
    logger.info('Starting processing of path ' + path_input)
    if os.path.isdir(path_input):
        logger.debug('Input path is a directory.')
        process_directory(path_input)
    elif os.path.isfile(path_input):
        logger.debug('Input path is a file.')
        process_file(path_input)
    else:
        logger.info('Unknown input path type: ' + path_input)

    logger.info('Program finished.')
    return

"""
Python starting point with main check.
"""
if __name__ == '__main__':
    logger = Logger(debug)
    main()
