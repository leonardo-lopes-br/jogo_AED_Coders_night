#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importacao do pygame
import pygame
from pygame.locals import *
from sys import exit
from time import sleep

from pygame.time import Clock

import fila
import funcoes_classes_auxiliares
from random import randint
# altera o caminho do terminal para o caminho do arquivo
import os


# NUMERO DE LINHAS DOS ALGORITMOS
# NUMERO PRIMO: 14
# PA: 9
# FIBONACCI: 10


def coders_night():
    # region inicializacao de dados que não se alteram
    # inicializacao da library do pygame
    pygame.init()
    # pygame.key.set_repeat(300, 110)  # permite segurar uma tela_principal (como apagar os caracteres com o backspace)

    # cores dos objetos
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 50, 0)

    # dimensoes da janela do jogo
    largura_janela = 1280
    altura_janela = 720

    # tela_principal do jogo
    tela_principal = pygame.display.set_mode((largura_janela, altura_janela))
    fundo_jogo = pygame.image.load(os.path.join("Imagens", "background.png"))
    fundo_jogo = pygame.transform.scale(fundo_jogo, (80 * 16, 45 * 16))
    pygame.display.set_caption("Coder's Night")

    # sons
    drinking_sound = pygame.mixer.Sound(os.path.join('Sons', "som_bebendo_cafe.mpeg"))
    drinking_sound.set_volume(0.2)
    teclando = pygame.mixer.Sound(os.path.join('Sons', "one-click.mp3"))
    teclando.set_volume(0.65)
    resposta_errada = pygame.mixer.Sound(os.path.join('Sons', 'resposta_errada.mp3'))
    resposta_errada.set_volume(0.3)
    som_acabou_o_tempo = pygame.mixer.Sound(os.path.join('Sons', 'som_acabou_o_tempo.mpeg'))
    som_acabou_o_tempo.set_volume(0.09)
    som_jogador_perdeu = pygame.mixer.Sound(os.path.join('Sons', 'som_jogador_perdeu.wav'))
    som_jogador_perdeu.set_volume(0.09)
    som_jogador_ganhou = pygame.mixer.Sound(os.path.join('Sons', 'som_ganhou_jogo.wav'))
    som_jogador_ganhou.set_volume(0.09)
    som_level_up = pygame.mixer.Sound(os.path.join('Sons', 'level_up.mpeg'))
    som_level_up.set_volume(0.13)
    som_terminou_linha = pygame.mixer.Sound(os.path.join('Sons', 'som_terminou_uma_linha.wav'))
    som_terminou_linha.set_volume(0.4)
    som_botao_clicado = pygame.mixer.Sound(os.path.join('Sons', 'som_botao_clicado.mp3'))
    som_botao_clicado.set_volume(1)
    som_selecionando_botao = pygame.mixer.Sound(os.path.join('Sons', 'som_selecionando_botao.flac'))
    som_selecionando_botao.set_volume(0.3)
    pc_iniciando1 = pygame.mixer.Sound(os.path.join('Sons', 'pc_iniciando1.mpeg'))
    pc_iniciando1.set_volume(0.5)
    pc_iniciando2 = pygame.mixer.Sound(os.path.join('Sons', 'pc_iniciando2.mpeg'))
    pc_iniciando2.set_volume(0.5)
    som_cadeira_rodinhas = pygame.mixer.Sound(os.path.join('Sons', 'arrastando_cadeira.mpeg'))
    som_cadeira_rodinhas.set_volume(0.7)

    # definicao das fontes dos textos
    fonte_1 = pygame.font.SysFont('arial', 27, True, False)
    fonte_2 = pygame.font.SysFont('arial', 22, True, False)
    fonte_timer = pygame.font.SysFont('Rubik Wet Paint', 35, False, True)
    fonte_titulo_jogo = pygame.font.SysFont('Rubik Glitch', 80, True, True)

    # imagens

    img_cerebro = pygame.image.load(os.path.join('Imagens', 'brain.png')).convert_alpha()
    img_cerebro = pygame.transform.scale(img_cerebro, (30, 30))

    img_energia = pygame.image.load(os.path.join('Imagens', 'icone_energia.png'))
    img_energia = pygame.transform.scale(img_energia, (30, 30))
    img_energia = pygame.transform.flip(img_energia, True, False)

    # criando os objetos
    posicao_lua = (-70, -40)
    posicao_estrela_0 = (140, 45)
    posicao_estrela_1 = (20, 260)
    posicao_estrela_2 = (100, 240)
    posicao_estrela_3 = (70, 370)
    posicao_xicara = (980, 463)

    xicara = funcoes_classes_auxiliares.Xicara(tamanho=32 * 6, posicao_top_left=posicao_xicara)
    cerebro = funcoes_classes_auxiliares.FiguraClicavel(img_cerebro, (80, 620))
    energia = funcoes_classes_auxiliares.FiguraClicavel(img_energia, (80, 670))

    lua = funcoes_classes_auxiliares.Moon(tamanho=32 * 12, posicao_top_left=posicao_lua)
    estrela_0 = funcoes_classes_auxiliares.Star(tamanho=32 * 6, posicao_top_left=posicao_estrela_0)
    estrela_1 = funcoes_classes_auxiliares.Star(tamanho=32 * 6, posicao_top_left=posicao_estrela_1)
    estrela_2 = funcoes_classes_auxiliares.Star(tamanho=32 * 6, posicao_top_left=posicao_estrela_2)
    estrela_3 = funcoes_classes_auxiliares.Star(tamanho=32 * 6, posicao_top_left=posicao_estrela_3)

    # Grupo para os sprites
    grupo_sprites_permanentes = pygame.sprite.Group()
    grupo_sprites_permanentes.add(cerebro, xicara, energia)
    grupo_sprites_janela = pygame.sprite.Group()
    grupo_sprites_janela.add(lua, estrela_0, estrela_1, estrela_2, estrela_3)

    # clock
    clk: Clock = pygame.time.Clock()

    # Configurações de dificuldade
    decremento_barra_energia = 1.0
    delay_trecho_codigo = 15
    dano_acabou_tempo = 150

    # dimensoes das barras
    largura_max = 700
    largura_barra_energia = largura_max
    largura_barra_concentracao = largura_max

    x_pos_barra_energia = 100
    y_pos_barra_energia = 670

    x_pos_barra_conc = 100
    y_pos_barra_conc = 615

    # caixa de texto
    x_tam_caixa = 575
    y_tam_caixa = 270
    x_pos_caixa = (largura_janela / 2 - x_tam_caixa / 2) + 17
    y_pos_caixa = (altura_janela / 2 - y_tam_caixa / 2) - 117

    # Títulos dos algoritmos
    titulos_algoritmos = ['Numero primo', 'Progressão Aritmética', 'Fibonacci']

    # Mensagens fixas
    # msg_progresso = 'Progresso' TIRANDO A MSG DE PROGRESSO POIS JA É INTUITIVO
    msg_input_placeholder = 'Digite aqui...'
    msg_botao_iniciar = 'Iniciar'
    msg_nome_jogo = "Coder's Night"
    msg_botao_dificuldade = 'Dificuldade'
    msg_dificuldades = ['Fácil', 'Médio', 'Difícil']
    msg_botao_sair = 'Sair'
    msg_botao_sairr = 'Sair do jogo'
    msg_voltar_menu = 'Voltar ao menu'

    msg_padrao_derrota = 'Você perdeu!'
    msg_padrao_derrota2 = 'Mas está tudo bem, não se pode ganhar todas!'
    msg_padrao_derrota3 = 'Que pena, está demitido!'

    msg_derrota_energia = 'Você não tomou café para recuperar as energias!'
    msg_derrota_concentracao = 'Você digitou muitos caracteres errados!'

    msg_vitoria1 = 'Parabéns! Você conseguiu programar tudo!'
    msg_vitoria2 = 'Se manter a dedicação, talvez seja promovido!'
    msg_vitoria3 = 'Talvez agora deva ir programar de verdade'
    msg_vitoria4 = '.....'

    # Posição fixa do texto 'Progresso'
    # x_pos_progresso = x_pos_caixa + x_tam_caixa / 2
    # y_pos_progresso = y_pos_caixa + y_tam_caixa - 95

    # Posição fixa do texto 'Digite aqui...'
    x_pos_placeholder = x_pos_caixa + 40
    y_pos_placeholder = y_pos_caixa + 140

    # endregion

    tela_menu_inicial = True
    tela_menu_final = False

    final_jogo = 'derrota'

    indice_dificuldade_selecionada_por_ultimo = 4

    # Daqui pra cima, as declarações são fixas, pra baixo começa o loop que reseta as variáveis
    # laço do jogo inteiro (começa com a tela inicial e depois entra no laço principal do jogo)
    while True:

        # region Configurando tudo como o padrão inicial
        # Variaveis para tremer a tela_principal_principal com um erro do usuário
        screen_shake = 0
        deslocamento = [0, 0]

        # Resetando as cores das barras
        # cor barra_energia
        red_barra_energia = red_barra_concentracao = 0
        green_barra_energia = green_barra_concentracao = 255

        # variáveis de input e texto base a ser digitado
        input_text = ''
        cor_input_box = WHITE  # começa com branco pois o jogo ja começa com a caixa de texto selecionada
        texto_base = ''

        # region Cria uma fila e a preenche com caracteres do arquivo de algoritmos

        arquivo_algoritmos = open(os.path.join('Textos', 'algoritmos_textos.txt'), 'r')
        indice_linha_atual = 0  # para finalizar o jogo quando chegar no numero de linhas
        numero_linhas_arquivo = 0
        numero_linhas_por_algoritmo = [14, 9, 10]
        indice_linha_algoritmo_atual = 0
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
        # endregion

        # Resetando as vidas apos recuperar o valor para analisar no fim do jogo
        energia_final = largura_barra_energia
        concentracao_final = largura_barra_concentracao
        largura_barra_energia = largura_barra_concentracao = largura_max

        energia_baixa = 280

        # Resetando timer da msg de fim de jogo
        delay_msg_final_jogo = 0.5
        timer_msg_final_jogo = delay_msg_final_jogo

        # Este indice é utilizado para saber a partição atual da 'string' que já foi acertada
        indice_caractere_atual = 0

        # Define o acesso à caixa de texto como falso
        active = True
        timer_cursor = 0.5

        # Codigo que indica qual o algoritmo atual (numero primo, PA, etc..)
        codigo_indice = -1

        # Timer para digitar o trecho de código
        timer_trecho_codigo = delay_trecho_codigo

        # endregion

        # Resetando a msg padrão de derrota
        indice_msg_final_jogo = 0
        msg_format_padrao_derrota1 = msg_format_padrao_derrota2 = msg_format_padrao_derrota3 = \
            fonte_2.render(' ', True, BLACK)
        msg_format_derrota_energia = msg_format_derrota_concentracao = msg_format_padrao_derrota1

        imprimiu_msg_padrao_derrota1 = imprimiu_msg_padrao_derrota2 = imprimiu_msg_padrao_derrota3 = False
        imprimiu_msg_derrota_energia = imprimiu_msg_derrota_concentracao = False

        # Resetando a msg padrão de vitória
        msg_format_padrao_vitoria1 = msg_format_padrao_vitoria2 = msg_format_padrao_derrota2
        msg_format_padrao_vitoria3 = msg_format_padrao_vitoria4 = msg_format_padrao_derrota2

        imprimiu_msg_padrao_vitoria1 = imprimiu_msg_padrao_vitoria2 = False
        imprimiu_msg_padrao_vitoria3 = imprimiu_msg_padrao_vitoria4 = False

        # Limpando a tela
        tela_principal.fill(BLACK)

        if tela_menu_final:
            pygame.mixer.music.pause()
            if final_jogo == 'derrota':
                som_jogador_perdeu.play()
            elif final_jogo == 'vitoria':
                som_jogador_ganhou.play()

        botao_voltar_ativo = botao_sairr_ativo = False
        botao_voltar = pygame.Rect(650, 290, 180, 30)
        botao_sairr = pygame.Rect(650, 325, 180, 30)

        ja_tocou_som_botao_selecionado = [False, False]
        delay_som_teclando_menu_final = 0.5
        timer_som_teclando_menu_final = delay_som_teclando_menu_final
        atraso_imprimir_msg = 0.2
        atraso = True
        pular_escrita = False

        lua.Stop_Animar()
        estrela_0.Stop_Animar()
        estrela_1.Stop_Animar()
        estrela_2.Stop_Animar()
        estrela_3.Stop_Animar()

        # Trabalhando na tela do menu final
        while tela_menu_final:
            clk.tick(25)
            tela_principal.blit(fundo_jogo, (0, 0))

            cor_botao_voltar, cor_texto_botao_voltar = funcoes_classes_auxiliares.configura_cor_botao(
                botao_voltar_ativo)
            cor_botao_sairr, cor_texto_botao_sairr = funcoes_classes_auxiliares.configura_cor_botao(botao_sairr_ativo)

            msg_format_botao_voltar = fonte_2.render(msg_voltar_menu, True, cor_texto_botao_voltar)
            msg_format_botao_sairr = fonte_2.render(msg_botao_sairr, True, cor_texto_botao_sairr)

            # Desenhando estrelas e lua
            grupo_sprites_janela.draw(tela_principal)
            grupo_sprites_janela.update()

            # Incluindo botões de voltar ao menu ou de sair do jogo independente do final
            if imprimiu_msg_padrao_derrota3 or imprimiu_msg_padrao_vitoria4:
                # Desenhando o botão de voltar ao menu
                pygame.draw.rect(tela_principal, cor_botao_voltar, botao_voltar, border_radius=100)
                # Desenhando o contorno do botão de voltar ao menu
                pygame.draw.rect(tela_principal, BLACK, (648, 288, 182, 32), 3, border_radius=100)

                # Desenhando o botão de sair do jogo
                pygame.draw.rect(tela_principal, cor_botao_sairr, botao_sairr, border_radius=100)
                # Desenhando o contorno do botão de sair do jogo
                pygame.draw.rect(tela_principal, BLACK, (648, 323, 182, 32), 3, border_radius=100)

                # Desenhando o texto do botão de voltar ao menu
                tela_principal.blit(msg_format_botao_voltar, (660, 291, 100, 30))
                tela_principal.blit(msg_format_botao_sairr, (675, 327, 100, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                mouse = pygame.mouse.get_pos()
                # Ativando ou não o botão de voltar
                if botao_voltar.collidepoint(mouse):
                    botao_voltar_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN and (imprimiu_msg_padrao_derrota3 or
                                                                 imprimiu_msg_padrao_vitoria4):
                        som_botao_clicado.play()
                        sleep(0.04)
                        funcoes_classes_auxiliares.transicao_telas(tela_principal)
                        tela_menu_inicial = True
                        tela_menu_final = False
                else:
                    botao_voltar_ativo = False
                # Ativando ou não o botão de sair
                if botao_sairr.collidepoint(mouse):
                    botao_sairr_ativo = True
                    if event.type == MOUSEBUTTONDOWN and (imprimiu_msg_padrao_derrota3 or imprimiu_msg_padrao_vitoria4):
                        som_botao_clicado.play()
                        sleep(0.35)
                        pygame.quit()
                        exit()
                else:
                    botao_sairr_ativo = False

                # Pulando a digitação da mensagem final se o usuário clicar na tela antes delas acabarem
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if not (imprimiu_msg_padrao_derrota3 or imprimiu_msg_padrao_vitoria4):
                        pular_escrita = True

            # Decrementando timer para escrever os textos de fim de jogo
            # Só vai ser mais lento pros tres pontinhos dramaticos da ultima msg de vitoria
            if not pular_escrita:
                if imprimiu_msg_padrao_vitoria3:
                    timer_msg_final_jogo -= 0.05
                    timer_som_teclando_menu_final -= 0.05
                else:
                    timer_msg_final_jogo -= 0.4
                    timer_som_teclando_menu_final -= 0.15
            else:
                timer_msg_final_jogo -= 6

            # Imprimindo textos para um final onde o jogador perde
            if final_jogo == 'derrota':
                if timer_msg_final_jogo <= 0 and not imprimiu_msg_padrao_derrota1:
                    timer_msg_final_jogo = delay_msg_final_jogo
                    if atraso and not pular_escrita:
                        atraso = False
                        sleep(atraso_imprimir_msg)
                    if pular_escrita:
                        indice_msg_final_jogo = len(msg_padrao_derrota)
                    particao_msg_padrao_derrota = msg_padrao_derrota[0:indice_msg_final_jogo]
                    msg_format_padrao_derrota1 = fonte_2.render(particao_msg_padrao_derrota, True, BLACK)
                    indice_msg_final_jogo += 1
                    if indice_msg_final_jogo > len(msg_padrao_derrota):
                        indice_msg_final_jogo = 0
                        imprimiu_msg_padrao_derrota1 = True
                        atraso = True

                if timer_msg_final_jogo <= 0 and not imprimiu_msg_padrao_derrota2 and imprimiu_msg_padrao_derrota1:
                    timer_msg_final_jogo = delay_msg_final_jogo
                    if atraso and not pular_escrita:
                        atraso = False
                        sleep(atraso_imprimir_msg)
                    if pular_escrita:
                        indice_msg_final_jogo = len(msg_padrao_derrota2)
                    particao_msg_padrao_derrota = msg_padrao_derrota2[0:indice_msg_final_jogo]
                    msg_format_padrao_derrota2 = fonte_2.render(particao_msg_padrao_derrota, True, BLACK)
                    indice_msg_final_jogo += 1
                    if indice_msg_final_jogo > len(msg_padrao_derrota2):
                        imprimiu_msg_padrao_derrota2 = True
                        indice_msg_final_jogo = 0
                        atraso = True

                # Msg personalizada -> final onde o jogador perde por errar muito caractere (barra concentracao <= 0)
                if concentracao_final <= 0:
                    if timer_msg_final_jogo <= 0 and imprimiu_msg_padrao_derrota2 \
                            and not imprimiu_msg_derrota_concentracao:
                        timer_msg_final_jogo = delay_msg_final_jogo
                        if atraso and not pular_escrita:
                            atraso = False
                            sleep(atraso_imprimir_msg)
                        if pular_escrita:
                            indice_msg_final_jogo = len(msg_derrota_concentracao)
                        particao_msg_padrao_derrota = msg_derrota_concentracao[0:indice_msg_final_jogo]
                        msg_format_derrota_concentracao = fonte_2.render(particao_msg_padrao_derrota, True, BLACK)
                        indice_msg_final_jogo += 1
                        if indice_msg_final_jogo > len(msg_derrota_concentracao):
                            imprimiu_msg_derrota_concentracao = True
                            indice_msg_final_jogo = 0
                            atraso = True

                # Msg personalizada -> final onde o jogador perde por não tomar café (barra energia <= 0)
                if energia_final <= 0:
                    if timer_msg_final_jogo <= 0 and imprimiu_msg_padrao_derrota2 \
                            and not imprimiu_msg_derrota_energia:
                        timer_msg_final_jogo = delay_msg_final_jogo
                        if atraso and not pular_escrita:
                            atraso = False
                            sleep(atraso_imprimir_msg)
                        if pular_escrita:
                            indice_msg_final_jogo = len(msg_derrota_energia)
                        particao_msg_padrao_derrota = msg_derrota_energia[0:indice_msg_final_jogo]
                        msg_format_derrota_energia = fonte_2.render(particao_msg_padrao_derrota, True, BLACK)
                        indice_msg_final_jogo += 1
                        if indice_msg_final_jogo > len(msg_derrota_energia):
                            imprimiu_msg_derrota_energia = True
                            indice_msg_final_jogo = 0
                            atraso = True

                # Imprimindo msg padrão final (que pena, está demitido)
                if (imprimiu_msg_derrota_energia and not imprimiu_msg_padrao_derrota3) or \
                        (imprimiu_msg_derrota_concentracao and not imprimiu_msg_padrao_derrota3):
                    if timer_msg_final_jogo <= 0:
                        timer_msg_final_jogo = delay_msg_final_jogo
                        if atraso and not pular_escrita:
                            atraso = False
                            sleep(atraso_imprimir_msg)
                        if pular_escrita:
                            indice_msg_final_jogo = len(msg_padrao_derrota3)
                        particao_msg_padrao_derrota = msg_padrao_derrota3[0:indice_msg_final_jogo]
                        msg_format_padrao_derrota3 = fonte_2.render(particao_msg_padrao_derrota, True, BLACK)
                        indice_msg_final_jogo += 1

                        if indice_msg_final_jogo > len(msg_padrao_derrota3):
                            imprimiu_msg_padrao_derrota3 = True
                            indice_msg_final_jogo = 0
                            atraso = True

                tela_principal.blit(msg_format_padrao_derrota1, (380, 130))
                tela_principal.blit(msg_format_padrao_derrota2, (380, 165))
                if energia_final <= 0:
                    tela_principal.blit(msg_format_derrota_energia, (380, 250))
                elif concentracao_final <= 0:
                    tela_principal.blit(msg_format_derrota_concentracao, (380, 250))
                tela_principal.blit(msg_format_padrao_derrota3, (380, 285))

            elif final_jogo == 'vitoria':
                if timer_msg_final_jogo <= 0 and not imprimiu_msg_padrao_vitoria1:
                    timer_msg_final_jogo = delay_msg_final_jogo
                    if atraso and not pular_escrita:
                        atraso = False
                        sleep(atraso_imprimir_msg)
                    if pular_escrita:
                        indice_msg_final_jogo = len(msg_vitoria1)
                    particao_msg_padrao_vitoria = msg_vitoria1[0:indice_msg_final_jogo]
                    msg_format_padrao_vitoria1 = fonte_2.render(particao_msg_padrao_vitoria, True, BLACK)
                    indice_msg_final_jogo += 1
                    if indice_msg_final_jogo > len(msg_vitoria1):
                        indice_msg_final_jogo = 0
                        imprimiu_msg_padrao_vitoria1 = True
                        atraso = True

                if timer_msg_final_jogo <= 0 and not imprimiu_msg_padrao_vitoria2:
                    timer_msg_final_jogo = delay_msg_final_jogo
                    if atraso and not pular_escrita:
                        atraso = False
                        sleep(atraso_imprimir_msg)
                    if pular_escrita:
                        indice_msg_final_jogo = len(msg_vitoria2)
                    particao_msg_padrao_vitoria = msg_vitoria2[0:indice_msg_final_jogo]
                    msg_format_padrao_vitoria2 = fonte_2.render(particao_msg_padrao_vitoria, True, BLACK)
                    indice_msg_final_jogo += 1
                    if indice_msg_final_jogo > len(msg_vitoria2):
                        indice_msg_final_jogo = 0
                        imprimiu_msg_padrao_vitoria2 = True
                        atraso = True

                if timer_msg_final_jogo <= 0 and not imprimiu_msg_padrao_vitoria3:
                    timer_msg_final_jogo = delay_msg_final_jogo
                    if atraso and not pular_escrita:
                        atraso = False
                        sleep(atraso_imprimir_msg)
                    if pular_escrita:
                        indice_msg_final_jogo = len(msg_vitoria3)
                    particao_msg_padrao_vitoria = msg_vitoria3[0:indice_msg_final_jogo]
                    msg_format_padrao_vitoria3 = fonte_2.render(particao_msg_padrao_vitoria, True, BLACK)
                    indice_msg_final_jogo += 1
                    if indice_msg_final_jogo > len(msg_vitoria3):
                        indice_msg_final_jogo = 0
                        imprimiu_msg_padrao_vitoria3 = True
                        atraso = True

                if timer_msg_final_jogo <= 0 and not imprimiu_msg_padrao_vitoria4:
                    timer_msg_final_jogo = delay_msg_final_jogo
                    if atraso and not pular_escrita:
                        atraso = False
                        sleep(atraso_imprimir_msg)
                    if pular_escrita:
                        indice_msg_final_jogo = len(msg_vitoria4)
                    particao_msg_padrao_vitoria = msg_vitoria4[0:indice_msg_final_jogo]
                    msg_format_padrao_vitoria4 = fonte_2.render(particao_msg_padrao_vitoria, True, BLACK)
                    indice_msg_final_jogo += 1
                    if indice_msg_final_jogo > len(msg_vitoria4):
                        indice_msg_final_jogo = 0
                        imprimiu_msg_padrao_vitoria4 = True
                        atraso = True

                tela_principal.blit(msg_format_padrao_vitoria1, (380, 130))
                tela_principal.blit(msg_format_padrao_vitoria2, (380, 165))
                tela_principal.blit(msg_format_padrao_vitoria3, (380, 250))
                tela_principal.blit(msg_format_padrao_vitoria4, (828, 250))

            # som de botao selecionado
            lista_booleans_botoes = [botao_voltar_ativo, botao_sairr_ativo]
            for indice, botao in enumerate(lista_booleans_botoes):
                if imprimiu_msg_padrao_vitoria4 or imprimiu_msg_padrao_derrota3:
                    if botao and not ja_tocou_som_botao_selecionado[indice]:
                        som_selecionando_botao.play()
                        ja_tocou_som_botao_selecionado[indice] = True
                    if not botao and ja_tocou_som_botao_selecionado[indice]:
                        ja_tocou_som_botao_selecionado[indice] = False

            if timer_som_teclando_menu_final <= 0 and \
                    not (imprimiu_msg_padrao_derrota3 or imprimiu_msg_padrao_vitoria4) and not pular_escrita:
                teclando.play()
                timer_som_teclando_menu_final = delay_som_teclando_menu_final

            pygame.display.flip()

        if tela_menu_inicial:
            pygame.mixer.music.load(os.path.join('Sons', 'som_fundo_tela_inicial.mp3'))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

        botao_iniciar_ativo = False
        botao_dificuldade_ativo = False
        botao_sair_ativo = False

        botao_facil_ativo = False
        botao_facil = pygame.Rect(largura_janela / 2 - 65, altura_janela / 2 - 50, 160, 60)

        botao_medio_ativo = True
        botao_medio = pygame.Rect(largura_janela / 2 - 65, altura_janela / 2 + 20, 160, 60)

        botao_dificil_ativo = False
        botao_dificil = pygame.Rect(largura_janela / 2 - 65, altura_janela / 2 + 90, 160, 60)

        escolheu_facil = indice_dificuldade_selecionada_por_ultimo == 3
        escolheu_medio = indice_dificuldade_selecionada_por_ultimo == 4
        escolheu_dificil = indice_dificuldade_selecionada_por_ultimo == 5

        mostrar_dificuldades = False

        ja_tocou_som_botao_selecionado = [False, False, False, False, False, False]
        ja_tocou_som_botao_selecionado[indice_dificuldade_selecionada_por_ultimo] = True

        # Limpando a tela
        tela_principal.fill(BLACK)
        while tela_menu_inicial:
            tela_principal.blit(fundo_jogo, (0, 0))

            # Configura a cor dos botões do menu
            cor_botao_iniciar, cor_texto_botao_iniciar = funcoes_classes_auxiliares.configura_cor_botao(
                botao_iniciar_ativo)
            cor_botao_dificuldade, cor_texto_botao_dificuldade = funcoes_classes_auxiliares.configura_cor_botao(
                botao_dificuldade_ativo)
            cor_botao_sair, cor_texto_botao_sair = funcoes_classes_auxiliares.configura_cor_botao(botao_sair_ativo)
            cor_botao_facil, cor_texto_botao_facil = funcoes_classes_auxiliares.configura_cor_botao(botao_facil_ativo)
            cor_botao_medio, cor_texto_botao_medio = funcoes_classes_auxiliares.configura_cor_botao(botao_medio_ativo)
            cor_botao_dificil, cor_texto_botao_dificil = funcoes_classes_auxiliares.configura_cor_botao(
                botao_dificil_ativo)

            # region Trabalhando o menu inicial do jogo

            # lua e estrelas
            grupo_sprites_janela.draw(tela_principal)
            grupo_sprites_janela.update()

            # Retângulo principal com as opções
            pygame.draw.rect(tela_principal, (60, 60, 200),
                             (x_pos_caixa - 2, y_pos_caixa + 4, x_tam_caixa + 2, y_tam_caixa - 12))

            # Botão iniciar o jogo
            botao_iniciar = pygame.draw.rect(tela_principal, cor_botao_iniciar,
                                             (largura_janela / 2 - 260, altura_janela / 2 - 140, 160, 80),
                                             100, border_radius=100)
            # Contorno do botão iniciar
            pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 262,
                                                     altura_janela / 2 - 142, 162, 82), 3, border_radius=100)

            # Botão escolher dificuldade do jogo
            botao_dificuldade = pygame.draw.rect(tela_principal, cor_botao_dificuldade,
                                                 (largura_janela / 2 - 65, altura_janela / 2 - 140, 160, 80),
                                                 100, border_radius=100)
            # Contorno do botao de dificuldade
            pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 67, altura_janela / 2 - 142, 162, 82),
                             3, border_radius=100)

            # Botão sair do jogo
            botao_sair = pygame.draw.rect(tela_principal, cor_botao_sair,
                                          (largura_janela / 2 + 128, altura_janela / 2 - 140, 160, 80),
                                          100, border_radius=100)
            # Contorno do botão de sair do jogo
            pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 + 126, altura_janela / 2 - 142, 162, 82),
                             3, border_radius=100)

            # Textos
            msg_format_nome_jogo = fonte_titulo_jogo.render(msg_nome_jogo, True, WHITE)
            msg_format_botao_iniciar = fonte_1.render(msg_botao_iniciar, True, cor_texto_botao_iniciar)
            msg_format_botao_dificuldade = fonte_1.render(msg_botao_dificuldade, True, cor_texto_botao_dificuldade)
            msg_format_botao_sair = fonte_1.render(msg_botao_sair, True, cor_texto_botao_sair)

            msg_format_botao_facil = fonte_1.render(msg_dificuldades[0], True, cor_texto_botao_facil)
            msg_format_botao_medio = fonte_1.render(msg_dificuldades[1], True, cor_texto_botao_medio)
            msg_format_botao_dificil = fonte_1.render(msg_dificuldades[2], True, cor_texto_botao_dificil)

            # Colocando os textos na tela
            tela_principal.blit(msg_format_nome_jogo, (largura_janela / 2 - 220, 70))
            tela_principal.blit(msg_format_botao_iniciar, (largura_janela / 2 - 223, altura_janela / 2 - 116, 160, 80))
            tela_principal.blit(msg_format_botao_dificuldade,
                                (largura_janela / 2 - 60, altura_janela / 2 - 116, 160, 80))
            tela_principal.blit(msg_format_botao_sair, (largura_janela / 2 + 177, altura_janela / 2 - 116, 160, 80))

            if mostrar_dificuldades:

                # Desenhando o botao da dificuldade facil
                pygame.draw.rect(tela_principal, cor_botao_facil, botao_facil, border_radius=100)
                # Contorno do botao da dificuldade facil
                pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 67, altura_janela / 2 - 52, 162, 62),
                                 3, border_radius=100)

                # Desenhando o botão da dificuldade média
                pygame.draw.rect(tela_principal, cor_botao_medio, botao_medio, border_radius=100)
                # Contorno do botão da dificuldade média
                pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 67, altura_janela / 2 + 18, 162, 62),
                                 3, border_radius=100)

                # Desenhando o botão da dificuldade dificil
                pygame.draw.rect(tela_principal, cor_botao_dificil, botao_dificil, border_radius=100)
                # Contorno do botão da dificuldade dificil
                pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 67, altura_janela / 2 + 88, 162, 62),
                                 3, border_radius=100)

                tela_principal.blit(msg_format_botao_facil, (largura_janela / 2 - 20, altura_janela / 2 - 37, 160, 60))
                tela_principal.blit(msg_format_botao_medio, (largura_janela / 2 - 28, altura_janela / 2 + 33, 160, 60))
                tela_principal.blit(msg_format_botao_dificil,
                                    (largura_janela / 2 - 29, altura_janela / 2 + 103, 160, 60))

                mouse = pygame.mouse.get_pos()

                if escolheu_facil and not escolheu_medio and not escolheu_dificil:
                    botao_facil_ativo = True
                else:
                    botao_facil_ativo = botao_facil.collidepoint(mouse)

                if escolheu_medio and not escolheu_facil and not escolheu_dificil:
                    botao_medio_ativo = True
                else:
                    botao_medio_ativo = botao_medio.collidepoint(mouse)
                if escolheu_dificil and not escolheu_facil and not escolheu_medio:
                    botao_dificil_ativo = True
                else:
                    botao_dificil_ativo = botao_dificil.collidepoint(mouse)

            # Eventos do menu inicial
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                posicao_mouse = pygame.mouse.get_pos()

                if botao_iniciar.collidepoint(posicao_mouse) and not mostrar_dificuldades:
                    botao_iniciar_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        tela_menu_inicial = False
                        som_botao_clicado.play()
                        funcoes_classes_auxiliares.transicao_telas(tela_principal)
                else:
                    botao_iniciar_ativo = False
                if botao_dificuldade.collidepoint(posicao_mouse):
                    botao_dificuldade_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        som_botao_clicado.play()
                        mostrar_dificuldades = not mostrar_dificuldades
                else:
                    botao_dificuldade_ativo = False

                # Testando dificuldades
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_facil.collidepoint(posicao_mouse):
                        som_botao_clicado.play()
                        escolheu_facil = True
                        escolheu_medio = False
                        escolheu_dificil = False
                    elif botao_medio.collidepoint(posicao_mouse):
                        som_botao_clicado.play()
                        escolheu_facil = False
                        escolheu_medio = True
                        escolheu_dificil = False
                    elif botao_dificil.collidepoint(posicao_mouse):
                        som_botao_clicado.play()
                        escolheu_facil = False
                        escolheu_medio = False
                        escolheu_dificil = True

                if botao_sair.collidepoint(posicao_mouse) and not mostrar_dificuldades:
                    botao_sair_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        som_botao_clicado.play()
                        sleep(0.25)
                        pygame.quit()
                        exit()
                else:
                    botao_sair_ativo = False

                # Se o usuário clicar em um lugar da tela que não seja o menu habilitado, este menu fecha
                if event.type == MOUSEBUTTONDOWN:
                    if mostrar_dificuldades and not botao_dificuldade.collidepoint(posicao_mouse):
                        mostrar_dificuldades = False

            # som de botao selecionado
            lista_booleans_botoes = [botao_iniciar_ativo, botao_dificuldade_ativo, botao_sair_ativo, botao_facil_ativo,
                                     botao_medio_ativo, botao_dificil_ativo]
            for indice, botao in enumerate(lista_booleans_botoes):
                if botao and not ja_tocou_som_botao_selecionado[indice]:
                    som_selecionando_botao.play()
                    ja_tocou_som_botao_selecionado[indice] = True
                if not botao and ja_tocou_som_botao_selecionado[indice]:
                    ja_tocou_som_botao_selecionado[indice] = False

            pygame.display.flip()
            # endregion

        # Configurando dificuldade selecionada
        musica_tela_jogo = ''
        if escolheu_facil:
            dano_acabou_tempo = 60
            decremento_barra_energia = 0.35
            delay_trecho_codigo = 30
            timer_trecho_codigo = delay_trecho_codigo
            indice_dificuldade_selecionada_por_ultimo = 3
            musica_tela_jogo = ['musica_lofi.mp3', 0.4]
        elif escolheu_medio:
            dano_acabou_tempo = 100
            decremento_barra_energia = 0.75
            delay_trecho_codigo = 25
            timer_trecho_codigo = delay_trecho_codigo
            indice_dificuldade_selecionada_por_ultimo = 4
            musica_tela_jogo = ['som_fundo_level2.mp3', 0.15]
        elif escolheu_dificil:
            dano_acabou_tempo = 100
            decremento_barra_energia = 1.0
            delay_trecho_codigo = 20
            timer_trecho_codigo = delay_trecho_codigo
            indice_dificuldade_selecionada_por_ultimo = 5
            musica_tela_jogo = ['som_fundo_level3.mp3', 0.15]

        # Resetando barra de progresso do algoritmo
        tamanho_barra_progresso = 0
        troquei_linha = False

        tomou_dano_por_tempo = False

        # Parando animação das xicaras caso na hora em que acabou estava ativa e o jogador voltou ao menu e recomeçou
        xicara.stop_flutuar(posicao_xicara)

        # Parando música da tela inicial
        pygame.mixer.music.pause()

        # Limpando a tela
        tela_principal.fill(BLACK)

        # Preparando tela do jogo principal (LEMBRA DE CONFIGURAR A MUSICA NO FINAL)
        tela_jogo_preparada = False
        terminou_som_pc_iniciando1 = terminou_som_pc_iniciando2 = terminou_som_cadeira_rodinhas = False
        terminou_som_clicando_musica = False
        # A cor do monitor no jogo é (60, 60, 200)
        red_retangulo_tela_monitor = green_retangulo_tela_monitor = blue_retangulo_tela_monitor = 0

        transparencia_inicial = 0

        while not tela_jogo_preparada:
            clk.tick(30)
            tela_principal.blit(fundo_jogo, (0, 0))

            # Retângulo principal (tela_principal central)
            pygame.draw.rect(tela_principal, (red_retangulo_tela_monitor, green_retangulo_tela_monitor,
                                              blue_retangulo_tela_monitor),
                             (x_pos_caixa - 2, y_pos_caixa + 4, x_tam_caixa + 2, y_tam_caixa - 12))

            # Desenhando barras de energia e concentração após pc iniciado
            if terminou_som_pc_iniciando2:
                # Barra de energia:
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (0, 255, 0, transparencia_inicial),
                                                           (x_pos_barra_energia, y_pos_barra_energia,
                                                            largura_barra_energia, 10))
                # Contorno barra energia
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (255, 255, 255, transparencia_inicial),
                                                           (x_pos_barra_energia - 2, y_pos_barra_energia - 2,
                                                            largura_barra_energia + 2, 15), 3)

                # Barra de concentração
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (0, 255, 0, transparencia_inicial),
                                                           (x_pos_barra_conc, y_pos_barra_conc,
                                                            largura_barra_concentracao, 10))
                # Contorno barra de concentração
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (255, 255, 255, transparencia_inicial),
                                                           (x_pos_barra_conc - 2, y_pos_barra_conc - 2,
                                                            largura_barra_concentracao + 2, 15), 3)

                # Input box
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (255, 255, 255, transparencia_inicial),
                                                           (x_pos_caixa + 30, y_pos_caixa + 135, x_tam_caixa - 60, 35))
                # Contorno da input box
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (0, 0, 0, transparencia_inicial),
                                                           (x_pos_caixa + 30, y_pos_caixa + 135, x_tam_caixa - 60, 35),
                                                           3)

                # Barra porcentagem
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (255, 255, 255, transparencia_inicial),
                                                           (x_pos_caixa + 40, y_pos_caixa + y_tam_caixa - 55,
                                                            x_tam_caixa - 80, 20), 20)
                # Contorno porcentagem
                funcoes_classes_auxiliares.draw_rect_alpha(tela_principal, (0, 0, 0, transparencia_inicial),
                                                           (x_pos_caixa + 38, y_pos_caixa + y_tam_caixa - 57,
                                                            x_tam_caixa - 78, 22), 3)

                grupo_sprites_permanentes.draw(tela_principal)
                grupo_sprites_permanentes.update()

                msg_timer = f'Tempo: {timer_trecho_codigo:2.2f}'
                msg_algoritmo = f'{titulos_algoritmos[0]}'

                msg_format_texto_timer_safe = fonte_timer.render(msg_timer, False, WHITE)
                msg_format_algoritmo = fonte_1.render(msg_algoritmo, False, WHITE)

                tela_principal.blit(msg_format_texto_timer_safe, (1050, 25))
                tela_principal.blit(msg_format_algoritmo,
                                    (x_pos_caixa + (x_tam_caixa / 2) - msg_format_algoritmo.get_width() / 2,
                                     y_pos_caixa + 20))

                if not terminou_som_cadeira_rodinhas:
                    som_cadeira_rodinhas.play()
                    terminou_som_cadeira_rodinhas = True
                if terminou_som_cadeira_rodinhas and not terminou_som_clicando_musica and not pygame.mixer.get_busy():
                    sleep(0.4)
                    terminou_som_clicando_musica = True
                    teclando.set_volume(1)
                    teclando.play()
                if terminou_som_clicando_musica and not pygame.mixer.get_busy():
                    teclando.set_volume(0.65)
                    tela_jogo_preparada = True

                if transparencia_inicial < 255:
                    transparencia_inicial += 3

            # Colocando imagens na tela_principal
            grupo_sprites_janela.draw(tela_principal)
            grupo_sprites_janela.update()

            if blue_retangulo_tela_monitor < 200:
                blue_retangulo_tela_monitor += 4
            if red_retangulo_tela_monitor < 60 and green_retangulo_tela_monitor < 60:
                red_retangulo_tela_monitor += 1.5
                green_retangulo_tela_monitor += 1.5

            # Lidando com os sons de ligar o pc e de colocar musica pra tocar
            if not terminou_som_pc_iniciando1:
                pc_iniciando1.play()
                terminou_som_pc_iniciando1 = True
            elif terminou_som_pc_iniciando1 and not terminou_som_pc_iniciando2 and not pygame.mixer.get_busy():
                pc_iniciando1.stop()
                pc_iniciando2.play()
                terminou_som_pc_iniciando2 = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()

        pygame.mixer.music.load(os.path.join('Sons', musica_tela_jogo[0]))
        pygame.mixer.music.set_volume(musica_tela_jogo[1])
        pygame.mixer.music.play(-1)

        # Laço principal do jogo
        while not tela_menu_inicial and not tela_menu_final:
            # region Jogo de fato (toda a lógica)
            # Definicao do framerate do jogo
            clk.tick(30)
            tela_principal.blit(fundo_jogo, (0, 0))

            #  Lógica para troca de linhas no algoritmo
            if minha_fila.vazia():
                if indice_linha_atual > 0 and not tomou_dano_por_tempo:
                    som_terminou_linha.play()
                troquei_linha = True
                indice_linha_atual += 1
                indice_linha_algoritmo_atual += 1
                texto_base = ''
                indice_caractere_atual = 0
                linha_arquivo_atual = arquivo_algoritmos.readline()
                linha_arquivo_atual = linha_arquivo_atual[:-1]
                # Condição de troca de algoritmo
                if linha_arquivo_atual == '#':
                    indice_linha_algoritmo_atual = 0
                    linha_arquivo_atual = arquivo_algoritmos.readline()
                    linha_arquivo_atual = linha_arquivo_atual[:-1]
                    codigo_indice += 1
                    if codigo_indice > 0:
                        som_level_up.play()
                linha_arquivo_atual = linha_arquivo_atual.strip()
                for caractere in linha_arquivo_atual:
                    minha_fila.insere(caractere)
                    texto_base += caractere

            # Desenhando barras de energia e concentração
            # Barra de energia:
            pygame.draw.rect(tela_principal, (red_barra_energia, green_barra_energia, 0), (x_pos_barra_energia,
                                                                                           y_pos_barra_energia,
                                                                                           largura_barra_energia, 10))
            # Contorno da barra de energia
            pygame.draw.rect(tela_principal, WHITE, (x_pos_barra_energia - 2, y_pos_barra_energia - 2,
                                                     largura_barra_energia + 2, 15), 3)
            # Barra de concentracao:
            pygame.draw.rect(tela_principal, (red_barra_concentracao, green_barra_concentracao, 0),
                             (x_pos_barra_conc, y_pos_barra_conc, largura_barra_concentracao, 10))
            # Contorno da barra de concentração
            pygame.draw.rect(tela_principal, WHITE, (x_pos_barra_conc - 2, y_pos_barra_conc - 2,
                                                     largura_barra_concentracao + 2, 15), 3)

            # Porcentagem para controlar a cor das barras (energia e concentração)
            barra_energia_porcentagem = largura_barra_energia / largura_max
            red_barra_energia = (1 - barra_energia_porcentagem) * 255 % 256
            green_barra_energia = barra_energia_porcentagem * 255 % 256

            barra_concentracao_porcentagem = largura_barra_concentracao / largura_max
            red_barra_concentracao = (1 - barra_concentracao_porcentagem) * 255 % 256
            green_barra_concentracao = barra_concentracao_porcentagem * 255 % 256

            # Desenhando retângulos dos textos:
            # Retângulo principal (tela_principal central)
            pygame.draw.rect(tela_principal, (60, 60, 200), (x_pos_caixa - 2, y_pos_caixa + 4, x_tam_caixa + 2,
                                                             y_tam_caixa - 12))

            # Retângulo da input box (é atribuído a uma variável para verificar a colisão)
            input_texto_box = pygame.draw.rect(tela_principal, cor_input_box, (x_pos_caixa + 30, y_pos_caixa + 135,
                                                                               x_tam_caixa - 60, 35))
            # Contorno do retângulo da input box
            pygame.draw.rect(tela_principal, BLACK, (x_pos_caixa + 30, y_pos_caixa + 135, x_tam_caixa - 60, 35), 3)

            # Barra de porcentagem concluída do jogo
            # Retângulo de fundo do progresso (branco)
            pygame.draw.rect(tela_principal, WHITE,
                             (x_pos_caixa + 40, y_pos_caixa + y_tam_caixa - 55, x_tam_caixa - 80, 20))
            if indice_linha_algoritmo_atual >= 0 and troquei_linha:
                tamanho_barra_progresso = (indice_linha_algoritmo_atual - 1) / \
                                          numero_linhas_por_algoritmo[codigo_indice] * (x_tam_caixa - 80)

            # Retângulo do progresso verde (barra verde por cima da cor branca de fundo, com base na % de linhas feitas)
            pygame.draw.rect(tela_principal, GREEN, (x_pos_caixa + 40, y_pos_caixa + y_tam_caixa - 55,
                                                     tamanho_barra_progresso, 20))
            # Retângulo de contorno do retângulo de progresso do jogo
            pygame.draw.rect(tela_principal, BLACK,
                             (x_pos_caixa + 38, y_pos_caixa + y_tam_caixa - 57, x_tam_caixa - 78, 22), 3)
            if tamanho_barra_progresso < indice_linha_algoritmo_atual / \
                    numero_linhas_por_algoritmo[codigo_indice] * (x_tam_caixa - 80):
                tamanho_barra_progresso += 1
                troquei_linha = False

            # Mostra a sentença algorítica a ser digitada (em branco) -> fica por baixo dos caracteres verdes (corretos)
            linha_arquivo_renderizar = fonte_2.render(linha_arquivo_atual, False, WHITE)
            tela_principal.blit(linha_arquivo_renderizar, (x_pos_caixa + 68, y_pos_caixa + 80))

            # Imprime a partição já correta do texto (a parte correta será de outra cor, por cima da branca original)
            texto = ''
            for token in texto_base[0:indice_caractere_atual]:
                texto += token
            msg_texto = f'{texto}'
            msg_timer = f'Tempo: {timer_trecho_codigo:2.2f}'

            # Formatando textos
            msg_format_texto_base = fonte_2.render(msg_texto, False, GREEN)
            msg_algoritmo = f'{titulos_algoritmos[codigo_indice]}'
            msg_format_algoritmo = fonte_1.render(msg_algoritmo, False, WHITE)
            msg_format_placeholder = fonte_2.render(msg_input_placeholder, False, (100, 100, 100))
            msg_format_input_text = fonte_2.render(input_text, False, BLACK)
            if timer_trecho_codigo <= 5.00:
                cor_timer_perigo = RED
            else:
                cor_timer_perigo = WHITE
            msg_format_texto_timer_safe = fonte_timer.render(msg_timer[0:6], False, WHITE)
            msg_format_texto_timer_perigo = fonte_timer.render(msg_timer[7:], False, cor_timer_perigo)

            # Colocando textos na tela_principal
            tela_principal.blit(msg_format_texto_timer_safe, (1050, 25))
            tela_principal.blit(msg_format_texto_timer_perigo, (1150, 25))
            tela_principal.blit(msg_format_texto_base, (x_pos_caixa + 68, y_pos_caixa + 80))
            tela_principal.blit(tela_principal,
                                deslocamento)  # Atualiza a tela_principal com um screen shake quando o player erra
            tela_principal.blit(msg_format_algoritmo,
                                (x_pos_caixa + (x_tam_caixa / 2) - msg_format_algoritmo.get_width() / 2,
                                 y_pos_caixa + 20))
            tela_principal.blit(msg_format_input_text, (x_pos_caixa + 40, y_pos_caixa + 140))
            # Só mostra o placeholder (Digite aqui...) quando a caixa de input não está ativa e não tem nada escrito
            if input_text == '' and not active:
                tela_principal.blit(msg_format_placeholder, (x_pos_placeholder, y_pos_placeholder))

            # Colocando imagens na tela_principal (xicaras e cerebro)
            grupo_sprites_permanentes.draw(tela_principal)
            grupo_sprites_permanentes.update()
            grupo_sprites_janela.draw(tela_principal)
            grupo_sprites_janela.update()

            # Animando a xicara de café quando a energia está baixa
            if largura_barra_energia <= energia_baixa:
                xicara.flutuar(posicao_xicara)

            # Animando as estrelas e a lua
            lua.Animar()
            estrela_0.Animar()
            estrela_1.Animar()
            estrela_2.Animar()
            estrela_3.Animar()

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
            largura_barra_energia -= decremento_barra_energia

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
                    if largura_barra_energia <= energia_baixa:
                        if xicara.rect.collidepoint(pos):
                            largura_barra_energia += 380
                            drinking_sound.play()
                            xicara.stop_flutuar(posicao_xicara)

                    # Se o usuário clicar na caixa de texto, ativá-la. Se clicar fora da caixa, desativá-la
                    if input_texto_box.collidepoint(pos):
                        active = True
                        cor_input_box = WHITE  # cor branca ao clicar na caixa de texto da entrada
                    else:
                        active = False
                        cor_input_box = (180, 180, 180)  # cor padrão cinza quando a entrada não está selecionada

                # Verificando o pressionar das teclas
                if event.type == pygame.KEYDOWN:
                    if active:
                        # Se a fila estiver vazia, o jogador venceu o jogo
                        if not minha_fila.vazia():

                            not_unicodes_especiais = event.key != pygame.K_LSHIFT and \
                                                     event.key != pygame.K_RSHIFT and event.key != pygame.K_CAPSLOCK \
                                                     and event.key != pygame.K_BACKSPACE and \
                                                     event.key != pygame.K_LCTRL and \
                                                     event.key != pygame.K_RCTRL and event.key != pygame.K_LALT and \
                                                     event.key != pygame.K_RALT and event.key != pygame.K_UP and \
                                                     event.key != pygame.K_DOWN and event.key != pygame.K_LEFT and \
                                                     event.key != pygame.K_RIGHT and event.key != pygame.K_ESCAPE
                            # Se a fila não é vazia, verifica se a entrada do usuario é igual à primeira letra da fila
                            # e, se for, a remove e altera a cor da letra acertada para verde (atualiza o vetor de
                            # caracteres corretos)
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
                tomou_dano_por_tempo = False
            elif timer_trecho_codigo <= 0:
                tomou_dano_por_tempo = True
                input_text = ''
                minha_fila = fila.Fila()
                som_acabou_o_tempo.play()
                screen_shake = 10
                largura_barra_concentracao -= dano_acabou_tempo
                timer_trecho_codigo = delay_trecho_codigo

            # Esgotamento da barra de energia
            if largura_barra_energia <= 0 or largura_barra_concentracao <= 0:
                final_jogo = 'derrota'
                tela_menu_final = True

            #  linhas que começam com hashtag separam os algoritmos
            if indice_linha_atual - numero_hashtags == numero_linhas_arquivo:
                final_jogo = 'vitoria'
                tela_menu_final = True

            pygame.display.flip()
            # endregion


if __name__ == '__main__':
    coders_night()
