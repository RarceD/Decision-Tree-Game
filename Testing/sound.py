import pygame

win = pygame.display.set_mode((1024, 768))
pygame.init()
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("press")
            pygame.mixer.music.load('two.wav')
            pygame.mixer.music.play(0)
    pygame.display.flip()
    clock.tick(30)