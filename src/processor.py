#!/usr/bin/env python3

import argparse
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError


def xml_validator(some_xml_string, xsd_file='gpx.xsd'):
    try:
        schema = etree.XMLSchema(file=xsd_file)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(some_xml_string, parser)
        print("YEAH!, my xml file has validated")
    except XMLSyntaxError:
        # handle exception here
        print("Oh NO!, my xml file does not validate")


def validate_xml():
    xml_file = open('test.xml', 'r')
    xml_string = xml_file.read()
    xml_file.close()

    xml_validator(xml_string)


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
    args = parser.parse_args()

    print("Success!")
    print(vars(args))


if __name__ == '__main__':
    main()
