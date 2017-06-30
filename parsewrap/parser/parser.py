import configparser
from abc import ABC, abstractmethod

class Parser(ABC):
    def __init__(self):
        self.cp = configparser.ConfigParser()
        self.cp.read("../config/paths.conf")

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
           
