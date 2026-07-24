import pygame
import sys
import math
from ambiente.qbert_env import QbertEnv
from agentes.busca_heuristica import AgenteBuscaHeuristica
from agentes.busca_heuristica_dinamica import AgenteBuscaHeuristicaDinamica
from agentes.agente_genetico import AgenteGenetico
from agentes.agente_genetico_dinamico import AgenteGeneticoDinamico
from agentes.agente_reforco import AgenteReforco
from agentes.agente_reforco_dinamico import AgenteReforcoDinamico

pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Q*bert Agentes")
relogio = pygame.time.Clock()

fonte_texto = pygame.font.SysFont("Arial", 22)
fonte_subtitulo = pygame.font.SysFont("Arial", 18)
fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fonte_card = pygame.font.SysFont("Arial", 24, bold=True)

def desenhar_texto(texto, font, cor, x, y, centralizado=True):
    img = font.render(texto, True, cor)
    if centralizado:
        x -= img.get_width() // 2
    tela.blit(img, (x, y))

def animar_fade_texto(texto, font, cor, y, fade_in=True, velocidade=15):
    """
    Executa uma animação rápida de fade in ou fade out para um texto centralizado.
    """
    alpha_inicio = 0 if fade_in else 255
    alpha_fim = 255 if fade_in else 0
    passo = velocidade if fade_in else -velocidade

    for alpha in range(alpha_inicio, alpha_fim + (1 if fade_in else -1), passo):
        pygame.event.pump()
        tela.fill((20, 20, 30))
        
        img = font.render(texto, True, cor)
        img.set_alpha(max(0, min(255, alpha)))
        
        x = (LARGURA - img.get_width()) // 2
        tela.blit(img, (x, y))
        
        pygame.display.flip()
        pygame.time.delay(15)

