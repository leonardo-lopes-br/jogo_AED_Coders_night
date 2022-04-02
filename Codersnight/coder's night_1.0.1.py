#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importacao do pygame
import pygame
from pygame.locals import *
from sys import exit
import fila
import game_end
# altera o caminho do terminal para o caminho do arquivo
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# inicializacao da library do pygame
pygame.init()
pygame.key.set_repeat(300, 110)  # permite segurar uma tela (como apagar os caracteres com o backspace)

# dimensoes das barras
largura_max = 1000
largura_barra_energia = largura_max
largura_barra_concentracao = largura_max

x_pos_barra_energia = 100
y_pos_barra_energia = 640

x_pos_barra_conc = 100
y_pos_barra_conc = 565

# cores dos objetos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
# cor botao
red_botao = 255
green_botao = 0
# cor barra_energia
red_barra_energia = red_barra_concentracao = 0
green_barra_energia = green_barra_concentracao = 255

# musica de fundo
pygame.mixer.music.load("musiquinha_fundo.flac")
pygame.mixer.music.play(-1)  # tocando infinitamente
# sons
drinking_sound = pygame.mixer.Sound("sound_drinking.mp3")
teclando = pygame.mixer.Sound("one-click.mp3")

# dimensoes da janela do jogo
largura_janela = 1280
altura_janela = 720

# localizacao do botao na tela
x_pos_botao = 250
y_pos_botao = 80

# caixa de texto
x_tam_caixa = 500
y_tam_caixa = 300
x_pos_caixa = largura_janela / 2 - x_tam_caixa / 2
y_pos_caixa = altura_janela / 2 - y_tam_caixa / 2

# definicao das fontes dos textos
fonte_1 = pygame.font.SysFont('arial', 27, True, False)
fonte_2 = pygame.font.SysFont('arial', 22, True, False)

# imagens
img_xicara_cafe = pygame.image.load('xicara.png')
rect_img_xicara_cafe = img_xicara_cafe.get_rect()
# img_1 = pygame.image.load("fundo.jpg")  # imagem teste de fundo

# tela do jogo
tela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Coder's Night")

# clock
clk = pygame.time.Clock()

input_text = ''
cor_input_box = WHITE
texto_base = ''

# Cria uma fila e a preenche com caracteres do arquivo de algoritmos
# Abrindo o arquivo de algoritmos para o jogador digitar
arquivo_algoritmos = open('algoritmos_textos.txt', 'r')
indice_linha_atual = 0  # para finalizar o jogo quando chegar no numero de linhas
numero_linhas_arquivo = 0
linha_arquivo = arquivo_algoritmos.readline()
while linha_arquivo:
    numero_linhas_arquivo += 1
    linha_arquivo = arquivo_algoritmos.readline()

arquivo_algoritmos.seek(0)  # retorna para a primeira linha do arquivo

arquivo_algoritmos.readline()  # ignora a primeira linha, que é o nome do algoritmo
linha_arquivo_atual = ''
fila = fila.Fila()

# Este indice é utilizado para saber a partição atual da 'string' que já foi acertada
indice_caractere_atual = 0

# Define o acesso à caixa de texto como falso
active = False

# Mensagens
# msg_cafe = f"Tomar Café"
msg_barra_energia = f"Barra de Energia"
msg_barra_conc = f"Barra de Concentração"
msg_algoritmo = f'Algoritmo'

