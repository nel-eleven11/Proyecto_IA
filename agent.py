'''
agent.py
Módulo para lógica del agente IA sin PP: estado, heurística, simulación con Expectimax.
'''

import random
from type_table import TypeTable

class GameState:
    """
    Estado dinámico del combate:
    - hp1, hp2: vida actual de cada Pokémon
    """
    def __init__(self, hp1, hp2):
        self.hp1 = hp1
        self.hp2 = hp2

    def is_terminal(self):
        return self.hp1 <= 0 or self.hp2 <= 0

    def clone(self):
        return GameState(self.hp1, self.hp2)

class PokemonInfo:
    """
    Información estática de un Pokémon:
    - name: nombre
    - max_hp: HP máximo
    - stats: dict con 'ataque', 'defensa', 'ataque_especial', 'defensa_especial', 'velocidad'
    - types: lista de strings (tipos)
    - moveset: lista de dicts, cada uno con 'nombre','tipo','categoría','poder','precision'
    """
    def __init__(self, name, max_hp, stats, types, moveset):
        self.name = name
        self.max_hp = max_hp
        self.stats = stats
        self.types = types
        self.moveset = moveset

class GameContext:
    """
    Combina info estática de ambos Pokémon.
    """
    def __init__(self, p1: PokemonInfo, p2: PokemonInfo):
        self.p1 = p1
        self.p2 = p2

# ----- Heurística -----
def get_best_type_potential(moveset, defender_types, type_table: TypeTable):
    best = 0.0
    for move in moveset:
        if move['poder'] <= 0:
            continue
        eff = 1.0
        for dt in defender_types:
            eff *= type_table.calculate_effectivity(move['tipo'], [dt])
        #power = eff * move['poder']
        precision = move.get('precision', 1.0)
        power = eff * move['poder'] * precision
        if power > best:
            best = power
    return best


def evaluate_state(state: GameState, context: GameContext, type_table: TypeTable,
                   w_hp=1.0, w_type=0.5, w_speed=0.1, w_def=0.1, w_spdef=0.1):
    """
    - Diferencia porcentual de HP
    - Diferencia de potencial de tipo
    - Ventaja de velocidad, defensa y defensa especial
    """
    r_hp = (state.hp1 / context.p1.max_hp) - (state.hp2 / context.p2.max_hp)
    pot1 = get_best_type_potential(context.p1.moveset, context.p2.types, type_table)
    pot2 = get_best_type_potential(context.p2.moveset, context.p1.types, type_table)
    s1, s2 = context.p1.stats['velocidad'], context.p2.stats['velocidad']
    r_spd = (s1 - s2) / max(s1, s2)
    d1, d2 = context.p1.stats['defensa'], context.p2.stats['defensa']
    r_def = (d1 - d2) / max(d1, d2)
    sd1, sd2 = context.p1.stats['defensa_especial'], context.p2.stats['defensa_especial']
    r_spdef = (sd1 - sd2) / max(sd1, sd2)
    return (w_hp * r_hp + w_type * (pot1 - pot2) + w_speed * r_spd + w_def * r_def + w_spdef * r_spdef)

# ----- Daño determinístico -----
def apply_damage(state: GameState, context: GameContext,
                 attacker: PokemonInfo, defender: PokemonInfo,
                 move, type_table: TypeTable, hit: bool) -> GameState:
    """
    Aplica daño según move, retorna nuevo GameState.
    Usa context para decidir a quién restar HP.
    """
    if not hit:
        return state
    hp1, hp2 = state.hp1, state.hp2
    # elegir stat de ataque y defensa según categoría
    atk = attacker.stats['ataque_especial'] if move['categoría']=='Especial' else attacker.stats['ataque']
    df  = defender.stats['defensa_especial'] if move['categoría']=='Especial' else defender.stats['defensa']
    # calcular efectividad
    eff = 1.0
    for dt in defender.types:
        eff *= type_table.calculate_effectivity(move['tipo'], [dt])
    dmg = int((move['poder'] * atk / df) * eff)
    # restar al oponente
    if attacker is context.p1:
        hp2 -= dmg
    else:
        hp1 -= dmg
    return GameState(hp1, hp2)

