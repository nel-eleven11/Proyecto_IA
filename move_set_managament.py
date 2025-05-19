import json

def load_pokemon_moves(pokemon_name):
    file_path = f'./pokemon_moves/{pokemon_name}_moves.json'
    moves = {}
    try:

        with open(file_path, 'r', encoding='utf-8') as f:
            moves = json.load(f)

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{file_path}'.")

    return moves
