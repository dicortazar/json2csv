# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Daniel Izquierdo Cortazar <dizquierdo@bitergia.com>
#

import argparse
import csv
import json
import sys


"""The following global variables assume the following JSON
structure coming from ElasticSearch:
{
    "<index_name>": {
        "mappings": {
            "items": {
                ...,
                "properties":{
                    ....
                }
            }
        }
    }
}
"""

MAPPINGS = "mappings"
ITEMS = "items"
PROPERTIES = "properties"
TYPE = "type"


COLUMN_NAME = "name"
COLUMN_TYPE = "type"

DESCRIPTION = "Translate JSON to CSV"


def parse_args():
    """ Parse arguments from the command line"""

    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-f', '--filepath', dest="filepath",
           required=True, help='JSON document filepath')

    return parser.parse_args()


def json2tuple(filepath):
    """Read a file containing a JSON document to export to CSV
    writing the result in the standard output.
    The input format is the usual mapping for ElasticSearch (5.x/6)
      {"properties": {
          "fieldname": {
              "type": "type"
          }
      }
      }

    That JSON document would be exported as:
    $ fieldname,type
    """

    json_data = open(filepath).read()
    full_mapping = json.loads(json_data)

    # Look for the 'properties' key
    index_name = list(full_mapping.keys())[0]
    properties_mapping = full_mapping[index_name][MAPPINGS][ITEMS]

    csv_trans = []
    for key, val in properties_mapping[PROPERTIES].items():
        csv_trans.append((key, val[TYPE]))

    return csv_trans


def main():
    """Translate from ElasticSearch JSON mapping to
    CSV format
    """

    args = parse_args()
    filepath = args.filepath

    csv_data = json2tuple(filepath)

    csv_writer = csv.writer(sys.stdout)

    # write header
    csv_writer.writerow((COLUMN_NAME, COLUMN_TYPE))
    # write data
    for val in csv_data:
        csv_writer.writerow(val)


if __name__ == "__main__":main()

