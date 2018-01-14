#!/usr/bin/env python3

import random
import click
import numpy as np
from collections import defaultdict

from magic import plint

class Dummy:
    life = 0
    fir_q = 0
    sec_q = 0
    fir_ch = 0
    sec_ch = 0

    def tick(self):
        self.life += 1

class Machine:
    def __init__(self, pi1, pi2):
        self.PI1 = 1 - pi1
        self.PI2 = 1 - pi2
        self.generated = []
        self.processed = []
        self.generator = 2
        self.channel1 = None
        self.channel2 = None
        self.queue1 = None
        self.queue2 = None
        self.ticks = 0
        self.dropped = 0
        self.states = defaultdict(int)

    def step(self):

        state = "P"

        pi1 = True if random.uniform(0.0, 1) > self.PI1 else False
        pi2 = True if random.uniform(0.0, 1) > self.PI2 else False
        if self.generator == 1:
            state += '1'
        else:
            state += '2'

        if self.queue1:
            state += '1'
            self.queue1.tick()
            self.queue1.fir_q += 1
        else:
            state += '0'
        if self.queue2:
            state += '1'
            self.queue2.tick()
            self.queue2.sec_q += 1
        else:
            state += '0'
        if self.channel1:
            state += '1'
            self.channel1.tick()
            self.channel1.fir_ch += 1
        else:
            state += '0'
        if self.channel2:
            state += '1'
            self.channel2.tick()
            self.channel2.sec_ch += 1
        else:
            state += '0'

        self.states[state] += 1

        if self.channel2 and not pi2:
            self.processed.append(self.channel2)
            self.channel2 = None
        if self.queue2 and not self.channel2:
            self.channel2 = self.queue2
            self.queue2 = None
        if self.channel1 and not pi1:
            if not self.channel2:
                self.channel2 = self.channel1
            elif not self.queue2:
                self.queue2 = self.channel1
            self.channel1 = None
        if self.queue1 and not self.channel1:
            self.channel1 = self.queue1
            self.queue1 = None
        if self.generator == 2:
            self.generator = 1
        else:
            self.generator = 2
            self.generated.append(Dummy())
            if not self.channel1:
                self.channel1 = self.generated[-1]
            elif not self.queue1:
                self.queue1 = self.generated[-1]
            else:
                self.dropped += 1

TICKS = 100000

@click.command(help='Run Markov state machine')
@click.argument(
    'pi1', required=True, type=click.FLOAT, metavar='<first channel>')
@click.argument(
    'pi2', required=True, type=click.FLOAT, metavar='<second channel>')
def markov(pi1, pi2):

    machine = Machine(pi1, pi2)

    for _ in range(TICKS):
        machine.step()

    states = sorted(machine.states.keys())
    for state in states:
        print('{}: {}'.format(state, machine.states[state] / TICKS))

    print('Q: {}'.format(len(machine.processed) / len(machine.generated)))
    Lq1 = [i.fir_q for i in machine.generated if i.fir_q]
    Lq2 = [i.sec_q for i in machine.generated if i.sec_q]
    Lch1 = [i.fir_ch for i in machine.generated if i.fir_ch]
    Lch2 = [i.sec_ch for i in machine.generated if i.sec_ch]
    # Wq1 = np.array(Lq1).mean()
    # Wq2 = np.array(Lq2).mean()
    Wq1 = sum(Lq1) / (len(machine.generated) - machine.dropped)
    Wq2 = sum(Lq2) / len(machine.processed)
    Wch1 = np.array(Lch1).mean()
    Wch2 = np.array(Lch2).mean()
    Wc = Wq1 + Wq2 + Wch1 + Wch2
    # plint(pi1, pi2, Wc)
    print('Wc: {}'.format(Wc))
    print('A: {}'.format(len(machine.processed) / TICKS))
    print('Wq1: {}'.format(Wq1))
    print('Wq2: {}'.format(Wq2))
    print('Wch1: {}'.format(Wch1))
    print('Wch2: {}'.format(Wch2))

if __name__ == '__main__':
    markov()
