# importacao do pygame
import pygame
from pygame.locals import *
from sys import exit

from pygame.time import Clock

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
    # region inicializacao de dados que não se alteram
    # inicializacao da library do pygame
    pygame.init()
    # pygame.key.set_repeat(300, 110)  # permite segurar uma tela_principal (como apagar os caracteres com o backspace)

    # dimensoes da janela do jogo
    largura_janela = 1280
    altura_janela = 720

    # Pegando as dimensoes do monitor do usuario
    # ARRUMAR DEPOIS -> SE A TELA FOR PEQUENA, O JOGO NÃO VAI MOSTRAR TODAS AS INFO
    monitor = pygame.display.Info()
    if monitor.current_w < 1280:
        largura_janela = 960
        altura_janela = 540

    # Variável para controlar o fullscreen
    fullscreen = False

    # tela_principal do jogo
    tela_principal = pygame.display.set_mode((largura_janela, altura_janela))
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

    # definicao das fontes dos textos
    fonte_1 = pygame.font.SysFont('arial', 27, True, False)
    fonte_2 = pygame.font.SysFont('arial', 22, True, False)
    fonte_timer = pygame.font.SysFont('Rubik Wet Paint', 35, False, True)
    fonte_titulo_jogo = pygame.font.SysFont('Rubik Glitch', 80, True, True)

    # Grupo para os sprites
    grupo_sprites_permanentes = pygame.sprite.Group()

    # clock
    clk: Clock = pygame.time.Clock()

    # cor barra_energia
    red_barra_energia = red_barra_concentracao = 0
    green_barra_energia = green_barra_concentracao = 255

    # caixa de texto
    x_tam_caixa = 500
    y_tam_caixa = 300
    x_pos_caixa = largura_janela / 2 - x_tam_caixa / 2
    y_pos_caixa = altura_janela / 2 - y_tam_caixa / 2


    # Animação da xícara de café
    valor_seno_alfa_xicara = 1.57  # para animar a xicara (ficar piscando com energia baixa)

    # Títulos dos algoritmos
    titulos_algoritmos = ['Numero primo', 'PA', 'Sacar no Banco']

    # Mensagens fixas
    msg_progresso = 'Progresso'
    msg_input_placeholder = 'Digite aqui...'
    msg_botao_iniciar = 'Jogar'
    msg_nome_jogo = "Coder's Night"
    msg_botao_dificuldade = 'Dificuldade'
    msg_dificuldades = ['Fácil', 'Médio', 'Difícil']
    msg_botao_opcoes = 'Opções'
    msg_opcoes = ['Tela cheia']
    msg_botao_sair = 'Sair'

    # Posição fixa do texto 'Progresso'
    x_pos_progresso = x_pos_caixa + x_tam_caixa / 2
    y_pos_progresso = y_pos_caixa + y_tam_caixa - 95
    # Posição fixa do texto 'Digite aqui...'
    x_pos_placeholder = x_pos_caixa + 40
    y_pos_placeholder = y_pos_caixa + 140

    # endregion

    tela_menu_inicial = True
    tela_menu_final = False

    # Daqui pra cima, as declarações são fixas, pra baixo começa o loop que reseta as variáveis
    # laço do jogo inteiro (começa com a tela inicial e depois entra no laço principal do jogo)
    while True:

        # region Configurando tudo como o padrão inicial

        # Variaveis para tremer a tela_principal_principal com um erro do usuário
        screen_shake = 0
        deslocamento = [0, 0]

        # variáveis de input e texto base a ser digitado
        input_text = ''
        cor_input_box = (180, 180, 180)  # começa com um tom cinza quando está selecionado
        texto_base = ''

        # region Cria uma fila e a preenche com caracteres do arquivo de algoritmos

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
        # endregion

        # Controla a cor do algoritmo atual (trecho e borda da caixa)
        cor_algoritmo_atual = -1

        # Este indice é utilizado para saber a partição atual da 'string' que já foi acertada
        indice_caractere_atual = 0

        # Define o acesso à caixa de texto como falso
        active = False
        timer_cursor = 0.5

        # Codigo que indica qual o algoritmo atual (numero primo, PA, etc..)
        codigo_indice = -1

        # Timer para digitar o trecho de código
        delay_trecho_codigo = 20  # estava 15 (e tava dificil)
        timer_trecho_codigo = delay_trecho_codigo

        # endregion

        if tela_menu_inicial:
            pygame.mixer.music.load(os.path.join('Sons', 'musica_suspense_menu_game.mpeg'))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

        botao_iniciar_ativo = False
        botao_dificuldade_ativo = False
        botao_opcoes_ativo = False
        botao_sair_ativo = False

        mostrar_dificuldades = False
        mostrar_opcoes = False

        area_dificuldades = pygame.draw.rect(tela_principal, WHITE, (20, 20, 40, 40), 40)
        area_opcoes = pygame.draw.rect(tela_principal, WHITE, (20, 20, 40, 40), 40)

        while tela_menu_inicial:
            tela_principal.fill(BLACK)
            # Configura a cor dos botões do menu
            cor_botao_iniciar, cor_texto_botao_iniciar = game_end.configura_cor_botao(botao_iniciar_ativo)
            cor_botao_dificuldade, cor_texto_botao_dificuldade = game_end.configura_cor_botao(botao_dificuldade_ativo)
            cor_botao_sair, cor_texto_botao_sair = game_end.configura_cor_botao(botao_sair_ativo)
            cor_botao_opcoes, cor_texto_botao_opcoes = game_end.configura_cor_botao(botao_opcoes_ativo)

            # region Trabalhando o menu inicial do jogo
            # Retângulo principal com as opções
            pygame.draw.rect(tela_principal, (60, 60, 200),
                             (largura_janela / 2 - 200, altura_janela / 2 - 200, 400, 500), 200)
            # Contorno do retangulo principal com as opções
            pygame.draw.rect(tela_principal, WHITE, (largura_janela / 2 - 202,
                                                     altura_janela / 2 - 202, 402, 502), 4)
            # Botão iniciar o jogo
            botao_iniciar = pygame.draw.rect(tela_principal, cor_botao_iniciar,
                                             (largura_janela / 2 - 100, altura_janela / 2 - 150, 200, 80), 100)
            # Contorno do botão iniciar
            pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 102,
                                                     altura_janela / 2 - 152, 202, 82), 3)

            # Botão escolher dificuldade do jogo
            botao_dificuldade = pygame.draw.rect(tela_principal, cor_botao_dificuldade,
                                                 (largura_janela / 2 - 100, altura_janela / 2 - 45, 200, 80), 100)
            # Contorno do botao de dificuldade
            pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 102, altura_janela / 2 - 47, 202, 82), 3)

            # Botão de opções
            botao_opcoes = pygame.draw.rect(tela_principal, cor_botao_opcoes,
                                            (largura_janela / 2 - 100, altura_janela / 2 + 60, 200, 80), 100)
            # Contorno do botao de opções do jogo
            pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 102, altura_janela / 2 + 58, 202, 82), 3)

            # Botão sair do jogo
            botao_sair = pygame.draw.rect(tela_principal, cor_botao_sair,
                                          (largura_janela / 2 - 100, altura_janela / 2 + 165, 200, 80), 100)
            # Contorno do botão de sair do jogo
            pygame.draw.rect(tela_principal, BLACK, (largura_janela / 2 - 102, altura_janela / 2 + 163, 202, 82), 3)

            # Textos
            msg_format_nome_jogo = fonte_titulo_jogo.render(msg_nome_jogo, True, WHITE)
            msg_format_botao_iniciar = fonte_1.render(msg_botao_iniciar, True, cor_texto_botao_iniciar)
            msg_format_botao_dificuldade = fonte_1.render(msg_botao_dificuldade, True, cor_texto_botao_dificuldade)
            msg_format_botao_opcoes = fonte_1.render(msg_botao_opcoes, True, cor_texto_botao_opcoes)
            msg_format_botao_sair = fonte_1.render(msg_botao_sair, True, cor_texto_botao_sair)

            # Colocando os textos na tela
            tela_principal.blit(msg_format_nome_jogo, (largura_janela / 2 - 220, 70))
            tela_principal.blit(msg_format_botao_iniciar, (largura_janela / 2 - 39, altura_janela / 2 - 130, 185, 80))
            tela_principal.blit(msg_format_botao_dificuldade,
                                (largura_janela / 2 - 78, altura_janela / 2 - 22, 200, 80))
            tela_principal.blit(msg_format_botao_opcoes, (largura_janela / 2 - 55, altura_janela / 2 + 82, 200, 80))
            tela_principal.blit(msg_format_botao_sair, (largura_janela / 2 - 30, altura_janela / 2 + 187, 200, 80))

            if mostrar_dificuldades:
                #  Desenhando o retângulo principal com as dificuldades do jogo
                area_dificuldades = pygame.draw.rect(tela_principal, WHITE, (largura_janela / 2 - 100,
                                                                             altura_janela / 2 + 20, 200, 200), 200)
            if mostrar_opcoes:
                # Desenhando o retângulo principal com as opções do jogo
                area_opcoes = pygame.draw.rect(tela_principal, WHITE,
                                               (largura_janela / 2 - 100, altura_janela / 2 + 140,
                                                200, 200), 200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                posicao_mouse = pygame.mouse.get_pos()
                if botao_iniciar.collidepoint(posicao_mouse):
                    botao_iniciar_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        tela_menu_inicial = False
                        pygame.mixer.music.load(os.path.join('Sons', "musica_lofi.mp3"))
                        pygame.mixer.music.set_volume(0.4)
                        pygame.mixer.music.play(-1)
                else:
                    botao_iniciar_ativo = False
                if botao_dificuldade.collidepoint(posicao_mouse):
                    botao_dificuldade_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mostrar_dificuldades = not mostrar_dificuldades
                else:
                    botao_dificuldade_ativo = False
                if botao_sair.collidepoint(posicao_mouse):
                    botao_sair_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        exit()
                else:
                    botao_sair_ativo = False
                if botao_opcoes.collidepoint(posicao_mouse):
                    botao_opcoes_ativo = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mostrar_opcoes = not mostrar_opcoes
                else:
                    botao_opcoes_ativo = False
                # Se o usuário clicar em um lugar da tela que não seja o menu habilitado, este menu fecha
                if event.type == MOUSEBUTTONDOWN:
                    if mostrar_opcoes and not area_opcoes.collidepoint(posicao_mouse):
                        mostrar_opcoes = False
                    if mostrar_dificuldades and not area_opcoes.collidepoint(posicao_mouse):
                        mostrar_dificuldades = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        fullscreen = True
                        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    elif event.key == pygame.K_DOWN:
                        pygame.display.set_mode((largura_janela, altura_janela))

            pygame.display.flip()
            # endregion

        # region Configurando sempre a dimensão pois é possível que o usuário tenha habilitado fullscreen
        # Configurando as dimensões das coisas com base na largura e altura da tela (necessário caso o
        # usuário tenha colocado em fullscreen no menu inicial, por exemplo)
        monitor = pygame.display.Info()
        largura_janela = monitor.current_w
        altura_janela = monitor.current_h

        # dimensoes das barras de concentração e energia
        largura_max = largura_janela * 0.84375
        largura_barra_energia = largura_max
        largura_barra_concentracao = largura_max

        x_pos_barra_energia = largura_janela * 0.078125
        y_pos_barra_energia = altura_janela * 0.8888888888888

        x_pos_barra_conc = x_pos_barra_energia
        y_pos_barra_conc = altura_janela * 0.78472222222

        # imagens
        largura_xicara = altura_xicara = largura_janela * 0.04296875
        img_xicara_cafe = pygame.image.load(os.path.join('Imagens', 'xicara.png')).convert_alpha()
        img_xicara_cafe = pygame.transform.scale(img_xicara_cafe, (largura_xicara, altura_xicara))

        largura_cerebro = altura_cerebro = largura_janela * 0.04296875
        img_cerebro = pygame.image.load(os.path.join('Imagens', 'brain.png')).convert_alpha()
        img_cerebro = pygame.transform.scale(img_cerebro, (largura_cerebro, altura_cerebro))

        # criando os objetos
        x_pos_xicara = largura_xicara - (0.1 * largura_xicara)
        x_pos_cerebro = largura_cerebro - (0.1 * largura_cerebro)
        y_pos_xicara = altura_janela * 0.90972222222
        y_pos_cerebro = altura_janela * 0.80555555555
        xicara_cafe = game_end.FiguraClicavel(img_xicara_cafe, (x_pos_xicara, y_pos_xicara))
        cerebro = game_end.FiguraClicavel(img_cerebro, (x_pos_cerebro, y_pos_cerebro))

        grupo_sprites_permanentes.add(xicara_cafe, cerebro)
        #endregion

        # Trabalhando na tela do menu final
        while tela_menu_final:
            pass

        # Laço principal do jogo
        while True:
            # region Jogo de fato (toda a lógica)
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
            pygame.draw.rect(tela_principal, GREEN, (x_pos_caixa + 40,
                                                     y_pos_caixa + y_tam_caixa - 55,
                                                     (indice_linha_atual - 1) / numero_linhas_arquivo *
                                                     (x_tam_caixa - 80), 35))
            # Retângulo de contorno do retângulo de progresso do jogo
            pygame.draw.rect(tela_principal, BLACK,
                             (x_pos_caixa + 38, y_pos_caixa + y_tam_caixa - 57, x_tam_caixa - 78, 37), 3)

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
            # Só mostra o placeholder (Digite aqui...) quando a caixa de input não está ativa e não tem nada escrito
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
                                                     event.key != pygame.K_RSHIFT and event.key != pygame.K_CAPSLOCK \
                                                     and event.key != pygame.K_BACKSPACE and \
                                                     event.key != pygame.K_LCTRL and \
                                                     event.key != pygame.K_RCTRL and event.key != pygame.K_LALT and \
                                                     event.key != pygame.K_RALT and event.key != pygame.K_UP and \
                                                     event.key != pygame.K_DOWN and event.key != pygame.K_LEFT and \
                                                     event.key != pygame.K_RIGHT
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
            # endregion


if __name__ == '__main__':
    coders_night()
