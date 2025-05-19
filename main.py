from move_set_managament import load_pokemon_moves
from pokemon_data import get_pokemon_stats
from type_table import TypeTable

# obteniendo la pool de los movimientos para cada pokemon inicial
charizard_moves = load_pokemon_moves("charizard")
blastoise_moves = load_pokemon_moves("blastoise")
venusaur_moves = load_pokemon_moves("venusaur")
print(charizard_moves,"\n")
print(blastoise_moves,"\n")
print(venusaur_moves,"\n")

# obteniendo las stats de cada pokemon (no tienen un set de 4 movimientos aun)
charizard = get_pokemon_stats("Charizard")
print(charizard)
blastoise = get_pokemon_stats("Blastoise")
print(blastoise)
venusaur = get_pokemon_stats("Venusaur")
print(venusaur)

#traer la tabla de tipos y una prueba
tabla_tipos = TypeTable()

efectividad = tabla_tipos.calculate_effectivity("Roca", charizard["tipo"])
print(f"La efectividad es de {efectividad}")