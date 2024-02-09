import pygame
import os
import sys

def load_image(name, colorkey=None):
    fullname = os.path.join('image', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class ImageButton:
    def __init__(self, x, y, width, height, text, image_path, image_cursor=None, sound_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.heignt = height
        self.text = text
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.cursor_image = self.image
        if image_cursor:
            self.image_cursor = load_image(image_cursor)
            self.image_cursor = pygame.transform.scale(self.image_cursor, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        # наведена ли мышка на кнопку
        self.is_hovered = False

    def draw(self, screen):
        #если мышка наведена на кнопку то отображаем картинку
        #при наведении, если нет то отображаем другую картинку
        current_image = self.image_cursor if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    #проверка наведена ли мышка
    def check_cursor(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
