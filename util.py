import pandas as pd
import itertools
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

def create_variant(address):
    """
    Create variations of an address to test fuzzy matching algorithms

    e.g. 2923 Beacon Grove Street -> ["2923 Beacon Grove Street", "2923 Beacon Grv Street", "2923 Beacon Grv St", "2923 Beacon Grv Strt", "2923 Beacon Grv Str"]
    """

    # split the address into its components
    address = address.split()

    # create a list of address variations
    address_variants = []

    # iterate over the components of the address
    for part in address:
        new_address_variants = []
        for key, value in ADDRESS_VARIANTS.items():
            if part in value:
                for variant in value:
                    new_address_variants.append(part.replace(part, variant))

        if new_address_variants:
            address_variants.append(new_address_variants)
        else:
            address_variants.append([part])

    # create a list of all possible address variations
    address_variants = list(itertools.product(*address_variants))

    # join the components of the address
    address_variants = [" ".join(variant) for variant in address_variants]

    return address_variants

    

if __name__ == "__main__":
    # create csv file with addresses variations that will be used to test fuzzy matching algorithms

    # list of addresses
    data = pd.read_csv("addresses.csv")
    addresses = data["address"].tolist()

    # create a list of address variations
    address_variants = []
    for address in addresses:
        address_variants.extend(create_variant(address))
    
    # create a dataframe with the address variations
    address_variants = pd.DataFrame(address_variants, columns=["address"])
    address_variants.to_csv("address_variants.csv", index=False)

    


