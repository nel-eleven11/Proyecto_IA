# ambientes.py

import random

class EnvironmentTable:
    def __init__(self):
        # Ajustes porcentuales por tipo: positivo mejora, negativo debilita
        self.tabla = {
            "Día Lluvioso":      {"Agua": 0.10, "Volador": -0.05, "Planta": 0.03, "Fuego": -0.10, "Veneno": 0.00},
            "Tormenta de Arena": {"Agua": -0.05, "Volador":  0.00, "Planta": -0.10, "Fuego":  0.05, "Veneno": 0.02},
            "Nevada":            {"Agua": 0.00, "Volador": -0.05, "Planta": -0.10, "Fuego": -0.05, "Veneno": 0.00},
            "Desierto":          {"Agua": -0.10, "Volador": 0.00, "Planta": -0.05, "Fuego": 0.08, "Veneno": 0.03},
            "Inundación":        {"Agua": 0.10, "Volador": 0.00, "Planta": 0.02, "Fuego": -0.08, "Veneno": -0.05},
            "Día Soleado":        {"Agua": 0.00, "Volador": -0.01, "Planta": -0.05, "Fuego": 0.10, "Veneno": -0.05},
        }

    def get_random_environment(self) -> str:
        return random.choice(list(self.tabla.keys()))

    def apply_environment(self, env_name: str, pokemon_info):
        """
        Modifica pokemon_info.stats en base a pokemon_info.base_stats y
        al ajuste acumulado de sus tipos, e imprime el efecto.
        """
        ajustes = self.tabla.get(env_name, {})
        # Factor total sumando ajustes por cada tipo del Pokémon
        factor = sum(ajustes.get(tipo, 0) for tipo in pokemon_info.types)
        porcentaje = factor * 100
        # Informe del cambio
        if porcentaje > 0:
            print(f"-> Las stats de {pokemon_info.name} aumentaron un {porcentaje:.1f}%")
        elif porcentaje < 0:
            print(f"-> Las stats de {pokemon_info.name} disminuyeron un {abs(porcentaje):.1f}%")
        else:
            print(f"-> Las stats de {pokemon_info.name} no se vieron afectadas")
        # Aplicar cambios numéricos (excluye HP)
        for stat, base_val in pokemon_info.base_stats.items():
            pokemon_info.stats[stat] = int(base_val * (1 + factor))
        
