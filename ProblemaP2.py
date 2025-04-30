import sys
from collections import deque

def find(parent, x):
    # Encuentra la raíz con compresión de rutas
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(parent, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra != rb:
        parent[ra] = rb

def solucion(n, energy_start, robots, powers):
    # DSU para teletransportes (plataformas con robots)
    dsu_parent = list(range(n + 2))
    for r in robots:
        if 0 <= r <= n:
            union(dsu_parent, r, r + 1)

    # visited_energy[i] = mejor energía al llegar a i
    visited_energy = [-1] * (n + 1)
    visited_energy[0] = energy_start

    # Estructuras para estados sin clases
    state_pos = [0]
    state_energy = [energy_start]
    state_parent = [-1]
    state_action = [None]

    dq = deque([0])  # cola de índices de estado

    while dq:
        idx = dq.popleft()
        pos = state_pos[idx]
        energy = state_energy[idx]

        # Meta alcanzada
        if pos == n:
            # Reconstruir ruta
            actions = []
            cur = idx
            while state_parent[cur] != -1:
                actions.append(state_action[cur])
                cur = state_parent[cur]
            actions.reverse()
            return actions

        # 1) Caminar normal
        for delta, token in ((1, 'C+'), (-1, 'C-')):
            j = pos + delta
            if 0 <= j <= n and j not in robots:
                new_energy = energy
                if new_energy > visited_energy[j]:
                    visited_energy[j] = new_energy
                    # crear nuevo estado
                    state_parent.append(idx)
                    state_action.append(token)
                    state_pos.append(j)
                    state_energy.append(new_energy)
                    dq.append(len(state_pos) - 1)

        # 2) Salto potenciado
        if pos in powers:
            k = powers[pos]
            for delta, token in ((k, 'S+'), (-k, 'S-')):
                j = pos + delta
                if 0 <= j <= n and j not in robots:
                    new_energy = energy
                    if new_energy > visited_energy[j]:
                        visited_energy[j] = new_energy
                        state_parent.append(idx)
                        state_action.append(token)
                        state_pos.append(j)
                        state_energy.append(new_energy)
                        dq.append(len(state_pos) - 1)

        # 3) Teletransportación
        low = max(0, pos - energy)
        high = min(n, pos + energy)
        j = find(dsu_parent, low)
        while j <= high:
            new_energy = energy - abs(pos - j)
            if new_energy >= 0 and new_energy > visited_energy[j]:
                visited_energy[j] = new_energy
                state_parent.append(idx)
                state_action.append(f'T{j - pos}')
                state_pos.append(j)
                state_energy.append(new_energy)
                dq.append(len(state_pos) - 1)
            union(dsu_parent, j, j + 1)
            j = find(dsu_parent, j)

    # No se pudo
    return None


def main():
    input = sys.stdin.readline
    line = input().strip()
    if not line:
        return
    T = int(line)
    out = []
    for _ in range(T):
        # Leer n y e
        line = input().strip()
        while not line:
            line = input().strip()
        n, e = map(int, line.split())
        # Robots
        robots_line = input().strip()
        robots = set(map(int, robots_line.split())) if robots_line else set()
        # Powers
        powers_line = input().strip()
        parts = list(map(int, powers_line.split())) if powers_line else []
        powers = {parts[i]: parts[i+1] for i in range(0, len(parts), 2)}

        actions = solucion(n, e, robots, powers)
        if actions is None:
            out.append('NO SE PUEDE')
        else:
            out.append(f"{len(actions)} {' '.join(actions)}")
    sys.stdout.write("\n".join(out))

if __name__ == '__main__':
    main()
