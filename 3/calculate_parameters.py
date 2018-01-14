#!/usr/bin/env python3

import sympy as sym
import re

p, pi1, pi2 = sym.var('p pi1 pi2')

P20000 = sym.Symbol('P20000')
P10000 = sym.Symbol('P10000')
P20010 = sym.Symbol('P20010')
P20011 = sym.Symbol('P20011')
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

for i in sorted(nodes.keys()):
    print('{} = {}'.format(i, nodes[i]))
good_keys = [x for x in nodes.keys() if x[1] == '1']
nodes['P20000'] = ' + '.join(nodes.keys()) + '-1'

equations = [
    sym.sympify(expr).subs({
        pi1: 0.5,
        pi2: 0.6
    }) for expr in nodes.values()
]

result = sym.solve(equations, list(nodes.keys()))

nodes['P20000'] = ' + '.join(good_keys) + '-1'
equations = [
    sym.sympify(expr).subs({
        pi1: 0.5,
        pi2: 0.6
    }) for expr in nodes.values()
]

result2 = sym.solve(equations, list(nodes.keys()))

pi1 = 0.5
pi2 = 0.6

LAMBDA = 0.5

A = sum([v for k, v in result.items() if str(k)[5] == '1']) * (1 - pi2)

Q = A / LAMBDA

Lqueue = sum([v for k, v in result.items() if str(k)[2] == '1']) + \
         sum([v for k, v in result.items() if str(k)[3] == '1'])
Lq1 = sum([v for k, v in result.items() if str(k)[2] == '1'])
Lq2 = sum([v for k, v in result.items() if str(k)[3] == '1'])
Lpi1 = sum([v for k, v in result.items() if str(k)[4] == '1'])
Lpi2 = sum([v for k, v in result.items() if str(k)[5] == '1'])

Lc = Lqueue + sum([v for k, v in result.items() if str(k)[4] == '1']) + \
     sum([v for k, v in result.items() if str(k)[5] == '1'])
Pdrop = sum([v for k, v in result2.items() if str(k)[1] == '1' and str(k)[2] == '1'and str(k)[4] == '1']) * (1-pi1)
Qsource = 1 - Pdrop
Asource = Qsource * LAMBDA

Wq1 = (Lq1) / Asource
Wq2 = Lq2 / A
Wch1 = 1 / (1 - pi1)
Wch2 = 1 / (1 - pi2)
Wc =  Wq1 + Wq2 + Wch1 + Wch2
#Wc =  (Q/(1-pi1)) + (Lq2/A) + (Lq1/LAMBDA) + (Q/(1-pi2))
for pair in sorted(result2.items(), key=str):
    print('{}: {}'.format(*pair))
print('Q: {}'.format(Q))
print('Wc: {}'.format(Wc))
print('A: {}'.format(A))
print('Lq: {}'.format(Lqueue))
print('Pdrop: {}'.format(Pdrop))
print('Qsource: {}'.format(Qsource))
print('Asource: {}'.format(Asource))
print('Wq1: {}'.format(Wq1))
print('Wq2: {}'.format(Wq2))
print('Wch1: {}'.format(Wch1))
print('Wch2: {}'.format(Wch2))
