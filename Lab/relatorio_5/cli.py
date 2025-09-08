class SimpleCLI:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, function):
        self.commands[name] = function

    def run(self):
        while True:
            command = input("Digite um comando: ")
            if command == "quit":
                print("Até logo!")
                break
            elif command in self.commands:
                self.commands[command]()
            else:
                print("Comando inválido. Tente novamente.")


class LivroCLI(SimpleCLI):
    def __init__(self, livro_model):
        super().__init__()
        self.livro_model = livro_model
        self.add_command("create", self.create_livro)
        self.add_command("read", self.read_livro)
        self.add_command("update", self.update_livro)
        self.add_command("delete", self.delete_livro)

    def create_livro(self):
        titulo = input("Digite o título: ")
        autor = input("Digite o autor: ")
        ano = int(input("Digite o ano: "))
        preco = float(input("Digite o preço: "))
        self.livro_model.create_livro(titulo, autor, ano, preco)

    def read_livro(self):
        id = input("Digite o id do livro: ")
        livro = self.livro_model.read_livro_by_id(id)
        if livro:
            print(f"Título: {livro['titulo']}")
            print(f"Autor: {livro['autor']}")
            print(f"Ano: {livro['ano']}")
            print(f"Preço: {livro['preco']}")

    def update_livro(self):
        id = input("Digite o id do livro: ")
        titulo = input("Novo título: ")
        autor = input("Novo autor: ")
        ano = int(input("Novo ano: "))
        preco = float(input("Novo preço: "))
        self.livro_model.update_livro(id, titulo, autor, ano, preco)

    def delete_livro(self):
        id = input("Digite o id do livro: ")
        self.livro_model.delete_livro(id)

    def run(self):
        print("Bem-vindo à CLI de Livros!")
        print("Comandos disponíveis: create, read, update, delete, quit")
        super().run()