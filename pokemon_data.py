def get_pokemon_stats(nombre_pokemon):
    charizard = {
        "nombre": "Charizard",
        "tipo": ["Fuego", "Volador"],
        "stats": {
            "hp": 866,
            "ataque": 155,
            "defensa": 144,
            "ataque_especial": 200,
            "defensa_especial": 157,
            "velocidad": 184
        }
    }

    blastoise = {
        "nombre": "Blastoise",
        "tipo": ["Agua"],
        "stats": {
            "hp": 868,
            "ataque": 153,
            "defensa": 184,
            "ataque_especial": 157,
            "defensa_especial": 193,
            "velocidad": 144
        }
    }

    venusaur = {
        "nombre": "Venusaur",
        "tipo": ["Planta", "Veneno"],
        "stats": {
            "hp": 870,
            "ataque": 152,
            "defensa": 153,
            "ataque_especial": 184,
            "defensa_especial": 184,
            "velocidad": 148
        }
    }

    if nombre_pokemon == "Charizard":
        return charizard
    elif nombre_pokemon == "Blastoise":
        return blastoise
    elif nombre_pokemon == "Venusaur":
        return venusaur
    else:
        return None
