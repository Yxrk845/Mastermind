import pygame
import random
import sys

# Configuraciones
WHITE = (200, 200, 200)
BLACK = (30, 30, 30)
DARKGREY = (40, 40, 40)
LIGHTGREY = (120, 80, 80)
DARKBROWN = (55, 22, 30)
GREEN = (0, 210, 0)
RED = (210, 0, 0)
YELLOW = (210, 210, 0)
PINK = (210, 0, 210)
ORANGE = (210, 110, 0)
BGCOLOUR = (122, 70, 51)
BLUE = (11, 188, 235)
COLOURS = (RED, GREEN, BLUE, YELLOW)

# Otras configuraciones
ROWS = 5
COLS = 12
TILESIZE = 60
AMOUNT_COLOUR = 4  # Cantidad de colores

WIDTH = (ROWS * TILESIZE) + 1
HEIGHT = (COLS * TILESIZE) + 1
FPS = 60
TITLE = "Mastermind"

# Inicialización de Pygame
pygame.init()
pygame.font.init()

# Clases de los pins
class Pin:
    def __init__(self, x, y, colour=None, revealed=True):
        self.x, self.y = x, y
        self.colour = colour
        self.revealed = revealed

    def draw(self, screen):
        center = (self.x + (TILESIZE / 2), self.y + (TILESIZE / 2))
        if self.colour is not None and self.revealed:
            pygame.draw.circle(screen, tuple(x * 0.3 for x in self.colour), tuple(x + 1 for x in center), 15)
            pygame.draw.circle(screen, self.colour, center, 15)
        elif not self.revealed:
            pygame.draw.circle(screen, LIGHTGREY, center, 15)
            pygame.draw.circle(screen, BLACK, center, 15, 3)
        else:
            pygame.draw.circle(screen, DARKBROWN, center, 10)

class CluePin(Pin):
    def draw(self, screen):
        center = (self.x + (TILESIZE / 2.5), self.y + (TILESIZE / 2.5))
        if self.colour is not None:
            pygame.draw.circle(screen, self.colour, center, 6)
        else:
            pygame.draw.circle(screen, DARKBROWN, center, 5)

