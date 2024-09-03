from enum import Enum
import random
import time

class MovimentosAgenteLabirinto(Enum):
    CIMA = 1
    BAIXO = 2
    ESQUERDA = 3
    DIREITA = 4

def criar_labirinto(tamanho):
    return [["S" for _ in range(tamanho)] for _ in range(tamanho)]

def exibir_labirinto(labirinto, pos_agente):
    for i, linha in enumerate(labirinto):
        for j, cell in enumerate(linha):
            if (i, j) == pos_agente:
                print("*A*", end=" | ")
            else:
                print(cell, end=" | ")
        print("\n" + "-" * (4 * len(linha) - 1))
    print("\n")

def retornar_movimento(pos, movimento, tamanho):
    x, y = pos
    if movimento == MovimentosAgenteLabirinto.CIMA and x > 0:
        x -= 1
    elif movimento == MovimentosAgenteLabirinto.BAIXO and x < tamanho - 1:
        x += 1
    elif movimento == MovimentosAgenteLabirinto.ESQUERDA and y > 0:
        y -= 1
    elif movimento == MovimentosAgenteLabirinto.DIREITA and y < tamanho - 1:
        y += 1
    return (x, y)

def limpar_vizinhos(labirinto, pos):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto):
            if labirinto[nx][ny] == "S":
                labirinto[nx][ny] = "L"

def movimentar_agente(labirinto, pos_agente, movimento, tamanho):
    # Limpar a posição atual
    labirinto[pos_agente[0]][pos_agente[1]] = "L"

    # Verificar vizinhos e limpar
    limpar_vizinhos(labirinto, pos_agente)

    # Escolher próximo movimento
    proximo_movimento = random.choice(list(MovimentosAgenteLabirinto))
    proximo_pos = retornar_movimento(pos_agente, proximo_movimento, tamanho)

    return proximo_pos

if __name__ == "__main__":
    tamanho_labirinto = 5
    labirinto = criar_labirinto(tamanho_labirinto)
    pos_agente = (2, 2)
    movimento = MovimentosAgenteLabirinto.CIMA

    exibir_labirinto(labirinto, pos_agente)

    while any("S" in linha for linha in labirinto):
        pos_agente = movimentar_agente(labirinto, pos_agente, movimento, tamanho_labirinto)
        exibir_labirinto(labirinto, pos_agente)
        time.sleep(1.5)
