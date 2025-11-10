from neo4j import GraphDatabase, Driver
from typing import List, Dict, Any

class Neo4jDatabase:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "neo4jneo4j"):
        try:
            self.driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
            print(f"[Neo4j] Conectado a {uri} como {user}")
        except Exception as e:
            print("[Neo4j] Erro ao conectar:", e)
            raise

        self.drop_all()

    def close(self):
        self.driver.close()

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        parameters = parameters or {}
        data = []
        with self.driver.session() as session:
            results = session.run(query, parameters)
            for record in results:
                data.append(record.data())
        return data

    def drop_all(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("[Neo4j] Graph cleared.")
