# Update Street names and Postal Codes
import re
import audit


# Mapping for names to be updated
mapping = { 
	    " St ": "Street",
            "St": "Street",
            "St. ": "Street",
            "Blvd": "Boulevard",
            "Ct": "Court",
            "Dr, ": "Drive ",
            " Dr ": "Drive ",
            "Dr. ": "Drive ",
            "Rd": "Road",
            "Rd ": "Road",
            "Rd.": "Road",
            "Pl": "Place",
            "Ave": "Avenue ",
            "Ave.": "Avenue",
            "ln " : "Lane",            
            "S ": "South ",
            "S. ": " South ",
            "N ": " North ",
            "N. ": " North ",
            "W " : " West ",
            "W. ": " West ",
            "E ": "East ",
            "E. ": "East ",
            "Hwy ":"Highway ",
            }

            

# Improving Street names
def update_name(name, mapping):
    for key in mapping.iterkeys():
        if re.search(key, name):
            name = re.sub(key, mapping[key], name)

    return name

def improve_street_name():
    st_types = audit.audit(OSM_FILE)   

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)            
            print name, "=>", better_name     
       
                
            #Second Check replace bad street names with corrected ones       
            if "Streetewart" in better_name:
                better_name = better_name.replace(" Streetewart", " Stewart")                
                print name, "=>", better_name 




# Noted a postalcode with a +4 number, will drop this and maintain only 9-digit postal code

area_postcode_re = re.compile('^[A-Z]{1,2}[0-9]{1,2}[A-Z]? ?[0-9]?$')

def update_postcode(odd_postcode):
    if area_postcode_re.search(odd_postcode):
        postcode = " "
    else:
        postcode = odd_postcode.split("-")[0]
    return postcode


def improve_postcode():
    postcode_all = audit.find_postcode()

    for postcode in postcode_all[1]:
        better_postcode = update_postcode(postcode)
        print postcode, "=>", better_postcode





# Fix postal codes
improve_postcode()


