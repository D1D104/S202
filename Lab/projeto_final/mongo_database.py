import pymongo
from typing import Optional

class MongoDatabase:
    def __init__(self, host: str = "localhost", port: int = 27017, database: str = "postsdb", collection: str = "posts", username: Optional[str]=None, password: Optional[str]=None):
        """
        Minimal Mongo wrapper. If username/password provided, will try to use them.
        """
        self.host = host
        self.port = port
        conn_str = f"mongodb://{host}:{port}"
        if username and password:
            conn_str = f"mongodb://{username}:{password}@{host}:{port}"
        try:
            self.client = pymongo.MongoClient(conn_str, tlsAllowInvalidCertificates=True)
            self.db = self.client[database]
            self.collection = self.db[collection]
            self.users_meta = self.db["users_meta"]
            print(f"[Mongo] Conectado a {conn_str} -> DB: {database}, collection: {collection}")
        except Exception as e:
            print("[Mongo] Erro ao conectar:", e)
            raise

        self.reset_collection()

    def reset_collection(self):
        try:
            self.db.drop_collection(self.collection.name)
            self.db.drop_collection("users_meta")
            self.db.drop_collection("counters")
            print("[Mongo] Collection resetada.")
            try:
                self.db["counters"].insert_one({"_id": "user_id", "seq": 0})
                print("[Mongo] Counters inicializado.")
            except Exception:
                pass
        except Exception as e:
            print("[Mongo] Erro ao resetar collection:", e)