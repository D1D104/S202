from typing import List, Dict, Any, Optional
from pymongo.collection import Collection
from pymongo import ASCENDING, TEXT
from bson import ObjectId
from datetime import datetime

class MongoDAO:
    def __init__(self, posts_col: Collection, users_meta_col: Collection):
        self.posts = posts_col
        self.users_meta = users_meta_col
        self.counters = self.users_meta.database["counters"]

    def create_indexes(self):
        try:
            self.posts.create_index([("titulo", TEXT), ("corpo", TEXT)], name="text_idx")
            self.posts.create_index("tags", name="idx_tags")
            self.posts.create_index([("author_id", ASCENDING), ("ts", -1)], name="idx_author_ts")
            print("[MongoDAO] Indexes criados.")
        except Exception as e:
            print("[MongoDAO] Erro ao criar indexes:", e)

    def create_post(self, post_doc: Dict[str, Any]) -> str:
        post_doc.setdefault("ts", datetime.utcnow())
        post_doc.setdefault("comentarios", [])
        res = self.posts.insert_one(post_doc)
        print(f"[MongoDAO] Post inserido: {res.inserted_id}")
        return str(res.inserted_id)

    def read_post(self, post_id: str) -> Optional[Dict[str, Any]]:
        q = {"_id": ObjectId(post_id)} if ObjectId.is_valid(post_id) else {"_id": post_id}
        return self.posts.find_one(q)

    def update_post(self, post_id: str, updates: Dict[str, Any]) -> int:
        q = {"_id": ObjectId(post_id)} if ObjectId.is_valid(post_id) else {"_id": post_id}
        res = self.posts.update_one(q, {"$set": updates})
        print(f"[MongoDAO] Posts modificados: {res.modified_count}")
        return res.modified_count

    def delete_post(self, post_id: str) -> int:
        q = {"_id": ObjectId(post_id)} if ObjectId.is_valid(post_id) else {"_id": post_id}
        res = self.posts.delete_one(q)
        print(f"[MongoDAO] Posts deletados: {res.deleted_count}")
        return res.deleted_count

    def list_recent_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        return list(self.posts.find().sort("ts", -1).limit(limit))

    def add_comment(self, post_id: str, user_id: str, texto: str) -> int:
        comment = {"user_id": user_id, "texto": texto, "ts": datetime.utcnow()}
        q = {"_id": ObjectId(post_id)} if ObjectId.is_valid(post_id) else {"_id": post_id}
        res = self.posts.update_one(q, {"$push": {"comentarios": comment}})
        print(f"[MongoDAO] Comentários adicionados/modificados: {res.modified_count}")
        return res.modified_count

    def find_by_tag(self, tag: str, limit: int = 50) -> List[Dict[str, Any]]:
        return list(self.posts.find({"tags": tag}).sort("ts", -1).limit(limit))

    def text_search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        cursor = self.posts.find({"$text": {"$search": query}}, {"score": {"$meta": "textScore"}})
        cursor = cursor.sort([("score", {"$meta": "textScore"})]).limit(limit)
        return list(cursor)

    def feed_for_authors(self, author_ids: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        pipeline = [
            {"$match": {"author_id": {"$in": author_ids}}},
            {"$project": {
                "titulo": 1,
                "author_id": 1,
                "ts": 1,
                "comentarios_count": {"$size": {"$ifNull": ["$comentarios", []]}}
            }},
            {"$sort": {"ts": -1}},
            {"$limit": limit}
        ]
        return list(self.posts.aggregate(pipeline))

    def create_user_meta(self, user_doc: Dict[str, Any]) -> str:
        if "_id" not in user_doc or user_doc.get("_id") in (None, ""):
            next_id = self.get_next_sequence("user_id")
            user_doc["_id"] = str(next_id)

        res = self.users_meta.insert_one(user_doc)
        print(f"[MongoDAO] UserMeta criado: {res.inserted_id}")
        return str(res.inserted_id)

    def get_next_sequence(self, name: str) -> int:
        doc = self.counters.find_one_and_update(
            {"_id": name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True
        )
        if not doc:
            self.counters.insert_one({"_id": name, "seq": 1})
            return 1
        return int(doc.get("seq", 0))

    def get_user_meta(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users_meta.find_one({"_id": user_id})

    def list_users_meta(self, limit: int = 50) -> List[Dict[str, Any]]:
        return list(self.users_meta.find().limit(limit))
