import sys
import argparse
from argparse import ArgumentParser
from udpipe import UDPipe

p = ArgumentParser()
p.add_argument('--train', action='store_true')
p.add_argument('--parse', action='store_true')
p.add_argument('--evaluate', action='store_true')
p.add_argument('model')
p.add_argument('extra', nargs=argparse.REMAINDER)
args = p.parse_args()

# handling shitty errors
if not args.train ^ args.parse:
    raise SyntaxError("Dodgy args mate")

u = MaltParser()
u.run(sys.stdin, **vars(args))

