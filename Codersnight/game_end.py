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


class Xicara(pygame.sprite.Sprite): #NEW
    def __init__(self, tamanho, posicao_top_left):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.tamanho = tamanho
        self.sprites.append(pygame.image.load('Imagens/Coffe empty.png'))
        self.sprites.append(pygame.image.load('Imagens/coffe_fully1.png'))
        self.sprites.append(pygame.image.load('Imagens/coffe_fully2.png'))
        self.sprites.append(pygame.image.load('Imagens/coffe_fully3.png'))
        self.sprites.append(pygame.image.load('Imagens/coffe_fully4.png'))
        self.sprites.append(pygame.image.load('Imagens/coffe_fully5.png'))
        self.sprites.append(pygame.image.load('Imagens/coffe_fully6.png'))
        self.vazia = 0
        self.atual = 1
        self.image = self.sprites[self.vazia]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

        self.rect = self.image.get_rect()
        self.rect.topleft = posicao_top_left
        self.animar = False

    def flutuar(self, posicao):
        self.rect.topleft = posicao
        self.animar = True

    def stop_flutuar(self, posicao):
        self.rect.topleft = posicao
        self.animar = False
        self.image = self.sprites[self.vazia]
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))

    def update(self):
        if self.animar:
            self.atual = self.atual + 0.25
            if self.atual >= len(self.sprites):
                self.atual = 1
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))


def configura_cor_botao(ativo):
    if ativo:
        cor_botao = (80, 200, 255)
        cor_texto = WHITE
    else:
        cor_botao = (210, 210, 210)
        cor_texto = BLACK
    return cor_botao, cor_texto



