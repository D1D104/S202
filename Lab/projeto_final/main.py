from pprint import pprint
from mongo_database import MongoDatabase
from neo4j_database import Neo4jDatabase
from DAO_mongo import MongoDAO
from DAO_neo4j import Neo4jDAO

def build_default_connections():
    mongo_db = MongoDatabase(host="localhost", port=27017, database="postsdb", collection="posts")
    neo4j_db = Neo4jDatabase(uri="bolt://localhost:7687", user="neo4j", password="neo4jneo4j")
    return mongo_db, neo4j_db

def run_cli(mongo_db: MongoDatabase, neo4j_db: Neo4jDatabase):
    mongo = MongoDAO(mongo_db.collection, mongo_db.users_meta)
    neo = Neo4jDAO(neo4j_db.driver)

    mongo.create_indexes()
    neo.create_constraints()

    menu = """
Menu:
1 - Criar usuário (meta + nó)
2 - Criar post
3 - Ler post / Listar recentes
4 - Atualizar post
5 - Deletar post
6 - Comentar post
7 - Buscar posts por tag
8 - Busca de texto (text index)
9 - Seguir usuário (grafo)
10 - Recomendar usuários (grafo)
11 - Ver feed
12 - Curtir post (grafo)
0 - Sair
"""
    while True:
        print(menu)
        op = input("Escolha: ").strip()
        if op == "1":
            nome = input("nome: ").strip()
            perfil = input("perfil: ").strip()
            created_id = mongo.create_user_meta({"nome": nome, "perfil": perfil})
            neo.merge_user(created_id, nome=nome, perfil=perfil)
            print(f"Usuário criado. id: {created_id}")
        elif op == "2":
            author = input("author_id: ").strip()
            titulo = input("titulo: ").strip()
            corpo = input("corpo: ").strip()
            tags = [t.strip() for t in input("tags (comma separated): ").split(",") if t.strip()]
            pid = mongo.create_post({"author_id": author, "titulo": titulo, "corpo": corpo, "tags": tags})
            print("Post criado id:", pid)
        elif op == "3":
            pid = input("post id (deixe vazio para recentes): ").strip()
            if not pid:
                for p in mongo.list_recent_posts(10):
                    print(f"{p.get('_id')} | {p.get('titulo')} | {p.get('author_id')} | {p.get('ts')}")
            else:
                p = mongo.read_post(pid)
                pprint(p)
        elif op == "4":
            pid = input("post id: ").strip()
            titulo = input("novo titulo (enter mantém): ").strip()
            corpo = input("novo corpo (enter mantém): ").strip()
            updates = {}
            if titulo:
                updates["titulo"] = titulo
            if corpo:
                updates["corpo"] = corpo
            if updates:
                mongo.update_post(pid, updates)
            else:
                print("Nada para atualizar.")
        elif op == "5":
            pid = input("post id: ").strip()
            mongo.delete_post(pid)
        elif op == "6":
            pid = input("post id: ").strip()
            uid = input("seu user id: ").strip()
            texto = input("texto comentario: ").strip()
            mongo.add_comment(pid, uid, texto)
        elif op == "7":
            tag = input("tag: ").strip()
            for p in mongo.find_by_tag(tag):
                print(f"{p.get('_id')} | {p.get('titulo')} | {p.get('author_id')}")
        elif op == "8":
            q = input("texto busca: ").strip()
            for p in mongo.text_search(q):
                print(f"{p.get('_id')} (score) | {p.get('titulo')}")
        elif op == "9":
            a = input("seu id: ").strip()
            b = input("seguir id: ").strip()
            neo.follow(a, b)
            print(f"{a} agora segue {b}")
        elif op == "10":
            uid = input("user id: ").strip()
            recs = neo.recommend_users(uid)
            if not recs:
                print("Sem recomendações.")
            else:
                for r in recs:
                    print(f"{r['id']} | nome: {r.get('nome')} | mutuals: {r.get('mutual')}")
        elif op == "11":
            uid = input("user id: ").strip()
            followed = neo.get_followed_ids(uid)
            if uid not in followed:
                followed.append(uid)
            feed = mongo.feed_for_authors(followed, limit=20)
            for it in feed:
                print(f"{it.get('_id')} | {it.get('titulo')} | by {it.get('author_id')} | comments: {it.get('comentarios_count')}")
        elif op == "12":
            uid = input("user id: ").strip()
            pid = input("post id: ").strip()
            neo.like_post(uid, pid)
            print("Like registrado.")
        elif op == "0":
            print("Saindo...")
            try:
                neo4j_db.close()
            except Exception:
                pass
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    mongo_db, neo4j_db = build_default_connections()
    run_cli(mongo_db, neo4j_db)
