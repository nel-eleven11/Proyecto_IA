# test_agent.py
# Prueba básica del agente Expectimax sin PP

from agent import GameState, PokemonInfo, GameContext, pick_best_move
from type_table import TypeTable


def main():
    # Definición de movimientos de Blastoise
    blastoise_moves = [
        {"nombre": "Hidrobomba",   "tipo": "Agua",  "categoría": "Especial", "poder": 110, "precision": 0.80},
        {"nombre": "Pistola Agua", "tipo": "Agua",  "categoría": "Especial", "poder": 40,  "precision": 1.00},
        {"nombre": "Demolición",   "tipo": "Lucha", "categoría": "Físico",   "poder": 75,  "precision": 0.80},
        {"nombre": "Cascada",      "tipo": "Agua",  "categoría": "Físico",   "poder": 80,  "precision": 1.00},
    ]
    # Stats y tipos de Blastoise
    blastoise_info = PokemonInfo(
        name="Blastoise",
        max_hp=268,
        stats={
            "ataque": 153,
            "defensa": 184,
            "ataque_especial": 157,
            "defensa_especial": 193,
            "velocidad": 144
        },
        types=["Agua"],
        moveset=blastoise_moves
    )

    # Definición de movimientos de Charizard
    charizard_moves = [
        {"nombre": "Lanzallamas",  "tipo": "Fuego",   "categoría": "Especial", "poder": 90,  "precision": 1.00},
        {"nombre": "Pulso Dragón", "tipo": "Dragón",  "categoría": "Especial", "poder": 85,  "precision": 1.00},
        {"nombre": "Tajo Aéreo",   "tipo": "Volador", "categoría": "Especial", "poder": 75,  "precision": 0.95},
        {"nombre": "Nitrocarga",   "tipo": "Fuego",   "categoría": "Físico",   "poder": 50,  "precision": 1.00},
    ]
    # Stats y tipos de Charizard
    charizard_info = PokemonInfo(
        name="Charizard",
        max_hp=266,
        stats={
            "ataque": 155,
            "defensa": 144,
            "ataque_especial": 200,
            "defensa_especial": 157,
            "velocidad": 184
        },
        types=["Fuego", "Volador"],
        moveset=charizard_moves
    )

    # Contexto de combate
    context = GameContext(blastoise_info, charizard_info)

    # Estado inicial (ambos al máximo de HP)
    initial_state = GameState(
        hp1=blastoise_info.max_hp,
        hp2=charizard_info.max_hp
    )

    # Tabla de tipos
    type_table = TypeTable()

    # Elegir mejor movimiento con profundidad 2
    best_idx = pick_best_move(initial_state, context, type_table, depth=2)
    best_move = blastoise_info.moveset[best_idx]

    print(f"El agente elige usar: {best_move['nombre']} (índice {best_idx})")


if __name__ == '__main__':
    main()
