from database import Database
from livroModel import LivroModel
from cli import LivroCLI

db = Database(database="Biblioteca", collection="Livros")
livroModel = LivroModel(database=db)

livroCLI = LivroCLI(livroModel)
livroCLI.run()
