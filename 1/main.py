#!/usr/bin/env python3

import numpy as np
import math
import click
import matplotlib.pyplot as plt
from scipy import stats

N = 15_000_0


def lcg(a, modulus, seed):
    while True:
        seed = a * seed % modulus
        yield seed / modulus


@click.command()
@click.option('-a', default=134775813, help='a coefficient')
@click.option('-m', default=2**32 - 1, help='modulus')
@click.option('-s', default=12345, help='seed')
def main(a, m, s):

    rand = lcg(a, m, s)

    numbers = np.fromiter(rand, dtype=np.float32, count=N)

    print('A: {}'.format(a))
    print('Modulus: {}'.format(m))
    print('Seed: {}'.format(s))
    print('Mean: {}'.format(np.mean(numbers)))
    print('Variance: {}'.format(np.var(numbers, ddof=1)))
    print('Std: {}'.format(np.std(numbers, ddof=1)))

    pairs = zip(numbers[::2], numbers[1::2])

    K = 0
    for pair in pairs:
        x1, x2 = pair
        if x1 * x1 + x2 * x2 < 1:
            K += 1

    print('Indirect assessment: {}'.format((2 * K) / N - np.pi / 4))

    xv = numbers[-1]
    index1 = index2 = -1
    for i in range(N):
        if math.isclose(numbers[i], xv):
            if index1 == -1:
                index1 = i
            elif index2 == -1:
                index2 = i
                break

    period = (index2 if index2 != -1 else N - 1) - index1
    print('Period: {}'.format(period))

    index1 = index2 = 0

    for i in range(N - period):
        if math.isclose(numbers[i], numbers[i + period]):
            index1 = i
            break

    for i in range(period, N - period):
        if math.isclose(numbers[i], numbers[i + period]):
            index2 = i
            break

    aperiodic = min(index1, index2) + period

    print('La: {}'.format(aperiodic))

    plt.hist(numbers, bins=20, normed=True, edgecolor='w')
    plt.savefig("out.png", fmt='png')


if __name__ == '__main__':
    main()
