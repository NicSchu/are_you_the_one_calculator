class Round:
    def __init__(self, num, _values, males, females):
        self.round_num = num
        self.truth_booth_pair = [_values['tb%d-m' % num], _values['tb%d-m' % num]]
        self.is_truth_booth_match = _values['match_%d' % num]
        self.is_truth_booth_set = self.truth_booth_pair.count('') == 0

        self.pairs = []
        self.beams = int(_values['beams_%d' % num])
        for i in range(1, 11):
            if num % 2 == 1:
                self.pairs.append([_values['mn%d-m%d' % (num, i)], females[i-1]])
            else:
                self.pairs.append([males[i-1], _values['mn%d-f%d' % (num, i)]])
        self.is_round_complete = sum(list(map(lambda pair: pair.count(''), self.pairs))) == 0
