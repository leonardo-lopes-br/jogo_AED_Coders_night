import pygame.time
from coders_night import *

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class FiguraClicavel(pygame.sprite.Sprite):
    def __init__(self, meu_sprite, posicao):
        super().__init__()
        self.image = meu_sprite
        self.posicao = posicao
        self.rect = self.image.get_rect(center=self.posicao)


class Xicara(pygame.sprite.Sprite):
    def __init__(self, tamanho, posicao_top_left):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.tamanho = tamanho
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'Coffe empty.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'coffe_fully1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'coffe_fully2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'coffe_fully3.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'coffe_fully4.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'coffe_fully5.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'coffe_fully6.png')))
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


class Moon(pygame.sprite.Sprite):
    def __init__(self, tamanho, posicao_top_left):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.posicao = posicao_top_left
        self.tamanho = tamanho
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_moon0.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_moon1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_moon2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_moon3.png')))
        self.vazia = 0
        self.atual = 1
        self.image = self.sprites[self.vazia]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

        self.rect = self.image.get_rect()
        self.rect.topleft = posicao_top_left
        self.animar_bool = False

    def animar(self):
        self.rect.topleft = self.posicao
        self.animar_bool = True

    def stop_animar(self):
        self.rect.topleft = self.posicao
        self.animar_bool = False
        self.image = self.sprites[self.vazia]
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))

    def update(self):
        if self.animar_bool:
            self.atual = self.atual + 0.05
            if self.atual >= len(self.sprites):
                self.atual = 1
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))


class Star(pygame.sprite.Sprite):
    def __init__(self, tamanho, posicao_top_left):
        pygame.sprite.Sprite.__init__(self)
        self.posicao = posicao_top_left
        self.sprites = []
        self.tamanho = tamanho
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_star0.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_star1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_star2.png')))
        self.sprites.append(pygame.image.load(os.path.join('Imagens', 'sprite_star3.png')))
        self.vazia = 0
        self.atual = 1
        self.image = self.sprites[self.vazia]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

        self.rect = self.image.get_rect()
        self.rect.topleft = posicao_top_left
        self.animar_bool = False

    def animar(self):
        self.rect.topleft = self.posicao
        self.animar_bool = True

    def stop_animar(self):
        self.rect.topleft = self.posicao
        self.animar_bool = False
        self.image = self.sprites[self.vazia]
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))

    def update(self):
        if self.animar_bool:
            self.atual = self.atual + 0.05
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


def draw_rect_alpha(superficie, cor, retangulo, width=0):
    shape_surf = pygame.Surface(pygame.Rect(retangulo).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, cor, shape_surf.get_rect(), width=width)
    superficie.blit(shape_surf, retangulo)


def transicao_telas(superficie):
    alfa_transicao = 0
    clock = pygame.time.Clock()
    # Escurecendo a tela
    while alfa_transicao < 190:
        clock.tick(25)
        draw_rect_alpha(superficie, (0, 0, 0, alfa_transicao), (0, 0, 1280, 720))
        alfa_transicao += 10
        pygame.display.flip()
