#!/usr/bin/env python3

import random
from collections import Counter

P = 0.75
PI1 = 0.7
PI2 = 0.65

TICKS = 1_000_00


class State:
    def __init__(self, channel1, queue, channel2):
        self.channel1 = channel1
        self.channel2 = channel2
        self.queue = queue

    def __str__(self):
        return 'P{}{}{}'.format(self.channel1, self.queue, self.channel2)


cnt = Counter()

Wc = 0
arrivals = []
arrivals_mean = []
income = 0
processed = 0
source_blocked = 0
Lqueue = 0

state = State(0, 0, 0)

for tick in range(TICKS):

    arrival = True if random.uniform(0.0, 1) > P else False
    first_can_service = True if random.uniform(0.0, 1) > PI1 else False
    second_can_service = True if random.uniform(0.0, 1) > PI2 else False

    if state.channel2 == 1:
        if second_can_service:
            state.channel2 = 0
            processed += 1
            arrivals_mean.append(arrivals.pop())

    if state.queue != 0:
        if state.channel2 == 0:
            state.channel2 = 1
            state.queue -= 1

    if state.channel1 == 1:

        if first_can_service:
            if state.queue == 0 and state.channel2 == 0:
                state.channel1 = 0
                state.channel2 = 1
            elif state.queue < 2 and state.channel2 == 1:
                state.queue += 1
                state.channel1 = 0

    if arrival:
        income += 1
        if state.channel1 == 0:
            arrivals.append(0)
            state.channel1 = 1
        else:
            source_blocked += 1

    Lqueue += state.queue
    arrivals = [arrival +  1 for arrival in arrivals]

    cnt[str(state)] += 1

for k, v in sorted(cnt.items()):
    print('{}: {}'.format(k, v / TICKS))

print('Pотк.ист: {}'.format(source_blocked / TICKS))
print('Lоч: {}'.format(Lqueue / TICKS))
print('Wc: {}'.format(sum(arrivals_mean)/len(arrivals_mean)))
