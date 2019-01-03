from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from settings import *

def dificuldadeLoop(janela):

    button_1 = Sprite(button_dif_SPRITE_1)
    button_2 = Sprite(button_dif_SPRITE_2)
    button_3 = Sprite(button_dif_SPRITE_3)

    button_2.set_position(janela_WIDTH/2 - button_2.width/2, int(janela_HEIGHT/2 - button_2.height/2))
    button_1.set_position(janela_WIDTH/2 - button_1.width/2, int(button_2.y - button_1.height - BUTTON_SPACE))
    button_3.set_position(janela_WIDTH/2 - button_3.width/2, int(button_2.y + button_2.height + BUTTON_SPACE))

    mouse = Mouse()
    mouse_click_state = True
    tempo_entrada = janela.time_elapsed()

    while(True):
        janela.set_background_color([0,0,0])

        button_1.draw()
        button_2.draw()
        button_3.draw()

        janela.update()

        #Testa clique com o primeiro botão
        if(mouse.is_over_object(button_1)):
            if(mouse.is_button_pressed(1)):
                if(not mouse_click_state):
                    dificuldade = 1
                    return dificuldade
            else:
                mouse_click_state = False

        #Testa clique com o segundo botão
        elif(mouse.is_over_object(button_2)):
                if(mouse.is_button_pressed(1)):
                    if(not mouse_click_state):
                        dificuldade = 2
                        return dificuldade
                else:
                    mouse_click_state = False

        #Testa clique com o terceiro botão
        elif(mouse.is_over_object(button_3)):
                if(mouse.is_button_pressed(1)):
                    if(not mouse_click_state):
                        dificuldade = 3
                        return dificuldade
                else:
                    mouse_click_state = False
