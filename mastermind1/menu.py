import pygame
import sys
import os
from multiprocessing import Process
from tkinter import Tk, Text, Scrollbar, VERTICAL, END

# Constantes de colores mejorados
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HOVER_YELLOW = (255, 255, 153)
HOVER_GREEN = (153, 255, 153)
HOVER_RED = (255, 153, 153)
BUTTON_WIDTH = 0.3
BUTTON_HEIGHT = 0.1
BORDER_RADIUS = 15

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Menú de Mastermind")
        self.clock = pygame.time.Clock()
        self.selected_option = None
        self.background_image = self.load_background_image(os.path.join("img.mastermind", "fondo1.jpg"))
        

    def load_background_image(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        return image


    def run(self):
        running = True
        while running:
            self.screen.blit(pygame.transform.scale(self.background_image, self.screen.get_size()), (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.option_4_rect.collidepoint(mouse_pos):
                        self.selected_option = 4
                        running = False
                    elif self.quit_rect.collidepoint(mouse_pos):
                        running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((max(800, event.w), max(600, event.h)), pygame.RESIZABLE)
                    self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())

            self.draw_buttons(mouse_pos)
            pygame.display.flip()
            self.clock.tick(30)

    def draw_buttons(self, mouse_pos):
        font = pygame.font.Font(None, int(self.screen.get_height() * 0.04))

        button_width = int(self.screen.get_width() * BUTTON_WIDTH)
        button_height = int(self.screen.get_height() * BUTTON_HEIGHT)

        self.option_4_rect = pygame.Rect(self.screen.get_width() * 0.35, self.screen.get_height() * 0.4, button_width, button_height)
        self.quit_rect = pygame.Rect(self.screen.get_width() * 0.35, self.screen.get_height() * 0.55, button_width, button_height)

        self.draw_button(self.option_4_rect, "Jugar", mouse_pos, font, GREEN, HOVER_GREEN)
        self.draw_button(self.quit_rect, "Salir", mouse_pos, font, RED, HOVER_RED)

    def draw_button(self, rect, text, mouse_pos, font, color, hover_color):
        if rect.collidepoint(mouse_pos):
            current_color = hover_color
        else:
            current_color = color

        pygame.draw.rect(self.screen, current_color, rect, border_radius=BORDER_RADIUS)

        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

def run_game(file):
    p = Process(target=os.system, args=(f"python {file}",))
    p.start()
    p.join()

if __name__ == "__main__":
    menu = Menu()
    while True:
        menu.run()

        if menu.selected_option == 4:
            p = Process(target=run_game, args=("mastermind.niveles/main.py",))
            p.start()
            p.join()
            menu.selected_option = None
        elif menu.selected_option is None:
            break
