import pygame
import random

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, int(height * 0.6))


    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return True
        return False

class Snake:
    def __init__(self, x, y, color, speed=10):
        self.body = [(x, y)]
        self.direction = (1, 0)
        self.color = color
        self.speed = speed

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0] * 20, segment[1] * 20, 20, 20))

class Food:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = self.randomize_position()
        self.color = (255, 0, 0)

    def randomize_position(self):
        return (random.randint(0, (self.screen_width - 20) // 20),
                random.randint(0, (self.screen_height - 20) // 20))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0] * 20, self.position[1] * 20, 20, 20))

class PowerUp:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = self.randomize_position()
        self.color = (255, 255, 0)

    def randomize_position(self):
        return (random.randint(0, (self.screen_width - 20) // 20),
                random.randint(0, (self.screen_height - 20) // 20))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0] * 20, self.position[1] * 20, 20, 20))

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Human vs. AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, int(self.screen_height * 0.06))
        self.paused = False
        self.game_over_state = False

        # Movement timers
        self.player_move_timer = 0
        self.ai_move_timer = 0

        # Buttons
        self.pause_button = Button(self.screen_width - 120, 10, 100, 40, "Pause", (100, 100, 100), (150, 150, 150))
        self.continue_button = Button(self.screen_width // 2 - 150, self.screen_height // 2, 100, 50, "Continue", (0, 150, 0), (0, 200, 0))
        self.quit_button = Button(self.screen_width // 2 + 50, self.screen_height // 2, 100, 50, "Quit", (150, 0, 0), (200, 0, 0))
        self.restart_button = Button(self.screen_width // 2 - 150, self.screen_height // 2 + 60, 100, 50, "Restart", (0, 150, 0), (0, 200, 0))
        self.home_button = Button(self.screen_width // 2 + 50, self.screen_height // 2 + 60, 100, 50, "Home", (150, 0, 0), (200, 0, 0))
        
        self.reset_game()

    def reset_game(self):
        self.player_snake = Snake(10, 15, (0, 255, 0), speed=5)
        self.ai_snake = Snake(30, 15, (0, 0, 255), speed=3)
        self.food = Food(self.screen_width, self.screen_height)
        self.powerup = None
        self.powerup_timer = 0
        self.player_score = 100
        self.ai_score = 100
        self.paused = False
        self.game_over_state = False


    def draw_scores(self):
        player_text = self.font.render(f"Player: {self.player_score}", True, (255, 255, 255))
        ai_text = self.font.render(f"AI: {self.ai_score}", True, (255, 255, 255))
        self.screen.blit(player_text, (10, 10))
        self.screen.blit(ai_text, (self.screen_width - ai_text.get_width() - 10, 10))

    def draw_legend(self):
        legend_font = pygame.font.Font(None, int(self.screen_height * 0.035))
        player_text = legend_font.render("■ Player (Green)", True, (0, 255, 0))
        ai_text = legend_font.render("■ AI (Blue)", True, (0, 0, 255))
        food_text = legend_font.render("■ Food (Red)", True, (255, 0, 0))
        self.screen.blit(player_text, (10, self.screen_height - 80))
        self.screen.blit(ai_text, (10, self.screen_height - 55))
        self.screen.blit(food_text, (10, self.screen_height - 30))

    def game_over_screen(self, winner):
        self.game_over_state = True
        while self.game_over_state:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit_game"
                if self.restart_button.is_clicked(event):
                    return "restart"
                if self.home_button.is_clicked(event):
                    return "home"

            self.screen.fill((0, 0, 0))
            text = self.font.render(f"{winner} Wins!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
            self.screen.blit(text, text_rect)

            self.restart_button.check_hover(mouse_pos)
            self.home_button.check_hover(mouse_pos)
            self.restart_button.draw(self.screen)
            self.home_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(15)

    def check_collisions(self):
        # Player snake collisions
        if (self.player_snake.body[0][0] < 0 or self.player_snake.body[0][0] * 20 >= self.screen_width or
                self.player_snake.body[0][1] < 0 or self.player_snake.body[0][1] * 20 >= self.screen_height):
            return "AI"
        if self.player_snake.body[0] in self.ai_snake.body:
            return "AI"
        if self.player_snake.body[0] in self.player_snake.body[1:]:
            return "AI"

        # AI snake collisions
        if (self.ai_snake.body[0][0] < 0 or self.ai_snake.body[0][0] * 20 >= self.screen_width or
                self.ai_snake.body[0][1] < 0 or self.ai_snake.body[0][1] * 20 >= self.screen_height):
            return "Player"
        if self.ai_snake.body[0] in self.player_snake.body:
            return "Player"
        if self.ai_snake.body[0] in self.ai_snake.body[1:]:
            return "Player"
        return None

    def run(self):
        running = True
        while running:
            delta_time = self.clock.tick(60) / 1000.0
            self.player_move_timer += delta_time
            self.ai_move_timer += delta_time

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.pause_button.is_clicked(event):
                    self.paused = not self.paused

                if self.paused:
                    if self.continue_button.is_clicked(event):
                        self.paused = False
                    if self.quit_button.is_clicked(event):
                        running = False
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.player_snake.direction != (0, 1):
                            self.player_snake.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.player_snake.direction != (0, -1):
                            self.player_snake.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.player_snake.direction != (1, 0):
                            self.player_snake.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.player_snake.direction != (-1, 0):
                            self.player_snake.direction = (1, 0)

            if self.paused:
                self.continue_button.check_hover(mouse_pos)
                self.quit_button.check_hover(mouse_pos)
                
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                self.screen.blit(overlay, (0, 0))

                self.continue_button.draw(self.screen)
                self.quit_button.draw(self.screen)
                pygame.display.flip()
                continue

            player_move_interval = 1.0 / self.player_snake.speed
            if self.player_move_timer >= player_move_interval:
                self.player_snake.move()
                self.player_move_timer -= player_move_interval

            ai_move_interval = 1.0 / self.ai_snake.speed
            if self.ai_move_timer >= ai_move_interval:
                if self.ai_snake.body[0][0] < self.food.position[0]:
                    self.ai_snake.direction = (1, 0)
                elif self.ai_snake.body[0][0] > self.food.position[0]:
                    self.ai_snake.direction = (-1, 0)
                elif self.ai_snake.body[0][1] < self.food.position[1]:
                    self.ai_snake.direction = (0, 1)
                elif self.ai_snake.body[0][1] > self.food.position[1]:
                    self.ai_snake.direction = (0, -1)
                self.ai_snake.move()
                self.ai_move_timer -= ai_move_interval

            winner = self.check_collisions()
            if winner:
                action = self.game_over_screen(winner)
                if action == "restart":
                    self.reset_game()
                    continue
                else:
                    running = False
                    continue

            if self.player_snake.body[0] == self.food.position:
                self.player_snake.grow()
                self.food.position = self.food.randomize_position()
                self.player_score += 10
                self.ai_score -= 10

            if self.ai_snake.body[0] == self.food.position:
                self.ai_snake.grow()
                self.food.position = self.food.randomize_position()
                self.ai_score += 10
                self.player_score -= 10

            if self.powerup is None and random.randint(0, 500) == 0:
                self.powerup = PowerUp(self.screen_width, self.screen_height)

            if self.powerup:
                if self.player_snake.body[0] == self.powerup.position:
                    self.player_snake.speed += 2
                    self.powerup = None
                    self.powerup_timer = pygame.time.get_ticks()
                elif self.ai_snake.body[0] == self.powerup.position:
                    self.ai_snake.speed += 2
                    self.powerup = None
                    self.powerup_timer = pygame.time.get_ticks()

            if self.powerup_timer and pygame.time.get_ticks() - self.powerup_timer > 5000:
                self.player_snake.speed = 5
                self.ai_snake.speed = 3
                self.powerup_timer = 0

            if self.player_score <= 0:
                action = self.game_over_screen("AI")
                if action == "restart":
                    self.reset_game()
                    continue
                else:
                    running = False
            elif self.ai_score <= 0:
                action = self.game_over_screen("Player")
                if action == "restart":
                    self.reset_game()
                    continue
                else:
                    running = False

            self.screen.fill((0, 0, 0))
            self.player_snake.draw(self.screen)
            self.ai_snake.draw(self.screen)
            self.food.draw(self.screen)
            if self.powerup:
                self.powerup.draw(self.screen)
            self.draw_scores()
            self.draw_legend()
            
            self.pause_button.check_hover(mouse_pos)
            self.pause_button.draw(self.screen)

            pygame.display.flip()