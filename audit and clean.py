import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict



OSM_FILE = "map_AJ.osm"


# Audit file

# Audit street names------------------------------------------------------------------------------
# Regular expression to check for characters at end of string, including optional period.
# Eg "Street" or "St."

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)

# Common street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Road", "Parkway", "Freeway", "Close", "Highway", "Circle", "Trail", "US"]


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



# Mapping for names to be updated
mapping = { "St": "Street", "Rd": "Road", "Rd.": "Road", "Ave": "Avenue", " St ": "Street",  "St": "Street", "St. ": "Street",
            "Blvd": "Boulevard", "Ct": "Court", "Dr, ": "Drive ", " Dr ": "Drive ", "Dr. ": "Drive ", "Rd": "Road", "Rd ": "Road",
            "Rd.": "Road", "Pl": "Place", "Ave ": "Avenue ", "Ave.": "Avenue", "ln " : "Lane", "S ": "South ", "S. ": " South ",
            "N ": " North ", "N. ": " North ", "W " : " West ", "W. ": " West ", "E ": "East ",  "E. ": "East ", "E ": "East ",            
            "Hwy ":"Highway "
            }

            


# In[6]:


# Test audit function
audit(OSM_FILE)


# In[7]:


# Improving Street names
def update_name(name, mapping):
    for key in mapping.iterkeys():
        if re.search(key, name):
            name = re.sub(key, mapping[key], name)

    return name

def improve_street_name():
    st_types = audit(OSM_FILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)            
            print name, "=>", better_name
    
            #Second Check        
            if " Streetewart" in better_name:
                    better_name = better_name.replace(" Streetewart", " Streetewart")    
                    print name, "=>", better_name    
            


# In[8]:


# Clean streets 
improve_street_name()


# In[9]:


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



# In[10]:


# Audit postal codes
find_postcode()


# In[11]:


# Noted a postalcode with a +4 number, will drop this and maintain only 9-digit postal code

area_postcode_re = re.compile('^[A-Z]{1,2}[0-9]{1,2}[A-Z]? ?[0-9]?$')

def update_postcode(odd_postcode):
    if area_postcode_re.search(odd_postcode):
        postcode = " "
    else:
        postcode = odd_postcode.split("-")[0]
    return postcode


def improve_postcode():
    postcode_all = find_postcode()

    for postcode in postcode_all[1]:
        better_postcode = update_postcode(postcode)
        print postcode, "=>", better_postcode


# In[12]:


# Fix postal codes
improve_postcode()





