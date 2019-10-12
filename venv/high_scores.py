import pygame
import sys


class High_Scores:
    def __init__(self, ai_settings, screen):
        self.ai_settings = ai_settings
        self.screen = screen

        # Font settings for scoring information.
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Gather scores stored in text file
        file = open("high_scores.txt", "r")
        self.scores = []
        self.initials = []
        i = 0
        for line in file:
            if i < 10:
                self.scores.append(int(line))
            else:
                self.initials.append(line)
            i += 1

    def append_score(self, new_high_score, rank):
        # Place the new score in the list
        next_score = new_high_score
        next_ini = ""
        for i in range(rank, 10):
            temp1 = self.scores[i]
            self.scores[i] = next_score
            next_score = temp1
            temp2 = self.initials[i]
            self.initials[i] = next_ini
            next_ini = temp2

        # Get new initials
        text = ''
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                text = text[:3]
            self.display()
            text_image = self.font.render(text, True, self.green, self.ai_settings.bg_color)
            text_rect = text_image.get_rect()
            text_rect.x = 450
            text_rect.y = 80 + (50 * rank)
            self.screen.blit(text_image, text_rect)
            text_image = self.font.render("Enter your initials:", True, self.green, self.ai_settings.bg_color)
            text_rect = text_image.get_rect()
            text_rect.x = 100
            text_rect.y = 80 + (50 * rank)
            self.screen.blit(text_image, text_rect)
            pygame.display.flip()

        # Place the new initials in the list
        text += "\n"
        self.initials[rank] = text

        # Write the new highscore list to a text file
        file = open("high_scores.txt", "w")
        for score in self.scores:
            file.write(str(score))
            file.write("\n")
        for ini in self.initials:
            file.write(ini)

    def display(self):
        self.screen.fill(self.ai_settings.bg_color)

        fontL = pygame.font.SysFont(None, 68)
        textobj = fontL.render("High", 1, self.green)
        textrect = textobj.get_rect()
        textrect.topleft = 470, 10
        self.screen.blit(textobj, textrect)
        textobj = fontL.render("Scores", 1, self.white)
        textrect = textobj.get_rect()
        textrect.topleft = 600, 10
        self.screen.blit(textobj, textrect)

        x1 = 450
        x2 = 600
        y = 80
        for i in range(10):
            textobj = self.font.render(self.initials[i][:3], 1, self.green)
            textrect = textobj.get_rect()
            textrect.topleft = x1, y + (50 * i)
            self.screen.blit(textobj, textrect)

            textobj = self.font.render(str(self.scores[i]), 1, self.white)
            textrect = textobj.get_rect()
            textrect.topleft = x2, y + (50 * i)
            self.screen.blit(textobj, textrect)