from datetime import datetime

import pandas as pd
import Levenshtein as levenshtein
import difflib
from fuzzywuzzy import fuzz
import os
from util import split_address_number_from_string, move_number_to_beginning_of_string, compare_addressess_street_suffix
        
def direct_matching(addresses, addresses_to_match):
    """
    Directly match addresses to test the performance of the fuzzy matching algorithms
    """
    matches = []
    for address in addresses:
        if address in addresses_to_match:
            matches.append(
                {
                    "address": address,
                    "address_to_match": address,
                    "similarity": 1
                }
            )

    return matches

def levenshtein_matching(addresses, addresses_to_match):
    """
    Use the Levenshtein distance to match addresses
    """
    matches = []
    for address in addresses:
        number, _ = split_address_number_from_string(address)

        for address_to_match in addresses_to_match:
            if number not in address_to_match or not compare_addressess_street_suffix(address, address_to_match):
                continue

            similarity = levenshtein.ratio(address, address_to_match)

            if similarity >= 0.7:
                matches.append(
                    {
                        "address": address,
                        "address_to_match": address_to_match,
                        "similarity": similarity
                    }
                )

    return matches

def difflib_matching(addresses, addresses_to_match):
    """
    Use the difflib library to match addresses
    """
    matches = []
    compared_pairs = set()
    for address in addresses:
        number, _ = split_address_number_from_string(address)

        for address_to_match in addresses_to_match:
            pair = (address, address_to_match)
            if pair in compared_pairs:
                continue

            if number not in address_to_match or not compare_addressess_street_suffix(address, address_to_match):
                continue

            compared_pairs.add(pair)
            similarity = difflib.SequenceMatcher(None, address, move_number_to_beginning_of_string(address_to_match, number)).ratio()

            if similarity >= 0.70:
                matches.append({
                    "address": address,
                    "address_to_match": address_to_match,
                    "similarity": similarity
                })

    return matches
    

def jaro_winkler_matching(addresses, addresses_to_match):
    """
    Use the jaro winkler distance to match addresses
    """
    matches = []
    for address in addresses:
        number, _ = split_address_number_from_string(address)

        for address_to_match in addresses_to_match:
            if number not in address_to_match or not compare_addressess_street_suffix(address, address_to_match):
                continue

            similarity = levenshtein.jaro_winkler(address, move_number_to_beginning_of_string(address_to_match, number))

            if similarity >= 0.80:
                matches.append({
                    "address": address,
                    "address_to_match": address_to_match,
                    "similarity": similarity
                })

    return matches


def fuzzywuzzy_matching(addresses, addresses_to_match):
    """
    Use the fuzzywuzzy library to match addresses
    """
    matches = []
    for address in addresses:
        number, _ = split_address_number_from_string(address)

        for address_to_match in addresses_to_match:

            if number not in address_to_match or not compare_addressess_street_suffix(address, address_to_match):
                continue

            similarity = fuzz.ratio(address, move_number_to_beginning_of_string(address_to_match, number))


            if similarity >= 70:
                matches.append({
                    "address": address,
                    "address_to_match": address_to_match,
                    "similarity": similarity
                })

    return matches


if __name__ == "__main__":
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
    INPUT_DIR = os.path.join(os.path.dirname(__file__), "input")
    # compare the performance of different fuzzy matching algorithms

    # load the data
    data = pd.read_csv(os.path.join(INPUT_DIR, "addresses.csv"))
    addresses = data["address"].tolist()

    correct_address_matches = pd.read_csv(os.path.join(INPUT_DIR, "address_correct_variants.csv"))
    addresses_to_match = correct_address_matches["address"].tolist()

    wrong_address_matches = pd.read_csv(os.path.join(INPUT_DIR, "address_wrong_variants.csv"))
    addresses_to_match += wrong_address_matches["address"].tolist()

    # check csv file with total of addresses tested, total of variations tested, total of matches found, and time taken to run the algorithm
    
    algorithms = [direct_matching, levenshtein_matching, difflib_matching, fuzzywuzzy_matching, jaro_winkler_matching]
    results_summary = []
    results_matches_per_algorithm = {}

    for algorithm in algorithms:
        start_time = datetime.now()
        matches = algorithm(addresses, addresses_to_match)
        time_taken_ms = (datetime.now() - start_time).total_seconds() * 1000

        for match in matches:
            if match["address_to_match"] in correct_address_matches["address"].tolist():
                match["correct"] = True
            else:
                match["correct"] = False

        false_positives = len([match for match in matches if match["correct"] == False])
        true_positives = len([match for match in matches if match["correct"] == True])

        success_rate = true_positives / (true_positives + false_positives) * 100 if true_positives + false_positives > 0 else 0

        result = {
            "Algorithm": algorithm.__name__,
            "Total of addresses tested": len(addresses),
            "Total of correct variations tested": len(correct_address_matches),
            "Total of wrong variations tested": len(wrong_address_matches),
            "Total of matches found": len(matches),
            "True positives": true_positives,
            "False positives": false_positives,
            "Time taken ms": time_taken_ms,
            "success rate %": success_rate
        }
        
        for key, value in result.items():
            print(key, ":", value)

        print("")

        results_matches_per_algorithm[algorithm.__name__] = matches
        results_summary.append(result)

    # create a csv file with the results
    results_summary = pd.DataFrame(results_summary)
    results_summary.to_csv(os.path.join(OUTPUT_DIR, "results.csv"), index=False)

    # create a csv file with the matches found by each algorithm
    for algorithm, matches in results_matches_per_algorithm.items():
        matches = pd.DataFrame(matches)
        matches.to_csv(os.path.join(OUTPUT_DIR, f"{algorithm}_matches.csv"), index=False)

