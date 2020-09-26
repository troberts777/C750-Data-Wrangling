import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict


OSM_FILE = "map_PHX_Metro.osm" # My OSM FILE


# Audit file

# Audit street names------------------------------------------------------------------------------
# Regular expression to check for characters at end of string, including optional period.
# Eg "Street" or "St."

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)

# Common street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Road", "Parkway", "Commons", "Close", "Highway", "Circle", "Trail", "US"]


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)



def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

# Iterate over the osmfile and create a dictionary mapping from expected street names
# to collected streets.
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    osm_file.close()
    return street_types   


# Check Postalcodes for addresses 

# Regular expression to check whether postalcode is in appropriate format
postcode_re = re.compile('^[A-Z]{1,2}[0-9]{1,2}[A-Z]? [0-9][A-Z]{2}$') 

def is_postcode(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")


# Search for postcodes within "way" and "node"
def find_postcode():
    osm_file = open(OSM_FILE, "r")
    postcode_types = set()
    odd_postcode = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    m = postcode_re.search(tag.attrib['v'])
                    if m:
                        postcode_types.add(tag.attrib['v'])  
                    else:
                        odd_postcode.add(tag.attrib['v'])
                        

    osm_file.close()


    return (postcode_types, odd_postcode)

















