import PySimpleGUI as sg
import json

from src.Round import Round
from calculations import calculate_possibilities, rank_possible_couples, get_all_couples


def get_pairs_overview(_round, _males_copy, _females_copy):
    females_first = _round % 2 == 1
    pairs = [[sg.Text('Pair %d:' % i, size=(5, 1)),
              sg.Text(_females_copy[i - 1] if females_first and len(_females_copy) > i else _males_copy[i - 1]
              if not females_first and len(_males_copy) > i else '',
                      key='mn%d-%s%d' % (_round, 'f' if females_first else 'm', i), size=(20, 1)),
              sg.Combo([''] + _males_copy if females_first else [''] + _females_copy,
                       key='mn%d-%s%d' % (_round, 'm' if females_first else 'f', i), size=(20, 1), enable_events=True)
              ]
             for i in range(1, 11)]
    return pairs


def get_round_layout(_round, _males, _females, col_size):
    _males_copy = list(filter(lambda m: len(m) > 0, _males))
    _females_copy = list(filter(lambda f: len(f) > 0, _females))
    col1 = [
               [sg.Text("%d. Round" % _round, size=(10, 2))],
               [sg.Text('Trooth booth:')],
               [sg.Combo(_males_copy, key='tb%d-m' % _round, size=(20, 1)),
                sg.Combo(_females_copy, key='tb%d-f' % _round, size=(20, 1))],
               [sg.Radio('Match', "match_%d" % _round, key='match_%d' % _round),
                sg.Radio('No Match', "match_%d" % _round, key='no_match_%d' % _round)],
               [sg.Text('Matching Night:')],
           ] + get_pairs_overview(_round, _males_copy, _females_copy) + \
           [
               [sg.Text('Number of Beams:')],
               [sg.Slider(range=(0, 10), default_value=0, size=(43, 15), orientation='horizontal',
                          key='beams_%d' % _round)],
               [sg.Button("Save", size=(10, 1), pad=(35, (10, 5)), key='Save%d' % (_round - 1)),
                sg.Button("Calculate", size=(10, 1), pad=(35, (10, 5)), key='Calculate%d' % (_round - 1))]
           ]
    output = [[sg.Multiline(key='OUT%d' % _round, size=(50, 28), background_color='black', pad=((10, 0), (20, 10)))]]
    return [[sg.Column(col1, size=col_size), sg.Column(output, size=col_size)]]


def get_main_layout(_males, _females, col_size):
    header = [
        [sg.Text("Please enter the names of the participants:")],
        [sg.Text('Males', size=(22, 1)), sg.Text('Females', size=(22, 1))],
    ]
    content = [[sg.Text('%d:' % row, size=(2, 1), pad=(5, 8)) if col % 2 == 0
                else sg.Input(default_text=_males[row - 1] if col == 1 else _females[row - 1],
                              size=(20, 1), key='%s-%d' % ('m' if col == 1 else 'f', row), pad=(5, 8))
                for col in range(4)] for row in range(1, 11)]
    footer = [[sg.Button("Save", size=(10, 1), pad=(35, (10, 5)), key='Save'),
               sg.Button("Calculate", size=(10, 1), pad=(35, (10, 5)), key='Calculate')]]
    output = [
        [
            sg.Multiline(key='OUT0', size=(50, 28), background_color='black', pad=((10, 0), (20, 10)))
        ], [
            sg.FileSaveAs("Save to File", size=(10, 1), pad=(20, (10, 5)), key='SaveFile',
                          file_types=(("Text File", "*.txt"),), enable_events=True, target='SaveFile'),
            sg.FileBrowse("Load from File", size=(10, 1), pad=(20, (10, 5)), key='Load', initial_folder='./',
                          file_types=(("Text File", "*.txt"),), enable_events=True, target='Load'),
            sg.Button("Clear All", size=(10, 1), pad=(20, (10, 5)), key='Clear')
        ]]
    layout = [[sg.Column(header + content + footer, size=col_size), sg.Column(output, size=col_size)]]
    return layout


def all_filled(_list):
    return len(list(filter(lambda e: len(e) > 0, _list))) == len(_list)


def get_layout(_males, _females):
    col_size = (400, 550)

    return [
        [sg.TabGroup([[
                          sg.Tab('Candidates', get_main_layout(_males, _females, col_size)),
                      ] + [sg.Tab('Round %d' % r, get_round_layout(r, _males, _females, col_size)) for r in range(1, 11)]
                      + [sg.Text('Version ' + version)]
                      ], key="tab")
         ]
    ]