def desenhar_card(texto, x, y, largura, altura, selecionado, cor_destaque=(0, 255, 150)):
    """
    Desenha um cartão moderno com bordas arredondadas e efeito de seleção.
    """
    cor_fundo = (35, 35, 55) if selecionado else (22, 22, 35)
    cor_borda = cor_destaque if selecionado else (60, 60, 80)
    espessura_borda = 3 if selecionado else 1
    
    if selecionado:
        pygame.draw.rect(tela, (0, 0, 0, 100), (x + 3, y + 3, largura, altura), border_radius=10)
        
    pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura), border_radius=10)
    pygame.draw.rect(tela, cor_borda, (x, y, largura, altura), espessura_borda, border_radius=10)
    
    cor_texto = (255, 255, 255) if selecionado else (150, 150, 170)
    desenhar_texto(texto, fonte_card, cor_texto, x + (largura // 2), y + (altura // 2) - 13)

def rodar_menu():
    """
    Exibe a tela inicial de menu e retorna as escolhas do usuário.
    """
    agente_escolhido = "1"  # Padrão: A*
    com_inimigos = False    # Padrão: Sem inimigos (Cenário Estático)
    rodando = True

    while rodando:
        tempo = pygame.time.get_ticks()
        tela.fill((15, 15, 25))
        
        # --- TÍTULO ---
        desenhar_texto("Q*BERT AGENTS", fonte_titulo, (255, 215, 0), LARGURA // 2, 40)
        desenhar_texto("Selecione o Agente (Teclas 1, 2 ou 3):", fonte_subtitulo, (180, 180, 200), LARGURA // 2, 110)
        
        # --- CARTÕES DE OPÇÕES DOS AGENTES ---
        larg_card, alt_card = 460, 55
        x_card = (LARGURA - larg_card) // 2
        
        desenhar_card("[ 1 ] Busca Heurística (A*)", x_card, 150, larg_card, alt_card, agente_escolhido == "1", (0, 255, 150))
        desenhar_card("[ 2 ] Algoritmo Genético (Evolutivo)", x_card, 215, larg_card, alt_card, agente_escolhido == "2", (0, 200, 255))
        desenhar_card("[ 3 ] Q-Learning (Reforço)", x_card, 280, larg_card, alt_card, agente_escolhido == "3", (255, 150, 0))
        
        # --- CONFIGURAÇÃO DE INIMIGOS ---
        desenhar_texto("Modo do Ambiente (Pressione 'I' para alternar):", fonte_subtitulo, (180, 180, 200), LARGURA // 2, 365)
        
        larg_ini, alt_ini = 460, 60
        x_ini = (LARGURA - larg_ini) // 2
        cor_destaque_ini = (255, 80, 80) if com_inimigos else (80, 220, 255)
        texto_ini = "COM INIMIGO (Dinâmico)" if com_inimigos else "SEM INIMIGO (Estático)"
        
        desenhar_card(texto_ini, x_ini, 400, larg_ini, alt_ini, True, cor_destaque_ini)
        
        escala_pulso = (math.sin(tempo * 0.005) + 1) * 0.5
        cor_pulso = (int(200 + 55 * escala_pulso), int(200 + 55 * escala_pulso), int(50 * escala_pulso))
        desenhar_texto("Pressione [ ENTER ] para Iniciar a Simulação", fonte_texto, cor_pulso, LARGURA // 2, 510)

        pygame.display.flip()
        
        # --- CAPTURA DE EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    agente_escolhido = "1"
                elif evento.key == pygame.K_2:
                    agente_escolhido = "2"
                elif evento.key == pygame.K_3:
                    agente_escolhido = "3"
                elif evento.key == pygame.K_i:
                    com_inimigos = not com_inimigos
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return agente_escolhido, com_inimigos

        relogio.tick(30)

def carregar_agente(escolha, env):
    """
    Instancia e, se necessário, treina o agente escolhido antes de abrir o jogo.
    """
    if escolha == "1":
        if env.com_inimigos:
            print("\nCarregando Busca Heurística Dinâmica...")
            return AgenteBuscaHeuristicaDinamica()
        
        print("\nCarregando Busca Heurística (A*)...")
        agente_a = AgenteBuscaHeuristica()
        
        # Se for no modo estático, pré-calculamos a rota toda com tela de loading
        if not env.com_inimigos:
            animar_fade_texto("Calculando Melhor Rota...", fonte_titulo, (0, 255, 0), ALTURA // 2, fade_in=True)
            
            print("Pré-calculando rota do A* em background...")
            env_sim = QbertEnv(niveis=env.niveis, com_inimigos=False)
            env_sim.reset()
            rota_calculada = []
            
            # Roda o A* em loop até zerar a pirâmide na simulação
            while True:
                acao = agente_a.obter_acao(env_sim.estado_blocos, env_sim.posicao_agente, env_sim.grafo)
                if not acao: break
                rota_calculada.append(acao)
                _, _, vitoria = env_sim.step(acao)
                if vitoria: break
            
            # Salva a rota no agente para ser lida sequencialmente na tela
            agente_a.cromossomo = rota_calculada
            print(f"Rota de {len(rota_calculada)} passos calculada com sucesso!")

            animar_fade_texto("Calculando Melhor Rota...", fonte_titulo, (0, 255, 0), ALTURA // 2, fade_in=False)
            
        return agente_a
        
    elif escolha == "2":
        if env.com_inimigos:
            print("\nEvoluindo população contra os Inimigos...")
            animar_fade_texto("Evoluindo Genética...", fonte_titulo, (0, 255, 255), ALTURA // 2, fade_in=True)
            
            env_treino = QbertEnv(niveis=env.niveis, com_inimigos=True)
            env_treino.silencioso = True 
            
            agente_gen = AgenteGeneticoDinamico(tamanho_populacao=100, taxa_mutacao=0.02, tamanho_cromossomo=65)
            melhor_individuo = agente_gen.treinar(env_treino, num_geracoes=1000)
            
            animar_fade_texto("Evoluindo Genética...", fonte_titulo, (0, 255, 255), ALTURA // 2, fade_in=False)

            return melhor_individuo
            
        else:
            print("\nEvoluindo população com Algoritmo Genético...")
            animar_fade_texto("Evoluindo Genética...", fonte_titulo, (0, 255, 255), ALTURA // 2, fade_in=True)
            
            env_treino = QbertEnv(niveis=env.niveis, com_inimigos=False)
            agente_gen = AgenteGenetico(tamanho_populacao=150, taxa_mutacao=0.05, tamanho_cromossomo=40)
            melhor_individuo = agente_gen.treinar(env_treino, num_geracoes=1000)
            
            animar_fade_texto("Evoluindo Genética...", fonte_titulo, (0, 255, 255), ALTURA // 2, fade_in=False)

            return melhor_individuo
        
    elif escolha == "3":
        if env.com_inimigos:
            print("\nCarregando agente Q-Learning Dinâmico...")
        else:
            print("\nCarregando agente Q-Learning...")

        tela.fill((20, 20, 30))
        desenhar_texto(
            "Treinando Q-Learning...",
            fonte_titulo,
            (0,255,255),
            LARGURA//2,
            ALTURA//2
        )
        pygame.display.flip()

        if env.com_inimigos:
            agente = AgenteReforcoDinamico()
            arquivo = "q_table_dinamica.pkl"
        else:
            agente = AgenteReforco()
            arquivo = "q_table.pkl"

        try:
            agente.carregar(arquivo)
            print("Tabela Q carregada.")

        except FileNotFoundError:
            print("Tabela não encontrada.")
            print("Treinando...")
            agente.treinar(
                env,
                episodios=10000
            )
            agente.salvar(arquivo)

        return agente

def desenhar_pontuacao(tela, pontuacao, sprites, x, y, espacamento=4):
    texto = f"{pontuacao:05d}"

    for digito in texto:
        img = sprites[digito]
        tela.blit(img, (x, y))
        x += img.get_width() + espacamento

def rodar_jogo(env, agente, escolha_agente, com_inimigos):
    """
    Controla o loop gráfico do Pygame, animando o agente escolhido na pirâmide.
    """
    try:
        # Carrega os sprites dos números
        sprites_numeros = {}
        for i in range(10):
            sprites_numeros[str(i)] = pygame.image.load(
                f"sprites/cenario/numero-{i}.png"
            ).convert_alpha()

        img_bloco_dir_fase1 = pygame.image.load("sprites/cenario/plataforma-direita-fase1.png").convert_alpha()
        img_bloco_esq_fase1 = pygame.image.load("sprites/cenario/plataforma-esquerda-fase1.png").convert_alpha()
        img_bloco_esq_comp = pygame.image.load("sprites/cenario/plataforma-esquerda-fase1-completa.png").convert_alpha()
        img_bloco_dir_comp = pygame.image.load("sprites/cenario/plataforma-direita-fase1-completa.png").convert_alpha()
        img_agente = pygame.image.load("sprites/qbert/qbert-frente-esquerda.png").convert_alpha()


        # Carrega os sprites do Q*bert para diferentes direções
        sprites_qbert = {
            'baixo_esq': pygame.image.load("sprites/qbert/qbert-frente-esquerda.png").convert_alpha(),
            'baixo_dir': pygame.image.load("sprites/qbert/qbert-frente-direita.png").convert_alpha(),
            'cima_esq':  pygame.image.load("sprites/qbert/qbert-costas-esquerda.png").convert_alpha(),
            'cima_dir':  pygame.image.load("sprites/qbert/qbert-costas-direita.png").convert_alpha()
        }

        img_hit = pygame.image.load("sprites/qbert/hit.png").convert_alpha()

        # Carrega os sprites da Coily (Ovo e Cobra)
        sprites_coily_ovo = [
            pygame.image.load("sprites/personagens/bola-roxa-2.png").convert_alpha(),  # Redonda
            pygame.image.load("sprites/personagens/bola-roxa-1.png").convert_alpha()   # Achatada
        ]
        sprites_coily_cobra = [
            pygame.image.load("sprites/personagens/cobra-roxa-3.png").convert_alpha(),
            pygame.image.load("sprites/personagens/cobra-roxa-2.png").convert_alpha(),
            pygame.image.load("sprites/personagens/cobra-roxa-1.png").convert_alpha(),
            pygame.image.load("sprites/personagens/cobra-roxa-2.png").convert_alpha(),
            pygame.image.load("sprites/personagens/cobra-roxa-3.png").convert_alpha()
        ]

        mult_x, mult_y = 1.4, 1
        nova_largura = int(img_bloco_dir_fase1.get_width() * mult_x)
        nova_altura = int(img_bloco_dir_fase1.get_height() * mult_y)

        img_bloco_dir_fase1 = pygame.transform.scale(img_bloco_dir_fase1, (nova_largura, nova_altura))
        img_bloco_esq_fase1 = pygame.transform.scale(img_bloco_esq_fase1, (nova_largura, nova_altura))
        img_bloco_dir_comp = pygame.transform.scale(img_bloco_dir_comp, (nova_largura, nova_altura))
        img_bloco_esq_comp = pygame.transform.scale(img_bloco_esq_comp, (nova_largura, nova_altura))
    except FileNotFoundError:
        print("Erro: Imagens não encontradas na pasta 'sprites/'. Verifique os caminhos.")
        return

    ESPACAMENTO_X, ESPACAMENTO_Y = 102, 58

    OFFSET_ESQ_X = -10
    OFFSET_DIR_X = 10
    OFFSET_Y_EXTRA = 3
    
    # Sincroniza posições e temporizador (800ms entre pulos para podermos assistir)
    posicao_atual = env.reset()
    linha_agente, coluna_agente = posicao_atual
    
    TEMPO_POR_PASSO = 1000
    ultimo_passo = pygame.time.get_ticks()
    
    # Controle da animação da cobra
    inicio_animacao_cobra = None
    coily_apareceu = False

    # Controle da animação do ovo da Coily
    ultima_posicao_coily = None
    inicio_ovo = None
    TEMPO_OVO_ALTO = 600  # tempo flutuando antes de aparecer no chão
    
    # Índice para ler a lista de comandos caso o agente seja o Genético
    passo_genetico = 0
    passos_totais = 0
    ultima_acao = 'baixo_esq'
    fim_de_jogo = None
    rodando = True

    while rodando:
        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if tempo_atual - ultimo_passo > TEMPO_POR_PASSO:
            ultimo_passo = tempo_atual
            acao = None

            # 1. Escolhe como pegar a ação, se o agente tiver uma lista pré-calculada (Genético ou A* Estático), lê da lista
            if hasattr(agente, 'cromossomo'):
                if passo_genetico < len(agente.cromossomo):
                    acao_gene = agente.cromossomo[passo_genetico]
                    passo_genetico += 1

                    if com_inimigos and escolha_agente == "2":
                        pos_atual = env.posicao_agente
                        vizinhos_validos = env.grafo.get(pos_atual, {})

                        if acao_gene not in vizinhos_validos:
                            idx_borda = abs(hash(acao_gene)) % len(vizinhos_validos)
                            acao = list(vizinhos_validos.keys())[idx_borda]
                        else:
                            acao = acao_gene

                        if hasattr(env, 'coily') and env.coily.ativa and env.posicao_coily in vizinhos_validos.values():
                            saidas_seguras = [act for act, pos in vizinhos_validos.items() if pos != env.posicao_coily]
                            if saidas_seguras:
                                idx_fuga = abs(hash(acao)) % len(saidas_seguras)
                                acao = saidas_seguras[idx_fuga]
                    else:
                        acao = acao_gene

            # A* Dinâmico (com inimigos ativos) calcula em tempo real
            else:
                if isinstance(agente, AgenteBuscaHeuristicaDinamica):
                    # Passa a posição atual da Coily para o agente conseguir desviar
                    pos_inimigo = env.posicao_coily if (env.com_inimigos and env.coily.ativa) else None
                    acao = agente.obter_acao(env.estado_blocos, env.posicao_agente, env.grafo, posicao_inimigo=pos_inimigo)
                elif isinstance(agente, AgenteReforcoDinamico):
                    acao = agente.obter_acao(
                        env.estado_blocos,
                        env.posicao_agente,
                        env.posicao_coily,
                        env.coily.estado,
                        env.grafo
                    )
                else:
                    acao = agente.obter_acao(env.estado_blocos, env.posicao_agente, env.grafo)

            # 2. Executa a ação no ambiente se ela existir
            if acao is not None:
                passos_totais += 1
                nova_posicao, recompensa, vitoria = env.step(acao)
                linha_agente, coluna_agente = nova_posicao

                if hasattr(env, 'coily') and env.coily.ativa:
                    if env.posicao_coily != ultima_posicao_coily:
                        inicio_ovo = pygame.time.get_ticks()
                        ultima_posicao_coily = env.posicao_coily

                if acao in sprites_qbert:
                    ultima_acao = acao

                print(f"Passo: {passo_genetico if escolha_agente == '2' else ''} | Ação: {acao.upper():10} | Posição: {nova_posicao} | Recompensa: {recompensa}")

                if vitoria:
                    print("\nVITÓRIA! O agente zerou a pirâmide!")
                    fim_de_jogo = "vitoria"
                    # mostrar_tela_fim(True, passos_totais)
                    # rodando = False
                elif recompensa in (-10, -100):
                    print("\nGAME OVER! O Q*bert caiu no abismo ou foi pego!")
                    fim_de_jogo = "derrota"
                    # mostrar_tela_fim(False, passos_totais)
                    # rodando = False
            else:
                print("\nO agente finalizou sua sequência de ações.")
                rodando = False

        tela.fill((10, 10, 15))
        
        x_topo = LARGURA // 2 - (ESPACAMENTO_X // 2)
        y_topo = 100
        
        # Desenha os blocos da pirâmide
        for linha in range(6):
            for coluna in range(linha + 1):
                x_base = x_topo + (coluna * ESPACAMENTO_X) - (linha * (ESPACAMENTO_X // 2))
                y_base = y_topo + (linha * ESPACAMENTO_Y)

                ja_pintado = env.estado_blocos.get((linha, coluna), 0) == 1
                
                if coluna <= linha // 2:
                    img_atual = img_bloco_esq_comp if ja_pintado else img_bloco_esq_fase1
                    x_pixel = x_base + OFFSET_ESQ_X
                else:
                    img_atual = img_bloco_dir_comp if ja_pintado else img_bloco_dir_fase1
                    x_pixel = x_base + OFFSET_DIR_X

                y_pixel = y_base + OFFSET_Y_EXTRA
                
                tela.blit(img_atual, (x_pixel, y_pixel))

        # Seleciona o sprite correto de acordo com a última direção
        img_agente_atual = sprites_qbert.get(ultima_acao, sprites_qbert['baixo_esq'])

        colisao_com_cobra = (fim_de_jogo == "derrota" and com_inimigos)

        if colisao_com_cobra:
            img_agente_atual = img_hit
        else:
            img_agente_atual = sprites_qbert.get(ultima_acao, sprites_qbert['baixo_esq'])

        # Desenha o Q*bert na posição atual
        larg_bloco = img_bloco_dir_fase1.get_width()
        x_base_bloco = x_topo + (coluna_agente * ESPACAMENTO_X) - (linha_agente * (ESPACAMENTO_X // 2))
        y_base_bloco = y_topo + (linha_agente * ESPACAMENTO_Y)

        offset_personagem_x = OFFSET_ESQ_X if coluna_agente <= linha_agente // 2 else OFFSET_DIR_X

        x_agente = x_base_bloco + (larg_bloco // 2) - (img_agente_atual.get_width() // 2) + offset_personagem_x
        y_agente = y_base_bloco - img_agente_atual.get_height() + (ESPACAMENTO_Y // 2) - 22 + OFFSET_Y_EXTRA
        
        tela.blit(img_agente_atual, (x_agente, y_agente))

        # Desenha a Cobra Coily
        if not colisao_com_cobra and com_inimigos and hasattr(env, 'coily') and env.coily.ativa and env.posicao_coily:
            linha_coily, coluna_coily = env.posicao_coily

            # Inicia o contador somente quando a cobra surgir
            if not coily_apareceu:
                inicio_animacao_cobra = pygame.time.get_ticks()
                coily_apareceu = True
            
            # 1. Escolhe o sprite com base no estado e alterna o frame usando os passos totais
            if env.coily.estado == "OVO":
                tempo_ovo = pygame.time.get_ticks() - inicio_ovo
                if tempo_ovo < TEMPO_OVO_ALTO:
                    # ovo parado flutuando acima da plataforma
                    img_coily_atual = sprites_coily_ovo[0]
                    deslocamento_ovo = -30
                else:
                    # teleporta para o chão já achatado
                    img_coily_atual = sprites_coily_ovo[1]
                    deslocamento_ovo = 0
            else:  # Estado "COBRA"
                # Tempo desde que a cobra apareceu
                tempo_cobra = pygame.time.get_ticks() - inicio_animacao_cobra
                # 1600ms dividido em 5 frames = 320ms por frame
                frame_idx = (tempo_cobra // 400) % len(sprites_coily_cobra)
                img_coily_atual = sprites_coily_cobra[frame_idx]
            
            # 2. Calcula a posição isométrica (exatamente com a mesma matemática do Q*bert)
            x_base_coily = x_topo + (coluna_coily * ESPACAMENTO_X) - (linha_coily * (ESPACAMENTO_X // 2))
            y_base_coily = y_topo + (linha_coily * ESPACAMENTO_Y)

            offset_coily_x = OFFSET_ESQ_X if coluna_coily <= linha_coily // 2 else OFFSET_DIR_X
            
            # 3. Centraliza o sprite no bloco
            x_coily = x_base_coily + (larg_bloco // 2) - (img_coily_atual.get_width() // 2) + offset_coily_x
            y_coily = (
                y_base_coily
                - img_coily_atual.get_height()
                + (ESPACAMENTO_Y // 2)
                - 22
                + deslocamento_ovo
                + OFFSET_Y_EXTRA
            )
            
            tela.blit(img_coily_atual, (x_coily, y_coily))

        # Desenha a pontuação
        desenhar_pontuacao(
            tela,
            env.pontuacao,
            sprites_numeros,
            60,
            45
        )

        pygame.display.flip()
        relogio.tick(30)

        if fim_de_jogo is not None:
            pygame.time.delay(1000)
            
            cor_flash = (0, 150, 0) if fim_de_jogo == "vitoria" else (150, 0, 0)
            for _ in range(2):
                overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
                overlay.fill((*cor_flash, 30))
                tela.blit(overlay, (0, 0))
                pygame.display.flip()
                pygame.time.delay(200)
                
                pygame.display.flip()
                pygame.time.delay(200)
            
            pygame.time.delay(400)
            mostrar_tela_fim(fim_de_jogo == "vitoria", passos_totais)
            rodando = False

def mostrar_tela_fim(vitoria, passos_totais):
    """
    Exibe um painel centralizado com o resultado e os passos antes de voltar ao menu.
    """
    esperando = True
    while esperando:
        # Fundo escuro semi-transparente cobrindo o jogo
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))
        
        # Caixa de diálogo central
        larg_caixa, alt_caixa = 520, 260
        x_caixa = (LARGURA - larg_caixa) // 2
        y_caixa = (ALTURA - alt_caixa) // 2
        
        pygame.draw.rect(tela, (25, 25, 40), (x_caixa, y_caixa, larg_caixa, alt_caixa), border_radius=12)
        pygame.draw.rect(tela, (0, 255, 255), (x_caixa, y_caixa, larg_caixa, alt_caixa), 3, border_radius=12)
        
        # Textos informativos
        titulo = "VITÓRIA!" if vitoria else "FIM DE JOGO"
        cor_titulo = (0, 255, 150) if vitoria else (255, 80, 80)
        
        desenhar_texto(titulo, fonte_titulo, cor_titulo, LARGURA // 2, y_caixa + 35)
        
        status_txt = "A pirâmide foi totalmente pintada!" if vitoria else "O agente falhou ou caiu no abismo."
        desenhar_texto(status_txt, fonte_texto, (255, 255, 255), LARGURA // 2, y_caixa + 95)
        
        desenhar_texto(f"Passos utilizados: {passos_totais}", fonte_texto, (255, 255, 0), LARGURA // 2, y_caixa + 145)
        
        desenhar_texto("Pressione [ENTER] para voltar ao Menu", fonte_texto, (200, 200, 200), LARGURA // 2, y_caixa + 205)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    esperando = False
        relogio.tick(30)

if __name__ == "__main__":
    while True:
        # 1. Abre o Menu Interativo
        escolha_agente, modo_inimigos = rodar_menu()
        print(f"\nConfiguração selecionada -> Agente: [{escolha_agente}] | Inimigos: {modo_inimigos}")
        
        # 2. Cria o ambiente
        env = QbertEnv(niveis=6, com_inimigos=modo_inimigos)
        
        # 3. Carrega (ou treina) o agente na memória
        agente_carregado = carregar_agente(escolha_agente, env)
        
        # 4. Inicia o jogo gráfico com o agente pronto
        if agente_carregado:
            rodar_jogo(env, agente_carregado, escolha_agente, modo_inimigos)
            