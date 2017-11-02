#!/usr/bin/env python3

import sympy as sym
import re

p, pi1, pi2 = sym.var('p pi1 pi2')

P20000 = sym.Symbol('P20000')
P10000 = sym.Symbol('P10000')
P20001 = sym.Symbol('P20001')
P20010 = sym.Symbol('P20010')
P20011 = sym.Symbol('P20011')
P20101 = sym.Symbol('P20101')
P20111 = sym.Symbol('P20111')
P21010 = sym.Symbol('P21010')
P21011 = sym.Symbol('P21011')
P21111 = sym.Symbol('P21111')
P10001 = sym.Symbol('P10001')
P10010 = sym.Symbol('P10010')
P10011 = sym.Symbol('P10011')
P10101 = sym.Symbol('P10101')
P10111 = sym.Symbol('P10111')
P11010 = sym.Symbol('P11010')
P11011 = sym.Symbol('P11011')
P11111 = sym.Symbol('P11111')

with open('state_diagram.dot', 'r') as f:
    lines = f.read().splitlines()

lines = [line.strip() for line in lines]
import pdb
pdb.set_trace()
nodes = {}
for line in lines:

    if '->' not in line:
        continue

    right = 'P{}'.format(line.split('->')[1][1:6])
    left = line.split('->')[0]
    equation = re.findall(r'"([^"]*)"', line)[0]

    if not nodes.get(right):
        nodes[right] = 'P{} * ({})'.format(left, equation)
    else:
        nodes[right] += ' + P{} * ({})'.format(left, equation)


nodes.update((k, '{} - {}'.format(v, k)) for k, v in nodes.items())

nodes['P20000'] = ' + '.join(nodes.keys()) + '-1'

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
