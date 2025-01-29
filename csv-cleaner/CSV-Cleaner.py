#
# Transaction CSV Cleaner
#
# Version 1.1.0
# 2025-01-29
#

import csv
import glob
import os
import sys
import typing

from pathlib import Path

from Logger import Logger
from Transaction import Transaction
from ProviderSelector import Provider, ProviderSelector
from CSVTransformer import CSVTransformer

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
        outfile: typing.IO = open(path_output, mode='xt', encoding='utf-8-sig')
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

def parse_file(path_input: str) -> list[Transaction]:
    """
    Reads and parses given file to a list of transactions.
    :param path_input:
    :return:
    """
    logger.info('Parsing contents of ' + path_input)

    transactions: list[Transaction] = []
    try:
        with open(path_input, mode='rt', newline='', encoding='utf-8-sig') as csvfile:
            row_num: int = 0
            #failed_num = 0
            csvreader = csv.reader(csvfile, delimiter=DELIMITER)
            selector: ProviderSelector = ProviderSelector(logger)
            provider: Provider
            transformer: CSVTransformer
            for row in csvreader:
                if row_num == 0: ## Header row. Select transformer for the data format
                    provider: Provider = selector.select_provider(row)
                    transformer = selector.get_transformer(provider)
                    row_num += 1
                    continue ## Do not parse the header into a transaction
                tr: Transaction = transformer.transform(row)
                transactions.append(tr)
                logger.debug('Parsed transaction on row ' + str(row_num))
                row_num += 1
            #logger.info('Parsed ' + str(row_num - 1) + ' rows into ' + str(len(transactions)) + ' transactions, failing on ' + str(failed_num) + ' transactions.')
            logger.info('Parsed ' + str(row_num - 1) + ' rows into ' + str(len(transactions)) + ' transactions.')

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
