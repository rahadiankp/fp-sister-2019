import pygame

class StartScene:
    def __init__(self):
        self.screen = None
        self.SCREEN_RESOLUTION = (640, 640)
        self.resource = {}
        self.username = ''
        self.username_rect = pygame.rect.Rect(150, 250, 350, 80)
        self.start_rect = pygame.rect.Rect(40, 480, 260, 60)
        self.quit_rect = pygame.rect.Rect(40, 550, 260, 60)
        self.boxcolor = pygame.Color('black')
        self.loadresource()

    def loadresource(self):
        self.resource.update({'background': (pygame.image.load("assets/background.png"), (0, 0))})

    def drawscreen(self):
        for item in self.resource:
            self.screen.blit(self.resource[item][0], self.resource[item][1])

        pygame.draw.rect(self.screen, self.boxcolor, self.username_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.start_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.quit_rect, 8)

        username_surface = pygame.font.Font(None, 64).render(self.username, True, pygame.Color('black'))
        start_surface = pygame.font.Font(None, 64).render('START', True, pygame.Color('white'))
        quit_surface = pygame.font.Font(None, 64).render('QUIT', True, pygame.Color('white'))

        username_fill = pygame.Surface((350, 80))
        start_fill = pygame.Surface((260, 60))
        quit_fill = pygame.Surface((260, 60))

        username_fill.fill((255, 255, 255))
        start_fill.fill((0, 0, 0))
        quit_fill.fill((0, 0, 0))

        self.screen.blit(username_fill, (self.username_rect.x, self.username_rect.y))
        self.screen.blit(start_fill, (self.start_rect.x, self.start_rect.y))
        self.screen.blit(quit_fill, (self.quit_rect.x, self.quit_rect.y))
        
        self.screen.blit(username_surface, (self.username_rect.x + 8, self.username_rect.y + 8))
        self.screen.blit(start_surface, (self.start_rect.x + 8, self.start_rect.y + 8))
        self.screen.blit(quit_surface, (self.quit_rect.x + 8, self.quit_rect.y + 8))

    def startscene(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)
        mousepos = None
        running = True
        is_username = False
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 0
                mousepos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.username_rect.collidepoint(mousepos):
                        is_username = True
                    else:
                        is_username =  False

                    if self.quit_rect.collidepoint(mousepos):
                        return 0

                    if self.start_rect.collidepoint(mousepos):
                        return 0

                if is_username:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            self.username += chr(event.key)
        
                self.drawscreen()
                pygame.display.update()
