#!/usr/bin/env python3

import sympy as sym
import re

p, pi1, pi2 = sym.var('p pi1 pi2')

P000 = sym.Symbol('P000')
P100 = sym.Symbol('P100')
P001 = sym.Symbol('P001')
P101 = sym.Symbol('P101')
P111 = sym.Symbol('P111')
P011 = sym.Symbol('P011')
P121 = sym.Symbol('P121')
P021 = sym.Symbol('P021')

with open('state_diagram.dot', 'r') as f:
    lines = f.read().splitlines()

lines = [line.strip() for line in lines]

nodes = {}
for line in lines:

    if '->' not in line:
        continue

    right = 'P{}'.format(line.split('->')[1][1:4])
    left = line.split('->')[0]
    equation = re.findall(r'"([^"]*)"', line)[0]

    if not nodes.get(right):
        nodes[right] = 'P{} * ({})'.format(left, equation)
    else:
        nodes[right] += ' + P{} * ({})'.format(left, equation)

nodes.update((k, '{} - {}'.format(v, k)) for k, v in nodes.items())

nodes['P011'] = ' + '.join(nodes.keys()) + '-1'

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

Pblock = (
    1 - p) * pi1 * sum([v for k, v in result.items() if str(k)[1] == '1'])
Pblockpi1 = pi2 * (result[P121] + result[P021])

Lqueue = 1 * (result[P111] + result[P011]) + 2 * (result[P021] + result[P121])

Wc = 1 / (1 - p) * (1 - Pblock - Pblockpi1)



for pair in sorted(result.items(), key=str):
    print('{}: {}'.format(*pair))
print('Pбл.ист: {}'.format(Pblock))
print('Lоч: {}'.format(Lqueue))
print('Wc: {}'.format(Wc))
