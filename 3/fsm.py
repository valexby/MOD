#!/usr/bin/env python3

import random
from collections import Counter
from time import sleep
import click
import numpy as np

TICKS = 100000

class State:
    def __init__(self, source, queue1, queue2, channel1, channel2):
        self.source = source
        self.channel1 = channel1
        self.channel2 = channel2
        self.queue1 = queue1
        self.queue2 = queue2

    def __str__(self):
        return 'P{}{}{}{}{}'.format(self.source, self.queue1, self.queue2,
                                    self.channel1, self.channel2)

    def __eq__(self, other):
        return str(self) == other

state = State(2, 0, 0, 0, 0)
cnt = Counter()

processed = 0
generated = 0
system = []
times = [0, 0, 0, 0]
total_times = []

@click.command(help='Run Markov state machine')
@click.argument(
    'pi1', required=True, type=click.FLOAT, metavar='<first channel>')
@click.argument(
    'pi2', required=True, type=click.FLOAT, metavar='<second channel>')
def markov(pi1, pi2):

    PI1 = 1 - pi1
    PI2 = 1 - pi2

    for _ in range(TICKS):
        fsm(PI1, PI2)

    for k, v in sorted(cnt.items()):
        print('{}: {}'.format(k, v / TICKS))

    print('Q: {}'.format(processed / generated))
    print('Wc: {}'.format(np.array(total_times).mean()))
    print('A: {}'.format(processed / TICKS))


