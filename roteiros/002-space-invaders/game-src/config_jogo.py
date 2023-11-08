
from vetor2d import Vetor2D


class ConfigJogo:
    DIM_TELA = Vetor2D(700, 700)
    TAM_JOGADOR = Vetor2D(30, 50)
    VEL_JOGADOR = 0.3
    Y_JOGADOR = int(DIM_TELA.y * 0.9)
    TAM_INIMIGO = Vetor2D(30, 30)
    VEL_INIMIGO = 0.1

    MOVIMENTO_INIMIGO_Y = int(0.01 * DIM_TELA.x)
    N_LINHAS_ENXAME = 4
    N_COLUNAS_ENXAME = 12
    Y_ENXAME = int(0.1 * DIM_TELA.y)
    ESPACO_ENTRE_INIMIGOS = int(0.01 * DIM_TELA.x)

    TAM_TIRO = Vetor2D(int(0.004 * DIM_TELA.x), int(0.02 * DIM_TELA.x))
    VEL_TIRO = 0.4
    ESPERA_TIRO = 0.5

    PONTUACAO_MATAR_INIMIGO = 2
    PONTUACAO_JATO_RECEBER_TIRO = 100
