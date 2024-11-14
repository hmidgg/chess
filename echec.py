import pygame
import chess
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load images
def load_images():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
    images = {}
    for piece in pieces:
        file_name = "{}.png".format(piece)
        file_path = os.path.join("C:\\ahmed\\travail\\jeu echec", file_name)
        if os.path.exists(file_path):
            images[piece] = pygame.transform.scale(pygame.image.load(file_path), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Initialize window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

# Board class to handle the board state
class Board:
    def __init__(self):
        self.board = chess.Board()
        self.selected_square = None
        self.valid_moves = []
        self.images = load_images()
        self.game_over = False
        self.result = ""

    def draw(self, win):
        self.draw_board(win)
        self.draw_pieces(win)
        
        if self.board.is_check():
            self.draw_check_message(win)

    def draw_board(self, win):
        colors = [WHITE, BLACK]
        for row in range(ROWS):
            for col in range(COLS):
                color = colors[(row + col) % 2]
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if self.selected_square and (row, col) in self.valid_moves:
                    pygame.draw.rect(win, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    def draw_pieces(self, win):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                row, col = divmod(square, 8)
                piece_symbol = piece.symbol()
                piece_color = 'w' if piece.color == chess.WHITE else 'b'
                piece_type = piece_symbol.upper()
                image = self.images[f'{piece_color}{piece_type}']
                
                # Check if the piece is a king and in check
                if self.board.is_check() and piece_type == 'K' and piece.color == self.board.turn:
                    image.fill(RED, special_flags=pygame.BLEND_ADD)  # Highlight king in red
                
                win.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def draw_check_message(self, win):
        font = pygame.font.Font(None, 74)
        text = font.render("Check!", True, (255, 0, 0))  # Red color
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    def select_square(self, row, col):
        if self.game_over:
            return
        
        square = chess.square(col, row)
        if self.board.piece_at(square) and self.board.piece_at(square).color == self.board.turn:
            self.selected_square = square
            self.valid_moves = [divmod(move.to_square, 8) for move in self.board.legal_moves if move.from_square == square]
        elif self.selected_square:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.check_game_over()
            self.selected_square = None
            self.valid_moves = []

    def check_game_over(self):
        if self.board.is_checkmate():
            self.game_over = True
            self.result = "Blanc gagne" if self.board.turn == chess.BLACK else "Noir gagne"
        elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition() or self.board.is_variant_draw():
            self.game_over = True
            self.result = "Match nul"

# Main loop
def main():
    clock = pygame.time.Clock()
    board = Board()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                board.select_square(row, col)

        WIN.fill(BLACK)  # Fill the window with black color
        pygame.draw.rect(WIN, WHITE, (WIDTH - SQUARE_SIZE, 0, SQUARE_SIZE, HEIGHT))  # Draw a white rectangle on the right side
        pygame.draw.rect(WIN, WHITE, (0, 0, SQUARE_SIZE, HEIGHT))  # Draw a white rectangle on the left side
        board.draw(WIN)
        pygame.display.flip()

        if board.game_over:
            print(board.result)
            pygame.time.wait(3000)  # Wait for 3 seconds before quitting
            run = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


