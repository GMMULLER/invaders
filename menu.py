from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from settings import *
from jogo import *
from dificuldade import *
from placar import *
from operator import itemgetter, attrgetter

mouse = Mouse()

def menuLoop(janela):

    button_1 = Sprite(button_menu_SPRITE_1)
    button_2 = Sprite(button_menu_SPRITE_2)
    button_3 = Sprite(button_menu_SPRITE_3)
    button_4 = Sprite(button_menu_SPRITE_4)

    button_2.set_position(janela_WIDTH/2 - button_2.width/2, int(janela_HEIGHT/2 - button_2.height - BUTTON_SPACE))
    button_1.set_position(janela_WIDTH/2 - button_1.width/2, int(button_2.y - button_1.height - BUTTON_SPACE))
    button_3.set_position(janela_WIDTH/2 - button_3.width/2, int(janela_HEIGHT/2 + BUTTON_SPACE/2))
    button_4.set_position(janela_WIDTH/2 - button_4.width/2, int(button_3.y + button_3.height + BUTTON_SPACE))

    #Marca o momento que a função foi chamada
    tempo_entrada = 0
    mouse_click_state = False

    #Por default a dificuldade do jogo é Fácil
    dificuldade = 1

    while(True):
        pontuacao = 0

        janela.set_background_color([0,0,0])

        #Sistema de clique para o primeiro botão
        if(mouse.is_over_object(button_1)):
            if(mouse.is_button_pressed(1)):
                if(not mouse_click_state):
                    pontuacao = jogoLoop(janela, dificuldade)
                    #Se o jogador tiver feito alguma pontuação é inserido no arquivo e ordenado
                    if(pontuacao != 0):
                        #Abre o arquivo para atualização
                        arq = open("placar.txt", 'a+')
                        print("Nome: ")
                        nome = input()
                        aux_print = str(nome)+": "+str(pontuacao)+"\n"
                        arq.write(aux_print)
                        #Recoloca o ponteiro do arquivo para o começo
                        arq.seek(0)
                        all_lines = arq.readlines()
                        aux_format_lines = []
                        arq.close()
                        #Percorre todas as linhas do arquivo criando uma matriz com as pontuações em int
                        for k,player in enumerate(all_lines):
                            aux_nome = player.split(':')
                            #Retira o espaço antes do número
                            aux_pontuacao = int(aux_nome[1].lstrip())
                            aux_format_lines.append([aux_nome[0],aux_pontuacao])

                        #Ordena as linhas em ordem decrescente em relação à pontuação
                        all_lines_sorted = sorted(aux_format_lines, key = itemgetter(1), reverse = True)
                        #Reabre o arquivo para sobreescrita
                        arq = open("placar.txt", 'w')
                        for player in all_lines_sorted:
                            # [0] - Nome, [1] - Pontuação
                            aux_print = player[0]+": "+str(player[1])+"\n"
                            arq.write(aux_print)
                        arq.close()
                        #Retorna mostra o placar para o jogador
                        placarLoop(janela)
                mouse_click_state = True
            else:
                mouse_click_state = False

        #Sistema de clique para o segundo botão
        elif(mouse.is_over_object(button_2)):
            if(mouse.is_button_pressed(1)):
                if(not mouse_click_state):
                    dificuldade = dificuldadeLoop(janela)
                mouse_click_state = True
            else:
                mouse_click_state = False

        #Sistema de clique para o terceiro botão
        elif(mouse.is_over_object(button_3)):
            if(mouse.is_button_pressed(1)):
                if(not mouse_click_state):
                    placarLoop(janela)
                mouse_click_state = True
            else:
                mouse_click_state = False

        #Sistema de clique para o quarto botão
        elif(mouse.is_over_object(button_4)):
            if(mouse.is_button_pressed(1)):
                if(not mouse_click_state):
                    janela.close()
            else:
                mouse_click_state = False

        button_1.draw()
        button_2.draw()
        button_3.draw()
        button_4.draw()

        janela.update()
