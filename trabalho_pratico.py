import random
import sys

NUM_COLUNAS = 7
NUM_LINHAS = 6
RED = "\033[1;31m"
BLUE = "\033[1;34m"
RESET = "\033[0;0m"


def comeco():
    print("::: LIGUE4 :::\n")
    modo_de_jogo = input(
        "Que modo de jogo deseja jogar?\n\n1. Humano X Humano\n2. Humano X Computador\nDigite o número da opção: "
    )
    tabuleiro = iniciar_tabuleiro()

    if int(modo_de_jogo) == 1:
        jogar_contra_humano(tabuleiro)
    elif int(modo_de_jogo) == 2:
        jogar_contra_maquina(tabuleiro)
    else:
        comeco()


def iniciar_tabuleiro():
    tabuleiro = []
    for i in range(0, NUM_LINHAS):
        tabuleiro.append([])
        for j in range(0, NUM_COLUNAS):
            tabuleiro[i].append("V")
    return tabuleiro


def imprimir_tabuleiro(tabuleiro):
    print("")
    print("     ::: TABULEIRO :::")
    for i in reversed(range(0, NUM_LINHAS)):
        for j in range(0, NUM_COLUNAS):
            if j == 0:
                print("| ", end="")
            if tabuleiro[i][j] == "V":
                print("  | ", end="")
            else:
                sys.stdout.write(RED) if tabuleiro[i][j] == "R" else sys.stdout.write(
                    BLUE
                )
                print("O", end="")
                sys.stdout.write(RESET)
                print(" | ", end="")

        print("")
    print("")


def jogar_contra_humano(tabuleiro):
    print("Jogador 1 vai ser as peças R e Jogador 2 vai ser as peças B")
    imprimir_tabuleiro(tabuleiro)
    continua = True
    jogador_1 = True
    while continua:
        if jogador_1:
            tabuleiro = solicitar_jogada(tabuleiro, 1, True)
        else:
            tabuleiro = solicitar_jogada(tabuleiro, 2, True)

        imprimir_tabuleiro(tabuleiro)
        continua = examinar_tabuleiro(tabuleiro)
        if continua == False:
            if jogador_1:
                print("Jogador 1 venceu!")
            else:
                print("Jogador 2 venceu!")
        if ver_se_tabuleiro_esta_cheio(tabuleiro):
            print("Empate!")
            continua = False
        jogador_1 = not jogador_1


def jogar_contra_maquina(tabuleiro):
    print("Jogador 1 vai ser as peças R e Computador vai ser as peças B")
    imprimir_tabuleiro(tabuleiro)
    continua = True
    jogador_1 = True
    while continua:
        if jogador_1:
            tabuleiro = solicitar_jogada(tabuleiro, 1, True)
        else:
            tabuleiro = solicitar_jogada(tabuleiro, 2, False)

        imprimir_tabuleiro(tabuleiro)
        continua = examinar_tabuleiro(tabuleiro)
        if continua == False:
            if jogador_1:
                print("Jogador 1 venceu!")
            else:
                print("computador venceu!")
        if ver_se_tabuleiro_esta_cheio(tabuleiro):
            print("Empate!")
            continua = False
        jogador_1 = not jogador_1


def solicitar_jogada(tabuleiro, jogador, humano):
    if humano:
        jogada = input(
            f"Jogador {jogador}, digite qual coluna será colocada sua peça (de 1 a {NUM_COLUNAS}): "
        )
    else:
        jogadas = [1, 2, 3, 4, 5, 6, 7]
        jogada = random.choice(jogadas)

    jogada = int(jogada)

    if jogada < 1 or jogada > NUM_COLUNAS:
        if humano:
            print("Jogada inválida, tente novamente.")
        solicitar_jogada(tabuleiro, jogador, humano)

    jogada = jogada - 1
    coluna_cheia = True
    for linha in tabuleiro:
        if linha[jogada] == "V":
            coluna_cheia = False
    if coluna_cheia:
        print("Coluna cheia, tente novamente.")
        solicitar_jogada(tabuleiro, jogador, humano)

    if not humano:
        print(f"Computador jogou na coluna {jogada + 1}!")
    copia_tabuleiro = tabuleiro
    for idx, linha in enumerate(copia_tabuleiro):
        if linha[jogada] == "V":
            if jogador == 1:
                tabuleiro[idx][jogada] = "R"
            else:
                tabuleiro[idx][jogada] = "B"
            break
    return tabuleiro


def examinar_tabuleiro(tabuleiro):
    linhas = [[] for _ in range(NUM_LINHAS)]
    colunas = [[] for _ in range(NUM_COLUNAS)]
    diagonais_principais = [[] for _ in range(NUM_LINHAS + NUM_COLUNAS)]
    diagonais_secundarias = [[] for _ in range(len(diagonais_principais))]
    min_diagonais_secundarias = -NUM_LINHAS + 1

    for j in range(NUM_COLUNAS):
        for i in range(NUM_LINHAS):
            linhas[i].append(tabuleiro[i][j])
            colunas[j].append(tabuleiro[i][j])
            diagonais_principais[i + j].append(tabuleiro[i][j])
            diagonais_secundarias[i - j - min_diagonais_secundarias].append(
                tabuleiro[i][j]
            )

    # Confere se houve vitória nas linhas
    if checa_vitoria(linhas):
        return False
    if checa_vitoria(colunas):
        return False
    if checa_vitoria(diagonais_principais):
        return False
    if checa_vitoria(diagonais_secundarias):
        return False

    return True


def checa_vitoria(vetor):
    for lista in vetor:
        if len(lista) >= 4:
            valor_anterior = ""
            contador = 0
            for valor in lista:
                if valor_anterior == "":
                    valor_anterior = valor
                else:
                    if (
                        valor_anterior == valor
                        and valor_anterior != "V"
                        and valor != "V"
                    ):
                        contador = contador + 1
                    else:
                        contador = 0
                valor_anterior = valor
                if contador == 3:
                    return True
    return False


def ver_se_tabuleiro_esta_cheio(tabuleiro):
    cheio = True
    for linha in tabuleiro:
        if "V" in linha:
            cheio = False
    return cheio


def main():
    comeco()


if __name__ == "__main__":
    main()
