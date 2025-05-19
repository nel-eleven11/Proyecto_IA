from move_set_managament import load_pokemon_moves
from pokemon_data import get_pokemon_stats

charizard_moves = load_pokemon_moves("charizard")
blastoise_moves = load_pokemon_moves("blastoise")
venusaur_moves = load_pokemon_moves("venusaur")

print(charizard_moves,"\n")
print(blastoise_moves,"\n")
print(venusaur_moves,"\n")

charizard_data = get_pokemon_stats("Charizard")
print(charizard_data)

blastoise_data = get_pokemon_stats("Blastoise")
print(blastoise_data)

pikachu_data = get_pokemon_stats("Venusaur")
print(pikachu_data)