class Passageiro:
    def __init__(self,nome,documento):
        self.nome = nome
        self.documento = documento

    def to_dict(self):
        return{
            "nome": self.nome,
            "documento": self.documento
        }