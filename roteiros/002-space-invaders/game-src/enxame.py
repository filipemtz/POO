
import random
import pygame
from typing import List

from config_jogo import ConfigJogo
from vetor2d import Vetor2D
from utils import ler_imagem, posicao_retangulo_esta_na_tela
from inimigo import Inimigo


class Enxame:
    def __init__(self):
        self._inimigos: List[Inimigo] = []

        self._criar_enxame()

        self._posicao_enxame = Vetor2D(0, ConfigJogo.Y_ENXAME)

        self._tamanho_enxame = Vetor2D(
            ConfigJogo.N_COLUNAS_ENXAME * (ConfigJogo.TAM_INIMIGO.x +
                                           ConfigJogo.ESPACO_ENTRE_INIMIGOS),
            ConfigJogo.N_LINHAS_ENXAME * (ConfigJogo.TAM_INIMIGO.y + ConfigJogo.ESPACO_ENTRE_INIMIGOS))

        self._velocidade_enxame = Vetor2D(ConfigJogo.VEL_INIMIGO, 0)

    def _criar_enxame(self):
        for i in range(ConfigJogo.N_LINHAS_ENXAME):
            for j in range(ConfigJogo.N_COLUNAS_ENXAME):

                x = j * (ConfigJogo.TAM_INIMIGO.x +
                         ConfigJogo.ESPACO_ENTRE_INIMIGOS)

                y = i * (ConfigJogo.TAM_INIMIGO.y +
                         ConfigJogo.ESPACO_ENTRE_INIMIGOS) + \
                    ConfigJogo.Y_ENXAME

                self._inimigos.append(Inimigo(
                    posicao=Vetor2D(x, y),
                    velocidade=Vetor2D(ConfigJogo.VEL_INIMIGO, 0)
                ))

    def atualiza_estado(self):
        nova_posicao = self._posicao_enxame + self._velocidade_enxame

        if posicao_retangulo_esta_na_tela(
                nova_posicao.x,
                nova_posicao.y,
                self._tamanho_enxame.x,
                self._tamanho_enxame.y):
            self._posicao_enxame = nova_posicao
            for i in self._inimigos:
                i.atualiza_estado()
        else:
            self._velocidade_enxame.x = -self._velocidade_enxame.x
            self._posicao_enxame.y += ConfigJogo.MOVIMENTO_INIMIGO_Y

            for i in self._inimigos:
                i._velocidade.x = -i._velocidade.x
                i._posicao.y += ConfigJogo.MOVIMENTO_INIMIGO_Y

    def desenha(self, tela: pygame.Surface):
        for i in self._inimigos:
            i.desenha(tela)

    def inimigo_aleatorio(self):
        return random.choice(self._inimigos)
