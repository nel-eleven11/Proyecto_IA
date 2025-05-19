from move_set_managament import load_pokemon_moves, get_random_moveset, show_moves_list
from pokemon_data import get_pokemon_stats
from type_table import TypeTable

def seleccionar_pokemon():
    print("\nPokémon disponibles:")
    print("1. Charizard (Fuego/Volador)")
    print("2. Blastoise (Agua)")
    print("3. Venusaur (Planta/Veneno)")
    
    seleccionados = []
    while len(seleccionados) < 2:
        try:
            opcion = int(input(f"\nSelecciona el Pokémon {len(seleccionados)+1} (1-3): "))
            if opcion < 1 or opcion > 3:
                print("Por favor ingresa un número entre 1 y 3")
                continue
                
            pokemon = ["Charizard", "Blastoise", "Venusaur"][opcion-1]
            
            if pokemon in seleccionados:
                print("¡Este Pokémon ya fue seleccionado!")
            else:
                seleccionados.append(pokemon)
                print(f"¡{pokemon} seleccionado!")
        except ValueError:
            print("Por favor ingresa un número válido")
    
    return seleccionados

def asignar_movimientos(pokemon_nombre, movimientos_disponibles):
    #Permite elegir entre asignar movimientos aleatorios o manuales
    #
    print(f"\nConfigurando movimientos para {pokemon_nombre}")
    print("1. Asignar movimientos aleatoriamente")
    print("2. Elegir movimientos manualmente")
    
    while True:
        try:
            opcion = int(input("Selecciona una opción (1-2): "))
            if opcion == 1:
                moveset = get_random_moveset(movimientos_disponibles)
                print("\nMovimientos asignados aleatoriamente:")
                show_moves_list(moveset)
                return moveset
            elif opcion == 2:
                print("\nMovimientos disponibles:")
                show_moves_list(movimientos_disponibles)
                moveset = []
                
                while len(moveset) < 4:
                    nombre_movimiento = input(f"\nElige el movimiento {len(moveset)+1} (nombre exacto): ").strip()
                    movimiento_elegido = None
                    
                    for mov in movimientos_disponibles:
                        if mov["nombre"].lower() == nombre_movimiento.lower():
                            movimiento_elegido = mov
                            break
                    
                    if movimiento_elegido:
                        if movimiento_elegido in moveset:
                            print("¡Este movimiento ya fue seleccionado!")
                        else:
                            moveset.append(movimiento_elegido)
                            print(f"¡{movimiento_elegido['nombre']} añadido!")
                    else:
                        print("Movimiento no encontrado. Por favor ingresa el nombre exacto.")
                
                print("\nMovimientos seleccionados:")
                show_moves_list(moveset)
                return moveset
            else:
                print("Opción inválida. Por favor elige 1 o 2")
        except ValueError:
            print("Por favor ingresa un número válido")

# obteniendo la pool de los movimientos para cada pokemon inicial
movimientos = {
    "Charizard": load_pokemon_moves("charizard"),
    "Blastoise": load_pokemon_moves("blastoise"),
    "Venusaur": load_pokemon_moves("venusaur")
}

# obteniendo las stats de cada pokemon (no tienen un set de 4 movimientos aun)
# ej:
# "nombre": "Blastoise",
#  "tipo": ["Agua"],
#  "stats": {
#             "hp": 268,
#             "ataque": 153,
#             "defensa": 184,
#             "ataque_especial": 157,
#             "defensa_especial": 193,
#             "velocidad": 144
#  }
pokemons = {
    "Charizard": get_pokemon_stats("Charizard"),
    "Blastoise": get_pokemon_stats("Blastoise"),
    "Venusaur": get_pokemon_stats("Venusaur")
}

# traer tabla de tipos
tabla_tipos = TypeTable()

efectividad = tabla_tipos.calculate_effectivity("Roca", pokemons["Charizard"]["tipo"])
print(f"La efectividad es de {efectividad}")

print("Bienvenido a la simulación de combate Pokémon con IA")

# Selección de Pokémon
pokemons_seleccionados = seleccionar_pokemon()

# Configuración de movimientos para los seleccionados
for pokemon in pokemons_seleccionados:
    movimientos_pokemon = asignar_movimientos(pokemon, movimientos[pokemon])
    pokemons[pokemon]["movimientos"] = movimientos_pokemon

# extraer los seleccionados
pokemons_finales = {pokemon: pokemons[pokemon] for pokemon in pokemons_seleccionados}
    
# Mostrar resumen final
print("\n¡Configuración completada! Estos son los Pokémon que competirán:")
for pokemon in pokemons_finales:
    print(f"\n{pokemon} (Tipo: {'/'.join(pokemons_finales[pokemon]['tipo'])})")
    print("Stats:")
    for stat, valor in pokemons_finales[pokemon]['stats'].items():
        print(f"  {stat}: {valor}")
    print("Movimientos:")
    show_moves_list(pokemons_finales[pokemon]["movimientos"])


print("\nTodo listo para el combate :o")

# en este punto los pokemon que van a combatir estna en el dict "pokemons_finales"
# y los movimientos estarian en pokemons_finales["Charizard"]["Movimientos"] por ejemplo
# aca se puede ver la estructura del dict :)
print(pokemons_finales)