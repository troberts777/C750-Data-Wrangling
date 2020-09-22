# Audit file
import re
from collections import defaultdict


OSM_FILE = "map_AJ.osm"  #My OSM file

#Audit street names------------------------------------------------------------------------------
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



#Mapping for names to be updated
mapping = { "St": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "Ave": "Avenue",
            "S L": "South L",
            "E ": "East ",
            "5810 A":"A",
            "Hwy ":"Highway "
            }

            
