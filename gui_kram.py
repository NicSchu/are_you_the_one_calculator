import PySimpleGUI as sg

from Round import Round
from calculations import calculate_possibilities


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


def get_round_layout(_round, _males, _females):
    _males_copy = list(filter(lambda m: len(m) > 0, _males))
    _females_copy = list(filter(lambda f: len(f) > 0, _females))
    return [
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


def get_main_layout(_males, _females):
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
    return header + content + footer


def all_filled(_list):
    return len(list(filter(lambda e: len(e) > 0, _list))) == len(_list)


def get_layout(_males, _females):
    return [
        [sg.TabGroup([[
                          sg.Tab('Candidates', get_main_layout(_males, _females)),
                      ] + [sg.Tab('Round %d' % r, get_round_layout(r, _males, _females)) for r in range(1, 11)]
                      ])
         ]
    ]


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


def save_rounds(event, values, rounds_dict, found_matches, impossible_matches, males, females):
    round_num = int(event[-1]) + 1
    rounds_dict[round_num] = Round(round_num, values, males, females)


def event_loop():
    males, females = ['' for i in range(10)], ['' for i in range(10)]
    possible_combinations = []
    rounds_dict = {}
    found_matches = []
    impossible_matches = []
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
                print(males)
                print(females)
            else:
                sg.popup('There are missing candidates')
        elif event in ['Save%d' % i for i in range(10)]:
            print('hallo')
            save_rounds(event, values, rounds_dict, found_matches, impossible_matches, males, females)
        elif event in ['Calculate%d' % i for i in range(10)] + ['Calculate']:
            calculate_possibilities(rounds_dict, found_matches, impossible_matches, possible_combinations, males, females)
            print('Das Rechnen möge beginnen')
    window.close()

    # TODO:
    # - save data to file or something else
    # - calculate with given data
    # - wahrscheinlichkeiten für bestimmte matches nach aktuellem Wissensstand: #kombinationen mit dem Paar/#kombinationen insgesamt


if __name__ == '__main__':
    event_loop()
