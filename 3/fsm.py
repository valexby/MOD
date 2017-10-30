#!/usr/bin/env python3

import random
from collections import Counter


class State:
    def __init__(self, source, channel1, queue, channel2):
        self.source = source
        self.channel1 = channel1
        self.channel2 = channel2
        self.queue = queue

    def __str__(self):
        return 'P{}{}{}{}'.format(self.source, self.channel1, self.queue,
                                  self.channel2)

    def __eq__(self, other):
        return str(self) == other


P = 0.25
PI1 = 0.3
PI2 = 0.35
TICKS = 100000

state = State(0, 0, 0, 0)
cnt = Counter()

source_blocked = 0
channel_blocked = 0
queue = 0
system = 0


def fsm():

    global state, source_blocked, channel_blocked, queue, system

    p = True if random.uniform(0.0, 1) > P else False
    pi1 = True if random.uniform(0.0, 1) > PI1 else False
    pi2 = True if random.uniform(0.0, 1) > PI2 else False

    cnt[str(state)] += 1

    queue += state.queue

    if state == 'P0000':
        system += 1
        if p:
            state = State(0, 0, 0, 0)
        elif not p:
            state = State(0, 1, 0, 0)

    elif state == 'P0100':
        system += 1
        if not p and not pi1:
            state = State(0, 1, 0, 1)
        elif p and not pi1:
            state = State(0, 0, 0, 1)
        elif p and pi1:
            state = State(0, 1, 0, 0)
        elif not p and pi1:
            state = State(1, 1, 0, 0)

    elif state == 'P1100':
        system += 1
        source_blocked += 1
        if pi1:
            state = State(1, 1, 0, 0)
        elif not pi1:
            state = State(0, 1, 0, 1)

    elif state == 'P0001':
        system += 1
        if p and not pi2:
            state = State(0, 0, 0, 0)
        elif p and pi2:
            state = State(0, 0, 0, 1)
        elif not p and not pi2:
            state = State(0, 1, 0, 0)
        elif not p and pi2:
            state = State(0, 1, 0, 1)

    elif state == 'P0101':
        system += 1
        if p and pi1 and not pi2:
            state = State(0, 1, 0, 0)
        elif not p and not pi1 and pi2:
            state = State(0, 1, 1, 1)
        elif (p and pi1 and pi2) or (not p and not pi1 and not pi2):
            state = State(0, 1, 0, 1)
        elif p and not pi1 and not pi2:
            state = State(0, 0, 0, 1)
        elif p and not pi1 and pi2:
            state = State(0, 0, 1, 1)
        elif not p and pi1 and pi2:
            state = State(1, 1, 0, 1)
        elif not p and pi1 and not pi2:
            state = State(1, 1, 0, 0)

    elif state == 'P1101':
        system += 1
        source_blocked += 1
        if pi1 and not pi2:
            state = State(1, 1, 0, 0)
        elif pi1 and pi2:
            state = State(1, 1, 0, 1)
        elif not pi1 and not pi2:
            state = State(0, 1, 0, 1)
        elif not pi1 and pi2:
            state = State(0, 1, 1, 1)

    elif state == 'P0111':
        system += 2
        if p and not pi1 and not pi2:
            state = State(0, 0, 1, 1)
        elif p and pi1 and not pi2:
            state = State(0, 1, 0, 1)
        elif not p and not pi1 and pi2:
            state = State(0, 1, 2, 1)
        elif (not p and not pi1 and not pi2) or (p and pi1 and pi2):
            state = State(0, 1, 1, 1)
        elif p and not pi1 and pi2:
            state = State(0, 0, 2, 1)
        elif not p and pi1 and pi2:
            state = State(1, 1, 1, 1)
        elif not p and pi1 and not pi2:
            state = State(1, 1, 0, 1)

    elif state == 'P1111':
        system += 2
        source_blocked += 1
        if not pi1 and pi2:
            state = State(0, 1, 2, 1)
        elif pi1 and not pi2:
            state = State(1, 1, 0, 1)
        elif not pi1 and not pi2:
            state = State(0, 1, 1, 1)
        elif pi1 and pi2:
            state = State(1, 1, 1, 1)

    elif state == 'P0011':
        system += 2
        if p and pi2:
            state = State(0, 0, 1, 1)
        elif not p and pi2:
            state = State(0, 1, 1, 1)
        elif p and not pi2:
            state = State(0, 0, 0, 1)
        elif not p and not pi2:
            state = State(0, 1, 0, 1)

    elif state == 'P0121':
        system += 3
        if p and pi1 and not pi2:
            state = State(0, 1, 1, 1)
        elif (p and pi1 and pi2) or (not p and not pi1 and not pi2):
            state = State(0, 1, 2, 1)
        elif p and not pi1 and not pi2:
            state = State(0, 0, 2, 1)
        elif p and not pi1 and pi2:
            state = State(0, 2, 2, 1)
        elif not p and pi1 and not pi2:
            state = State(1, 1, 1, 1)
        elif not p and pi1 and pi2:
            state = State(1, 1, 2, 1)
        elif not p and not pi1 and pi2:
            state = State(1, 2, 2, 1)

    elif state == 'P0221':
        system += 3
        channel_blocked += 1
        if not pi1 and not pi2:
            state = State(0, 1, 2, 1)
        elif p and pi2:
            state = State(0, 2, 2, 1)
        elif p and not pi2:
            state = State(0, 0, 2, 1)
        elif not p and pi2:
            state = State(1, 2, 2, 1)

    elif state == 'P1121':
        system += 3
        source_blocked += 1
        if pi1 and pi2:
            state = State(1, 1, 2, 1)
        elif not pi1 and pi2:
            state = State(1, 2, 2, 1)
        elif pi1 and not pi2:
            state = State(1, 1, 1, 1)
        elif not pi1 and not pi2:
            state = State(0, 1, 2, 1)

    elif state == 'P1221':
        system += 3
        source_blocked += 1
        channel_blocked += 1
        if pi2:
            state = State(1, 2, 2, 1)
        elif not pi2:
            state = State(0, 1, 2, 1)

    elif state == 'P0021':
        system += 3
        if p and pi2:
            state = State(0, 0, 2, 1)
        elif not p and pi2:
            state = State(0, 1, 2, 1)
        elif not p and not pi2:
            state = State(0, 1, 1, 1)
        elif p and not pi2:
            state = State(0, 0, 1, 1)


for _ in range(TICKS):
    fsm()

for k, v in sorted(cnt.items()):
    print('{}: {}'.format(k, v / TICKS))

Pblocked = source_blocked / TICKS
Pchannel = channel_blocked / TICKS

print('Pblocked: {}'.format(source_blocked / TICKS))
print('Lqueue: {}'.format(queue / TICKS))
print('Wc: {}'.format((system / TICKS) / ((P) * (1 - Pblocked - Pchannel))))
