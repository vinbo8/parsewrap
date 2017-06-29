from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def train(self, conllu, **kwargs):
        pass
    
    @abstractmethod
    def parse(self, conllu, **kwargs):
        pass

    @abstractmethod
    def eval(self, conllu, **kwargs):
        pass

    @abstractmethod
    def run(self, conllu, **kwargs):
        if kwargs['train']:
            self.train(conllu, **kwargs)
        # no need to use elif, it oughtn't to reach here
        if kwargs['parse']:
            if kwargs['evaluate']:
                self.eval(conllu, **kwargs)
            else:
                self.parse(conllu, **kwargs)
           
