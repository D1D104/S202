from database import Database
from helper.writeAJson import writeAJson

db = Database(database="pokedex", collection="pokemons")
#db.resetDatabase()
class Pokedex: 

    def __init__(self, db: Database):
        self.collection = db.collection

    def getPokemonsByCandyCount(self, min_candies: int):
        return list(self.collection.find({"candy_count": {"$gt": min_candies}}, {"name": 1, "candy_count": 1}))

    def getPokemonsByWeaknesses(self, weaknesses: list[str]):
        return list(self.collection.find({"weaknesses": {"$all": weaknesses}}, {"name": 1, "weaknesses": 1}))
    
    def getPokemonsWithMultipleEvolutions(self):
        return list(self.collection.find({"next_evolution.1": {"$exists": True}}, {"name": 1, "next_evolution": 1}))
    
    def getTopSpawnChance(self, limit: int = 5):
        return list(self.collection.find({}, {"name": 1, "spawn_chance": 1})
                    .sort("spawn_chance", -1).limit(limit))

    def getStrongEvolutionPokemons(self):
        return list(self.collection.find({"next_evolution": {"$exists": True},
                                          "multipliers": {"$elemMatch": {"$gt": 1.5}}},
                                         {"name": 1, "multipliers": 1, "next_evolution": 1}))

pokedex = Pokedex(db)

candy_count = pokedex.getPokemonsByCandyCount(50)
writeAJson(candy_count,"50_candy_to_evolve")

weakness_fire_ice = pokedex.getPokemonsByWeaknesses(["Fire","Ice"])
writeAJson(weakness_fire_ice, "weakness_fire_ice")

multi_evol = pokedex.getPokemonsWithMultipleEvolutions()
writeAJson(multi_evol, "multi_evolutions")

top_spawn = pokedex.getTopSpawnChance(10)
writeAJson(top_spawn, "top_spawn_chance")

strong_evolution = pokedex.getStrongEvolutionPokemons()
writeAJson(strong_evolution, "strong_evolution")