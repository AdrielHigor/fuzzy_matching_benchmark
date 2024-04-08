from functools import lru_cache


ADDRESS_VARIANTS = {
    "Apartment": ["Apt", "Apartment", "Apmt", "Unit", "U"],
    "Street": ["St", "Street", "Str", "Strt", "St."],
    "Road": ["Rd", "Road", "Rd."],
    "Drive": ["Dr", "Drive"],
    "Lane": ["Ln", "Lane", "Ln."],
    "Circle": ["Cir", "Circle", "Circ"],
    "Court": ["Ct", "Court"],
    "Place": ["Pl", "Place", "Pl."],
    "Terrace": ["Ter", "Terrace"],
    "Highway": ["Hwy", "Highway"],
    "Square": ["Sq", "Square"],
    "Building": ["Bldg", "Building"],
    "Floor": ["Fl", "Floor", "Fl."],
    "Room": ["Rm", "Room"],
    "Suite": ["Ste", "Suite", "Ste."],
    "Grove": ["Grv", "Grove"],
    "Boulevard": ["Blvd", "Boulevard"],
    "Avenue": ["Ave", "Avenue", "Ave."],
}

@lru_cache(maxsize=None)
def split_address_number_from_string(address):
    """
    Split the address number from the address string and return both
    """

    address = address.split()

    for i, part in enumerate(address):
        if part.isdigit():
            return " ".join(address[:i+1]), " ".join(address[i+1:])
        
def move_number_to_beginning_of_string(address, number):
    """
    Move the address number to the beginning of the address string
    """

    address = address.replace(number, "")
    return f"{number} {address}"

def get_address_street_suffix(address):
    """
    Get the street suffix of an address
    """

    address = address.lower().split()
    for part in address:
        for key, value in ADDRESS_VARIANTS.items():
            for value_part in value:
                if part == value_part.lower():
                    return key

    return None

def compare_addressess_street_suffix(address, address_to_match):
    """
    Compare the street suffix of two addresses
    """

    street_suffix = get_address_street_suffix(address)
    street_suffix_to_match = get_address_street_suffix(address_to_match)

    if street_suffix and street_suffix_to_match:
        return street_suffix == street_suffix_to_match

    return False