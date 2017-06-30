import sys
import re
import subprocess
from parser import Parser

class MaltParser(Parser):
    def __init__(self):
        super().__init__()
        self.path = self.cp.get('maltparser', 'path')

        # make this customisable
        self.feature_path = re.sub(r'/[^/]*$', '', self.path) + '/appdata/features/liblinear/conllu/NivreEager.xml'
        sys.stdout.write("Initialised MaltParser instance..\n")

    def run(self, conllu, *args, **kwargs):
        return super(MaltParser, self).run(conllu, **kwargs)

    def train(self, conllu, *args, **kwargs):
        with open(".temp", "w") as f:
            for line in conllu:
                f.write(line)
        
        proc = subprocess.Popen(['java', '-jar', self.path,
                                 '-c', kwargs['model'], '-i',
                                 '.temp', '-if', 'conllu',
                                 '-F', self.feature_path,
                                 '-m', 'learn'])

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

