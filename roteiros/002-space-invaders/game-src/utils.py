
import pygame
from typing import Tuple
from config_jogo import ConfigJogo


def ler_imagem(caminho: str, tamanho: Tuple[int, int]):
    # le a imagem do arquivo
    image = pygame.image.load(caminho)

    # redimensiona a imagem para o tamanho especificado
    image = pygame.transform.scale(image, tamanho)

    # ajusta o colorkey para dar suporte para transparencia
    image = image.convert_alpha()

    return image


def posicao_retangulo_esta_na_tela(x: float, y: float, w: float, h: float):
    if (x < 0) or (y < 0) or \
            (x + w > ConfigJogo.DIM_TELA.x) or (y + h > ConfigJogo.DIM_TELA.y):
        return False

    return True
