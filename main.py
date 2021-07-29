import random
import timeit


# Matching night
from gui_kram import event_loop


def get_number_of_beams(matches, solution):
    return len(list(filter(lambda p: p in solution, matches)))


# Truth booth
def is_perfect_match(pairing, solution):
    return pairing in solution


def get_random_pairs(male_list, female_list):
    pair_list = []
    female_list = female_list.copy()
    for m in male_list:
        f = random.choice(female_list)
        female_list.remove(f)
        pair_list.append([m, f])
    return pair_list


def get_all_possible_combinations(combinations, males, females, combination):
    if len(males) == 0:
        combinations.append(combination)
    else:
        m = males[0]
        for f in females:
            comb_copy = combination.copy()
            comb_copy.append([m, f])
            m_copy = males[1: len(males)]
            f_copy = females.copy()
            f_copy.remove(f)
            get_all_possible_combinations(combinations, m_copy, f_copy, comb_copy)


def delete_impossible_combinations_after_truth_booth(combinations, pair, is_match):
    if is_match:
        return list(filter(lambda c: pair in c, combinations))
    else:
        return list(filter(lambda c: pair not in c, combinations))


def common_members(combination, matching_night_set, beams):
    return len(set(tuple(x) for x in combination).intersection(matching_night_set)) == beams


def delete_impossible_combinations_after_matching_night(combinations, matching_night_combo, beams):
    matching_night_set = set(tuple(x) for x in matching_night_combo)
    return list(filter(lambda c: common_members(c, matching_night_set, beams), combinations))


def find_perfect_matches(males, females, solution, pre_knowledge=None):
    combinations = []
    get_all_possible_combinations(combinations, males, females, [])

    # for i in range(1, 11):
    i = 0
    while len(combinations) > 1:
        i += 1
        print("%d.Runde: %d Kombinationen möglich" % (i, len(combinations)))
        truth_booth_pair = random.choice(random.choice(combinations))
        match = is_perfect_match(truth_booth_pair, solution)
        combinations = delete_impossible_combinations_after_truth_booth(combinations, truth_booth_pair, match)

        matching_night_pairs = random.choice(combinations)
        beams = get_number_of_beams(matching_night_pairs, solution)
        combinations = delete_impossible_combinations_after_matching_night(combinations, matching_night_pairs, beams)
    return combinations.pop(), i


def statistic_runs(runs):
    males = ['Abraham', 'Bernd', 'Carl', 'Detlef', 'Emil', 'Farad', 'Gerald', 'Hugo', 'Ingo', 'Jusuf']
    females = ['Anna', 'Birte', 'Clementine', 'Demi', 'Eva', 'Franziska', 'Gertrud', 'Hannah', 'Inge', 'Josefine']
    all_rounds = []
    for i in range(runs):
        pairs = get_random_pairs(males, females)
        found_combination, rounds = find_perfect_matches(males, females, pairs)
        print('Berechnete couples:')
        print(found_combination)
        print('Echte couples:')
        print(pairs)
        all_rounds.append(rounds)
        print(rounds)
    mean_rounds = sum(all_rounds) / len(all_rounds)
    print("In %d Durchläufen, wurde durchschnittlich in der %f. Runde die richtige Lösung gefunden"
          % (runs, mean_rounds))


def get_possibilities(males, females, pre_knowledge):
    pairs = get_random_pairs(males, females)
    found_combination, rounds = find_perfect_matches(males, females, pairs, pre_knowledge)
    print('Berechnete couples:')
    print(found_combination)
    print('Echte couples:')
    print(pairs)


def read_pre_given_info():
    with open('input.txt') as f:
        contents = f.readlines()

    # for c in contents:
    #     if c.startswith('-'):

    males = []
    females = []
    pre_knowledge = contents
    return males, females, pre_knowledge


if __name__ == '__main__':
    # start = timeit.default_timer()
    # males, females, pre_knowledge = read_pre_given_info()
    # # statistic_runs(200)
    # get_possibilities(males, females, pre_knowledge)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)

    event_loop()
