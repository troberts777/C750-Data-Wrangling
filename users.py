# Users function

import xml.etree.cElementTree as ET
import pprint
import re

OSM_FILE = "map_AJ.osm"  # Replace this with your osm file

def get_user(element):
    return

# Generates list of users
def process_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        name = element.attrib.get('user')
        if name != None:
            if name not in users:
                users.add(name)
                
    pass
    return users





# Check Users
process_users(OSM_FILE)
