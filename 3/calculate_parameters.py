#!/usr/bin/env python3

import sympy as sym
import re

p, pi1, pi2 = sym.var('p pi1 pi2')

P0000 = sym.Symbol('P0000')
P0001 = sym.Symbol('P0001')
P0011 = sym.Symbol('P0011')
P0021 = sym.Symbol('P0021')
P0100 = sym.Symbol('P0100')
P0101 = sym.Symbol('P0101')
P0111 = sym.Symbol('P0111')
P0121 = sym.Symbol('P0121')
P0221 = sym.Symbol('P0221')
P1100 = sym.Symbol('P1100')
P1101 = sym.Symbol('P1101')
P1111 = sym.Symbol('P1111')
P1121 = sym.Symbol('P1121')
P1221 = sym.Symbol('P1221')

with open('state_diagram.dot', 'r') as f:
    lines = f.read().splitlines()

lines = [line.strip() for line in lines]

nodes = {}
for line in lines:

    if '->' not in line:
        continue

    right = 'P{}'.format(line.split('->')[1][1:5])
    left = line.split('->')[0]
    equation = re.findall(r'"([^"]*)"', line)[0]

    if not nodes.get(right):
        nodes[right] = 'P{} * ({})'.format(left, equation)
    else:
        nodes[right] += ' + P{} * ({})'.format(left, equation)


nodes.update((k, '{} - {}'.format(v, k)) for k, v in nodes.items())

nodes['P0000'] = ' + '.join(nodes.keys()) + '-1'

equations = [
    sym.sympify(expr).subs({
        p: 0.75,
        pi1: 0.7,
        pi2: 0.65
    }) for expr in nodes.values()
]

result = sym.solve(equations, list(nodes.keys()))

p = 0.75
pi1 = 0.7
pi2 = 0.65

Pblock = sum([v for k, v in result.items() if str(k)[1] == '1'])
Pblockpi1 = sum([v for k, v in result.items() if str(k)[2] == '2'])

Lqueue = 1 * sum([v for k, v in result.items() if str(k)[3] == '1']) + 2 * sum(
    [v for k, v in result.items() if str(k)[3] == '2'])

Lc = Lqueue + sum([v for k, v in result.items() if str(k)[2] != '0']) + sum(
    [v for k, v in result.items() if str(k)[4] == '1'])

Wc = Lc / ((1 - p) * (1 - Pblock))

for pair in sorted(result.items(), key=str):
    print('{}: {}'.format(*pair))
print('Pblocked: {}'.format(Pblock))
print('Lqueue: {}'.format(Lqueue))
print('Wc: {}'.format(Wc))
