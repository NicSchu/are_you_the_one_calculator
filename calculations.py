from statistics import common_members


def is_possible(combination, matching_night):
    beams = matching_night[0]
    pairs = matching_night[1]
    matching_night_set = set(tuple(x) for x in pairs)
    return common_members(combination, matching_night_set, beams)


def get_all_possible_combinations(combinations, males, females, combination, impossible_matches, matching_nights):
    if len(males) == 0:
        possible = True
        for matching_night in matching_nights:
            if not is_possible(combination, matching_night):
                possible = False
                break
        if possible:
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
                get_all_possible_combinations(combinations, m_copy, f_copy, comb_copy, impossible_matches,
                                              matching_nights)


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
            matching_nights.append([value.beams, value.pairs])
    return found_matches, impossible_matches, matching_nights


def get_males_females_without_found_matches(males, females, found_matches):
    males_copy = males.copy()
    females_copy = females.copy()
    for match in found_matches:
        males_copy.remove(match[0])
        females_copy.remove(match[1])
    return males_copy, females_copy


def calculate_possibilities(rounds_dict, males, females):
    found_matches, impossible_matches, matching_nights = evaluate_information(rounds_dict)
    possible_combinations = []
    males_copy, females_copy = get_males_females_without_found_matches(males, females, found_matches)
    get_all_possible_combinations(possible_combinations, males_copy, females_copy, found_matches,
                                  impossible_matches, matching_nights)
    return possible_combinations, found_matches, impossible_matches


def get_all_couples(males, females, impossible_couples, found_couples):
    couples = []
    males_wo_couples, females_wo_couples = get_males_females_without_found_matches(males, females, found_couples)
    for m in males_wo_couples:
        for f in females_wo_couples:
            couple = [m, f]
            if couple not in impossible_couples:
                couples.append(couple)
    return couples


def rank_possible_couples(all_couples, possible_combinations, found_matches, impossible_matches):
    couples = list(map(lambda c: [c, 0], all_couples))
    for combination in possible_combinations:
        for couple in couples:
            if couple[0] in combination:
                couple[1] += 1
    return sorted(couples, key=lambda match: match[1], reverse=True)

