#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:07:45 2019

@author: digomattar
"""

# -*- coding: utf-8 -*-
 
# Importando as bibliotecas necessárias.
import pygame
from os import path
import random
from random import randint

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Criando uma classe Mob
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Carregando a imagem
        mob_img= pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
        self.image = pygame.transform.scale(mob_img,(50,30))
        
        #Colocando a posicao do meteoro
        posicaox = random.randrange(0,WIDTH)
        posicaoy = random.randrange(-100,-40)
        #Detalhes sobre o posicionamento
        self.rect = self.image.get_rect()
        self.rect.x = posicaox
        self.rect.y = posicaoy
        #Velocidade aleatoria
        velx = random.randrange(-3,3)
        vely = random.randrange(2,9)
        #raio do meteoro
        self.radius = int(self.rect.width*.85/2)
        
        self.speedx = velx
        self.speedy = vely
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
 #classe player           
class Player(pygame.sprite.Sprite):
#Adiucionando uma Nave
    def __init__(self):
        #construtor da classe pai (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem de de fundo
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = player_img
        
        #Diminuindo o tamanho da imagem 
        self.image = pygame.transform.scale(player_img, (50,38))
        
        #Deixando trasnparente 
        self.image.set_colorkey(BLACK)
        
        #Detalhes sobre o posicionamento
        self.rect = self.image.get_rect()
        
        #centraliza embaixo da tela
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10 
        
        #velocidade da nave 
        self.speedx = 0 
        
        #raio da nbave
        self.radius = 25
        
    def update(self):
        self.rect.x += self.speedx
        
        #Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0 
            

 
    
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Asteroids")

#Nome do jogo
pygame.display.set_caption("Navinha")

#Variavel para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
#carrega os sons do jogo
pygame.mixer.music.load(path.join(snd_dir,('tgfcoder-FrozenJam-SeamlessLoop.ogg')))
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound(path.join(snd_dir,'expl3.wav'))

#cria uma nave o construtor sera chamado automaticamente
player = Player()
#cria um grupo para todos os sprites e adiciona umanave
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#cria um grupo soh dos meteoros 
mobs = pygame.sprite.Group()

#cria um grupo para tiros 
bullets = pygame.sprite.Group()


# Inicialização do Pygame.
#Cria uma nave. O construtor sera chamado automaticamente
player = Player()

#Cria um grupo de sprites e adiciona a nave
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
#cria 8 meteoros
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
# Comando para evitar travamentos.
try:
    
    # Loop principal.
    running = True
    pygame.mixer.music.play(loops=-1)
    while running:
        
        #Ajusta a velocidade do jogo
        clock.tick(FPS)
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #Verifica se apertou alguma tecla
            if event.type == pygame.KEYDOWN:
                #Depdendendo da tecla, altera a velocidade 
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                    
            #Verifica se soltou alguma tecla
            if event.type == pygame.KEYUP:
                #Dependendo da tecla, altera a velocidade
                if event.key == pygame.K_LEFT:
                    player.sppedx = 0 
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                    
        #Depois de processar od eventos 
        #Atualiza a acao de cada sprite
        all_sprites.update()
        
        #verifica se houve colisao entre nave e meteoro
        hits = pygame.sprite.spritecollide(player,mobs,False, pygame.sprite.collide_circle)
        if hits:
            #toca o som da colisao
            boom_sound.play()
            time.sleep(1) #precisa esperar senao fecha
            
            running = False
            
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
