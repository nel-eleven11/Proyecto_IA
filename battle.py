# battle.py
# Simulación completa de combate Pokémon usando el flujo principal y agentes Expectimax

import random
from move_set_managament import load_pokemon_moves, get_random_moveset, show_moves_list
from pokemon_data import get_pokemon_stats
from type_table import TypeTable
from agent import GameState, PokemonInfo, GameContext, pick_best_move, apply_damage, pick_best_move_ab
from environment import EnvironmentTable

# --- Funciones de selección y asignación ---
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
            nombre = ["Charizard","Blastoise","Venusaur"][opcion-1]
            if nombre in seleccionados:
                print("¡Este Pokémon ya fue seleccionado!")
            else:
                seleccionados.append(nombre)
                print(f"¡{nombre} seleccionado!")
        except ValueError:
            print("Por favor ingresa un número válido")
    return seleccionados


def asignar_movimientos(pokemon_nombre, movimientos_disponibles):
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
                    nombre_mov = input(f"\nElige el movimiento {len(moveset)+1} (nombre exacto): ").strip()
                    encontrado = next((m for m in movimientos_disponibles if m['nombre'].lower()==nombre_mov.lower()), None)
                    if encontrado:
                        if encontrado in moveset:
                            print("¡Este movimiento ya fue seleccionado!")
                        else:
                            moveset.append(encontrado)
                            print(f"¡{encontrado['nombre']} añadido!")
                    else:
                        print("Movimiento no encontrado. Por favor ingresa el nombre exacto.")
                print("\nMovimientos seleccionados:")
                show_moves_list(moveset)
                return moveset
            else:
                print("Opción inválida. Por favor elige 1 o 2")
        except ValueError:
            print("Por favor ingresa un número válido")


# --- Flujo principal ---
def main():
    movimientos_pool = {
        "Charizard": load_pokemon_moves("charizard"),
        "Blastoise": load_pokemon_moves("blastoise"),
        "Venusaur": load_pokemon_moves("venusaur")
    }
    pokemons_data = {name: get_pokemon_stats(name) for name in movimientos_pool}
    tabla_tipos = TypeTable()

    print("Bienvenido a la simulación de combate Pokémon con IA")
    # Selección y configuración
    seleccionados = seleccionar_pokemon()
    infos = {}
    for nombre in seleccionados:
        stats = pokemons_data[nombre]['stats']
        types = pokemons_data[nombre]['tipo']
        raw_moves = movimientos_pool[nombre]
        moveset = asignar_movimientos(nombre, raw_moves)
        # añadir precision fijo o default
        for mv in moveset:
            mv.setdefault('precision', 1.0)
        infos[nombre] = PokemonInfo(
            name=nombre,
            max_hp=pokemons_data[nombre]['stats']['hp'],
            stats={
                'ataque': stats['ataque'],
                'defensa': stats['defensa'],
                'ataque_especial': stats['ataque_especial'],
                'defensa_especial': stats['defensa_especial'],
                'velocidad': stats['velocidad']
            },
            types=types,
            moveset=moveset
        )
        infos[nombre].base_stats = infos[nombre].stats.copy()

    #Se pide qué estrategia usar
    print("¿Qué tipo de IA deseas usar para P1?")
    print("1. Expectimax normal")
    print("2. Expectimax con poda α–β")

    modo = None
    while modo not in ('1','2'):
        modo = input("Selecciona 1 o 2: ").strip()

    # Contexto y estado inicial
    p1, p2 = infos[seleccionados[0]], infos[seleccionados[1]]
    context = GameContext(p1, p2)
    state = GameState(p1.max_hp, p2.max_hp)
    depth = 2

    env_table = EnvironmentTable()
    # Simulación de batalla
    turn = 1
    while not state.is_terminal():
        print(f"Turno {turn}: {p1.name} HP={state.hp1}, {p2.name} HP={state.hp2}")

        if turn > 1:
            #Cambia el ambiente de la batalla
            for info in infos.values():
                info.stats = info.base_stats.copy()

            env = env_table.get_random_environment()
            print(f"-> Nuevo ambiente: {env}. ¡Esto afecta a los pokemon!")
            for info in infos.values():
                env_table.apply_environment(env, info)

        # Decisión de movimientos
        if modo == '1':
            idx1 = pick_best_move(state, context, tabla_tipos, depth)
        else:
            idx1 = pick_best_move_ab(state, context, tabla_tipos, depth)
        move1 = p1.moveset[idx1]
        swapped_state = GameState(state.hp2, state.hp1)
        swapped_ctx = GameContext(p2, p1)
        idx2 = pick_best_move(swapped_state, swapped_ctx, tabla_tipos, depth)
        move2 = p2.moveset[idx2]
        print(f"{p1.name} usa {move1['nombre']}, {p2.name} usa {move2['nombre']}")

        # Orden de ataque
        first = p1.stats['velocidad'] >= p2.stats['velocidad']
        if first:
            # Primer ataque p1
            if random.random() <= move1['precision']:
                state = apply_damage(state, context, p1, p2, move1, tabla_tipos, True)
                print(f"  Impacta {move1['nombre']}! {p2.name} HP ahora {state.hp2}")
            else:
                print(f"  Falla {move1['nombre']}!")
            # Segundo ataque p2
            if state.hp2 > 0:
                if random.random() <= move2['precision']:
                    state = apply_damage(state, context, p2, p1, move2, tabla_tipos, True)
                    print(f"  Impacta {move2['nombre']}! {p1.name} HP ahora {state.hp1}")
                else:
                    print(f"  Falla {move2['nombre']}!")
        else:
            # Primer ataque p2
            if random.random() <= move2['precision']:
                state = apply_damage(state, context, p2, p1, move2, tabla_tipos, True)
                print(f"  Impacta {move2['nombre']}! {p1.name} HP ahora {state.hp1}")
            else:
                print(f"  Falla {move2['nombre']}!")
            # Segundo ataque p1
            if state.hp1 > 0:
                if random.random() <= move1['precision']:
                    state = apply_damage(state, context, p1, p2, move1, tabla_tipos, True)
                    print(f"  Impacta {move1['nombre']}! {p2.name} HP ahora {state.hp2}")
                else:
                    print(f"  Falla {move1['nombre']}!")

        turn += 1

    # Resultado final
    winner = p1.name if state.hp2 <= 0 else p2.name
    print(f"¡Victoria de {winner}!")

if __name__ == '__main__':
    main()