from Database import Database
from bson.objectid import ObjectId
from Model.Motorista import Motorista

class MotoristaDAO:
    def __init__(self, db: Database):
        self.db = db
        
    def create_motorista(self, motorista: Motorista):
        try:
            result = self.db.collection.insert_one(motorista.to_dict())
            motorista_id = result.inserted_id
            print("Motorista criado com sucesso! ID: ", motorista_id)
            return motorista_id
        except Exception as e:
            print("Erro ao criar motorista: ", e)
            return None
        
    def read_motorista_by_id(self, motorista_id):
        try:
            motorista = self.db.collection.find_one({"_id": ObjectId(motorista_id)})
            if motorista:
                print("Motorista encontrado: ", motorista)
                return motorista
            else:
                print("Motorista não encontrado")
                return None
        except Exception as e:
            print("Erro ao encontrar motorista: ", e)
            return None
        
    def update_motorista(self, motorista_id, motorista):
        try:
            result = self.db.collection.update_one({"_id": ObjectId(motorista_id)}, {"$set": motorista})
            if result.modified_count:
                print(f"Motorista {motorista_id} atualizado com sucesso!")
                return True
            else:
                print("Motorista não encontrado")
                return False
        except Exception as e:
            print("Erro ao atualizar motorista: ", e)
            return False
        
    def delete_motorista(self, motorista_id):
        try:
            result = self.db.collection.delete_one({"_id": ObjectId(motorista_id)})
            if result.deleted_count:
                print(f"Motorista {motorista_id} deletado com sucesso!")
                return True
            else:
                print("Motorista não encontrado")
                return False
        except Exception as e:
            print("Erro ao deletar motorista: ", e)
            return False
        
    