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

COR_CIANO = "\033[36m"
COR_PADRAO = "\033[0m"

def exibir_labirinto(labirinto, pos_agente):
    for i, linha in enumerate(labirinto):
        for j, cell in enumerate(linha):
            if (i, j) == pos_agente:
                if (i, j) == (2, 2) or (i, j) == (2, 1):
                    print(f"{COR_CIANO}A{COR_PADRAO}", end=" ¦ ")
                else:
                    print(f"{COR_CIANO}A{COR_PADRAO}", end=" | ")
            else:
                if (i, j) == (2, 2) or (i, j) == (2, 1):
                    print(cell, end=" ¦ ")
                else:
                    print(cell, end=" | ")
        print("\n" + "-" * (4 * len(linha) - 1))
    print("\n")

def retornar_movimento(pos, movimento, tamanho):
    x, y = pos
    movimento_valido = False
    
    while not movimento_valido:
        if movimento == MovimentosAgenteLabirinto.CIMA and x > 0:
            x -= 1
            movimento_valido = True
        elif movimento == MovimentosAgenteLabirinto.BAIXO and x < tamanho - 1:
            x += 1
            movimento_valido = True
        elif movimento == MovimentosAgenteLabirinto.ESQUERDA and y > 0:
            y -= 1
            movimento_valido = True
        elif movimento == MovimentosAgenteLabirinto.DIREITA and y < tamanho - 1:
            y += 1
            movimento_valido = True
        else:
            movimento = random.choice(list(MovimentosAgenteLabirinto))
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

def carregar(pos_agente, base_carregamento, bateria, porcentagem_critica_bateria, labirinto):
    bateria -= (bateria_informada * 0.05)
    if bateria <= porcentagem_critica_bateria:
        print(f"Bateria atual: {bateria:.0f}%")
        print("Indo para a base de carregamento...\n")
        exibir_labirinto(labirinto, pos_agente)
        # Movimento contínuo até a base
        while pos_agente != base_carregamento and bateria > 0:
            pos_agente = list(pos_agente)
            
            # Movimento vertical
            if pos_agente[0] < base_carregamento[0]:
                pos_agente[0] += 1
            elif pos_agente[0] > base_carregamento[0]:
                pos_agente[0] -= 1
            
            # Movimento horizontal
            elif pos_agente[1] < base_carregamento[1]:
                pos_agente[1] += 1
            elif pos_agente[1] > base_carregamento[1]:
                pos_agente[1] -= 1

            # Converta a lista de volta para uma tupla
            pos_agente = tuple(pos_agente)
            bateria -= (bateria_informada * 0.01)  # Simulação de gasto de bateria a cada movimento
            
            print(f"Bateria atual: {bateria:.0f}%\n")
            exibir_labirinto(labirinto, pos_agente)
            time.sleep(1.5)  # Simulação do tempo para movimento
        
        if bateria <= 0:
            print("\n\nOps! Parece que o seu aspirador descarregou!")
            exit()
        
        # Se o agente chegar à base de carregamento
        if pos_agente == base_carregamento:
            print("Carregando...")
            while bateria < bateria_informada:
                bateria += (bateria_informada * 0.10)
                bateria = min(bateria, bateria_informada)
                print(f"Bateria recarregada: {bateria:.0f}% | {bateria//10:.0f} / {bateria_informada//10:.0f}")
                time.sleep(1)
            
            print("Bateria recarregada para 100% na base de carregamento.\n")
    return pos_agente, bateria

def sujar(labirinto):
    listaDeSujeira = []
    for i, linha in enumerate(labirinto):
        for j, cell in enumerate(linha):        
            if cell == 'L':
                coordenada = (i, j)
                listaDeSujeira.append(coordenada)
    if listaDeSujeira:
        gerarNovaSujeira = random.choice(listaDeSujeira)
        labirinto[gerarNovaSujeira[0]][gerarNovaSujeira[1]] = 'S'

if __name__ == "__main__":
    tamanho_labirinto = 5
    labirinto = criar_labirinto(tamanho_labirinto)
    bateria = 100
    bateria_informada = bateria
    porcentagem_critica_bateria = 20
    pos_agente = (2, 2)
    base_carregamento = (2, 2)
    print(f"Bateria atual: {bateria:.0f}%\n")
    exibir_labirinto(labirinto, pos_agente)

    while any("S" in linha for linha in labirinto):
        if bateria > porcentagem_critica_bateria:
            pos_agente = movimentar_agente(labirinto, pos_agente, random.choice(list(MovimentosAgenteLabirinto)), tamanho_labirinto)
        pos_agente, bateria = carregar(pos_agente, base_carregamento, bateria, porcentagem_critica_bateria, labirinto)
        sujar(labirinto)
        print(f"Bateria atual: {bateria:.0f}%\n")
        exibir_labirinto(labirinto, pos_agente)
        time.sleep(1.5)
