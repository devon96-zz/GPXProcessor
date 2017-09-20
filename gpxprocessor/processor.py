#!/usr/bin/env python3
'''Processor for GPX and LOG files
Author: Konrad Dryja
License: GPLv3'''

import argparse
import sys
import re
import time
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError


def validate_gpx(xml_file):
    '''Function to validate GPX file against XSD schema of gpx file'''

    # Copy all GPX file's contents into a string variable.
    xml_string = xml_file.read()
    xml_file.close()

    # Try to parse the schema.
    try:
        # Declare schema to use.
        schema = etree.XMLSchema(file='gpx.xsd')

        # Create a parser which we will match against our xml string.
        parser = objectify.makeparser(schema=schema)

        # Match XSD with the XML file. Nothing will happen if successful.
        # XMLSyntaxError will be raised if unsuccessful.
        objectify.fromstring(str.encode(xml_string), parser)

    # Capture the exception.
    except XMLSyntaxError:
        # Print error message and exit the program.
        print("ERROR. Failed to validate the GPX file.")
        sys.exit(1)


def produce_output(gpx_file, log_file, verbose, merge, threshold):

    base_range = range(-150, 15)
    green_range = range(threshold, 14)
    orange_range = range(-149, threshold + 1)
    red_range = range(-150, -149)

    root = etree.Element("gpx")
    root.set('version', '1.1')
    root.set('xmlns', 'http://www.topografix.com/GPX/1/1')

    root.append(etree.Element("child1"))
    child2 = etree.SubElement(root, "child2")
    child3 = etree.SubElement(root, "child3")

    print(etree.tostring(root, pretty_print=True,
                         xml_declaration=True, encoding='UTF-8').decode('UTF-8'))

    for line in log_file:
        if "PeerRSSI" in line:
            match = re.match(r'(.*\;.*);.*PeerRSSI:(-\d+)', line)
            print(time.strptime(match.group(1), "%Y.%m.%d;%H:%M:%S.%f"))
            print(match.group(2))


def main():
    '''Main point of entry to the program'''

    # Define parser for command line arguments
    parser = argparse.ArgumentParser(description='Process GPX and LOG files.')

    # Add argument to fetch gpx file location and make sure it opens
    # (i.e. file exists and permissions are in order)
    parser.add_argument('gpx', metavar='*.gpx', type=argparse.FileType('r'),
                        help='.gpx file path')

    # Same as above but with log file.
    parser.add_argument('log', metavar='*.log', type=argparse.FileType('r'),
                        help='.log file path')

    # Capture whether user intends to run the program with increased verbosity level. Default false.
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="""report .log radio test numbers with associated .gpx lat/lon co-ords
                                to stderr during processing""")

    # Capture whether user intends to merge gpx and log files during execution. Defaults false.
    parser.add_argument('--merge', '-m', action='store_true',
                        help="""add radio tests as waypoints into the output file which combines the
                                trackpoints from .gpx and the radio tests from .log as waypoints""")

    # Allows user to enter his own threshold. If left blank, will use -125.
    parser.add_argument('--gothresh', type=int, action='store', metavar='[-148-14]',
                        choices=range(-148, 15),
                        help="""threshold in dBm between strong signal (green)
                                and marginal signal (orange). Default is -125.""",
                        default=49)

    # Parse all arguments to the Namespace object.
    args = parser.parse_args(['file1.gpx', 'file2.log'])

    # Save passed .gpx file to a variable.
    gpx_file = vars(args)['gpx']

    # Save passed .log file to a variable.
    log_file = vars(args)['log']

    # Save whether to run the program in increase verbosity
    verbose = vars(args)['verbose']

    # Save whether to merge .gpx with .log
    merge = vars(args)['merge']

    # Save passed threshold value.
    threshold = vars(args)['gothresh']

    # Validate passed .gpx file against .xsd schema.
    validate_gpx(gpx_file)

    # Go through the files and produce the output.
    produce_output(gpx_file, log_file, verbose, merge, threshold)


# Start function main() if it is the main entry point.
if __name__ == '__main__':
    main()