def fsm(PI1, PI2):

    global state, processed, generated, system, times, total_times

    pi1 = True if random.uniform(0.0, 1) > PI1 else False
    pi2 = True if random.uniform(0.0, 1) > PI2 else False

    cnt[str(state)] += 1
    if state.channel2 == 1 and not pi2:
        processed += 1
    if state.source == 1:
        generated += 1

    system.append(state.channel1 + state.channel2 + state.queue1 + state.queue2)

    if state == 'P20000':
        state = State(1, 0, 0, 0, 0)

    elif state == 'P10000':
        times[0] = 1
        state = State(2, 0, 0, 1, 0)

    elif state == 'P20010':
        if pi1:
            times[0] += 1
            state = State(1, 0, 0, 1, 0)
        elif not pi1:
            times[1] = times[0] + 1
            times[0] = 0
            state = State(1, 0, 0, 0, 1)

    elif state == 'P20011':
        if pi1 and pi2:
            times[0] += 1
            times[1] += 1
            state = State(1, 0, 0, 1, 1)
        elif not pi1 and pi2:
            times[3] = times[0] + 1
            times[0] = 0
            state = State(1, 0, 1, 0, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = 0
            times[0] += 1
            state = State(1, 0, 0, 1, 0)
        elif not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[0] + 1
            times[0] = 0
            state = State(1, 0, 0, 0, 1)

    elif state == 'P20111':
        if pi1 and pi2:
            times[0] += 1
            times[1] += 1
            times[3] += 1
            state = State(1, 0, 1, 1, 1)
        elif not pi1 and pi2:
            times[1] += 1
            times[3] += 1
            times[0] = 0
            state = State(1, 0, 1, 0, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = 0
            times[0] += 1
            state = State(1, 0, 0, 1, 1)
        elif not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = times[0] + 1
            times[0] = 0
            state = State(1, 0, 1, 0, 1)

    elif state == 'P21010':
        if pi1:
            times[0] += 1
            times[2] += 1
            state = State(1, 1, 0, 1, 0)
        elif not pi1:
            times[1] = times[0] + 1
            times[0] = times[2] + 1
            times[2] = 0
            state = State(1, 0, 0, 1, 1)

    elif state == 'P21011':
        if pi1 and pi2:
            times[2] += 1
            times[0] += 1
            times[1] += 1
            state = State(1, 1, 0, 1, 1)
        elif not pi1 and pi2:
            times[1] += 1
            times[3] += times[0] + 1
            times[0] = 1
            state = State(1, 0, 1, 1, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = 0
            times[2] += 1
            times[0] += 1
            state = State(1, 1, 0, 1, 0)
        elif not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[0] + 1
            times[0] = times[2] + 1
            times[2] = 0
            state = State(1, 0, 0, 1, 1)

    elif state == 'P21111':
        if pi1 and pi2:
            times = [x + 1 for x in times]
            state = State(1, 1, 1, 1, 1)
        elif not pi1 and pi2:
            times[1] += 1
            times[3] += 1
            times[2] = 0
            times[0] += 1
            state = State(1, 0, 1, 1, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = 0
            times[2] += 1
            times[0] += 1
            state = State(1, 1, 0, 1, 1)
        elif not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = times[0] + 1
            times[0] = times[2] + 1
            times[2] = 0
            state = State(1, 0, 1, 1, 1)

    elif state == 'P10001':
        times[0] = 1
        if pi2:
            times[1] += 1
            state = State(2, 0, 0, 1, 1)
        elif not pi2:
            total_times.append(times[1])
            times[1] = 0
            state = State(2, 0, 0, 1, 0)

    elif state == 'P10010':
        if pi1:
            times[0] += 1
            times[2] = 1
            state = State(2, 1, 0, 1, 0)
        elif not pi1:
            times[1] = times[0] + 1
            times[0] = 1
            state = State(2, 0, 0, 1, 1)

    elif state == 'P10011':
        if pi1 and pi2:
            times[1] += 1
            times[0] += 1
            state = State(2, 1, 0, 1, 1)
        elif not pi1 and pi2:
            times[1] += 1
            times[3] = times[0] + 1
            times[0] = 1
            state = State(2, 0, 1, 1, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = 0
            times[0] += 1
            times[2] = 1
            state = State(2, 1, 0, 1, 0)
        elif not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[0] + 1
            times[0] = 1
            state = State(2, 0, 0, 1, 1)

    elif state == 'P10101':
        if pi2:
            times[1] += 1
            times[3] += 1
            times[0] = 1
            state = State(2, 0, 1, 1, 1)
        elif not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = 0
            times[0] = 1
            state = State(2, 0, 0, 1, 1)

    elif state == 'P10111':
        if pi1 and pi2:
            times[1] += 1
            times[0] += 1
            times[3] += 1
            times[2] = 1
            state = State(2, 1, 1, 1, 1)
        elif not pi1 and pi2:
            times[1] += 1
            times[3] += 1
            times[0] = 1
            state = State(2, 0, 1, 1, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = 0
            times[1] += 1
            times[2] = 1
            state = State(2, 1, 0, 1, 1)
        elif  not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = times[0] + 1
            times[0] = 1
            state = State(2, 0, 1, 1, 1)

    elif state == 'P11010':
        if pi1:
            times[0] += 1
            times[2] += 1
            state = State(2, 1, 0, 1, 0)
        elif not pi1:
            times[1] = times[0] + 1
            times[0] = times[2] + 1
            times[2] = 1
            state = State(2, 1, 0, 1, 1)

    elif state == 'P11011':
        if pi1 and pi2:
            times[1] += 1
            times[0] += 1
            times[2] += 1
            state = State(2, 1, 0, 1, 1)
        elif not pi1 and pi2:
            times[1] += 1
            times[3] = times[0] + 1
            times[0] = times[2] + 1
            times[2] = 1
            state = State(2, 1, 1, 1, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = 0
            times[0] += 1
            times[2] += 1
            state = State(2, 1, 0, 1, 0)
        elif not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[0] + 1
            times[0] = times[2] + 1
            times[2] = 1
            state = State(2, 1, 0, 1, 1)

    elif state == 'P11111':
        if pi1 and pi2:
            times = [x + 1 for x in times]
            state = State(2, 1, 1, 1, 1)
        elif not pi1 and pi2:
            times[1] += 1
            times[3] += 1
            times[0] = times[2] + 1
            times[2] = 1
            state = State(2, 1, 1, 1, 1)
        elif pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = 0
            times[0] += 1
            times[2] += 1
            state = State(2, 1, 0, 1, 1)
        elif not pi1 and not pi2:
            total_times.append(times[1])
            times[1] = times[3] + 1
            times[3] = times[0] + 1
            times[0] = times[2] + 1
            times[2] = 1
            state = State(2, 1, 1, 1, 1)

if __name__ == '__main__':
    markov()
