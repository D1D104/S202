from Database import Database
from MotoristaCLI import MotoristaCLI
from MotoristaDAO import MotoristaDAO

db = Database(database = "Corridas", collection="Motoristas")

motorista_dao = MotoristaDAO(db)
motorista_cli = MotoristaCLI(motorista_dao)

motorista_cli.start()   