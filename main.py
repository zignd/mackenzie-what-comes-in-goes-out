import os, sys, pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(name):
    path = os.path.join(main_dir, 'assets', name)
    print(path)
    return pygame.image.load(path).convert()

def main():
    pygame.init()

    size = (1024, 768)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("What comes in, goes out!")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        start_scene(screen)
        pygame.display.update()

def start_scene(screen):
    background = load_image('background.png')
    screen.blit(background, (0, 0))

if __name__ == "__main__":
    main()
