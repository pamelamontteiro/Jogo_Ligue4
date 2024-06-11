#Aluno: Pamela monteiro 

import random
import sys
import inspect

RED = "\033[1;31m"
BLUE = "\033[1;34m"
RESET = "\033[0;0m"


class Tabuleiro:
    def __init__(self, num_linhas=6, num_colunas=7):
        self.__num_linhas = num_linhas
        self.__num_colunas = num_colunas
        self.__tabuleiro = self.iniciar_tabuleiro()

    def set_tabuleiro(self, linha, coluna, valor):
        self.__tabuleiro[linha][coluna] = valor

    def get_tabuleiro(self):
        return self.__tabuleiro

    def iniciar_tabuleiro(self):
        tabuleiro = []
        for i in range(0, self.__num_linhas):
            tabuleiro.append([])
            for j in range(0, self.__num_colunas):
                tabuleiro[i].append("V")
        return tabuleiro

    def imprimir_tabuleiro(self):
        print("")
        print("     ::: TABULEIRO :::")
        for i in reversed(range(0, self.__num_linhas)):
            for j in range(0, self.__num_colunas):
                if j == 0:
                    print("| ", end="")
                if self.__tabuleiro[i][j] == "V":
                    print("  | ", end="")
                else:
                    sys.stdout.write(RED) if self.__tabuleiro[i][
                        j
                    ] == "R" else sys.stdout.write(BLUE)
                    print("O", end="")
                    sys.stdout.write(RESET)
                    print(" | ", end="")
            print("")
        print("")

    def examinar_tabuleiro(self):
        linhas = [[] for _ in range(self.__num_linhas)]
        colunas = [[] for _ in range(self.__num_colunas)]
        diagonais_principais = [
            [] for _ in range(self.__num_linhas + self.__num_colunas)
        ]
        diagonais_secundarias = [[] for _ in range(len(diagonais_principais))]
        min_diagonais_secundarias = -self.__num_linhas + 1

        for j in range(self.__num_colunas):
            for i in range(self.__num_linhas):
                linhas[i].append(self.__tabuleiro[i][j])
                colunas[j].append(self.__tabuleiro[i][j])
                diagonais_principais[i + j].append(self.__tabuleiro[i][j])
                diagonais_secundarias[i - j - min_diagonais_secundarias].append(
                    self.__tabuleiro[i][j]
                )

        # Confere se houve vitória nas linhas
        if self.checa_vitoria(linhas):
            return False
        if self.checa_vitoria(colunas):
            return False
        if self.checa_vitoria(diagonais_principais):
            return False
        if self.checa_vitoria(diagonais_secundarias):
            return False

        return True

    def checa_vitoria(self, vetor):
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

    def ver_se_tabuleiro_esta_cheio(self):
        cheio = True
        for linha in self.__tabuleiro:
            if "V" in linha:
                cheio = False
        return cheio


class Jogador:
    def __init__(self, nome_jogador):
        self.__nome_jogador = nome_jogador

    def get_nome_jogador(self):
        return self.__nome_jogador

    def solicitar_jogada(self, num_colunas):
        jogada = input(
            f"Jogador {self.__nome_jogador}, digite qual coluna será colocada sua peça (de 1 a {num_colunas}): "
        )
        return jogada


class Robo(Jogador):
    def __init__(self, nome_jogador):
        super().__init__(nome_jogador)

    def solicitar_jogada(self, num_colunas):
        jogadas = [1, 2, 3, 4, 5, 6, 7]
        jogada = random.choice(jogadas)
        return jogada


class Ligue4:
    def __init__(self, tabuleiro: Tabuleiro, jogador1, jogador2):
        self.__tabuleiro = tabuleiro
        self.__jogador1 = jogador1
        self.__jogador2 = jogador2

    def comeco(self, modo):
        if int(modo) == 1 or int(modo) == 2:
            self.jogar()
        else:
            self.comeco()

    def solicitar_jogada(self, jogador, jogador_1):
        jogada = jogador.solicitar_jogada(7)
        jogada = int(jogada)

        if jogada < 1 or jogada > 7:
            if inspect.isclass(Jogador):
                print("Jogada inválida, tente novamente.")
            self.solicitar_jogada(jogador, jogador_1)

        jogada = jogada - 1
        coluna_cheia = True
        for linha in self.__tabuleiro.get_tabuleiro():
            if linha[jogada] == "V":
                coluna_cheia = False
        if coluna_cheia:
            print("Coluna cheia, tente novamente.")
            self.solicitar_jogada(jogador, jogador_1)

        if inspect.isclass(Robo):
            print(f"Computador jogou na coluna {jogada + 1}")

        copia_tabuleiro = self.__tabuleiro.get_tabuleiro()
        for idx, linha in enumerate(copia_tabuleiro):
            if linha[jogada] == "V":
                if jogador_1:
                    self.__tabuleiro.set_tabuleiro(idx, jogada, "R")
                else:
                    self.__tabuleiro.set_tabuleiro(idx, jogada, "B")
                break

    def jogar(self):
        print(
            f"{self.__jogador1.get_nome_jogador()} vai ser as peças vermelhaas e {self.__jogador2.get_nome_jogador()} vai ser as peças azuis"
        )
        self.__tabuleiro.imprimir_tabuleiro()
        continua = True
        jogador_1 = True
        while continua:
            if jogador_1:
                self.solicitar_jogada(self.__jogador1, jogador_1)
            else:
                self.solicitar_jogada(self.__jogador2, jogador_1)

            self.__tabuleiro.imprimir_tabuleiro()
            continua = self.__tabuleiro.examinar_tabuleiro()
            if continua == False:
                if jogador_1:
                    print(f"{self.__jogador1.get_nome_jogador()} venceu!")
                else:
                    print(f"{self.__jogador2.get_nome_jogador()} venceu!")
            if self.__tabuleiro.ver_se_tabuleiro_esta_cheio():
                print("Empate!")
                continua = False
            jogador_1 = not jogador_1


def main():
    tabuleiro = Tabuleiro()
    jogador_1 = Jogador("Jogador 1")
    print("::: LIGUE4 :::\n")
    modo_de_jogo = input(
        "Que modo de jogo deseja jogar?\n\n1. Humano X Humano\n2. Humano X Computador\nDigite o número da opção: "
    )
    if int(modo_de_jogo) == 1:
        jogador_2 = Jogador("Jogador 2")
    else:
        jogador_2 = Robo("Computador")
    jogo = Ligue4(tabuleiro, jogador_1, jogador_2)
    jogo.comeco(modo_de_jogo)


if __name__ == "__main__":
    main()
