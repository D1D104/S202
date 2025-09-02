from database import Database
from helper.writeAJson import writeAJson

db = Database(database="mercado", collection="compras")
#db.resetDatabase()

class ProductAnalyzer:

    def __init__(self, db: Database):
        self.collection = db.collection

    def vendasDia(self):
        result = self.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {
                "_id": "$data_compra",
                "total_vendas": {
                    "$sum": {
                        "$multiply": ["$produtos.quantidade", "$produtos.preco"]
                    }
                }
            }},
            {"$sort": {"_id": 1}}
        ])
        return list(result)    

    def produtoMaisVendido(self):
        result = self.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {
                "_id": "$produtos.descricao",
                "quantidade_total": {"$sum": "$produtos.quantidade"}
            }},
            {"$sort": {"quantidade_total": -1}},
            {"$limit": 1}
        ])
        return list(result)

    def clienteMaiorGasto(self):
        result = self.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {
                "_id": "$_id", 
                "cliente": {"$first": "$cliente_id"},
                "total": {
                    "$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}
                }
            }},
            {"$sort": {"total": -1}},
            {"$limit": 1}
        ])
        return list(result)

    def produtosAcimaUmaVenda(self):
        result = self.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {
                "_id": "$produtos.descricao",
                "quantidade_total": {"$sum": "$produtos.quantidade"}
            }},
            {"$match": {"quantidade_total": {"$gt": 1}}},
            {"$sort": {"quantidade_total": -1}}
        ])
        return list(result) 


produto = ProductAnalyzer(db)

vendasDia = produto.vendasDia()
writeAJson(vendasDia, "Vendas por dia")

produtoMaisVendido = produto.produtoMaisVendido()
writeAJson(produtoMaisVendido, "Produto mais vendido")

clienteMaiorGasto = produto.clienteMaiorGasto()
writeAJson(clienteMaiorGasto, "Cliente que mais gastou")

produtosAcimaUmaVenda = produto.produtosAcimaUmaVenda()
writeAJson(produtosAcimaUmaVenda, "Produtos acima de uma unidade")

# 1- Média de gasto total:
# result = db.collection.aggregate([
#    {"$unwind": "$produtos"},
#    {"$group": {"_id": "$cliente_id", "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
#    {"$group": {"_id": None, "media": {"$avg": "$total"}}}
# ])

# writeAJson(result, "Média de gasto total")

# # 2- Cliente que mais comprou em cada dia:
# result = db.collection.aggregate([
#     {"$unwind": "$produtos"},
#     {"$group": {"_id": {"cliente": "$cliente_id", "data": "$data_compra"}, "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
#     {"$sort": {"_id.data": 1, "total": -1}},
#     {"$group": {"_id": "$_id.data", "cliente": {"$first": "$_id.cliente"}, "total": {"$first": "$total"}}}
# ])

# writeAJson(result, "Cliente que mais comprou em cada dia")

# 3- Produto mais vendido:
#result = db.collection.aggregate([
 #   {"$unwind": "$produtos"},
  #  {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
   # {"$sort": {"total": -1}},
    #{"$limit": 1}
#])

#writeAJson(result, "Produto mais vendido")