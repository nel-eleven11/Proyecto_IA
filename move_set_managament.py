import json
import random

def load_pokemon_moves(pokemon_name):
    file_path = f'./pokemon_moves/{pokemon_name}_moves.json'
    moves = {}
    try:

        with open(file_path, 'r', encoding='utf-8') as f:
            moves = json.load(f)

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{file_path}'.")

    return moves

def get_random_moveset(move_list):
    random_move_set = random.sample(move_list, 4)
    return random_move_set

def show_moves_list(move_list):

    for move in move_list:

        for key, value in move.items():
            print(f"{key}: {value}, ", end="")
        
        print()