# ----- Expectimax -----
def expectimax(state: GameState, context: GameContext, type_table: TypeTable,
               depth: int, stage: str, m1_idx=None, m2_idx=None) -> float:
    """
    stage: 'agent', 'opponent', 'chance1', 'chance2'
    m1_idx y m2_idx son índices de movimientos en nodos chance.
    """
    if state.is_terminal() or depth == 0:
        return evaluate_state(state, context, type_table)
    # AGENT: maximiza
    if stage == 'agent':
        best = float('-inf')
        for i, mv in enumerate(context.p1.moveset):
            val = expectimax(state, context, type_table, depth, 'opponent', i, None)
            if val > best:
                best = val
        return best
    # OPPONENT: minimiza
    if stage == 'opponent':
        worst = float('inf')
        for j, mv in enumerate(context.p2.moveset):
            val = expectimax(state, context, type_table, depth, 'chance1', m1_idx, j)
            if val < worst:
                worst = val
        return worst
    # CHANCE 1: primer atacante
    if stage == 'chance1':
        first = context.p1.stats['velocidad'] >= context.p2.stats['velocidad']
        mv = context.p1.moveset[m1_idx] if first else context.p2.moveset[m2_idx]
        p = mv.get('precision', 1.0)
        # hit
        st_hit = apply_damage(state.clone(), context,
                              context.p1 if first else context.p2,
                              context.p2 if first else context.p1,
                              mv, type_table, True)
        v_hit  = expectimax(st_hit, context, type_table, depth, 'chance2', m1_idx, m2_idx)
        # miss
        st_miss = state.clone()
        v_miss  = expectimax(st_miss, context, type_table, depth, 'chance2', m1_idx, m2_idx)
        return p * v_hit + (1-p) * v_miss
    # CHANCE 2: segundo atacante
    if stage == 'chance2':
        first = context.p1.stats['velocidad'] >= context.p2.stats['velocidad']
        if state.hp1 <= 0 or state.hp2 <= 0:
            return expectimax(state, context, type_table, depth-1, 'agent')
        mv = context.p2.moveset[m2_idx] if first else context.p1.moveset[m1_idx]
        p = mv.get('precision', 1.0)
        # hit
        st_hit = apply_damage(state.clone(), context,
                              context.p2 if first else context.p1,
                              context.p1 if first else context.p2,
                              mv, type_table, True)
        v_hit  = expectimax(st_hit, context, type_table, depth-1, 'agent')
        # miss
        st_miss = state.clone()
        v_miss  = expectimax(st_miss, context, type_table, depth-1, 'agent')
        return p * v_hit + (1-p) * v_miss


#  Minimax con poda

def expectimax_ab(state, context, type_table, depth, stage, alpha, beta, m1_idx=None, m2_idx=None) -> float:
    """
    Igual que expectimax(), pero con poda α–β en los nodos de agente (max) y oponente (min).
    stage: 'agent', 'opponent', 'chance1', 'chance2'
    alpha, beta: valores de poda
    """
    # Terminal o profundidad cero
    if state.is_terminal() or depth == 0:
        return evaluate_state(state, context, type_table)
    
    # AGENT (maximiza)
    if stage == 'agent':
        value = float('-inf')
        for i, mv in enumerate(context.p1.moveset):
            v = expectimax_ab(state, context, type_table, depth, 'opponent', alpha, beta, i, None)
            value = max(value, v)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # poda β
        return value

    # OPPONENT (minimiza)
    if stage == 'opponent':
        value = float('inf')
        for j, mv in enumerate(context.p2.moveset):
            v = expectimax_ab(state, context, type_table, depth, 'chance1', alpha, beta, m1_idx, j)
            value = min(value, v)
            beta = min(beta, value)
            if beta <= alpha:
                break  # poda α
        return value

    # CHANCE 1 y CHANCE 2 idénticos a expectimax():
    if stage == 'chance1':
        first = context.p1.stats['velocidad'] >= context.p2.stats['velocidad']
        mv = (context.p1 if first else context.p2).moveset[m1_idx if first else m2_idx]
        p = mv.get('precision', 1.0)
        st_hit  = apply_damage(state.clone(), context,
                               context.p1 if first else context.p2,
                               context.p2 if first else context.p1,
                               mv, type_table, True)
        st_miss = state.clone()
        v_hit  = expectimax_ab(st_hit, context, type_table, depth, 'chance2', alpha, beta, m1_idx, m2_idx)
        v_miss = expectimax_ab(st_miss, context, type_table, depth, 'chance2', alpha, beta, m1_idx, m2_idx)
        return p * v_hit + (1-p) * v_miss

    if stage == 'chance2':
        first = context.p1.stats['velocidad'] >= context.p2.stats['velocidad']
        # si alguien ya muere, paso a siguiente profundidad
        if state.hp1 <= 0 or state.hp2 <= 0:
            return expectimax_ab(state, context, type_table, depth-1, 'agent', alpha, beta)
        mv = (context.p2 if first else context.p1).moveset[m2_idx if first else m1_idx]
        p = mv.get('precision', 1.0)
        st_hit  = apply_damage(state.clone(), context,
                               context.p2 if first else context.p1,
                               context.p1 if first else context.p2,
                               mv, type_table, True)
        st_miss = state.clone()
        v_hit  = expectimax_ab(st_hit, context, type_table, depth-1, 'agent', alpha, beta)
        v_miss = expectimax_ab(st_miss, context, type_table, depth-1, 'agent', alpha, beta)
        return p * v_hit + (1-p) * v_miss

# ----- Decisión del agente con prunning-----
def pick_best_move_ab(state, context, type_table, depth):
    best, best_i = float('-inf'), 0
    alpha, beta = float('-inf'), float('inf')
    for i, mv in enumerate(context.p1.moveset):
        val = expectimax_ab(state, context, type_table, depth, 'opponent', alpha, beta, i, None)
        if val > best:
            best, best_i = val, i
        alpha = max(alpha, best)
    return best_i


# ----- Decisión del agente -----
def pick_best_move(state: GameState, context: GameContext, type_table: TypeTable, depth: int) -> int:
    best, best_i = float('-inf'), 0
    for i, mv in enumerate(context.p1.moveset):
        val = expectimax(state, context, type_table, depth, 'opponent', i, None)
        if val > best:
            best, best_i = val, i
    return best_i
