from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from settings import *

def placarLoop(janela):
    teclado = janela.get_keyboard()

    #Abre o arquivo para leitura somente
    arq = open("placar.txt",'r')
    all_lines = arq.readlines()

    while(True):
        janela.set_background_color([0,0,0])

        janela.draw_text("Placar", janela_WIDTH/2 - 75, 20, 60, (255,255,255))

        #Variável para limitar o número de players que são exibidos
        aux_placar = 0

        #Percorre todas as linhas do arquivo desenhando-as na tela
        for k,line in enumerate(all_lines):
            if(aux_placar > 9):
                break
            line = line.strip('\n')
            janela.draw_text(line, janela_WIDTH/2 - 100, 100 + k * 40, 25, (255,255,255))
            aux_placar += 1

        if(teclado.key_pressed("escape")):
            return 0

        janela.update()