# ----------------------------------------------------
def get_candidates(_values):
    _males = []
    _females = []
    for i in range(1, 11):
        _males.append(_values['m-%d' % i])
        _females.append(_values['f-%d' % i])
    return _males, _females


def update_dropdowns(window, event, males, females, values):
    base = event[:-1]
    if base[-1] == '1':
        base = base[:-1]
    chosen = []
    for i in range(1, 11):
        person = values[base + str(i)]
        if person != '':
            chosen.append(person)
    new_values = [x for x in (males if base[-1] == 'm' else females) if x not in chosen]

    for i in range(1, 11):
        field_name = base + str(i)
        value = values[field_name]
        window[field_name].update(values=[''] + new_values)
        window[field_name].update(value)


def reload_saved_data(window, males, females):
    _males_copy = list(filter(lambda m: len(m) > 0, males))
    _females_copy = list(filter(lambda f: len(f) > 0, females))
    for i in range(1, 11):
        tb_key_m = 'tb%d-m' % i
        tb_key_f = 'tb%d-f' % i
        window[tb_key_m].update(values=[''] + _males_copy)
        window[tb_key_f].update(values=[''] + _females_copy)
        base_mn_key = 'mn%d-' % i
        for j in range(1, 11):
            mn_key_m = base_mn_key + 'm' + str(j)
            mn_key_f = base_mn_key + 'f' + str(j)
            # woman's choice
            if i % 2 == 1:
                field_value = _females_copy[j - 1] if len(_females_copy) > j - 1 else ''
                window[mn_key_f].update(field_value)
                window[mn_key_m].update(values=[''] + _males_copy)
            # men's choice
            else:
                field_value = _males_copy[j - 1] if len(_males_copy) > j - 1 else ''
                window[mn_key_m].update(field_value)
                window[mn_key_f].update(values=[''] + _females_copy)


def new_window(males, females):
    layout = get_layout(males, females)
    return sg.Window(title='Are you the one? - Calculator', layout=layout)


def close_input_fields(window):
    for i in range(1, 11):
        window['m-%d' % i].update(disabled=True, text_color='grey')
        window['f-%d' % i].update(disabled=True, text_color='grey')
    window['Save'].update(disabled=True)


def get_pretty_pair_print(pairs, ranked):
    st = ''
    for i in range(len(pairs)):
        if ranked:
            st += '%d. ' % (i+1)
        st += '%s and %s\n' % (pairs[i][0], pairs[i][1])
    return st


def get_pretty_ranked_print(ranking, num_poss):
    st = ''
    for i in range(len(ranking)):
        st += "%d. %s and %s (%f %%)\n" % (i + 1, ranking[i][0][0], ranking[i][0][1], (ranking[i][1] / num_poss) * 100)
    return st


def update_outputs(window, found_matches, impossible_matches, possible_combinations, couple_ranking):
    text = '\n\n----------------------------------\n'
    found = 'Matches found:\n' + get_pretty_pair_print(found_matches, True)
    impossible = 'No Matches:\n' + get_pretty_pair_print(impossible_matches, True)
    combs = 'Possible combinations left: ' + str(len(possible_combinations))
    top_most_likely_matches = get_pretty_ranked_print(couple_ranking[0:10], len(possible_combinations))
    top_least_likely_matches = get_pretty_ranked_print(couple_ranking[-10:], len(possible_combinations))
    for i in range(11):
        # window['OUT%d' % i]('')
        window['OUT%d' % i].print(text)
        window['OUT%d' % i].print(impossible, text_color='red')
        window['OUT%d' % i].print(found, text_color='green')
        window['OUT%d' % i].print(combs, text_color='white')
        window['OUT%d' % i].print(top_most_likely_matches, text_color='green')
        if len(possible_combinations) != 1:
            window['OUT%d' % i].print(top_least_likely_matches, text_color='red')


def save_round(round_num, values, rounds_dict, found_matches, impossible_matches, males, females, window):
    saved_round = Round(round_num, values, males, females)
    rounds_dict[round_num] = saved_round
    if saved_round.is_truth_booth_match:
        found_matches.append(saved_round.truth_booth_pair)
        for i in range(round_num, 11):
            # if i in rounds_dict.keys() &&
            base = 'mn%d-' % i
            for j in range(1, 11):
                m_string = base + 'm%d' % j
                f_string = base + 'f%d' % j
                if i % 2 == 0 and males[j-1] in saved_round.truth_booth_pair and values[f_string] == '':
                    female = [p for p in saved_round.truth_booth_pair if p != males[j-1]][0]
                    values[f_string] = female
                    window[f_string].update(female)
                    update_dropdowns(window, f_string, males, females, values)
                elif i % 2 == 1 and females[j-1] in saved_round.truth_booth_pair and values[m_string] == '':
                    male = [p for p in saved_round.truth_booth_pair if p != females[j-1]][0]
                    values[m_string] = male
                    window[m_string].update(male)
                    update_dropdowns(window, m_string, males, females, values)
    else:
        impossible_matches.append(saved_round.truth_booth_pair)


