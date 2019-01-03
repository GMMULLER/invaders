from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from settings import *
import random

def jogoLoop(janela,dificuldade):
    sp_monster = None
    teclado = janela.get_keyboard()

    #Configurações
    h_pressed = False
    show_fps = False
    dificult = dificuldade
    points = 0

    #Player
    player_life = 3
    player_vel = PLAYER_V * 10/dificult
    player = Sprite(player_img)
    player.set_position(janela_WIDTH/2 - PLAYER_WIDTH/2, janela_HEIGHT - 2 - PLAYER_HEIGHT)

    #Shoots
    shoot_vel = SHOOT_V * 10/dificult
    enemy_shoot_vel = SHOOT_V * 5/dificult
    shoots = []
    last_shoot = 0
    enemy_shoot_delay = 2000/(dificult * 0.8)
    last_enemy_shoot = 0
    enemy_shoots = []

    #Enemy
    #Com base no tamanho da tela calcula quantos monstros devem ter na matriz
    enemy_per_line = int(janela_WIDTH/(enemy1_width + enemy_padding + 3/100 * janela_WIDTH) - 2)
    enemy_per_col = int(janela_HEIGHT/(enemy1_height + enemy_padding + 3/100 * janela_HEIGHT) - 2)

    #Matriz
    matriz_mov_delay = 1000/(dificult * 0.7)
    matriz_width = ((enemy_per_line - 1) * (enemy1_width + enemy_padding) + enemy1_width)
    matriz_height = ((enemy_per_col - 1) * (enemy1_height + enemy_padding) + enemy1_height)
    matriz = []
    matriz_x = janela_WIDTH/2 - matriz_width/2
    matriz_y = 3/100 * janela_HEIGHT
    matriz_x_vel = matriz_x_ch
    left_collide = False
    right_collide = True

    #A cada 2 segundos a matriz move k pixels no eixo x
    last_mov = 0

    #Contador do fps
    fps_delay = 0

    #Animação
    explosoes = []

    rand_x = random.randint(0,enemy_per_col-1)
    rand_y = random.randint(0,enemy_per_line-1)

    #Cria a matriz de monstros inicial
    for i in range(0,enemy_per_col):
        aux = []
        aux_padding_y = 0
        if(i != 0):
            aux_padding_y = enemy_padding
        for j in range(0,enemy_per_line):
            aux_padding_x = 0
            if(j != enemy_per_line):
                aux_padding_x = enemy_padding
            if(i == rand_x and j == rand_y):
                enemy_aux = Sprite(enemy1_img_sp)
                sp_monster = enemy_aux
            else:
                enemy_aux = Sprite(enemy1_img)
            enemy_aux.set_position((j * (enemy1_width + enemy_padding)) + matriz_x, (i * (enemy1_height + enemy_padding)) + matriz_y)
            aux.append(enemy_aux)
        matriz.append(aux)


    while(True):
        janela.set_background_color([0,0,0])

        if(teclado.key_pressed("escape")):
            return points

        if(teclado.key_pressed("h")):
            if(not h_pressed):
                show_fps = not show_fps
            h_pressed = True
        else:
            h_pressed = False

        fps_delay += janela.delta_time()

        if(show_fps):
            #Só atualiza o fps a cada 0.75 segundos
            if(fps_delay >= 0.75):
                fps_delay = 0
                if(janela.delta_time() == 0):
                    text = "999"
                else:
                    text = str(int(1/janela.delta_time()))
            janela.draw_text(text, 5, 5, 12, (255,255,255))

        #Desenha a pontuação
        aux_points = "Points: "+str(points)
        janela.draw_text(aux_points, janela_WIDTH - 150, 20, 20, (255,255,255))

        #Desenha a quantidade de vida do player
        aux_life = "Life: "+str(player_life)
        janela.draw_text(aux_life, janela_WIDTH - 150, 50, 20, (255,255,255))

        #Faz o controle da movimentação do Player (d -> Direita, a -> Esquerda)
        if(teclado.key_pressed("d")):
            player.x += player_vel * janela.delta_time()
        elif(teclado.key_pressed("a")):
            player.x -= player_vel * janela.delta_time()

        #Faz o sistema de Warp do player nas bordas da tela
        if(player.x > janela_WIDTH):
            player.x = 0 - PLAYER_WIDTH
        if(player.x + PLAYER_WIDTH < 0):
            player.x = janela_WIDTH

        #Faz o disparo do tiro do Player
        if(janela.time_elapsed() - last_shoot > RELOAD_TIME * dificult):
            if(teclado.key_pressed("space")):
                last_shoot = janela.time_elapsed()
                shoot = Sprite(shoot_img)
                shoot.x = player.x + PLAYER_WIDTH/2
                shoot.y = player.y + 5
                shoots.append(shoot)

        #Atualiza a posição de cada tiro do Player
        for k,shoot in enumerate(shoots):
            #Se o tiro sair da tela ele deve ser destruido
            if(shoot.y - shoot.height < 0):
                del shoots[k]
            else:
                shoot.y -= shoot_vel * janela.delta_time()
                shoot.draw()

        #Redesenha os monstros com base no offset da matriz
        matriz_is_empty = True
        for i,line in enumerate(matriz):
            for j,enemy in enumerate(line):
                if(enemy != None):
                    #Guarda se a matriz está vazia
                    matriz_is_empty = False
                    enemy.set_position((j * (enemy1_width + enemy_padding)) + matriz_x, (i * (enemy1_height + enemy_padding)) + matriz_y)
                    enemy.draw()

        #Uma nova Wave só é criada se a matriz atual estiver vazia e ocupar menor de 2/3 do tamanho da tela
        if(matriz_is_empty and matriz_width < 2/3 * janela_WIDTH):
            #Cada level rende ao Player 1000 pontos
            points += 1000
            #Cada level aumenta a dificuldade em 0.5
            dificult += 0.5
            #Atualiza os valores que dependem da dificuldade
            player_vel = PLAYER_V * 10/dificult
            shoot_vel = SHOOT_V * 10/dificult
            matriz_mov_delay = 1000/(dificult * 0.7)
            enemy_shoot_delay = 1000/(dificult * 0.8)

            #Limpa a matriz de monstros
            matriz = []
            #Os monstros só são adicionados no sentido horizontal
            enemy_per_line = enemy_per_line + 1
            matriz_width += enemy1_width + enemy_padding
            matriz_x = janela_WIDTH/2 - matriz_width/2
            matriz_y = 3/100 * janela_HEIGHT

            #Randomiza o monstro especial
            rand_x = random.randint(0,enemy_per_col-1)
            rand_y = random.randint(0,enemy_per_line-1)

            #Passa novamente pelo processo de criação da matriz
            for i in range(0,enemy_per_col):
                aux = []
                aux_padding_y = 0
                if(i != 0):
                    aux_padding_y = enemy_padding
                for j in range(0,enemy_per_line):
                    aux_padding_x = 0
                    if(j != enemy_per_line):
                        aux_padding_x = enemy_padding
                    if(rand_x == i and rand_y == j):
                        enemy_aux = Sprite(enemy1_img_sp)
                        sp_monster = enemy_aux
                    else:
                        enemy_aux = Sprite(enemy1_img)
                    enemy_aux.set_position((j * (enemy1_width + enemy_padding)) + matriz_x, (i * (enemy1_height + enemy_padding)) + matriz_y)
                    aux.append(enemy_aux)
                matriz.append(aux)

        #Faz a movimentação de toda a matriz a cada determinado tempo
        if(janela.time_elapsed() - last_mov > matriz_mov_delay):
            last_mov = janela.time_elapsed()
            aux = -2
            #Faz os testes de colisão que são retornados para a variável aux
            for linha in matriz:
                for enemy in linha:
                    if(enemy != None):
                        #Testa se o monstro se chocou contra o player
                        if(enemy.y + enemy1_height >= player.y):
                            aux = 0
                            break
                        #Testa se o monstro está a 20 pixels de distância da borda e se ele pode colidir com o lado direito
                        if(enemy.x + enemy1_width > janela_WIDTH - 20 and right_collide):
                            #Como a movimentação da matriz é feita com porções de 10 pixels, deve-se
                            #criar uma flag que irá sinalizar se a matriz já colidiu com a extremidade
                            #oposta da tela, evitando sucessivas colisões
                            left_collide = True
                            right_collide = False
                            aux = -1
                            break
                        #Faz o mesmo do anterior, porém para o lado esquerdo
                        if(enemy.x < 20 and left_collide):
                            left_collide = False
                            right_collide = True
                            aux = -1
                            break
                #Se algum monstro já colidiu não a necessidade de continuar testando
                if(aux != -2):
                    break

            #Fim de jogo
            if(aux == 0):
                return points
            #Os monstros começam a se deslocar para o lado oposto
            elif(aux == -1):
                matriz_x_vel *= -1
                matriz_y += matriz_y_ch
            matriz_x += matriz_x_vel

        #Cria os tiros dos monstros
        if(janela.time_elapsed() - last_enemy_shoot > enemy_shoot_delay):
            last_enemy_shoot = janela.time_elapsed()
            aux_vetor_enemy = []
            #Percorre a matriz guardando todos os monstros que ainda estão vivos
            for i in matriz:
                for enemy in i:
                    if(enemy != None):
                        aux_vetor_enemy.append(enemy)

            #Escolhe um monstro aleatóriamente para atirar
            random.shuffle(aux_vetor_enemy)
            aux_shoot = Sprite(shoot_img)
            aux_shoot.x = aux_vetor_enemy[0].x + enemy1_width/2
            aux_shoot.y = aux_vetor_enemy[0].y + enemy1_height + 5
            enemy_shoots.append(aux_shoot)

        #Testa se cada tiro dos monstros se chocou contra o player
        for k,tiro in enumerate(enemy_shoots):
            if(tiro.y >= player.y):
                if(tiro.collided(player)):
                    player_life -= 1
                    del enemy_shoots[k]

        #Atualiza o tiro dos monstros
        for k,shoot in enumerate(enemy_shoots):
            #Testa se o tiro saiu da janela
            if(shoot.y > janela_HEIGHT):
                del enemy_shoots[k]
            else:
                shoot.y += enemy_shoot_vel * janela.delta_time()
                shoot.draw()

        if(player_life <= 0):
            return points

        #Colisão do tiro otimizada (FPS ocilando entre 200 e 300)
        for k,tiro in enumerate(shoots):
            #Otimização de colisão
            if(tiro.x >= matriz_x and tiro.x <= matriz_x + matriz_width and tiro.y >= matriz_y and tiro.y <= matriz_y + matriz_height):
                for i in range(len(matriz) - 1,-1,-1):
                    for j in range(len(matriz[i]) - 1,-1,-1):
                        if(matriz[i][j] != None):
                            if(tiro.collided(matriz[i][j])):
                                if(matriz[i][j] == sp_monster):
                                    player_life += 1
                                aux_explosao = Sprite("images/explosion.png", 14)
                                aux_explosao.set_total_duration(1000)
                                aux_explosao.set_position(matriz[i][j].x, matriz[i][j].y)
                                aux_explosao.set_loop(False)
                                explosoes.append(aux_explosao)
                                matriz[i][j] = None
                                points += 100
                                del shoots[k]

        #Colisão do tiro sem otimização (FPS ocilando entre 150 e 250)
        # for k,tiro in enumerate(shoots):
        #     for i in range(len(matriz)):
        #         for j in range(len(matriz[i])):
        #             if(matriz[i][j] != None):
        #                 if(tiro.collided(matriz[i][j])):
        #                     matriz[i][j] = None
        #                     del shoots[k]

        #Deleta todas as explosões que não estão mais animando
        #Desenha todas que ainda tem animação
        for k,explosao in enumerate(explosoes):
            if not explosao.is_playing():
                del explosoes[k]
            else:
                explosao.draw()
                explosao.update()

        player.draw()

        janela.update()
