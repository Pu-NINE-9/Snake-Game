import pygame
from menu import Menu

def main():
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    menu = Menu(screen_width, screen_height)
    menu.run()

if __name__ == '__main__':
    main()