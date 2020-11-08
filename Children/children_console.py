import pygame


def main():
    win = pygame.display.set_mode((1024, 768))
    font = pygame.font.Font(None, 52)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(350, 500, 400, 50)
    input_enter = pygame.Rect(450, 600, 140, 50)
    game_name = pygame.Rect(200, 100, 600, 300)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    child_name = ''
    run = True
    image = pygame.image.load(r'C:\Users\Tecnica2\Desktop\work\Decision-Tree-Game\Children\images\person_icon.png') 
    image = pygame.transform.scale(image, (50, 50))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                if input_enter.collidepoint(event.pos):
                    print("Enter Press")
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(child_name)
                        child_name = ''
                    elif event.key == pygame.K_BACKSPACE:
                        child_name = child_name[:-1]
                    else:
                        child_name += event.unicode

        win.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(child_name, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        win.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(win, color, input_box, 2)
        pygame.draw.rect(win, (123,0,0), input_enter)
        
        pygame.draw.rect(win, (255,255,255), game_name)
        txt_game_name = font.render("Nombre to guapo", True, (0,0,0))
        win.blit(txt_game_name, (350, 220))

        txt_game_name = font.render("Enter", True, (0xFF,0xFF,0xFF))
        win.blit(txt_game_name, (460,610))
        
        win.blit(image,(280,500))
        # txt_game_name = font.render("Enter", True, (0xFF,0xFF,0xFF))
        # win.blit(txt_game_name, (350, 220))
        
        i = 0
        while i < 1024:
            # pygame.draw.line(win, (133, 128, 123), (i, 0),(i,1024), 1)
            # pygame.draw.line(win, (133, 128, 123), (0, i),(1024,i), 1)
            i+=100

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
