import sys
import argparse
from argparse import ArgumentParser
from parsewrap.parser import UDPipe, MaltParser

def main():
    parser_dict = {'udpipe': UDPipe, 'maltparser': MaltParser}

    p = ArgumentParser()
    p.add_argument('-p', '--parser', required=True)
    p.add_argument('--train', action='store_true')
    p.add_argument('--parse', action='store_true')
    p.add_argument('--evaluate', action='store_true')
    p.add_argument('model')
    p.add_argument('extra', nargs=argparse.REMAINDER)
    args = p.parse_args()

    # handling shitty errors
    if not args.train ^ args.parse:
        raise SyntaxError("Dodgy args mate")

    # get parser type
    try:
        parser = parser_dict[args.parser]
    except:
        raise SyntaxError("Dodgy parser mate")
    
    u = parser() 
    u.run(sys.stdin, **vars(args))

