import pygame
import sys
import math

# Configurações da tela
WIDTH, HEIGHT = 300, 300  # Dimensões da tela do jogo
LINE_WIDTH = 15           # Largura das linhas do tabuleiro
BOARD_ROWS, BOARD_COLS = 3, 3  # Número de linhas e colunas do tabuleiro
SQUARE_SIZE = WIDTH // BOARD_COLS  # Tamanho de cada quadrado no tabuleiro
CIRCLE_RADIUS = SQUARE_SIZE // 3  # Raio dos círculos (O)
CIRCLE_WIDTH = 15  # Largura da borda dos círculos (O)
CROSS_WIDTH = 25   # Largura das linhas dos Xs
SPACE = 30         # Espaço entre as linhas dos Xs
WHITE = (255, 255, 255)  # Cor branca
BLACK = (0, 0, 0)       # Cor preta
GREEN = (0, 255, 0)     # Cor verde para as linhas do tabuleiro
LINE_COLOR = GREEN
CIRCLE_COLOR = WHITE
CROSS_COLOR = WHITE

# Inicializa o Pygame e configura a tela
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Cria a tela com as dimensões definidas
pygame.display.set_caption('Jogo da Velha')  # Define o título da janela
# Define as fontes para o texto exibido na tela
font_title = pygame.font.Font(None, 60)  # Fonte para o título
font_menu = pygame.font.Font(None, 40)   # Fonte para opções do menu
font_signature = pygame.font.Font(None, 20)  # Fonte para a assinatura
font_result = pygame.font.Font(None, 40)  # Fonte para resultados
clock = pygame.time.Clock()  # Controle da taxa de atualização do jogo

def draw_lines():
    """
    Desenha as linhas do tabuleiro de jogo.
    """
    # Desenha as linhas horizontais
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Desenha as linhas verticais
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_board(board):
    """
    Desenha o estado atual do tabuleiro com base na lista 'board'.
    """
    screen.fill(BLACK)  # Preenche o fundo da tela com a cor preta
    draw_lines()        # Desenha as linhas do tabuleiro
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Se o valor é 1, desenha um círculo
                pygame.draw.circle(
                    screen, CIRCLE_COLOR, 
                    (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )
            elif board[row][col] == 2:  # Se o valor é 2, desenha um X
                pygame.draw.line(
                    screen, CROSS_COLOR, 
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), 
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen, CROSS_COLOR, 
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                    CROSS_WIDTH
                )
    pygame.display.update()  # Atualiza a tela para mostrar as mudanças

def check_winner(board):
    """
    Verifica se há um vencedor no tabuleiro.
    """
    # Checa linhas
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            return board[row][0]

    # Checa colunas
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return board[0][col]

    # Checa diagonais
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]

    return 0  # Retorna 0 se não houver vencedor

