import pygame
import sys

def main():
    pygame.init()

    size = (1024, 768)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("What comes in, goes out!")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    main()