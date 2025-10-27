from database import Database

db = Database("bolt://18.204.243.124:7687", "neo4j", "copper-velocities-runaways")

class Query:
    def __init__(self, db):
        self.db = db

    #1-a
    def getRenzo(self):
        query = "MATCH (t:Teacher {name: 'Renzo'}) RETURN t.ano_nasc, t.cpf"
        return self.db.execute_query(query)

    #b
    def getStartsWithM(self):
        query = "MATCH (t:Teacher) WHERE t.name STARTS WITH 'M' RETURN t.name, t.cpf"
        return self.db.execute_query(query)

    #c
    def getAllCities(self):
        query = "MATCH (c:City) RETURN c.name"
        return self.db.execute_query(query)
    #d
    def getSchoolWithNumber(self):
        query = "MATCH (s:School) WHERE s.number >= 150 AND s.number <= 550 RETURN s.name, s.address, s.number"
        return self.db.execute_query(query)

    #2-a
    def getYoungestAndOldestTeacher(self):
        query = "MATCH (t:Teacher) RETURN min(t.ano_nasc), max(t.ano_nasc)"
        return self.db.execute_query(query)
    
    #b
    def getPopulationAverage(self):
        query = "MATCH (c:City) RETURN avg(c.population)"
        return self.db.execute_query(query)
    
    #c
    def getCityandSubstitute(self):
        query = "MATCH (c:City) WHERE c.cep = '37540-000' RETURN replace(c.name, 'a', 'A')"
        return self.db.execute_query(query)
    
    #d
    def getTeacherReturnChar(self):
        query = "MATCH (t:Teacher) RETURN t.name, substring(t.name, 3, 1)"
        return self.db.execute_query(query)
    

query = Query(db)

print("1-a")
aux = query.getRenzo()
print(f'Ano de nascimento: {aux[0]["t.ano_nasc"]}, CPF: {aux[0]["t.cpf"]}')
print("\n1-b")
aux = query.getStartsWithM()
for a in aux:
    print(f'Nome: {a["t.name"]}, CPF: {a["t.cpf"]}')
print("\n1-c")
aux = query.getAllCities()
for a in aux:
    print(f'Cidade: {a["c.name"]}')
print("\n1-d")
aux = query.getSchoolWithNumber()
for a in aux:
    print(f'Nome: {a["s.name"]}, Endereço: {a["s.address"]}, Número: {a["s.number"]}')
print("\n2-a")
aux = query.getYoungestAndOldestTeacher()
for a in aux:
    print(f'Ano de nascimento mais novo: {a["max(t.ano_nasc)"]}, Ano de nascimento mais velho: {a["min(t.ano_nasc)"]}')
print("\n2-b")
aux = query.getPopulationAverage()
for a in aux:
    print(f'Média da população: {a["avg(c.population)"]}')
print("\n2-c")
aux = query.getCityandSubstitute()
for a in aux:
    print('Cidade: {}'.format(a["replace(c.name, 'a', 'A')"]))
print("\n2-d")
aux = query.getTeacherReturnChar()
for a in aux:
    print(f'Char 3: {a["substring(t.name, 3, 1)"]}')