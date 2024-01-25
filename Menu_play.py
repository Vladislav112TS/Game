import pygame
import sys
from Button_effects import ImageButton
import os

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

pygame.init()
WIDTH, HEIGHT = 960, 600
MAX_FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("shogun showdown")
main_background = load_image('shogun-showdown.jpg')
main_background2 = load_image('main_background2.jpg')
main_background3 = load_image('main_background3.jpg')
level_passed = load_image('level_passed.jpg')
clock = pygame.time.Clock()
cursor = load_image('cursor.png')
pygame.mouse.set_visible(False)
victory_music = pygame.mixer.Sound('db344f8d1a8d5b5.ogg')
loss_music = pygame.mixer.Sound('z_uki-mech-_-telo.ogg')
all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

class Menu:
    def __init__(self):
        self.main_background = load_image('shogun-showdown.jpg')
        self.main_background2 = load_image('main_background2.jpg')
        self.main_background3 = load_image('main_background3.jpg')
        self.level_passed = load_image('level_passed.jpg')
        self.clock = pygame.time.Clock()
        self.cursor = load_image('cursor.png')
        pygame.mouse.set_visible(False)
        self.player_level1 = 5
        self.enemy_level1 = 4
        self.index_p = 4
        self.index_e = 9
        self.sprite = pygame.sprite.Sprite()
        self.bg = load_image('bg.png')
        self.sprite.image = load_image("Attack1.png")
        self.sprite.image = load_image("Attack2.png")

        self.hero_image = load_image("Attack1.png")
        self.hero_image2 = load_image("Attack2.png")
        self.enemy_image = load_image("Runattack.png")

        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.cell_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        pygame.mixer.music.load('menu_music.mp3')
        pygame.mixer.music.play(-1)
        self.defi = False

    def main_menu(self):
        start_button = ImageButton(WIDTH / 2 - (252 / 2), 200, 252, 74, "Новая игра", "knop2.jpg", "knop.jpg",
                                   "click.mp3")
        settigs_button = ImageButton(WIDTH / 2 - (252 / 2), 300, 252, 74, "Настройки", "knop2.jpg", "knop.jpg",
                                     "click.mp3")
        exit_button = ImageButton(WIDTH / 2 - (252 / 2), 400, 252, 74, "Выйти", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Shogun Showdown', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(460, 50))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == start_button:
                    self.fade()
                    self.hero_change()
                    running = False

                if event.type == pygame.USEREVENT and event.button == settigs_button:
                    self.fade()
                    self.settigs_menu()
                    running = False

                if event.type == pygame.USEREVENT and event.button == exit_button:
                    pygame.quit()
                    sys.exit()

                for btn in [start_button, settigs_button, exit_button]:
                    btn.handle_event(event)

            for btn in [start_button, settigs_button, exit_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def settigs_menu(self):
        audio_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, "Звук", "knop2.jpg", "knop.jpg", "click.mp3")
        pravila_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, "Правила игры", "knop2.jpg", "knop.jpg",
                                     "click.mp3")
        infa_enemy_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "Враги", "knop2.jpg", "knop.jpg",
                                        "click.mp3")
        back_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background, (0, -200))

            font = pygame.font.Font(None, 72)  # размер текста
            text_surface = font.render('Настройки', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(460, 50))
            screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == pravila_button:
                    self.fade()
                    self.pravil_game()
                    running = False

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.main_menu()
                    running = False

                if event.type == pygame.USEREVENT and event.button == infa_enemy_button:
                    self.fade()
                    self.enemy()
                    running = False

                if event.type == pygame.USEREVENT and event.button == audio_button:
                    self.fade()
                    self.music_fon()
                    running = False

                for btn in [audio_button, pravila_button, back_button, infa_enemy_button]:
                    btn.handle_event(event)

            for btn in [audio_button, pravila_button, back_button, infa_enemy_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def pravil_game(self):
        back_button = ImageButton(WIDTH / 2 - (252 / 2), 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background, (0, -200))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Правила игры', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('Цель игры: победить противника', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(300, 100))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('Управление игроком:', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(300, 150))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('"a" - передвижение игрока на одну платформу влево', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(445, 175))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('"d" - передвижение игрока на одну платформу вправо', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(455, 200))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('"q" - атака, которая сносит минимальное количество здоровья', True,
                                       (255, 255, 255))
            text_rect = text_surface.get_rect(center=(510, 225))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('"e" - атака, которая сносит максимальное', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(360, 250))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('количество здоровья', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(700, 275))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('"w" - разворот героя', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(210, 300))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('"f" - пропуск хода', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(200, 325))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('Каждый герой имеет свои характеристики,', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(350, 400))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 42)
            text_surface = font.render('с которомы можно ознакомиться при выборе героя', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(400, 450))
            screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    running = False

                for btn in [back_button]:
                    btn.handle_event(event)

            for btn in [back_button]:
                btn.check_cursor(pygame.mouse.get_pos())  # !
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def hero_change(self):
        hero1_button = ImageButton(100, 150, 252, 252, "", "Idle2.png", "Idle2.png", "click.mp3")
        hero2_button = ImageButton(350, 150, 252, 252, "", "Idle.png", "Idle.png", "click.mp3")
        hero3_button = ImageButton(600, 150, 252, 252, "", "Idle3.png", "Idle3.png", "click.mp3")
        back_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (-300, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Выбери персонажа', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == hero1_button:
                    self.fade()
                    self.menu_hero1()
                    running = False

                if event.type == pygame.USEREVENT and event.button == hero2_button:
                    self.fade()
                    self.menu_hero2()
                    running = False

                if event.type == pygame.USEREVENT and event.button == hero3_button:
                    self.fade()
                    self.menu_hero3()
                    running = False

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.main_menu()
                    running = False

                for btn in [hero1_button, hero2_button, hero3_button, back_button]:
                    btn.handle_event(event)

            for btn in [hero1_button, hero2_button, hero3_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())  # !
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def menu_hero1(self):
        hero1_button = ImageButton(100, 150, 252, 252, "", "Idle2.png", "Idle2.png", "click.mp3")
        choice_button = ImageButton(625, 500, 252, 74, "Выбрать", "knop2.jpg", "knop.jpg", "click.mp3")
        back_button = ImageButton(50, 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Выбери персонажа', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 70)
            text_surface = font.render('Рыцарь', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 150))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Ближний бой', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 250))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Очки здоровья : 15', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 300))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Слабая атака: урон 1 хп', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 350))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Сильная атака: урон 2 хп', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 400))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.hero_change()
                    running = False

                if event.type == pygame.USEREVENT and event.button == choice_button:
                    self.fade()
                    all_sprites = pygame.sprite.Group()
                    self.hit_1 = 1
                    self.hit_2 = 2
                    self.health_player = 12
                    self.player_image = load_image('Idle2.png')
                    self.player_hero_turn = 111
                    self.player_hero = 'hero1'
                    self.sprite.image = load_image("Attack1_hero1.png")
                    self.sprite.image = load_image("Attack2_hero1.png")
                    self.hero = AnimatedSprite(load_image("Attack1_hero1.png"), 8, 1, 400, 300)
                    self.hero2 = AnimatedSprite(load_image("Attack2_hero1.png"), 8, 1, 400, 300)
                    self.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
                    self.new_game()
                    running = False

                for btn in [hero1_button, choice_button, back_button]:
                    btn.handle_event(event)

            for btn in [hero1_button, choice_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())  # !
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def menu_hero2(self):
        hero1_button = ImageButton(100, 150, 252, 252, "", "Idle.png", "Idle.png", "click.mp3")
        choice_button = ImageButton(625, 500, 252, 74, "Выбрать", "knop2.jpg", "knop.jpg", "click.mp3")
        back_button = ImageButton(50, 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Выбери персонажа', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 70)
            text_surface = font.render('Магический рыцарь', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 150))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Дальний бой', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 250))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Очки здоровья : 8', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 300))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Слабая атака: урон 0.8 хп', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 350))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Сильная атака: урон 1.8 хп', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 400))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.hero_change()
                    running = False

                if event.type == pygame.USEREVENT and event.button == choice_button:
                    self.fade()
                    all_sprites = pygame.sprite.Group()
                    self.health_player = 8
                    self.hit_1 = 0.8
                    self.hit_2 = 1.8
                    self.player_image = load_image('Idle.png')
                    self.player_hero_turn = 222
                    self.player_hero = 'hero2'
                    #self.player_image2 = load_image('Idle32.png')
                    self.sprite.image = load_image("Attack1_hero2.png")
                    self.sprite.image = load_image("Attack2_hero2.png")
                    self.hero = AnimatedSprite(load_image("Attack1_hero2.png"), 8, 1, 400, 300)
                    self.hero2 = AnimatedSprite(load_image("Attack2_hero2.png"), 8, 1, 400, 300)
                    self.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
                    self.new_game()
                    running = False

                for btn in [hero1_button, choice_button, back_button]:
                    btn.handle_event(event)

            for btn in [hero1_button, choice_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())  # !
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def menu_hero3(self):
        hero1_button = ImageButton(100, 150, 252, 252, "", "Idle3.png", "Idle3.png", "click.mp3")
        choice_button = ImageButton(625, 500, 252, 74, "Выбрать", "knop2.jpg", "knop.jpg", "click.mp3")
        back_button = ImageButton(50, 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Выбери персонажа', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 70)
            text_surface = font.render('Маг', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 150))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Дальний бой', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 250))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Очки здоровья : 5', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 300))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Слабая атака: урон 1 хп', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 350))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Сильная атака: урон 2 хп', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 400))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.hero_change()
                    running = False

                if event.type == pygame.USEREVENT and event.button == choice_button:
                    self.fade()
                    all_sprites = pygame.sprite.Group()
                    self.health_player = 5
                    self.hit_1 = 1
                    self.hit_2 = 2
                    self.player_image = load_image('Idle3.png')
                    self.player_hero_turn = 333
                    self.player_hero = 'hero3'
                    self.player_image2 = load_image('Idle32.png')
                    self.sprite.image = load_image("Attack1.png")
                    self.sprite.image = load_image("Attack2.png")
                    self.hero = AnimatedSprite(load_image("Attack1.png"), 8, 1, 400, 300)
                    self.hero2 = AnimatedSprite(load_image("Attack2.png"), 8, 1, 400, 300)
                    self.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
                    self.new_game()
                    running = False

                for btn in [hero1_button, choice_button, back_button]:
                    btn.handle_event(event)

            for btn in [hero1_button, choice_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def music_fon(self):
        off_button = ImageButton(WIDTH / 2 - (252 / 2), 200, 252, 74, "Включить", "knop2.jpg", "knop.jpg", "click.mp3")
        on_button = ImageButton(WIDTH / 2 - (252 / 2), 300, 252, 74, "Выключить", "knop2.jpg", "knop.jpg", "click.mp3")
        back_button = ImageButton(WIDTH / 2 - (252 / 2), 400, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background, (0, -200))
            music_paused = False

            font = pygame.font.Font(None, 72)
            text_surface = font.render('Звук', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(460, 50))
            screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    running = False

                if event.type == pygame.USEREVENT and event.button == on_button:
                    music_paused = not music_paused
                    if music_paused:
                        pygame.mixer.music.pause()

                if event.type == pygame.USEREVENT and event.button == off_button:
                    pygame.mixer.music.unpause()

                for btn in [off_button, on_button, back_button]:
                    btn.handle_event(event)

            for btn in [off_button, on_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())  # !
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def new_game(self):
        back_button = ImageButton(WIDTH / 2 - (252 / 2), 400, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        start_new_game = ImageButton(WIDTH / 2 - (252 / 2), 300, 252, 74, "Играть", "knop2.jpg", "knop.jpg",
                                     "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background, (0, 0))
            font = pygame.font.Font(None, 72)  # размер текста
            text_surface = font.render('Добро пожаловать в игру!', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(400, 50))
            screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == start_new_game:
                    self.fade()
                    self.play()
                    running = False

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.hero_change()
                    running = False

                for btn in [start_new_game, back_button]:
                    btn.handle_event(event)

            for btn in [start_new_game, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())  # !
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def enemy(self):
        enemy1_button = ImageButton(100, 150, 252, 252, "", "Idle_enemy1.png", "Idle_enemy1.png", "click.mp3")
        enemy2_button = ImageButton(330, 150, 252, 252, "", "goblin1.png", "goblin1.png", "click.mp3")
        enemy3_button = ImageButton(600, 150, 252, 252, "", "Idle_skel_plus1.png", "Idle_skel_plus1.png", "click.mp3")
        back_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (-300, 0))
            font = pygame.font.Font(None, 52)
            text_surface = font.render('Выбери врага, о котором хочешь узнать инфрмацию', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(490, 50))
            screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == enemy1_button:
                    self.fade()
                    self.menu_enemy1()
                    running = False

                if event.type == pygame.USEREVENT and event.button == enemy2_button:
                    self.fade()
                    self.menu_enemy2()
                    running = False

                if event.type == pygame.USEREVENT and event.button == enemy3_button:
                    self.fade()
                    self.menu_enemy3()
                    running = False

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.settigs_menu()
                    running = False

                for btn in [enemy1_button, enemy2_button, enemy3_button, back_button]:
                    btn.handle_event(event)

            for btn in [enemy1_button, enemy2_button, enemy3_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())  # !
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def menu_enemy1(self):
        enemy1_button = ImageButton(100, 150, 252, 252, "", "Idle_enemy1.png", "Idle_enemy1.png", "click.mp3")
        back_button = ImageButton(350, 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Информация о враге', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 70)
            text_surface = font.render('Скелет', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 150))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Ближний бой', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 250))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Очки здоровья : 5', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 300))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Атака: урон 1 хп', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 350))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Передвижение: 1 шаг - 1 клетка', True, (249, 183, 225))
            text_rect = text_surface.get_rect(center=(600, 400))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.enemy()
                    running = False

                for btn in [enemy1_button, back_button]:
                    btn.handle_event(event)

            for btn in [enemy1_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def menu_enemy2(self):
        enemy1_button = ImageButton(100, 150, 252, 252, "", "goblin1.png", "goblin1.png", "click.mp3")
        back_button = ImageButton(350, 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Информация о враге', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 70)
            text_surface = font.render('Гоблин', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 150))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Ближний бой', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 250))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Очки здоровья : 6', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 300))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Атака: урон 2 хп', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 350))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Передвижение: 1 шаг - 1 клетка', True, (153, 156, 226))
            text_rect = text_surface.get_rect(center=(600, 400))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.enemy()
                    running = False

                for btn in [enemy1_button, back_button]:
                    btn.handle_event(event)

            for btn in [enemy1_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def menu_enemy3(self):
        enemy1_button = ImageButton(100, 150, 252, 252, "", "Idle_skel_plus1.png", "Idle_skel_plus1.png", "click.mp3")
        back_button = ImageButton(350, 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background2, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Информация о враге', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 70)
            text_surface = font.render('Гоблин', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 150))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Ближний бой', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 250))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Очки здоровья : 7', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 300))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Атака: урон 2 хп', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 350))
            screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 40)
            text_surface = font.render('Передвижение: 1 шаг - 1 клетка', True, (156, 226, 153))
            text_rect = text_surface.get_rect(center=(600, 400))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.enemy()
                    running = False


                for btn in [enemy1_button, back_button]:
                    btn.handle_event(event)

            for btn in [enemy1_button, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def play(self):
        level1 = ImageButton(220, 250, 74, 74, "1", "level_knop1.jpg", "level_knop2.jpg", "click.mp3")
        level2 = ImageButton(320, 250, 74, 74, "2", "level_knop1.jpg", "level_knop2.jpg", "click.mp3")
        level3 = ImageButton(420, 250, 74, 74, "3", "level_knop1.jpg", "level_knop2.jpg", "click.mp3")
        level4 = ImageButton(520, 250, 74, 74, "4", "level_knop1.jpg", "level_knop2.jpg", "click.mp3")
        level5 = ImageButton(620, 250, 74, 74, "5", "level_knop1.jpg", "level_knop2.jpg", "click.mp3")
        back_button = ImageButton(700, 500, 252, 74, "Назад", "knop2.jpg", "knop.jpg", "click.mp3")
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Выбери уровень', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(400, 50))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == level1:
                    self.fade()
                    self.level_111 = 1
                    self.index_p = 4
                    self.index_e = 9
                    self.health_enemy = 5
                    self.filename = 'test_map'
                    self.bg = load_image('bg.png')
                    self.hit_enemy = 1
                    self.skel_image = load_image('Idle_enemy.png')
                    self.level_game_play = 'one'
                    print('l1')
                    running = False

                if event.type == pygame.USEREVENT and event.button == level2:
                    self.fade()
                    self.level_222 = 2
                    self.index_p = 2
                    self.index_e = 4
                    self.health_enemy = 6
                    self.filename = 'test_map1'
                    self.bg = load_image('bg.png')
                    self.hit_enemy = 1
                    self.skel_image = load_image('Idle_enemy.png')
                    self.level_game_play = 'two'
                    print('l2')
                    running = False

                if event.type == pygame.USEREVENT and event.button == level3:
                    self.fade()
                    self.level_222 = 2
                    self.index_p = 2
                    self.index_e = 4
                    self.health_enemy = 6
                    self.filename = 'test_map1'
                    self.bg = load_image('bg.png')
                    self.hit_enemy = 2
                    self.skel_image = load_image('goblin1.png')
                    self.level_game_play = 'three'
                    print('l3')
                    running = False

                if event.type == pygame.USEREVENT and event.button == level4:
                    self.fade()
                    self.level_222 = 2
                    self.index_p = 7
                    self.index_e = 4
                    self.health_enemy = 6
                    self.filename = 'test_map2'
                    self.bg = load_image('bg.png')
                    self.hit_enemy = 2
                    self.skel_image = load_image('goblin.png')
                    self.level_game_play = 'four'
                    running = False

                if event.type == pygame.USEREVENT and event.button == level5:
                    self.fade()
                    self.level_222 = 2
                    self.index_p = 7
                    self.index_e = 4
                    self.health_enemy = 6.5
                    self.filename = 'test_map2'
                    self.bg = load_image('bg.png')
                    self.hit_enemy = 2
                    self.skel_image = load_image('Idle_skel_plus1.png')
                    self.level_game_play = 'five'
                    running = False

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.fade()
                    self.new_game()
                    running = False

                for btn in [level1, level2, level3, level4, level5, back_button]:
                    btn.handle_event(event)

            for btn in [level1, level2, level3, level4, level5, back_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def menu_level(self):
        next_level_button = ImageButton(600, 300, 74, 74, "", "next_level.jpg", "next_leve_lightl.jpg", "click.mp3")
        previos_level_button = ImageButton(300, 300, 74, 74, "", "previos_level_button.jpg",
                                           "previos_level_button_light.jpg", "click.mp3")
        all_level_button = ImageButton(400, 300, 74, 74, "", "again_button.jpg", "again_button_light.jpg", "click.mp3")
        menu_button = ImageButton(500, 300, 74, 74, "", "menu_button.jpg", "menu_button_light.jpg", "click.mp3")
        victory_music.play()
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(level_passed, (0, 0))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Уровень пройден!', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 55))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == next_level_button:
                    running = False
                    self.fade()
                    self.next_level_button = True

                if event.type == pygame.USEREVENT and event.button == previos_level_button:
                    running = False
                    self.fade()

                if event.type == pygame.USEREVENT and event.button == all_level_button:
                    running = False
                    self.fade()

                if event.type == pygame.USEREVENT and event.button == menu_button:
                    self.fade()
                    self.hero_change()
                    running = False

                for btn in [next_level_button, previos_level_button, all_level_button, menu_button]:
                    btn.handle_event(event)

            for btn in [next_level_button, previos_level_button, all_level_button, menu_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def defeat(self):
        all_level_button = ImageButton(400, 300, 74, 74, "", "again_button.jpg", "again_button_light.jpg", "click.mp3")
        menu_button = ImageButton(500, 300, 74, 74, "", "menu_button.jpg", "menu_button_light.jpg", "click.mp3")
        loss_music.play()
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(main_background3, (-300, -200))
            font = pygame.font.Font(None, 72)
            text_surface = font.render('Поражение. Тебя убили', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(500, 50))
            screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == all_level_button:
                    self.fade()
                    if self.player_hero == 'hero1':
                        all_sprites = pygame.sprite.Group()
                        self.hit_1 = 1
                        self.hit_2 = 2
                        self.health_player = 12
                        self.player_image = load_image('Idle2.png')
                        self.player_hero_turn = 111
                        self.player_hero = 'hero1'
                        self.sprite.image = load_image("Attack1_hero1.png")
                        self.sprite.image = load_image("Attack2_hero1.png")
                        self.hero = AnimatedSprite(load_image("Attack1_hero1.png"), 8, 1, 400, 300)
                        self.hero2 = AnimatedSprite(load_image("Attack2_hero1.png"), 8, 1, 400, 300)
                        self.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)

                    if self.player_hero == 'hero2':
                        self.fade()
                        all_sprites = pygame.sprite.Group()
                        self.health_player = 8
                        self.hit_1 = 0.8
                        self.hit_2 = 1.8
                        self.player_image = load_image('Idle.png')
                        self.player_hero_turn = 222
                        self.sprite.image = load_image("Attack1_hero2.png")
                        self.sprite.image = load_image("Attack2_hero2.png")
                        self.hero = AnimatedSprite(load_image("Attack1_hero2.png"), 8, 1, 400, 300)
                        self.hero2 = AnimatedSprite(load_image("Attack2_hero2.png"), 8, 1, 400, 300)
                        self.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)

                    if self.player_hero == 'hero3':
                        self.fade()
                        all_sprites = pygame.sprite.Group()
                        self.health_player = 5
                        self.hit_1 = 1
                        self.hit_2 = 2
                        self.player_image = load_image('Idle3.png')
                        self.player_hero_turn = 333
                        self.player_image2 = load_image('Idle32.png')
                        self.sprite.image = load_image("Attack1.png")
                        self.sprite.image = load_image("Attack2.png")
                        self.hero = AnimatedSprite(load_image("Attack1.png"), 8, 1, 400, 300)
                        self.hero2 = AnimatedSprite(load_image("Attack2.png"), 8, 1, 400, 300)
                        self.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)

                    if self.level_game_play == 'one':
                        self.fade()
                        self.continue_level = 'one'
                        self.level_111 = 1
                        self.index_p = 4
                        self.index_e = 9
                        self.health_enemy = 5
                        self.filename = 'test_map'
                        self.bg = load_image('bg.png')
                        self.hit_enemy = 1
                        self.skel_image = load_image('Idle_enemy.png')
                        self.level_game_play = 'one'
                        running = False

                    if self.level_game_play == 'two':
                        self.fade()
                        self.level_222 = 2
                        self.index_p = 2
                        self.index_e = 4
                        self.health_enemy = 6
                        self.filename = 'test_map1'
                        self.bg = load_image('bg.png')
                        self.hit_enemy = 1
                        self.skel_image = load_image('Idle_enemy.png')
                        self.level_game_play = 'two'
                        running = False

                    if self.level_game_play == 'three':
                        self.fade()
                        self.level_222 = 2
                        self.index_p = 2
                        self.index_e = 4
                        self.health_enemy = 6
                        self.filename = 'test_map1'
                        self.bg = load_image('bg.png')
                        self.hit_enemy = 2
                        self.skel_image = load_image('goblin1.png')
                        self.level_game_play = 'three'
                        running = False

                if event.type == pygame.USEREVENT and event.button == menu_button:
                    self.fade()
                    self.hero_change()
                    running = False

                for btn in [all_level_button, menu_button]:
                    btn.handle_event(event)

            for btn in [all_level_button, menu_button]:
                btn.check_cursor(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x, y))
            pygame.display.flip()

    def fade(self):
        running = True
        fade_alpha = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

            fade_alpha += 5
            if fade_alpha >= 100:
                fade_alpha = 255
                running = False

            pygame.display.flip()
            clock.tick(MAX_FPS)

