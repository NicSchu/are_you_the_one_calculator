import PySimpleGUI as sg


def get_pairs_overview(_round, _males_copy, _females_copy):
    females_first = _round % 2 == 1
    pairs = [[sg.Text('Pair %d:' % i, size=(5, 1)),
              sg.Text(_females_copy[i-1] if females_first and len(_females_copy) > i else _males_copy[i-1]
              if not females_first and len(_males_copy) > i else '',
                      key='mn%d-%s%d' % (_round, 'f' if females_first else 'm', i), size=(20, 1)),
              sg.Combo(_males_copy if females_first else _females_copy,
                       key='mn%d-%s%d' % (_round, 'm' if females_first else 'f', i), size=(20, 1)),
              # sg.Combo(_females_copy, key='mn%d-f%d' % (_round, i), size=(20, 1))
              ]
             for i in range(1, 11)]
    return pairs


def get_round_layout(_round, _males, _females):
    _males_copy = list(filter(lambda m: len(m) > 0, _males))
    _females_copy = list(filter(lambda f: len(f) > 0, _females))
    return [
        [sg.Text("%d. Round" % _round, size=(10, 2))],
        [sg.Text('Trooth booth:')],
        [sg.Combo(_males_copy, key='tb%d-m' % _round, size=(20, 1)), sg.Combo(_females_copy, key='tb%d-f' % _round, size=(20, 1))],
        [sg.Text('Matching Night:')],
    ] + get_pairs_overview(_round, _males_copy, _females_copy) + [[sg.Button("Save", size=(10, 1), pad=(35, (10, 5)))]]


def get_main_layout(_males, _females):
    header = [
        [sg.Text("Please enter the names of the participants:")],
        [sg.Text('Males', size=(22, 1)), sg.Text('Females', size=(22, 1))],
    ]
    content = [[sg.Text('%d:' % row, size=(2, 1)) if col % 2 == 0
                else sg.Input(default_text=_males[row-1]
                if col == 1 else _females[row-1], size=(20, 1), key='%s-%d' % ('m' if col == 1 else 'f', row))
                for col in range(4)] for row in range(1, 11)]
    footer = [[sg.Button("Save", size=(10, 1), pad=(35, (10, 5)))]]
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
                field_value = _females_copy[j-1] if len(_females_copy) > j-1 else ''
                window[mn_key_f].update(field_value)
                window[mn_key_m].update(values=_males_copy)
            # men's choice
            else:
                field_value = _males_copy[j-1] if len(_males_copy) > j-1 else ''
                window[mn_key_m].update(field_value)
                window[mn_key_f].update(values=_females_copy)


def new_window(males, females):
    layout = get_layout(males, females)
    return sg.Window(title='Are you the one? - Calculator', layout=layout)


def event_loop():
    males, females = ['' for i in range(10)], ['' for i in range(10)]
    # Window
    sg.theme('DarkAmber')
    window = new_window(males, females)
    # for i in range(1, 10000):
    #     sg.one_line_progress_meter('My Meter', i + 1, 10000, 'key', 'Optional message')

    while True:
        event, values = window.read()
        print(event, values)
        if event in (None, 'Cancel', sg.WIN_CLOSED):
            break
        elif event == 'Save':
            males, females = get_candidates(values)
            reload_saved_data(window, males, females)
            if all_filled(males) and all_filled(females):
                print('Hooray')
                print(males)
                print(females)
            else:
                sg.popup('There are missing candidates')
    window.close()

    # TODO:
    # - save data to file or something else
    # - save round data in variables/dictionary
    # -
