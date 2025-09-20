from Model.Corrida import Corrida

class Motorista:
    def __init__(self,nota,corridas=[]):
        self.nota = nota
        self.corridas = corridas

    def to_dict(self):
        return {
            "nota": self.nota,
            "corridas": [corrida.to_dict() for corrida in self.corridas]
        }
