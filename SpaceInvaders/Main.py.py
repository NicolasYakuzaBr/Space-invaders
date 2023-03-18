import pygame 
import math
import random 


pygame.init()

#Criar Janela |altura = 800, largura = 600|
janela = pygame.display.set_mode((800,600))

#Janelinha
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Imagem de fundo 
fundo = pygame.image.load("fundo.png")

#som
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)

#Cores RgB
vermelho = (255,0,0)
verde = (0,255,0)
azul = (0,0,255)
preto = (0,0,0)
branco = (255,255,255)

#Jogador
jogador_imagem = pygame.image.load('nave.png')
jogadorX = 370
jogadorY = 480
jogador_movimento = 0

#inimigo
inimigo_imagem = []
inimigoX = []
inimigoY = []
inimigoX_movimento = []
inimigoY_movimento = []
num_inimigos = 6

for i in range(num_inimigos):
    inimigo_imagem.append(pygame.image.load('inimigo.png'))
    inimigoX.append(random.randint(0, 736))
    inimigoY.append(random.randint(50, 150))
    inimigoX_movimento.append(4)
    inimigoY_movimento.append(40)

#Projétil

bala = pygame.image.load('bala.png')
balaX = 0
balaY = 480
balaX_movimento = 0
balaY_movimento = 10
bala_status = 'pronto'

#Placar
placar_valor = 0
fonte = pygame.font.Font('freesansbold.ttf', 32)

textoX = 10
textoY = 10

#Fim de jogo
fim_fonte = pygame.font.Font('freesansbold.ttf', 64)

def mostrar_pontos(x,y):
    pontos = fonte.render('Pontos: ' + str(placar_valor), True, (255,255,255))
    janela.blit(pontos, (x,y))

def fim_do_jogo_texto():
    fim_texto = fim_fonte.render("Fim do jogo!", True, (255,255,255))
    janela.blit(fim_texto, (200,250))

def jogador(x,y):
    janela.blit(jogador_imagem, (x,y))

def inimigo(x,y,i):
    janela.blit(inimigo_imagem[i], (x,y))

def atirando(x,y):
    global bala_status
    bala_status = 'atirar'
    janela.blit(bala, (x + 16, y +10))

def colisão(inimigoX, inimigoY, balaX, balaY):
    distância = math.sqrt(math.pow(inimigoX - balaX, 2) + (math.pow(inimigoY - balaY, 2)))
    if distância < 27:
        return True
    else:
        return False
    

#Variaveis_Global
executando = True
    

while executando:

    # RGB = Red, Green, Blue
    janela.fill(preto)
    # Background Image
    janela.blit(fundo, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jogador_movimento = -5
            if event.key == pygame.K_RIGHT:
                jogador_movimento = 5
            if event.key == pygame.K_SPACE:
                if bala_status == "pronto":
                    bulletSound = pygame.mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    balaX = jogadorX
                    atirando(balaX, balaY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jogador_movimento = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    jogadorX += jogador_movimento
    if jogadorX <= 0:
        jogadorX = 0
    elif jogadorX >= 736:
        jogadorX = 736

    # Enemy Movement
    for i in range(num_inimigos):

        # Game Over
        if inimigoY[i] > 440:
            for j in range(num_inimigos):
                inimigoY[j] = 2000
            fim_do_jogo_texto()
            music_fim = pygame.mixer.Sound('fim.wav')
            music_fim.play()
    
            break

        inimigoX[i] += inimigoX_movimento[i]
        if inimigoX[i] <= 0:
            inimigoX_movimento[i] = 4
            inimigoY[i] += inimigoY_movimento[i]
        elif inimigoX[i] >= 736:
            inimigoX_movimento[i] = -4
            inimigoY[i] += inimigoY_movimento[i]

        # Collision
        colidir = colisão(inimigoX[i], inimigoY[i], balaX, balaY)
        if colidir:
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()
            balaY = 480
            bala_status = "pronto"
            placar_valor += 1
            inimigoX[i] = random.randint(0, 736)
            inimigoY[i] = random.randint(50, 150)

        inimigo(inimigoX[i], inimigoY[i], i)

    # Bullet Movement
    if balaY <= 0:
        balaY = 480
        bala_status = "pronto"

    if bala_status == "atirar":
        atirando(balaX, balaY)
        balaY -= balaY_movimento

    jogador(jogadorX, jogadorY)
    mostrar_pontos(textoX, textoY)
    pygame.display.update()
