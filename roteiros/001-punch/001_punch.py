
import math
import pygame
import random 
from typing import Tuple

def ler_imagem(caminho: str, tamanho: Tuple[int, int]):
    # le a imagem do arquivo
    image = pygame.image.load(caminho)

    # redimensiona a imagem para o tamanho especificado 
    image = pygame.transform.scale(image, tamanho)

    # ajusta o colorkey para dar suporte para transparencia
    image = image.convert_alpha()

    return image


def polar2cart(magnitude: float, angulo: float):
    x = magnitude * math.cos(angulo)
    y = magnitude * math.sin(angulo)
    return x, y


pygame.init()
tela = pygame.display.set_mode((700, 700))

punho = ler_imagem('sprites/fist.png', (80, 80))
feliz = ler_imagem('sprites/smile.png', (80, 80))
triste = ler_imagem('sprites/painful.png', (80, 80))

feliz_x = 320
feliz_y = 240

feliz_magn = 0.1
feliz_angulo = random.uniform(-math.pi, math.pi)

punho_x = 320
punho_y = 240

punho_vx = 0
punho_vy = 0

sair = False
frames_triste = 0

while not sair:
    # tratamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = True

    teclas_pressionadas = pygame.key.get_pressed()
    
    # movimento na horizontal
    if teclas_pressionadas[pygame.K_a]:
        punho_vx = -0.1
    elif teclas_pressionadas[pygame.K_d]:
        punho_vx = 0.1
    else: 
        punho_vx = 0.0
    
    # movimento na vertical
    if teclas_pressionadas[pygame.K_s]:
        punho_vy = 0.1
    elif teclas_pressionadas[pygame.K_w]:
        punho_vy = -0.1
    else: 
        punho_vy = 0.0

    if teclas_pressionadas[pygame.K_j]:
        # obtem o retangulo ao redor do punho na posicao atual do punho
        punho_rect = punho.get_rect(x=punho_x, y=punho_y)
        # obtem o retangulo ao redor do rosto feliz na posicao atual do rosto feliz
        feliz_rect = feliz.get_rect(x=feliz_x, y=feliz_y)
        # verifca se houve colisao entre os dois retangulos
        if punho_rect.colliderect(feliz_rect):
            frames_triste = 500

    tela.fill("white")
    pygame.draw.circle(tela, "red", (100, 100), 10)
    pygame.draw.rect(tela, "green", (200, 300, 100, 200))

    feliz_vx, feliz_vy = polar2cart(feliz_magn, feliz_angulo)
    
    feliz_x += feliz_vx
    feliz_y += feliz_vy

    punho_x += punho_vx
    punho_y += punho_vy
        
    if (feliz_x < 0) or (feliz_x > tela.get_width()) or \
        (feliz_y < 0) or (feliz_y > tela.get_height()):
        feliz_angulo = random.uniform(-math.pi, math.pi)
    
    if punho_x < 0: punho_x = 0
    if punho_y < 0: punho_y = 0
    if punho_x + punho.get_width() > tela.get_width(): punho_x = tela.get_width()
    if punho_y + punho.get_height() > tela.get_height(): punho_y = tela.get_height()
    
    if frames_triste == 0:
        tela.blit(feliz, (feliz_x, feliz_y))
    else:
        tela.blit(triste, (feliz_x, feliz_y))    
        frames_triste -= 1
    
    tela.blit(punho, (punho_x, punho_y))
    
    pygame.display.flip()

pygame.quit()