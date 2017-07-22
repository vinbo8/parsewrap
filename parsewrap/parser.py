import sys
import re
import subprocess
import configparser
import os
import shutil
from abc import ABC, abstractmethod
from parsewrap.helpers import evaluate

class Parser(ABC):
    def __init__(self):
        module_dir = os.path.dirname(__file__)
        self.cp = configparser.ConfigParser()
        self.cp.read(os.path.join(os.path.expanduser('~'), '.config',
                                  'parsewrap', 'paths.conf'))

    def train(self, conllu, **kwargs):
        raise NotImplementedError
    
    def parse(self, conllu, **kwargs):
        raise NotImplementedError

    def eval(self, conllu, **kwargs):
        raise NotImplementedError

    def run(self, conllu, **kwargs):
        if kwargs['train']:
            self.train(conllu, **kwargs)
        # no need to use elif, it oughtn't to reach here
        if kwargs['parse']:
            if kwargs['evaluate']:
                self.eval(conllu, **kwargs)
            else:
                self.parse(conllu, **kwargs)
           
class MaltParser(Parser):
    def __init__(self):
        super().__init__()
        self.path = self.cp.get('maltparser', 'path')

        # make this customisable
        self.feature_path = re.sub(r'/[^/]*$', '', self.path) + '/appdata/features/liblinear/conllu/NivreEager.xml'
        sys.stderr.write("Initialised MaltParser instance..\n")

    def run(self, conllu, *args, **kwargs):
        return super(MaltParser, self).run(conllu, **kwargs)

    def train(self, conllu, *args, **kwargs):
        with open(".temp", "w") as f:
            for line in conllu:
                f.write(line)
        
        proc =  subprocess.Popen(['java', '-Xmx2000M', '-jar', self.path,
                                  '-c', '.temp.model', '-i',
                                  '.temp', '-if', 'conllu',
                                  '-F', self.feature_path,
                                  '-m', 'learn'])

        stdout, stderr = proc.communicate()
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stdout.write(stderr)

        # cleanup
        shutil.move('.temp.model.mco', os.path.join(os.getcwd(),
                                                    kwargs['model']))
        os.remove('.temp')

    def parse(self, conllu, *args, **kwargs):
        # mutability
        args = list(args)
        # convert to spacey stuff
        for kw in kwargs['extra']:
            args += kw.split("=")

        # write stdin to file
        with open(".temp", "w") as f:
            for line in conllu:
                f.write(line)

        shutil.copy(os.path.join(os.getcwd(),
                                 kwargs['model']),
                    '.temp.model.mco')
        parser_args = ['java', '-jar', self.path,
                       '-c', '.temp.model', '-i',
                       '.temp', '-o', '.temp_out',
                       '-m', 'parse']

        proc = subprocess.Popen(parser_args)

        stdout, stderr = proc.communicate()
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stdout.write(stderr)

        with open('.temp_out', 'r') as f:
            # evaluate
            if kwargs['evaluate']:
                uas, las = evaluate('.temp', '.temp_out')
                sys.stdout.write("LAS: {:.2f}; UAS: {:.2f}\n".format(las, uas))

            # write file to stdout
            else:
                for line in f:
                    sys.stdout.write(line)

        # cleanup
        os.remove('.temp.model.mco')
        os.remove('.temp')
        os.remove('.temp_out')

    def eval(self, conllu, *args, **kwargs):
        kwargs['eval'] = True
        self.parse(conllu, *args, **kwargs)

class UDPipe(Parser):
    def __init__(self):
        super().__init__()
        self.path = self.cp.get('udpipe', 'path')
        sys.stderr.write("Initialised UDPipe instance..\n")

    def run(self, conllu, *args, **kwargs):
        return super(UDPipe, self).run(conllu, **kwargs)

    def train(self, conllu, *args, **kwargs):
        proc = subprocess.Popen([self.path, "--train", "--tagger=none",
                                 "--tokenizer=none",
                                 os.path.join(os.getcwd(), kwargs['model'])],
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

        parser_args = [self.path, "--parse"] + args + [os.path.join(os.getcwd(),
                                                                   kwargs['model'])]
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

