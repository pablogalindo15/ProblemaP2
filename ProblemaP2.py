#!/usr/bin/env python3
import sys
from collections import deque

class State:
    __slots__ = ('pos', 'energy', 'parent', 'action')
    def __init__(self, pos, energy, parent, action):
        self.pos = pos
        self.energy = energy
        self.parent = parent      
        self.action = action      

class DSU:
    def __init__(self, size):
        self.parent = list(range(size))
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx != ry:
            self.parent[rx] = ry

def solve_case(n, energy_start, robots, powers):
    # Prepara DSU para saltar sobre ls paltaformas
    dsu = DSU(n + 2)
    for r in robots:
        if 0 <= r <= n:
            dsu.union(r, r + 1)

    visited_energy = [-1] * (n + 1)
    dq = deque()
    #Estado inicial
    dq.append(State(0, energy_start, None, None))
    visited_energy[0] = energy_start

    while dq:
        st = dq.popleft()
        pos, energy = st.pos, st.energy

        #Si llegamos a la meta, reconstruimos ruta:
        if pos == n:
            actions = []
            cur = st
            while cur.parent is not None:
                actions.append(cur.action)
                cur = cur.parent
            actions.reverse()
            return actions

        # 1.Caminar normal
        for delta, token in ((1, "C+"), (-1, "C-")):
            j = pos + delta
            if 0 <= j <= n and j not in robots:
                if energy > visited_energy[j]:
                    visited_energy[j] = energy
                    dq.append(State(j, energy, st, token))

        # 2. Salto potenciado
        if pos in powers:
            k = powers[pos]
            for delta, token in ((k, "S+"), (-k, "S-")):
                j = pos + delta
                if 0 <= j <= n and j not in robots:
                    if energy > visited_energy[j]:
                        visited_energy[j] = energy
                        dq.append(State(j, energy, st, token))

        # 3. Teletransportación (DSU para saltar plataformas con robots)
        low = max(0, pos - energy)
        high = min(n, pos + energy)
        j = dsu.find(low)
        while j <= high:
            new_energy = energy - abs(pos - j)
            if new_energy >= 0 and new_energy > visited_energy[j]:
                visited_energy[j] = new_energy
                dq.append(State(j, new_energy, st, f"T{j - pos}"))
            dsu.union(j, j + 1)
            j = dsu.find(j)

    # No es posible
    return None

def main():
    input = sys.stdin.readline
    T_line = input().strip()
    if not T_line:
        return
    T = int(T_line)
    out = []
    for _ in range(T):
        # Leer caso
        line = input().strip()
        while not line:
            line = input().strip()
        n, e = map(int, line.split())
        robots = set(map(int, input().split())) if n >= 0 else set()
        parts = list(map(int, input().split()))
        powers = {parts[i]: parts[i+1] for i in range(0, len(parts), 2)}

        res = solve_case(n, e, robots, powers)
        if res is None:
            out.append("NO SE PUEDE")
        else:
            out.append(f"{len(res)} {' '.join(res)}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
