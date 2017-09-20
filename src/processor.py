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


parser = argparse.ArgumentParser(description='Process GPX and LOG files.')
parser.add_argument('files', metavar='*.gpx', type=int, nargs='+',
                    help='a file to process')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
