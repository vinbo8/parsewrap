import sys
import subprocess
from parser import Parser

class UDPipe(Parser):
    def __init__(self):
        sys.stdout.write("Initialised UDPipe instance..\n")

    def run(self, conllu, *args, **kwargs):
        return super(UDPipe, self).run(conllu, **kwargs)

    def train(self, conllu, *args, **kwargs):
        proc = subprocess.Popen(["udpipe", "--train", "--tagger=none",
                                 "--tokenizer=none", "out.udpipe"],
                                stdin=subprocess.PIPE)

        # conllu is stdin; pipe to subprocess stdin
        for line in conllu:
            proc.stdin.write(line.encode('utf-8'))

        stdout, stderr = proc.communicate()
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stdout.write(stderr)

    def parse(self, conllu, *args, **kwargs):
        # mutability
        args = list(args)
        # convert to spacey stuff
        for kw in kwargs['extra']:
            args += kw.split("=")

        parser_args = ["udpipe", "--parse"] + args + [kwargs['model']]
        proc = subprocess.Popen(parser_args,
                                stdin=subprocess.PIPE)

        
        for line in conllu:
            proc.stdin.write(line.encode('utf-8'))

        stdout, stderr = proc.communicate()
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stdout.write(stderr)


    def eval(self, conllu, *args, **kwargs):
        args = list(args)
        args = args + ['--accuracy']
        self.parse(conllu, *args, **kwargs)

