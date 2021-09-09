import PySimpleGUI as sg
import json
import os.path

from Round import Round
from calculations import calculate_possibilities, rank_possible_couples, get_all_couples


def get_pairs_overview(_round, _males_copy, _females_copy):
    females_first = _round % 2 == 1
    pairs = [[sg.Text('Pair %d:' % i, size=(5, 1)),
              sg.Text(_females_copy[i - 1] if females_first and len(_females_copy) > i else _males_copy[i - 1]
              if not females_first and len(_males_copy) > i else '',
                      key='mn%d-%s%d' % (_round, 'f' if females_first else 'm', i), size=(20, 1)),
              sg.Combo(_males_copy if females_first else _females_copy,
                       key='mn%d-%s%d' % (_round, 'm' if females_first else 'f', i), size=(20, 1))
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
    # return col1


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
               sg.Button("Calculate", size=(10, 1), pad=(35, (10, 5)), key='Calculate')],
              [sg.Button("Load", size=(10, 1), key='Load', disabled=True)]]
    output = [[sg.Multiline(key='OUT0', size=(50, 28), background_color='black', pad=((10, 0), (20, 10)))]]
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
                      + [sg.Text('Version 0.9')]
                      ])
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


def reload_saved_data(window, males, females):
    _males_copy = list(filter(lambda m: len(m) > 0, males))
    _females_copy = list(filter(lambda f: len(f) > 0, females))
    for i in range(1, 11):
        tb_key_m = 'tb%d-m' % i
        tb_key_f = 'tb%d-f' % i
        window[tb_key_m].update(values=_males_copy)
        window[tb_key_f].update(values=_females_copy)
        base_mn_key = 'mn%d-' % i
        for j in range(1, 11):
            mn_key_m = base_mn_key + 'm' + str(j)
            mn_key_f = base_mn_key + 'f' + str(j)
            # woman's choice
            if i % 2 == 1:
                field_value = _females_copy[j - 1] if len(_females_copy) > j - 1 else ''
                window[mn_key_f].update(field_value)
                window[mn_key_m].update(values=_males_copy)
            # men's choice
            else:
                field_value = _males_copy[j - 1] if len(_males_copy) > j - 1 else ''
                window[mn_key_m].update(field_value)
                window[mn_key_f].update(values=_females_copy)


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
    top_5_most_likely_matches = get_pretty_ranked_print(couple_ranking[0:5], len(possible_combinations))
    top_5_least_likely_matches = get_pretty_ranked_print(couple_ranking[-5:], len(possible_combinations))
    for i in range(11):
        # window['OUT%d' % i]('')
        window['OUT%d' % i].print(text)
        window['OUT%d' % i].print(found, text_color='green')
        window['OUT%d' % i].print(impossible, text_color='red')
        window['OUT%d' % i].print(combs, text_color='white')
        window['OUT%d' % i].print(top_5_most_likely_matches, text_color='green')
        window['OUT%d' % i].print(top_5_least_likely_matches, text_color='red')


def save_rounds(event, values, rounds_dict, found_matches, impossible_matches, males, females):
    round_num = int(event[-1]) + 1
    rounds_dict[round_num] = Round(round_num, values, males, females)


def save_to_json(dictionary):
    with open("save.txt", 'w') as file:
        file.seek(0)
        json.dump(dictionary, file)
        file.truncate()


def load_from_json(window):
    d = json.load(open("save.txt"))
    for key, value in d.items():
        # FIXME: load to text fields does not work (radio buttons, slider, inputs and dropdowns already work!)
        window[key].update(value)
    return d


def event_loop():
    males, females = ['' for _ in range(10)], ['' for _ in range(10)]
    # males, females = ['Abraham', 'Bernd', 'Carl', 'Detlef', 'Emil', 'Farad', 'Gerald', 'Hugo', 'Ingo', 'Jusuf'],\
    #                  ['Anna', 'Birte', 'Clementine', 'Demi', 'Eva', 'Franziska', 'Gertrud', 'Hannah', 'Inge', 'Josefine']
    possible_combinations = []
    rounds_dict = {}
    found_matches = []
    impossible_matches = []
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
                save_to_json(values)
            else:
                sg.popup('There are missing candidates')
        elif event in ['Save%d' % i for i in range(10)]:
            save_rounds(event, values, rounds_dict, found_matches, impossible_matches, males, females)
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
            # file walker -> chose file to save and to load from
            if os.path.isfile("save.txt"):
                rounds_dict = load_from_json(window)
    window.close()

    # TODO:
    # - load data from file
    # - wahrscheinlichkeiten für beliebiges match nach aktuellem Wissensstand
    # - Perfect Matches automatisch eintragen


if __name__ == '__main__':
    event_loop()
