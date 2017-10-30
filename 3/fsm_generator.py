#!/usr/bin/env python3

import functools
import itertools
import re

with open('state_diagram.dot') as file:
    lines = file.read().splitlines()

states = [line.strip() for line in lines if '->' in line]

replacements = {'+': ' or ', '*': ' and '}

blocks = itertools.groupby(states, lambda s: s[:4])

condition_prefix = 'if'
fsm = []

for top, block in blocks:

    top_statement = '{} state == \'P{}\':'.format(condition_prefix, top)

    result = ''

    for statement in block:

        equation = re.findall(r'"([^"]*)"', statement)[0]

        without_operators = functools.reduce(
            lambda x, y: x.replace(y, replacements[y]), replacements, equation)
        cleaned = without_operators.replace('1-', ' not ').replace(
            '(', '').replace(')', '')

        if 'or' in cleaned:
            cleaned = cleaned.partition('or')
            cleaned = ' or '.join(['({})'.format(expression) for expression in cleaned if expression != 'or'])

        cleaned = ' '.join(cleaned.split())

        condition = ' ' * 4 + '{} {}:'.format(condition_prefix, cleaned)

        state = statement.split('->')[1].strip()[:4]

        transition = ' ' * 8 + 'state = State({}, {}, {}, {})'.format(*state)

        result += '\n'.join([condition, transition]) + '\n'

        condition_prefix = 'elif'

    fsm.append('\n'.join([top_statement, result]))

for line in fsm:
    print(line)
