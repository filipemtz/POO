
import pygame

from config_jogo import ConfigJogo
from vetor2d import Vetor2D
from utils import ler_imagem, posicao_retangulo_esta_na_tela


class Jato:
    def __init__(self, posicao: Vetor2D, velocidade: Vetor2D = Vetor2D()):
        self._posicao = posicao
        self._velocidade = velocidade
        self._img = ler_imagem(
            'sprites/jato.png', ConfigJogo.TAM_JOGADOR.as_tuple())

    def atualiza_estado(self):
        nova_posicao = self._posicao + self._velocidade

        if posicao_retangulo_esta_na_tela(
                nova_posicao.x,
                nova_posicao.y,
                ConfigJogo.TAM_JOGADOR.x,
                ConfigJogo.TAM_JOGADOR.y):
            self._posicao = nova_posicao

    def desenha(self, tela: pygame.Surface):
        tela.blit(self._img, self._posicao.as_tuple())
