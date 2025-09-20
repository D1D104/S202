from Model.Corrida import Corrida
from Model.Motorista import Motorista
from Model.Passageiro import Passageiro
from MotoristaDAO import MotoristaDAO

class MotoristaCLI:
    def __init__(self, dao: MotoristaDAO):
        self.dao = dao
        
    def menu(self):
        opcao = input("Escolha uma opção: \n"
                      "[1] - Create \n[2] - Read \n[3] - Update \n[4] - Delete \n")
        
        if opcao == "1":
            self.create()
        elif opcao == "2":
            self.read()
        elif opcao == "3":
            self.update()
        elif opcao == "4":
            self.delete()
        else:
            print("Opção inválida")
    
    def create(self):
        print("Cadastre um passageiro primeiro:")
        nome = input("Nome: ")
        documento = input("Documento: ")
        passageiro = Passageiro(nome, documento)
        aux = 1
        corridas = []
        while aux == 1:
            print("Cadastre uma corrida:")
            nota = float(input("Nota: "))
            distancia = float(input("Distância: "))
            valor = float(input("Valor: "))
            corrida = Corrida(nota, distancia, valor, passageiro)
            corridas.append(corrida)
            aux = int(input("Deseja cadastrar outra corrida? [1] - Sim [2] - Não \n"))
            nota = float(input("Nota do motorista: "))
            motorista = Motorista(nota, corridas)
        self.dao.create_motorista(motorista)
    
    def read(self):
        id = input("id do motorista a ser buscado: ")
        motorista = self.dao.read_motorista_by_id(id)
    
    def update(self):
        id = input("id do motorista a ser atualizado: ")
        motorista = self.dao.read_motorista_by_id(id)
        if motorista:
            nota = float(input("Nova nota: "))
            motorista["nota"] = nota
            self.dao.update_motorista(id, motorista)

    def delete(self):
        id = input("id do motorista a ser deletado: ")
        self.dao.delete_motorista(id)
        
    def start(self):
        while True:
            self.menu()
            aux = input("Deseja continuar no programa? [1] - Sim [2] - Não \n")
            if aux == 2:
                break
            else:
                continue