# Clase del tablero
class Board:
    def __init__(self):
        self.tries = 10
        self.pins_surface = pygame.Surface((4 * TILESIZE, 11 * TILESIZE))
        self.pins_surface.fill(BGCOLOUR)

        self.clue_surface = pygame.Surface((TILESIZE, 11 * TILESIZE))
        self.clue_surface.fill(BGCOLOUR)

        self.colour_selection_surface = pygame.Surface((4 * TILESIZE, 2 * TILESIZE))
        self.colour_selection_surface.fill(LIGHTGREY)

        self.colour_selection = []
        self.board_pins = []
        self.board_clues = []

        self.create_selection_pins()
        self.create_pins()
        self.create_clues()
        self.create_code()

    def create_clues(self):
        for i in range(1, 11):
            temp_row = []
            for row in range(2):
                for col in range(2):
                    temp_row.append(CluePin(col * (TILESIZE // 4), (row * (TILESIZE // 4)) + i * TILESIZE))
            self.board_clues.append(temp_row)

    def create_pins(self):
        for row in range(11):
            temp_row = []
            for col in range(4):
                temp_row.append(Pin(col * TILESIZE, row * TILESIZE))
            self.board_pins.append(temp_row)

    def create_selection_pins(self):
        colour_index = 0
        for y in range(2):
            for x in range(4):
                if colour_index < AMOUNT_COLOUR:
                    self.colour_selection.append(Pin(x * TILESIZE, y * TILESIZE, COLOURS[colour_index]))
                    colour_index += 1
                else:
                    break

    def draw(self, screen):
        # Dibujar la selección de colores
        for pin in self.colour_selection:
            pin.draw(self.colour_selection_surface)

        # Dibujar los pines
        for row in self.board_pins:
            for pin in row:
                pin.draw(self.pins_surface)

        # Dibujar las pistas
        for row in self.board_clues:
            for pin in row:
                pin.draw(self.clue_surface)

        screen.blit(self.pins_surface, (0, 0))
        screen.blit(self.clue_surface, (4 * TILESIZE, 0))
        screen.blit(self.colour_selection_surface, (0, 11 * TILESIZE))

        # Dibujar el indicador de fila
        pygame.draw.rect(screen, GREEN, (0, TILESIZE * self.tries, 4 * TILESIZE, TILESIZE), 2)

        # Dibujar el botón en la parte inferior derecha
        self.button_rect = pygame.Rect(WIDTH - TILESIZE, HEIGHT - TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, GREEN, self.button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render('IA', True, WHITE)
        text_rect = text.get_rect(center=self.button_rect.center)
        screen.blit(text, text_rect)

        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                pygame.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
                pygame.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

    def select_colour(self, mx, my, previous_colour):
        for pin in self.colour_selection:
            if pin.x < mx < pin.x + TILESIZE and pin.y < my - 11 * TILESIZE < pin.y + TILESIZE:
                return pin.colour

        return previous_colour

    def place_pin(self, mx, my, colour):
        for pin in self.board_pins[self.tries]:
            if pin.x < mx < pin.x + TILESIZE and pin.y < my < pin.y + TILESIZE:
                pin.colour = colour
                break

    def check_row(self):
        return all(pin.colour is not None for pin in self.board_pins[self.tries])

    def check_clues(self):
        colour_list = []
        for i, code_pin in enumerate(self.board_pins[0]):
            colour = None
            for j, user_pin in enumerate(self.board_pins[self.tries]):
                if user_pin.colour == code_pin.colour:
                    colour = WHITE
                    if i == j:
                        colour = RED
                        break
            if colour is not None:
                colour_list.append(colour)

        colour_list.sort()
        return colour_list

    def set_clues(self, colour_list):
        for colour, pin in zip(colour_list, self.board_clues[self.tries - 1]):
            pin.colour = colour

    def create_code(self):
        # Generar código aleatorio
        random_code = random.sample(COLOURS, 4)
        for i, pin in enumerate(self.board_pins[0]):
            pin.colour = random_code[i]
            pin.revealed = False
        print(random_code)

    def next_round(self):
        self.tries -= 1
        return self.tries > 0

    def reveal_code(self):
        for pin in self.board_pins[0]:
            pin.revealed = True

    def set_new_combination(self):
        if self.tries == 10:
            self.generate_random_combination()
        else:
            self.make_move_based_on_previous_attempts()

    def make_move_based_on_previous_attempts(self):
        previous_row = self.board_pins[self.tries + 1]
        previous_clues = self.board_clues[self.tries]

        new_combination = [None] * 4
        possible_colours = []

        # Usar colores de jugadas anteriores si hay aciertos
        for i in range(4):
            if previous_clues[i // 2 * 2 + i % 2].colour == RED:
                new_combination[i] = previous_row[i].colour

        # Determinar colores posibles para las posiciones restantes
        for pin in previous_row:
            if pin.colour not in new_combination:
                possible_colours.append(pin.colour)

        # Asignar colores posibles a las posiciones restantes
        for i in range(4):
            if new_combination[i] is None:
                new_combination[i] = possible_colours.pop()

        # Asignar una combinación aleatoria si no se pudo determinar una basada en las jugadas anteriores
        for pin, color in zip(self.board_pins[self.tries], new_combination):
            pin.colour = color if color else random.choice(COLOURS)

    def generate_random_combination(self):
        # Generar código aleatorio
        random_code = random.sample(COLOURS, 4)
        for i, pin in enumerate(self.board_pins[self.tries]):
            pin.colour = random_code[i]

# Clase del juegoclass Game:
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.end_time = None  # Almacena el tiempo en el que se mostró el mensaje de finalización
        self.showing_end_screen = False  # Bandera para indicar si se está mostrando la pantalla de finalización

        # Variables para la IA
        self.playing_ai = False

    def new(self):
        self.board = Board()
        self.colour = None

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            if self.showing_end_screen:
                # Verificar si han pasado al menos 4 segundos desde que se mostró el mensaje de finalización
                if pygame.time.get_ticks() - self.end_time >= 2000:
                    self.showing_end_screen = False
                    pygame.quit()  # Cerrar la ventana del juego
                    sys.exit()  # Salir del script


    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                self.colour = self.board.select_colour(mx, my, self.colour)
                if self.colour is not None:
                    self.board.place_pin(mx, my, self.colour)
                # Detectar clic en el botón
                if self.board.button_rect.collidepoint(mx, my):
                    self.board.set_new_combination()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.board.check_row():
                        clues_colour_list = self.board.check_clues()
                        self.board.set_clues(clues_colour_list)
                        if self.check_win(clues_colour_list):
                            self.show_message("¡Ganaste!")
                            self.end_time = pygame.time.get_ticks()
                            self.showing_end_screen = True
                        elif not self.board.next_round():
                            self.show_message("¡Juego terminado!")
                            self.end_time = pygame.time.get_ticks()
                            self.showing_end_screen = True
                elif event.key == pygame.K_SPACE:
                    self.board.set_new_combination()
                # Activar/desactivar la IA al presionar el botón
                elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.playing_ai = not self.playing_ai
                    if self.playing_ai:
                        self.run_ai()

    def check_win(self, colour_list):
        return len(colour_list) == 4 and all(colour == RED for colour in colour_list)

    def run_ai(self):
        while self.playing_ai and self.board.tries > 0:
            pygame.time.delay(500)  # Agrega un pequeño retraso para que sea visible
            self.board.set_new_combination()

    def show_message(self, message):
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Pausa para mostrar el mensaje durante 2 segundos


game = Game()
while True:
    game.new()
    game.run()
