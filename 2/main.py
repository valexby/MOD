#!/usr/bin/env python3

import numpy as np
import matplotlib

matplotlib.rcParams['backend'] = "Qt4Agg"
import matplotlib.pyplot as plt
import click

N = 10000
R = np.random.uniform(0.0, 1.0, N)


@click.group()
def cli():
    pass


@cli.resultcallback()
def draw_plot(*args):

    print('Mean: {}'.format(np.mean(args)))
    print('Std: {}'.format(np.std(args)))
    print('Variance: {}'.format(np.std(args)**2))

    plt.hist(args, bins=50)
    plt.show()
#    plt.savefig('out.png', fmt='png')


@cli.command(help='Generate uniform distribution')
@click.argument('a', required=True, type=click.FLOAT, metavar='<left margin>')
@click.argument('b', required=True, type=click.FLOAT, metavar='<right margin>')
def uniform(a, b):

    uni = a + (b - a) * R

    return uni


@cli.command(help='Generate normal distribution')
@click.argument('mean', required=True, type=click.FLOAT)
@click.argument('std', required=True, type=click.FLOAT)
def norm(mean, std):

    normed = np.empty_like(R)
    for i in range(N):
        normed[i] = mean + std * np.sqrt(2) * (sum(np.random.choice(R, 6)) - 3)

    return normed


@cli.command(help='Generate exponential distribution')
@click.argument('l', required=True, type=click.FLOAT)
def exponential(l):

    exp = -1 / l * np.log(R)

    return exp


@cli.command(help='Generate erlang distribution')
@click.argument('eta', required=True, type=click.INT)
@click.argument('l', required=True, type=click.FLOAT)
def erlang(eta, l):

    gamma = np.empty_like(R)
    for i in range(N):
        gamma[i] = (-1 / l) * np.log(np.prod(np.random.choice(R, eta)))

    return gamma


@cli.command(help='Generate triangular distribution')
@click.argument('a', required=True, type=click.FLOAT)
@click.argument('b', required=True, type=click.FLOAT)
@click.argument('pdf', required=True, default='down')
def triangular(a, b, pdf):

    f = max if pdf == 'up' else min

    triang = np.empty_like(R)
    for i in range(N):
        triang[i] = a + (b - a) * f(np.random.choice(R, 2))

    return triang


@cli.command(help='Generate simpson distribution')
@click.argument('a', required=True, type=click.FLOAT)
@click.argument('b', required=True, type=click.FLOAT)
def simpson(a, b):

    simp = np.empty_like(R)
    for i in range(N):
        simp[i] = sum(np.random.uniform(a / 2, b / 2, 2))

    return simp


if __name__ == '__main__':
    cli()
