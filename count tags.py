import xml.etree.cElementTree as ET
import pprint


OSM_FILE = "map_AJ.osm"  


# Iterative Parsing

# Count Tags
def count_tags(filename):
    tags = {}
    for _, elem in ET.iterparse(filename):
        tag = elem.tag
        if tag not in tags.keys():
            tags[tag] = 1
        else:
            tags[tag] += 1
    return tags


def test():
    tags = count_tags(OSM_FILE)
    pprint.pprint(tags)

    
test()


