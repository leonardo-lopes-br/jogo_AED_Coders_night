#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importacao do pygame
import pygame
from pygame.locals import *
from sys import exit
import fila
import game_end
from math import sin
from random import randint
# altera o caminho do terminal para o caminho do arquivo
import os

# cores dos objetos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 50, 0)
BLUE = (0, 50, 255)
YELLOW = (255, 255, 0)
ROXO = (153, 51, 153)

COR_ALGORITMOS = [GREEN, YELLOW, ROXO]


def coders_night():
    # inicializacao da library do pygame
    pygame.init()
    # pygame.key.set_repeat(300, 110)  # permite segurar uma tela_principal (como apagar os caracteres com o backspace)

    # dimensoes da janela do jogo
    largura_janela = 1280
    altura_janela = 720

    # tela_principal do jogo
    tela_principal = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Coder's Night")

    # dimensoes das barras
    largura_max = 1000
    largura_barra_energia = largura_max
    largura_barra_concentracao = largura_max

    x_pos_barra_energia = 100
    y_pos_barra_energia = 640

    x_pos_barra_conc = 100
    y_pos_barra_conc = 565

    # cor barra_energia
    red_barra_energia = red_barra_concentracao = 0
    green_barra_energia = green_barra_concentracao = 255

    # musica de fundo
    pygame.mixer.music.load(os.path.join('Sons', "musiquinha_fundo.flac"))
    pygame.mixer.music.set_volume(0.4)

    # sons
    drinking_sound = pygame.mixer.Sound(os.path.join('Sons', "som_bebendo_cafe.mpeg"))
    drinking_sound.set_volume(0.2)
    teclando = pygame.mixer.Sound(os.path.join('Sons', "one-click.mp3"))
    teclando.set_volume(0.65)
    resposta_errada = pygame.mixer.Sound(os.path.join('Sons', 'resposta_errada.mp3'))
    resposta_errada.set_volume(0.3)
    som_acabou_o_tempo = pygame.mixer.Sound(os.path.join('Sons', 'som_acabou_o_tempo.mpeg'))
    som_acabou_o_tempo.set_volume(0.15)

    # caixa de texto
    x_tam_caixa = 500
    y_tam_caixa = 300
    x_pos_caixa = largura_janela / 2 - x_tam_caixa / 2
    y_pos_caixa = altura_janela / 2 - y_tam_caixa / 2

    # definicao das fontes dos textos
    fonte_1 = pygame.font.SysFont('arial', 27, True, False)
    fonte_2 = pygame.font.SysFont('arial', 22, True, False)
    fonte_timer = pygame.font.SysFont('Rubik Wet Paint', 35, False, True)

    # imagens
    img_xicara_cafe = pygame.image.load(os.path.join('Imagens', 'xicara.png')).convert_alpha()
    img_xicara_cafe = pygame.transform.scale(img_xicara_cafe, (55, 55))
    valor_seno_alfa_xicara = 1.57

    img_cerebro = pygame.image.load(os.path.join('Imagens', 'brain.png')).convert_alpha()
    img_cerebro = pygame.transform.scale(img_cerebro, (55, 55))

    # criando os objetos
    xicara_cafe = game_end.FiguraClicavel(img_xicara_cafe, (x_pos_barra_energia - 50, y_pos_barra_energia + 15))
    cerebro = game_end.FiguraClicavel(img_cerebro, (x_pos_barra_conc - 50, y_pos_barra_conc + 15))

    # Grupo para os sprites
    grupo_sprites_permanentes = pygame.sprite.Group()
    grupo_sprites_permanentes.add(xicara_cafe, cerebro)

    # Variaveis para tremer a tela_principal_principal com um erro do usuário
    screen_shake = 0
    deslocamento = [0, 0]

    # clock
    clk = pygame.time.Clock()

    # variáveis de input e texto base a ser digitado
    input_text = ''
    cor_input_box = (180, 180, 180)  # começa com um tom cinza quando está selecionado
    texto_base = ''

    # Cria uma fila e a preenche com caracteres do arquivo de algoritmos
    # Abrindo o arquivo de algoritmos para o jogador digitar
    arquivo_algoritmos = open(os.path.join('Textos', 'algoritmos_textos.txt'), 'r')
    indice_linha_atual = 0  # para finalizar o jogo quando chegar no numero de linhas
    numero_linhas_arquivo = 0
    numero_hashtags = 0
    linha_arquivo = arquivo_algoritmos.readline()
    while linha_arquivo:
        linha_arquivo = linha_arquivo[:-1]
        if not linha_arquivo == '#':
            numero_linhas_arquivo += 1
        else:
            numero_hashtags += 1
        linha_arquivo = arquivo_algoritmos.readline()

    arquivo_algoritmos.seek(0)  # retorna para a primeira linha do arquivo
    linha_arquivo_atual = ''
    minha_fila = fila.Fila()
    cor_algoritmo_atual = -1

    # Este indice é utilizado para saber a partição atual da 'string' que já foi acertada
    indice_caractere_atual = 0

    # Define o acesso à caixa de texto como falso
    active = False
    timer_cursor = 0.5

    # Mensagens
    codigo_indice = -1
    titulos_algoritmos = ['Numero primo', 'PA', 'Sacar no Banco']

    msg_progresso = f'Progresso'
    x_pos_progresso = x_pos_caixa + x_tam_caixa / 2
    y_pos_progresso = y_pos_caixa + y_tam_caixa - 95

    msg_input_placeholder = f'Digite aqui...'
    x_pos_placeholder = x_pos_caixa + 40
    y_pos_placeholder = y_pos_caixa + 140

    # Timer para digitar o trecho de código
    delay_trecho_codigo = 20  # estava 15 (e tava dificil)
    timer_trecho_codigo = delay_trecho_codigo

    # Resetando tudo no jogo
    # input_text = ''
    # cor_input_box = (180, 180, 180)  # começa com um tom cinza quando está selecionado
    # texto_base = ''
    # pygame.mixer.music.pause()
    # while True:
    #    for event in pygame.event.get():
    #        # Evento de saída do jogo
    #        if event.type == QUIT:
    #            pygame.quit()
    #            exit()
    #        if event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_UP:
    #                print('entrei')
    #                pygame.mixer.music.play(-1)  # tocando infinitamente
    #                return
    tela_menu_inicial = False

    # Laço principal do jogo
    while True:
        # Caso o jogador retorne à ela inicial do jogo
        if tela_menu_inicial:
            tela_menu_inicial = False
        # Definicao do framerate do jogo
        clk.tick(25)
        tela_principal.fill(BLACK)

        #  Lógica para troca de linhas no algoritmo
        if minha_fila.vazia():
            indice_linha_atual += 1
            texto_base = ''
            indice_caractere_atual = 0
            linha_arquivo_atual = arquivo_algoritmos.readline()
            linha_arquivo_atual = linha_arquivo_atual[:-1]
            # Condição de troca de algoritmo
            if linha_arquivo_atual == '#':
                cor_algoritmo_atual += 1
                linha_arquivo_atual = arquivo_algoritmos.readline()
                linha_arquivo_atual = linha_arquivo_atual[:-1]
                codigo_indice += 1
            linha_arquivo_atual = linha_arquivo_atual.strip()
            for caractere in linha_arquivo_atual:
                minha_fila.insere(caractere)
                texto_base += caractere

        # Desenhando barras de energia e concentração
        # Barra de energia:
        pygame.draw.rect(tela_principal, (red_barra_energia, green_barra_energia, 0), (x_pos_barra_energia,
                                                                                       y_pos_barra_energia,
                                                                                       largura_barra_energia, 40))
        # Contorno da barra de energia
        pygame.draw.rect(tela_principal, WHITE, (x_pos_barra_energia - 2, y_pos_barra_energia - 2,
                                                 largura_barra_energia + 2, 42), 3)
        # Barra de concentracao:
        pygame.draw.rect(tela_principal, (red_barra_concentracao, green_barra_concentracao, 0),
                         (x_pos_barra_conc, y_pos_barra_conc, largura_barra_concentracao, 40))
        # Contorno da barra de concentração
        pygame.draw.rect(tela_principal, WHITE, (x_pos_barra_conc - 2, y_pos_barra_conc - 2,
                                                 largura_barra_concentracao + 2, 42), 3)

        # Porcentagem para controlar a cor das barras (energia e concentração)
        barra_energia_porcentagem = largura_barra_energia / largura_max
        red_barra_energia = (1 - barra_energia_porcentagem) * 255 % 256
        green_barra_energia = barra_energia_porcentagem * 255 % 256

        barra_concentracao_porcentagem = largura_barra_concentracao / largura_max
        red_barra_concentracao = (1 - barra_concentracao_porcentagem) * 255 % 256
        green_barra_concentracao = barra_concentracao_porcentagem * 255 % 256

        # Desenhando retângulos dos textos:
        # Retângulo principal (tela_principal central)
        pygame.draw.rect(tela_principal, (51, 153, 255), (x_pos_caixa, y_pos_caixa, x_tam_caixa, y_tam_caixa))
        # Contorno do retângulo da tela_principal central
        pygame.draw.rect(tela_principal, COR_ALGORITMOS[cor_algoritmo_atual], (x_pos_caixa - 2, y_pos_caixa - 2,
                                                                               x_tam_caixa + 2, y_tam_caixa + 2), 5)
        # Retângulo da input box (é atribuído a uma variável para verificar a colisão)
        input_texto_box = pygame.draw.rect(tela_principal, cor_input_box, (x_pos_caixa + 30, y_pos_caixa + 135,
                                                                           x_tam_caixa - 60, 35))
        # Contorno do retângulo da input box
        pygame.draw.rect(tela_principal, BLACK, (x_pos_caixa + 30, y_pos_caixa + 135, x_tam_caixa - 60, 35), 3)

        # Barra de porcentagem concluída do jogo
        # Retângulo de fundo do progresso (branco)
        pygame.draw.rect(tela_principal, WHITE,
                         (x_pos_caixa + 40, y_pos_caixa + y_tam_caixa - 55, x_tam_caixa - 80, 35))
        # Retângulo do progresso verde (barra verde por cima da cor branca de fundo, com base na % de linhas feitas)
        pygame.draw.rect(tela_principal, GREEN, (x_pos_caixa + 40, y_pos_caixa + y_tam_caixa - 55,
                                                 (indice_linha_atual - 1) / numero_linhas_arquivo * (x_tam_caixa - 80),
                                                 35))
        # Retângulo de contorno do retângulo de progresso do jogo
        pygame.draw.rect(tela_principal, BLACK,
                         (x_pos_caixa + 38, y_pos_caixa + y_tam_caixa - 57, x_tam_caixa - 78, 37), 3)

        # Mostra a sentença algorítica a ser digitada (em branco) -> fica por baixo dos caracteres verdes (corretos)
        linha_arquivo_renderizar = fonte_2.render(linha_arquivo_atual, False, WHITE)
        tela_principal.blit(linha_arquivo_renderizar, (x_pos_caixa + 68, y_pos_caixa + 80))

        # Imprime a partição já correta do texto (a parte correta será verde, sobreposta à expressão branca original)
        texto = ''
        for token in texto_base[0:indice_caractere_atual]:
            texto += token
        msg_texto = f'{texto}'
        msg_timer = f'Tempo: {timer_trecho_codigo:2.2f}'

        # Formatando textos
        msg_format_texto_base = fonte_2.render(msg_texto, False, COR_ALGORITMOS[cor_algoritmo_atual])
        msg_algoritmo = f'Algoritmo {codigo_indice + 1}: {titulos_algoritmos[codigo_indice]}'
        msg_format_algoritmo = fonte_1.render(msg_algoritmo, False, WHITE)
        msg_format_progresso = fonte_2.render(msg_progresso, False, WHITE)
        msg_format_placeholder = fonte_2.render(msg_input_placeholder, False, (100, 100, 100))
        msg_format_input_text = fonte_2.render(input_text, False, BLACK)
        largura_input_texto = msg_format_input_text.get_width()
        if timer_trecho_codigo <= 5.00:
            cor_timer_perigo = RED
        else:
            cor_timer_perigo = WHITE
        msg_format_texto_timer_safe = fonte_timer.render(msg_timer[0:6], False, WHITE)
        msg_format_texto_timer_perigo = fonte_timer.render(msg_timer[7:], False, cor_timer_perigo)

        # Colocando textos na tela_principal
        tela_principal.blit(msg_format_progresso,
                            (x_pos_progresso - msg_format_progresso.get_width() / 2, y_pos_progresso))
        tela_principal.blit(msg_format_texto_timer_safe, (50, 50))
        tela_principal.blit(msg_format_texto_timer_perigo, (150, 50))
        tela_principal.blit(msg_format_texto_base, (x_pos_caixa + 68, y_pos_caixa + 80))
        tela_principal.blit(tela_principal,
                            deslocamento)  # Atualiza a tela_principal com um screen shake quando o player erra
        tela_principal.blit(msg_format_algoritmo,
                            (x_pos_caixa + (x_tam_caixa / 2) - msg_format_algoritmo.get_width() / 2,
                             y_pos_caixa + 20))
        tela_principal.blit(msg_format_input_text, (x_pos_caixa + 40, y_pos_caixa + 140))
        # Só mostra o placeholder (Digite aqui...) quando a caixa de input não está ativa e não tem nada escrito nela
        if input_text == '' and not active:
            tela_principal.blit(msg_format_placeholder, (x_pos_placeholder, y_pos_placeholder))

        # Colocando imagens na tela_principal (xicara e cerebro)
        grupo_sprites_permanentes.draw(tela_principal)

        # Animando a xicara de café quando a energia está baixa
        if largura_barra_energia <= 400:
            xicara_cafe.image.set_alpha(abs(sin(valor_seno_alfa_xicara) * 255))  # animando a xícara
            valor_seno_alfa_xicara += 0.09
        else:
            xicara_cafe.image.set_alpha(255)

        # Tremendo a tela_principal quando o player erra um caractere:
        if screen_shake > 0:
            screen_shake -= 1
        if screen_shake:
            deslocamento[0] = randint(0, 8) - 4
            deslocamento[1] = randint(0, 8) - 4
        else:
            deslocamento = [0, 0]

        # Trabalhando com o tempo para digitar
        timer_trecho_codigo -= 0.0375

        # Trabalhando com o tempo para o cursor ficar piscando
        timer_cursor -= 0.06
        if timer_cursor < - 0.5:
            timer_cursor = 0.5

        # Criando o cursor se a input box está ativa (e de acordo com o timer do cursor pra ele piscar)
        if active and timer_cursor > 0:
            # Desenha o cursor quando a input box está ativa e a cada unidade de tempo determinada pelo timer
            pygame.draw.rect(tela_principal, BLACK, (x_pos_caixa + 30 + msg_format_input_text.get_width() + 10,
                                                     y_pos_caixa + 140, 3, msg_format_input_text.get_height()))
        # Controle da decrementacao das barras
        largura_barra_energia -= 0.4

        # Eventos do jogo
        for event in pygame.event.get():
            # Evento de saída do jogo
            if event.type == QUIT:
                pygame.quit()
                exit()
            # Deteccao de LEFT CLICK
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Recuperando energia ao clicar na xicara
                if largura_barra_energia <= 400:
                    if xicara_cafe.rect.collidepoint(pos):
                        largura_barra_energia += 350
                        drinking_sound.play()
                # Se o usuário clicar na caixa de texto, ativá-la. Se clicar fora da caixa, desativá-la
                if input_texto_box.collidepoint(pos):
                    active = True
                    cor_input_box = WHITE  # cor branca ao clicar na caixa de texto da entrada
                else:
                    active = False
                    cor_input_box = (180, 180, 180)  # cor padrão branca quando a entrada não está selecionada

            # Verificando o pressionar das teclas
            if event.type == pygame.KEYDOWN:
                # debug tela inicial (apagar depois)
                if event.key == pygame.K_UP:
                    pass
                if active:
                    # if event.key == pygame.K_BACKSPACE:
                    #    input_text = input_text[:-1]
                    # Se a fila estiver vazia, o jogador venceu o jogo
                    if not minha_fila.vazia() and largura_input_texto < 415:

                        not_unicodes_especiais = event.key != pygame.K_LSHIFT and \
                                                 event.key != pygame.K_RSHIFT and event.key != pygame.K_CAPSLOCK and \
                                                 event.key != pygame.K_BACKSPACE and event.key != pygame.K_LCTRL and \
                                                 event.key != pygame.K_RCTRL and event.key != pygame.K_LALT and \
                                                 event.key != pygame.K_RALT and event.key != pygame.K_UP and \
                                                 event.key != pygame.K_DOWN and event.key != pygame.K_LEFT and \
                                                 event.key != pygame.K_RIGHT
                        # Se a fila não é vazia, verifica se a entrada do usuario é igual à primeira letra da fila e, se
                        # for, a remove e altera a cor da letra acertada para verde (atualiza o vetor de caracteres
                        # corretos)
                        if event.unicode == minha_fila.primeiro.dado:
                            teclando.play()
                            minha_fila.remove()
                            indice_caractere_atual += 1
                            input_text += event.unicode
                        elif not_unicodes_especiais:
                            screen_shake = 7
                            largura_barra_concentracao -= 40
                            resposta_errada.play()

        # limpa a caixa de texto de input ao trocar de linha no arquivo
        if minha_fila.vazia():
            input_text = ''
            timer_trecho_codigo = delay_trecho_codigo
        elif timer_trecho_codigo <= 0:
            input_text = ''
            minha_fila = fila.Fila()
            som_acabou_o_tempo.play()
            screen_shake = 10
            largura_barra_concentracao -= 100
            timer_trecho_codigo = delay_trecho_codigo

        # Esgotamento da barra de energia
        if largura_barra_energia <= 0 or largura_barra_concentracao <= 0:
            print("Voce perdeu!!!")
            game_end.game_end('derrota')
            pygame.quit()
            exit()

        #  linhas que começam com hashtag separam os algoritmos
        if indice_linha_atual - numero_hashtags == numero_linhas_arquivo:
            print("Voce ganhou!!")
            game_end.game_end('vitoria')
            pygame.quit()
            exit()

        pygame.display.flip()


if __name__ == '__main__':
    coders_night()
