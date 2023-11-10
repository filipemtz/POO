
import sys
import pygame
import random
from time import time
from typing import Tuple, List

from tiro import Tiro
from vetor2d import Vetor2D
from cronometro import Cronometro
from config_jogo import ConfigJogo
from jato import Jato
from inimigo import Inimigo
from enxame import Enxame


class SpaceInvaders:
    def __init__(self):
        pygame.init()

        self._tela = pygame.display.set_mode((
            ConfigJogo.DIM_TELA.x,
            ConfigJogo.DIM_TELA.y
        ))

        # salvamos a fonte para nao precisar criar ela toda hora
        self._font = pygame.font.SysFont(None, 48)

        self._jato = Jato(posicao=Vetor2D(
            (ConfigJogo.DIM_TELA.x - ConfigJogo.TAM_JOGADOR.x) // 2,
            ConfigJogo.Y_JOGADOR
        ))

        self._enxame = Enxame()

        self._tiros_jato: List[Tiro] = []
        self._tiros_inimigos: List[Tiro] = []
        self._cron_espera_tiro_jato = Cronometro()
        self._cron_espera_tiro_enxame = Cronometro()

        self._pontuacao = 0

    def executar(self):
        while True:
            self.tratamento_eventos()
            self.atualiza_estado()
            self.desenha()

    def tratamento_eventos(self):
        eventos = pygame.event.get()

        if pygame.key.get_pressed()[pygame.K_a]:
            self._jato._velocidade.x = -ConfigJogo.VEL_JOGADOR
        elif pygame.key.get_pressed()[pygame.K_d]:
            self._jato._velocidade.x = ConfigJogo.VEL_JOGADOR
        else:
            self._jato._velocidade.x = 0

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self._cron_espera_tiro_jato.tempo_passado() > ConfigJogo.ESPERA_TIRO:
                self._cria_tiro_jogador()
                self._cron_espera_tiro_jato.reset()

        # evento de saida
        if (pygame.key.get_pressed()[pygame.K_ESCAPE]):
            pygame.quit()
            sys.exit(0)

    def atualiza_estado(self):
        self._jato.atualiza_estado()
        self._enxame.atualiza_estado()

        for tiro in self._tiros_jato:
            tiro.atualiza_estado()

        for tiro in self._tiros_inimigos:
            tiro.atualiza_estado()

        if random.random() < 0.3:
            if self._cron_espera_tiro_enxame.tempo_passado() > ConfigJogo.ESPERA_TIRO:
                if len(self._enxame._inimigos) > 0:
                    inimigo = random.choice(self._enxame._inimigos)
                    self._cria_tiro_inimigo(inimigo)
                    self._cron_espera_tiro_enxame.reset()

        self._trata_colisoes()
        self._remove_tiros_fora_da_tela(self._tiros_inimigos)
        self._remove_tiros_fora_da_tela(self._tiros_jato)

    def desenha(self):
        self._tela.fill("black")
        self._jato.desenha(self._tela)
        self._enxame.desenha(self._tela)

        for tiro in self._tiros_jato:
            tiro.desenha(self._tela)

        for tiro in self._tiros_inimigos:
            tiro.desenha(self._tela)

        self._desenha_pontuacao(self._tela)

        pygame.display.flip()

    def _cria_tiro_jogador(self):
        x = self._jato._posicao.x + ConfigJogo.TAM_JOGADOR.x // 2
        y = self._jato._posicao.y

        self._tiros_jato.append(Tiro(
            posicao=Vetor2D(x, y),
            tamanho=ConfigJogo.TAM_TIRO,
            cor="red",
            velocidade=Vetor2D(0, -ConfigJogo.VEL_TIRO)
        ))

    def _cria_tiro_inimigo(self, inimigo: Inimigo):
        x = inimigo._posicao.x + ConfigJogo.TAM_INIMIGO.x // 2
        y = inimigo._posicao.y + ConfigJogo.TAM_INIMIGO.y

        self._tiros_inimigos.append(Tiro(
            posicao=Vetor2D(x, y),
            tamanho=ConfigJogo.TAM_TIRO,
            cor="blue",
            velocidade=Vetor2D(0, ConfigJogo.VEL_TIRO)
        ))

    def _trata_colisoes(self):
        for idx_tiro, tiro in enumerate(self._tiros_jato):
            for idx_inimigo, inimigo in enumerate(self._enxame._inimigos):
                rect_tiro = pygame.rect.Rect(
                    tiro.posicao.x,
                    tiro.posicao.y,
                    ConfigJogo.TAM_TIRO.x,
                    ConfigJogo.TAM_TIRO.y)

                rect_inimigo = pygame.rect.Rect(
                    inimigo._posicao.x,
                    inimigo._posicao.y,
                    ConfigJogo.TAM_INIMIGO.x,
                    ConfigJogo.TAM_INIMIGO.y)

                if rect_tiro.colliderect(rect_inimigo):
                    self._tiros_jato.pop(idx_tiro)
                    self._enxame._inimigos.pop(idx_inimigo)
                    self._pontuacao += ConfigJogo.PONTUACAO_MATAR_INIMIGO

        rect_jato = pygame.rect.Rect(
            self._jato._posicao.x,
            self._jato._posicao.y,
            ConfigJogo.TAM_JOGADOR.x,
            ConfigJogo.TAM_JOGADOR.y)

        for idx_tiro, tiro in enumerate(self._tiros_inimigos):
            rect_tiro = pygame.rect.Rect(
                tiro.posicao.x,
                tiro.posicao.y,
                ConfigJogo.TAM_TIRO.x,
                ConfigJogo.TAM_TIRO.y)

            if rect_tiro.colliderect(rect_jato):
                self._tiros_inimigos.pop(idx_tiro)
                self._pontuacao -= ConfigJogo.PONTUACAO_JATO_RECEBER_TIRO

    def _remove_tiros_fora_da_tela(self, lst_tiros: List[Tiro]):
        for idx_tiro, tiro in enumerate(lst_tiros):
            if not tiro.esta_na_tela():
                lst_tiros.pop(idx_tiro)

    def _desenha_pontuacao(self, tela: pygame.Surface):
        img = self._font.render(f'{self._pontuacao:03d}',
                                True, (255, 255, 255))
        px = (ConfigJogo.DIM_TELA.x - img.get_width()) // 2
        py = int(ConfigJogo.DIM_TELA.y * 0.02)
        tela.blit(img, (px, py))
