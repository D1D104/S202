class TeacherCRUD():
    def __init__(self, db):
        self.db = db

    def create(self, name, ano_nasc, cpf):
        query = f"CREATE (t:Teacher {{name: '{name}', ano_nasc: {ano_nasc}, cpf: '{cpf}'}})"
        self.db.execute_query(query)

    def read(self, name):
        query = f"MATCH (t:Teacher) WHERE t.name = '{name}' RETURN t.name, t.ano_nasc, t.cpf"
        return self.db.execute_query(query)

    def update(self, name, newCpf):
        query = f"MATCH (t:Teacher) WHERE t.name = '{name}' SET t.cpf = '{newCpf}'"
        self.db.execute_query(query)
    
    def delete(self, name):
        query = f"MATCH (t:Teacher) WHERE t.name = '{name}' DETACH DELETE t"
        self.db.execute_query(query)