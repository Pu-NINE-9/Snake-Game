import pygame
from game import Game

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, int(self.screen_height * 0.08))
        self.options = ["Human vs. AI", "Network Battle", "Quit"]
        self.selected_option = 0

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + i * int(self.screen_height * 0.1)))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.options):
                        text = self.font.render(option, True, (0,0,0))
                        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + i * int(self.screen_height * 0.1)))
                        if text_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                            if self.selected_option == 0:
                                game = Game(self.screen_width, self.screen_height)
                                game.run()
                            elif self.selected_option == 1:
                                self.show_coming_soon()
                            elif self.selected_option == 2:
                                running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            game = Game(self.screen_width, self.screen_height)
                            game.run()
                        elif self.selected_option == 1:
                            self.show_coming_soon()
                        elif self.selected_option == 2:
                            running = False
            self.draw_menu()
        pygame.quit()

    def show_coming_soon(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Coming Soon...", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)