def check_draw(board):
    """
    Verifica se o tabuleiro está cheio e não há vencedores (empate).
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:  # Se ainda há espaços vazios
                return False
    return True  # Retorna True se o tabuleiro estiver cheio

def minimax(board, depth, alpha, beta, is_maximizing):
    """
    Implementa o algoritmo Minimax com poda alfa-beta para encontrar a melhor jogada.
    """
    scores = {1: -1, 2: 1, 'draw': 0}  # Pontuações para cada resultado
    winner = check_winner(board)

    if winner != 0:
        return scores[winner]  # Retorna a pontuação do vencedor
    if check_draw(board):
        return scores['draw']  # Retorna a pontuação de empate

    if is_maximizing:
        best_score = -math.inf  # Inicializa o melhor score para maximização
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2  # Simula a jogada da IA
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = 0  # Reverte a jogada
                    best_score = max(score, best_score)  # Atualiza o melhor score
                    alpha = max(alpha, score)  # Atualiza o alfa
                    if beta <= alpha:
                        break  # Poda a árvore de busca
        return best_score
    else:
        best_score = math.inf  # Inicializa o melhor score para minimização
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1  # Simula a jogada do jogador
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = 0  # Reverte a jogada
                    best_score = min(score, best_score)  # Atualiza o melhor score
                    beta = min(beta, score)  # Atualiza o beta
                    if beta <= alpha:
                        break  # Poda a árvore de busca
        return best_score

def best_move(board):
    """
    Determina a melhor jogada para a IA usando o algoritmo Minimax.
    """
    best_score = -math.inf  # Inicializa o melhor score
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2  # Simula a jogada da IA
                score = minimax(board, 0, -math.inf, math.inf, False)
                board[row][col] = 0  # Reverte a jogada
                if score > best_score:
                    best_score = score  # Atualiza o melhor score
                    move = (row, col)  # Atualiza a melhor jogada
    return move

def show_result(message):
    """
    Exibe uma mensagem de resultado na tela.
    """
    screen.fill(BLACK)  # Preenche o fundo com a cor preta
    result_text = font_result.render(message, True, WHITE)  # Renderiza o texto da mensagem
    text_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centraliza o texto
    screen.blit(result_text, text_rect)  # Desenha o texto na tela
    pygame.display.update()  # Atualiza a tela para mostrar a mensagem
    pygame.time.wait(4000)  # Aguarda 4 segundos antes de retornar ao menu

def main_menu():
    """
    Exibe o menu principal do jogo e retorna a escolha do jogador.
    """
    screen.fill(BLACK)  # Preenche o fundo com a cor preta
    title = font_title.render("Jogo da Velha", True, WHITE)  # Renderiza o título
    two_player = font_menu.render("Jogar em Dupla", True, WHITE)  # Renderiza a opção "Jogar em Dupla"
    vs_ai = font_menu.render("Jogar Contra IA", True, WHITE)  # Renderiza a opção "Jogar Contra IA"
    signature = font_signature.render("by Thais R", True, WHITE)  # Renderiza a assinatura
    
    # Posiciona o título e opções no centro da tela
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    two_player_rect = two_player.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    vs_ai_rect = vs_ai.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    signature_rect = signature.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))  # Assinatura no canto inferior direito
    
    screen.blit(title, title_rect)  # Desenha o título
    screen.blit(two_player, two_player_rect)  # Desenha a opção "Jogar em Dupla"
    screen.blit(vs_ai, vs_ai_rect)  # Desenha a opção "Jogar Contra IA"
    screen.blit(signature, signature_rect)  # Desenha a assinatura
    pygame.display.update()  # Atualiza a tela para mostrar o menu

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if two_player_rect.collidepoint(pos):
                    return 1  # Retorna 1 para o modo "Jogar em Dupla"
                if vs_ai_rect.collidepoint(pos):
                    return 2  # Retorna 2 para o modo "Jogar Contra IA"

def game_loop(mode):
    """
    Executa o loop principal do jogo.
    """
    board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]  # Cria um tabuleiro vazio
    draw_board(board)  # Desenha o tabuleiro inicial
    current_player = 1  # Começa com o jogador 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE  # Converte a posição do mouse em índices de linha e coluna

                if board[row][col] == 0:  # Se a célula estiver vazia
                    board[row][col] = current_player  # Marca a célula com o jogador atual
                    draw_board(board)  # Atualiza o tabuleiro

                    winner = check_winner(board)  # Verifica se há um vencedor
                    if winner:
                        if mode == 1:  # Dois jogadores
                            show_result(f"Vencedor: Jogador {winner}")
                        else:  # Jogar contra IA
                            show_result("Vencedor: IA")
                        return
                    if check_draw(board):  # Verifica se o jogo terminou em empate
                        show_result("Empate!")
                        return

                    current_player = 2 if current_player == 1 else 1  # Alterna o jogador

        if mode == 2 and current_player == 2:  # Se for o turno da IA
            row, col = best_move(board)  # Encontra a melhor jogada para a IA
            if row is not None and col is not None:
                board[row][col] = current_player  # Marca a célula com a jogada da IA
                draw_board(board)  # Atualiza o tabuleiro

                if check_winner(board):  # Verifica se há um vencedor
                    show_result("Vencedor: IA")
                    return
                if check_draw(board):  # Verifica se o jogo terminou em empate
                    show_result("Empate!")
                    return

                current_player = 1  # Alterna para o jogador 1

def main():
    """
    Função principal que inicia o jogo.
    """
    while True:
        mode = main_menu()  # Exibe o menu principal e obtém o modo de jogo
        game_loop(mode)  # Executa o loop do jogo com base no modo selecionado

if __name__ == "__main__":
    main()  # Inicia o jogo se o script for executado diretamente