while True:
    # Definicao do framerate do jogo
    clk.tick(25)
    # tela.blit(img_1, (0, 0))  # Definicao do fundo do jogo
    tela.fill(BLACK)

    # Controle das cores dinamicas
    # Botao cafe
    if largura_barra_energia >= 400:
        green_botao = 0
        red_botao = 255
    else:
        green_botao = 255
        red_botao = 0

    #  Lógica para troca de linhas no algoritmo
    if fila.vazia():
        indice_linha_atual += 1
        texto_base = ''
        indice_caractere_atual = 0
        linha_arquivo_atual = arquivo_algoritmos.readline()
        linha_arquivo_atual = linha_arquivo_atual[:-1]
        linha_arquivo_atual = linha_arquivo_atual.strip()
        for caractere in linha_arquivo_atual:
            fila.insere(caractere)
            texto_base += caractere

    # Desenhos
    # Barra de energia:
    barra_energia = pygame.draw.rect(tela, (red_barra_energia, green_barra_energia, 0),
                                     (x_pos_barra_energia, y_pos_barra_energia, largura_barra_energia, 40))
    barra_energia_contorno = pygame.draw.rect(tela, WHITE, (x_pos_barra_energia - 2, y_pos_barra_energia - 2,
                                                            largura_barra_energia + 2, 42), 3)
    # Barra de concentracao:
    barra_conc = pygame.draw.rect(tela, (red_barra_concentracao, green_barra_concentracao, 0),
                                  (x_pos_barra_conc, y_pos_barra_conc, largura_barra_concentracao, 40))
    barra_concentracao_contorno = pygame.draw.rect(tela, WHITE, (x_pos_barra_conc - 2, y_pos_barra_conc - 2,
                                                                 largura_barra_concentracao + 2, 42), 3)

    # Porcentagem para controlar a cor das barras (energia e concentração)
    barra_energia_porcentagem = largura_barra_energia / largura_max
    red_barra_energia = (1 - barra_energia_porcentagem) * 255 % 256
    green_barra_energia = barra_energia_porcentagem * 255 % 256

    barra_concentracao_porcentagem = largura_barra_concentracao / largura_max
    red_barra_concentracao = (1 - barra_concentracao_porcentagem) * 255 % 256
    green_barra_concentracao = barra_concentracao_porcentagem * 255 % 256

    # Botao:
    # botao = pygame.draw.rect(tela, (red_botao, green_botao, 0), (x_pos_botao, y_pos_botao, 100, 100))
    # Textos:
    tela_textos = pygame.draw.rect(tela, (51, 153, 255), (x_pos_caixa, y_pos_caixa, x_tam_caixa, y_tam_caixa))
    input_texto_box = pygame.draw.rect(tela, cor_input_box, (x_pos_caixa + 30, y_pos_caixa + 135, x_tam_caixa - 60, 30))
    input_texto_contorno = pygame.draw.rect(tela, BLACK,
                                            (x_pos_caixa + 30, y_pos_caixa + 135, x_tam_caixa - 60, 30), 3)

    # Mostra a sentença algorítica a ser digitada (em branco) -> fica por baixo dos caracteres verdes (corretos)
    linha_arquivo_renderizar = fonte_2.render(linha_arquivo_atual, False, WHITE)
    tela.blit(linha_arquivo_renderizar, (x_pos_caixa + 68, y_pos_caixa + 80))

    # Imprime a partição já correta do texto (a parte correta será verde, sobreposta à expressão branca original)
    texto = ''
    for token in texto_base[0:indice_caractere_atual]:
        texto += token
    msg_texto = f'{texto}'
    msg_format_texto_base = fonte_2.render(msg_texto, False, GREEN)
    tela.blit(msg_format_texto_base, (x_pos_caixa + 68, y_pos_caixa + 80))

    # Formatando textos
    # msg_format_cafe = fonte_1.render(msg_cafe, False, WHITE)
    msg_format_energia = fonte_1.render(msg_barra_energia, False, WHITE)
    msg_format_conc = fonte_1.render(msg_barra_conc, False, WHITE)
    msg_format_algoritmo = fonte_1.render(msg_algoritmo, False, WHITE)
    msg_format_input_text = fonte_2.render(input_text, False, BLACK)
    largura_input_texto = msg_format_input_text.get_width()

    # Colocando textos na tela
    # tela.blit(msg_format_cafe, (200, 20))
    tela.blit(msg_format_energia, (105, 645))
    tela.blit(msg_format_conc, (105, 570))
    tela.blit(msg_format_algoritmo, (x_pos_caixa + 175, y_pos_caixa + 20))
    tela.blit(msg_format_input_text, (x_pos_caixa + 40, y_pos_caixa + 135))


    # Controle da decrementacao das barras
    largura_barra_energia -= 0.4  # valor estava em 1 (retornar)
    # largura_barra_concentracao -= 0.2

    # Eventos do jogo
    for event in pygame.event.get():
        # Evento de saída do jogo
        if event.type == QUIT:
            pygame.quit()
            exit()
        # Deteccao de LEFT CLICK
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Se o usuário clicar na caixa de texto, ativá-la. Se clicar fora da caixa, desativá-la
            if input_texto_box.collidepoint(pos):
                active = True
                cor_input_box = (180, 180, 180)  # uma cor cinza ao clicar na caixa de texto da entrada
            else:
                active = False
                cor_input_box = WHITE  # cor padrão branca quando a entrada não está selecionada

        # Verificando o pressionar das teclas
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif largura_input_texto < 415:
                    input_text += event.unicode
                # Se a fila estiver vazia, o jogador venceu o jogo
                if not fila.vazia() and largura_input_texto < 415:

                    not_unicodes_especiais = event.key != pygame.K_SPACE and event.key != pygame.K_LSHIFT and \
                                             event.key != pygame.K_RSHIFT and event.key != pygame.K_CAPSLOCK and \
                                             event.key != pygame.K_BACKSPACE and event.key != pygame.K_LCTRL and \
                                             event.key != pygame.K_RCTRL and event.key != pygame.K_LALT and \
                                             event.key != pygame.K_RALT and event.key != pygame.K_UP and \
                                             event.key != pygame.K_DOWN and event.key != pygame.K_LEFT and \
                                             event.key != pygame.K_RIGHT
                    # Se a fila não é vazia, verifica se a entrada do usuario é igual à primeira letra da fila e, se
                    # for, a remove e altera a cor da letra acertada para verde (atualiza o vetor de caracteres
                    # corretos)
                    if event.unicode == fila.primeiro.dado:
                        teclando.play()
                        fila.remove()
                        indice_caractere_atual += 1
                    elif not_unicodes_especiais:
                        largura_barra_concentracao -= 40
                        # largura_barra_energia -= 20
                        teclando.play()

    # limpa a caixa de texto de input ao trocar de linha no arquivo
    if fila.vazia():
        input_text = ''

    # Esgotamento da barra de energia
    if largura_barra_energia <= 0 or largura_barra_concentracao <= 0:
        print("Voce perdeu!!!")
        game_end.game_end('derrota')
        pygame.quit()
        exit()

    if indice_linha_atual == numero_linhas_arquivo:
        print("Voce ganhou!!")
        game_end.game_end('vitoria')
        pygame.quit()
        exit()

    # Colocando imagens na tela
    tela.blit(img_xicara_cafe, (x_pos_barra_energia - 15, y_pos_barra_energia))
    pygame.display.flip()