def save_to_json(dictionary):
    file = dictionary['SaveFile']
    if file != '':
        del dictionary['SaveFile']
        del dictionary['Load']
        with open(file, 'w') as file:
            file.seek(0)
            json.dump(dictionary, file)
            file.truncate()


def load_candidates(window, d, fields):
    candidates = []
    for field in fields:
        candidate = d[field]
        del d[field]
        window[field].update(candidate)
        candidates.append(candidate)
    return candidates


def load_males_and_females(window, d):
    m_fields = ['m-%d' % x for x in range(1, 11)]
    f_fields = ['f-%d' % x for x in range(1, 11)]
    return load_candidates(window, d, m_fields), load_candidates(window, d, f_fields)


def load_from_json(window, file, values):
    d = json.load(open(file))
    males, females = load_males_and_females(window, d)

    reload_saved_data(window, males, females)
    if all_filled(males) and all_filled(females):
        close_input_fields(window)

    candidate_fields = ['%s-%d' % (mf, x) for x in range(1, 11) for mf in ['m', 'f']]
    for key, value in d.items():
        if key in values:
            values[key] = value
        if key not in ['SaveFile', 'Load'] + candidate_fields:
            window[key].update(value)
            if key in ['mn%d-%s%d' % (i, mf, j) for i in range(1, 11) for j in range(1, 11) for mf in ['m', 'f']]:
                update_dropdowns(window, key, males, females, values)
    return males, females


def event_loop():
    males, females = ['' for _ in range(10)], ['' for _ in range(10)]
    # males, females = ['Abraham', 'Bernd', 'Carl', 'Detlef', 'Emil', 'Farad', 'Gerald', 'Hugo', 'Ingo', 'Jusuf'],\
    #                  ['Anna', 'Birte', 'Clementine', 'Demi', 'Eva', 'Franziska', 'Gertrud', 'Hannah', 'Inge', 'Josefine']
    rounds_dict = {}
    found_matches = []
    impossible_matches = []
    possible_combinations = []
    all_couples = []
    # Window
    sg.theme('DarkAmber')
    # sg.theme_previewer()
    window = new_window(males, females)

    while True:
        event, values = window.read()
        print(event, values)
        if event in (None, 'Cancel', sg.WIN_CLOSED):
            break
        elif event == 'Save':
            males, females = get_candidates(values)
            reload_saved_data(window, males, females)
            if all_filled(males) and all_filled(females):
                close_input_fields(window)
            else:
                sg.popup('There are missing candidates')
        elif event in ['Save%d' % i for i in range(10)]:
            save_round(int(event[-1]) + 1, values, rounds_dict, found_matches, impossible_matches, males, females, window)
        elif event == 'SaveFile':
            save_to_json(values)
        elif event in ['Calculate%d' % i for i in range(10)] + ['Calculate']:
            possible_combinations, found_matches, impossible_matches = \
                calculate_possibilities(rounds_dict, males, females)
            # safe fixed couples in lists
            all_couples = get_all_couples(males, females, impossible_matches, found_matches)
            couple_ranking, more_impossible_matches = rank_possible_couples(all_couples, possible_combinations)
            impossible_matches += more_impossible_matches
            update_outputs(window, found_matches, impossible_matches, possible_combinations, couple_ranking)
        elif event == 'Load':
            file = values[event]
            if file != '':
                males, females = load_from_json(window, file, values)
                # reload_saved_data(window, males, females)
                for i in range(1, 11):
                    save_round(i, values, rounds_dict, found_matches, impossible_matches, males, females, window)
        elif event in ['mn%d-%s%d' % (i, mf, j) for i in range(1, 11) for j in range(1, 11) for mf in ['m', 'f']]:
            update_dropdowns(window, event, males, females, values)
        elif event == 'Clear':
            found_matches, impossible_matches, males, females = [], [], ['' for _ in range(10)], ['' for _ in range(10)]
            rounds_dict = {}
            window.close()
            window = new_window(males, females)
    window.close()

    # TODO:
    # - Wahrscheinlichkeiten für beliebiges match nach aktuellem Wissensstand
    # - Namen fixen - warum kein Match?
    # - Option Männer/Damenwahl


if __name__ == '__main__':
    version = '1.0'
    event_loop()
