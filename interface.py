import pygame
import sys

pygame.init()
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Q*bert")
relogio = pygame.time.Clock()

try:
    img_bloco_dir = pygame.image.load("sprites/cenario/plataforma-direita.png").convert_alpha()
    img_bloco_esq = pygame.image.load("sprites/cenario/plataforma-esquerda.png").convert_alpha()
    img_agente = pygame.image.load("sprites/qbert/qbert-frente-esquerda.png").convert_alpha()

    multiplicador_x = 1.4
    multiplicador_y = 1

    nova_largura = int(img_bloco_dir.get_width() * multiplicador_x)
    nova_altura = int(img_bloco_dir.get_height() * multiplicador_y)

    img_bloco_dir = pygame.transform.scale(img_bloco_dir, (nova_largura, nova_altura))
    img_bloco_esq = pygame.transform.scale(img_bloco_esq, (nova_largura, nova_altura))
except FileNotFoundError:
    print("Erro: Imagem não encontrada. Verifique o caminho da pasta.")
    sys.exit()

ESPACAMENTO_X = 94  
ESPACAMENTO_Y = 58  

linha_agente = 0
coluna_agente = 0

def rodar(env, agente):
    global linha_agente, coluna_agente

    # Sincroniza a posição inicial
    posicao_atual = env.posicao_agente 
    linha_agente, coluna_agente = posicao_atual

    # Usamos o relógio do Pygame para controlar o tempo entre os passos (ex: a cada 500ms)
    TEMPO_POR_PASSO = 500  # milissegundos
    ultimo_passo = pygame.time.get_ticks()

    rodando = True
    while rodando:
        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
        
        # --- O AGENTE MOVE UM PASSO POR VEZ (Sem congelar a tela) ---
        if tempo_atual - ultimo_passo > TEMPO_POR_PASSO:
            ultimo_passo = tempo_atual
            
            # Pede a próxima ação para o agente atual
            acao = agente.obter_acao(env.estado_blocos, env.posicao_agente, env.grafo)
            
            if acao is not None:
                nova_posicao, recompensa, vitoria = env.step(acao)
                linha_agente, coluna_agente = nova_posicao
                
                print(f"IA moveu para: Linha {linha_agente}, Coluna {coluna_agente} | Recompensa: {recompensa}")
                
                if vitoria:
                    print("VITÓRIA! A IA completou o nível!")
                    rodando = False
                elif recompensa == -10:
                    print("GAME OVER! O Q*bert caiu no abismo!")
                    rodando = False
            else:
                print("A IA chegou ao objetivo ou não encontrou caminho.")
                rodando = False

        # --- DESENHO CONSTANTE DA TELA ---
        tela.fill((0, 0, 0))
        
        x_topo = LARGURA // 2 - (ESPACAMENTO_X // 2)
        y_topo = 100
        
        for linha in range(6):
            for coluna in range(linha + 1):
                x_pixel = x_topo + (coluna * ESPACAMENTO_X) - (linha * (ESPACAMENTO_X // 2))
                y_pixel = y_topo + (linha * ESPACAMENTO_Y)
                
                if coluna % 2 == 0:
                    tela.blit(img_bloco_dir, (x_pixel, y_pixel))
                else:
                    tela.blit(img_bloco_esq, (x_pixel, y_pixel))
       
        largura_agente = img_agente.get_width()
        altura_agente = img_agente.get_height()
        largura_bloco = img_bloco_dir.get_width()

        x_base_bloco = x_topo + (coluna_agente * ESPACAMENTO_X) - (linha_agente * (ESPACAMENTO_X // 2))
        y_base_bloco = y_topo + (linha_agente * ESPACAMENTO_Y)

        x_agente = x_base_bloco + (largura_bloco // 2) - (largura_agente // 2)
        y_agente = y_base_bloco - altura_agente + (ESPACAMENTO_Y // 2) - 24
        
        tela.blit(img_agente, (x_agente, y_agente))

        pygame.display.flip()
        relogio.tick(30)

    pygame.quit()