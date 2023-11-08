
import pygame as pg

from config_jogo import ConfigJogo
from vetor2d import Vetor2D


class Tiro:
    def __init__(self, posicao: Vetor2D, tamanho: Vetor2D, cor, velocidade: Vetor2D = Vetor2D()):
        self.posicao = posicao
        self.tamanho = tamanho
        self.cor = cor
        self.velocidade = velocidade

    def atualiza_estado(self):
        self.posicao = self.posicao + self.velocidade

    def esta_na_tela(self):
        return (self.posicao.x >= 0) and \
            (self.posicao.y >= 0) and \
            (self.posicao.x + self.tamanho.x <= ConfigJogo.DIM_TELA.x) and \
            (self.posicao.y + self.tamanho.y <= ConfigJogo.DIM_TELA.y)

    def desenha(self, tela):
        rect = (self.posicao.x,
                self.posicao.y,
                self.tamanho.x,
                self.tamanho.y)

        pg.draw.rect(
            tela,
            self.cor,
            rect
        )
