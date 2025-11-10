from neo4j import Driver
from typing import List, Dict, Any, Optional

class Neo4jDAO:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.create_constraints()

    def _execute(self, cypher: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        params = params or {}
        data = []
        with self.driver.session() as session:
            results = session.run(cypher, params)
            for r in results:
                data.append(r.data())
        return data

    def create_constraints(self):
        try:
            self._execute("CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
            print("[Neo4jDAO] Constraint User.id criado/assegurado.")
        except Exception as e:
            print("[Neo4jDAO] Erro ao criar constraint:", e)

    def merge_user(self, user_id: str, nome: Optional[str] = None, perfil: Optional[str] = None):
        cypher = "MERGE (u:User {id:$id}) SET u.nome = $nome, u.perfil = $perfil RETURN u.id AS id"
        return self._execute(cypher, {"id": user_id, "nome": nome, "perfil": perfil})

    def follow(self, a: str, b: str):
        cypher = """
        MERGE (a:User {id:$a})
        MERGE (b:User {id:$b})
        MERGE (a)-[:FOLLOWS]->(b)
        RETURN a.id AS from, b.id AS to
        """
        return self._execute(cypher, {"a": a, "b": b})

    def make_friend(self, a: str, b: str):
        cypher = """
        MERGE (a:User {id:$a})
        MERGE (b:User {id:$b})
        MERGE (a)-[:FRIENDS]->(b)
        MERGE (b)-[:FRIENDS]->(a)
        RETURN a.id AS a, b.id AS b
        """
        return self._execute(cypher, {"a": a, "b": b})

    def like_post(self, user_id: str, post_id: str):
        cypher = """
        MERGE (u:User {id:$uid})
        MERGE (p:Post {id:$pid})
        MERGE (u)-[r:LIKED_POST]->(p)
        SET r.ts = datetime()
        RETURN u.id AS user, p.id AS post
        """
        return self._execute(cypher, {"uid": user_id, "pid": post_id})

    def share_post(self, user_id: str, post_id: str):
        cypher = """
        MERGE (u:User {id:$uid})
        MERGE (p:Post {id:$pid})
        MERGE (u)-[r:SHARED_POST]->(p)
        SET r.ts = datetime()
        RETURN u.id AS user, p.id AS post
        """
        return self._execute(cypher, {"uid": user_id, "pid": post_id})

    def get_followed_ids(self, user_id: str) -> List[str]:
        cypher = "MATCH (u:User {id:$uid})-[:FOLLOWS]->(v) RETURN v.id AS id"
        rows = self._execute(cypher, {"uid": user_id})
        return [r["id"] for r in rows]

    def recommend_users(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        cypher = """
        MATCH (u:User {id:$uid})-[:FOLLOWS]->(f)-[:FOLLOWS]->(rec)
        WHERE NOT (u)-[:FOLLOWS]->(rec) AND rec.id <> $uid
        RETURN rec.id AS id, rec.nome AS nome, count(*) AS mutual
        ORDER BY mutual DESC
        LIMIT $limit
        """
        rows = self._execute(cypher, {"uid": user_id, "limit": limit})
        return rows

    def count_followers(self, user_id: str) -> int:
        cypher = "MATCH (u:User {id:$uid})<-[:FOLLOWS]-(:User) RETURN count(*) AS cnt"
        rows = self._execute(cypher, {"uid": user_id})
        return rows[0]["cnt"] if rows else 0
