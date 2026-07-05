import json
import random
import os

bairros = [f"Ponto_{i}" for i in range(1, 31)]
arestas = []

for i in range(29):
    arestas.append((bairros[i], bairros[i + 1], random.randint(5, 25)))

while len(arestas) < 50:
    u = random.choice(bairros)
    v = random.choice(bairros)
    if u != v:
        arestas.append((u, v, random.randint(5, 30)))

mapa = {"vertices": bairros, "arestas": arestas}
caminho = os.path.join("data", "logistica.json")
with open(caminho, "w", encoding="utf-8") as f:
    json.dump(mapa, f, indent=4)
print("Mapa de logística gerado com sucesso com 30 vértices e 50 arestas!")