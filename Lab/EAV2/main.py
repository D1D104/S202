from teacher_crud import TeacherCRUD
from database import Database

db = Database("bolt://18.204.243.124:7687","neo4j","copper-velocities-runaways")
crud = TeacherCRUD(db)

op = 0

while op != 5:
    print("1 - Criar professor")
    print("2 - Buscar professor")
    print("3 - Atualizar cpf professor")
    print("4 - Deletar professor")
    print("5 - Sair")
    
    op = int(input("Digite a opção desejada: "))
    
    if op == 1:
        name = input("Digite o nome do professor: ")
        ano_nasc = int(input("Digite o ano de nascimento do professor: "))
        cpf = input("Digite o cpf do professor: ")
        crud.create(name, ano_nasc, cpf)
    elif op == 2:
        name = input("Digite o nome do professor: ")
        teacher = crud.read(name)
        print(f'Nome: {teacher[0]["t.name"]}, Ano de nascimento: {teacher[0]["t.ano_nasc"]}, CPF: {teacher[0]["t.cpf"]}')
    elif op == 3:
        name = input("Digite o nome do professor: ")
        newCpf = input("Digite o novo cpf do professor: ")
        crud.update(name, newCpf)
    elif op == 4:
        name = input("Digite o nome do professor: ")
        crud.delete(name)
    elif op == 5:
        db.close()
    else:
        print("Opção inválida")