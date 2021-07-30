def get_all_possible_combinations(combinations, males, females, combination, impossible_matches):
    if len(males) == 0:
        combinations.append(combination)
    else:
        m = males[0]
        for f in females:
            if [m, f] not in impossible_matches:
                comb_copy = combination.copy()
                comb_copy.append([m, f])
                m_copy = males[1: len(males)]
                f_copy = females.copy()
                f_copy.remove(f)
                get_all_possible_combinations(combinations, m_copy, f_copy, comb_copy, impossible_matches)


def evaluate_information(rounds_dict):
    found_matches = []
    impossible_matches = []
    matching_nights = []
    for key, value in rounds_dict.items():
        if value.is_truth_booth_set:
            if value.is_truth_booth_match:
                found_matches.append(value.truth_booth_pair)
            else:
                impossible_matches.append(value.truth_booth_pair)
        if value.is_round_complete:
            pass
    # was ist hier verwertbares drin?
    return found_matches, impossible_matches, matching_nights


def calculate_possibilities(rounds_dict, found_matches, impossible_matches, possible_combinations, males, females):
    pass
