from coders_night import *


def game_end(final):
    if final == 'derrota':
        derrota()
    elif final == 'vitoria':
        vitoria()


def derrota():
    pass


def vitoria():
    pass


class FiguraClicavel(pygame.sprite.Sprite):
    def __init__(self, meu_sprite, posicao):
        super().__init__()
        self.image = meu_sprite
        self.posicao = posicao
        self.rect = self.image.get_rect(center=self.posicao)


def configura_cor_botao(ativo):
    if ativo:
        cor_botao = (80, 200, 255)
        cor_texto = WHITE
    else:
        cor_botao = (210, 210, 210)
        cor_texto = BLACK
    return cor_botao, cor_texto



