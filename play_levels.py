import pygame
import sys
import os
from menu_play import Menu


pygame.init()
pygame.key.set_repeat(100, 35)
FPS = 25
WIDTH = 960
HEIGHT = 600
STEP = 75
INDENT = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')
FPS1 = 30
clock = pygame.time.Clock()
player = None
skel = None
atack_hero = pygame.mixer.Sound('music/atack_hero.ogg')
atack_hero2 = pygame.mixer.Sound('music/atack_hero2.ogg')
atack_hero3 = pygame.mixer.Sound('music/atack_hero3.ogg')
atack_hero4 = pygame.mixer.Sound('music/atack_hero4.ogg')
atack_enemy = pygame.mixer.Sound('music/atack_enemy.ogg')
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
cell_group = pygame.sprite.Group()

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

def terminate():
    pygame.quit()
    sys.exit()

tile_images = {
    'white_string': load_image('white_string.png', -1)
}
my_menu = Menu()
my_menu.main_menu()

tile_width = tile_height = 75

class Cell(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, cell_group)
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_width, tile_height))
        self.rect = pygame.Rect(0, 0, tile_width + 1, tile_height + 1)
        self.rect.x, self.rect.y = tile_width * pos_x + INDENT, tile_height * 5 + tile_height // 2

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_width, tile_height))

        self.rect = self.image.get_rect().move(
            tile_width * pos_x + INDENT, tile_height * 5)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.transform.scale(my_menu.skel_image, (tile_width - 25, tile_height - 15))
        self.rect = pygame.Rect(0, 0, tile_width + 1, tile_height + 1)
        self.rect.x, self.rect.y = tile_width * pos_x + 15 + INDENT, tile_height * 5 + 5
        self.vx = 0
        self.vy = 0
        self.health = 4

    def set_health_enemy(self, health):
        self.health = health

    def change_skin_enemy(self, skel_image):
        self.image = pygame.transform.scale(skel_image, (tile_width - 15, tile_height - 15))

    def update(self):
        if not pygame.sprite.spritecollideany(self, box_group):
            self.rect = self.rect.move(self.vx, self.vy)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(my_menu.player_image, (tile_width - 15, tile_height - 15))
        self.rect = pygame.Rect(0, 0, tile_width + 1, tile_height + 1)
        self.rect.x, self.rect.y = tile_width * pos_x + 15 + INDENT, tile_height * 5 + 5
        self.vx = 0
        self.vy = 0
        self.health = 5

    def set_health_player(self, health):
        self.health = health

    def skin_player(self, player_image):
        self.image = pygame.transform.scale(player_image, (tile_width - 15, tile_height - 15))

    def change_skin(self, player_image):
        self.image = pygame.transform.scale(player_image, (tile_width - 15, tile_height - 15))

    def update(self):
        if pygame.sprite.spritecollideany(self, cell_group):
            self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect = self.rect.move(- self.vx, self.vy)

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

def load_level(filename):
    filename = my_menu.filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def generate_level(level):
    new_player, x, y = None, None, None
    new_skel, x, y = None, None, None
    new_string, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Cell('white_string', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
                new_string = Cell('white_string', x, y)
            elif level[y][x] == 's':
                new_skel = Enemy(x, y)
                new_string = Cell('white_string', x, y)

    return new_skel, new_player, x, y

def skin_enemy_player():
    if my_menu.player_hero_start == 1111:
        skin = load_image('Idle2.png')
        player.skin_player(skin)
    if my_menu.player_hero_start == 2222:
        skin = load_image('Idle.png')
        player.skin_player(skin)
    if my_menu.player_hero_start == 3333:
        skin = load_image('Idle3.png')
        player.skin_player(skin)
    if my_menu.levels_menu_change == 1 or my_menu.levels_menu_change == 2:
        skel_image = load_image('Idle_enemy.png')
        skel.change_skin_enemy(skel_image)
    if my_menu.levels_menu_change == 3 or my_menu.levels_menu_change == 5:
        skel_image = load_image('goblin1.png')
        skel.change_skin_enemy(skel_image)
    if my_menu.levels_menu_change == 5:
        skel_image = load_image('Idle_skel_plus1.png')
        skel.change_skin_enemy(skel_image)

run = False
all_sprites = pygame.sprite.Group()
count = 0
last = None
in_mission = False
music_paused = False
running = True
pygame.mixer.music.load('music/level_music.mp3')
pygame.mixer.music.play(-1)
turn = 'right'
qwe = 1
while running:
    if my_menu.filename == 'levels/test_map':
        qwe = 2
        del skel
        del player
        del my_menu.hero
        del my_menu.hero2
        del my_menu.enemy
        skel, player, level_x, level_y = generate_level(load_level(my_menu.filename))
        if my_menu.player_hero == 'hero1':
            my_menu.hero = AnimatedSprite(load_image("Attack1_hero1.png"), 8, 1, 400, 300)
            my_menu.hero2 = AnimatedSprite(load_image("Attack2_hero1.png"), 8, 1, 400, 300)
            my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            del my_menu.player_image
            del my_menu.skel_image
        if my_menu.player_hero == 'hero2':
            my_menu.hero = AnimatedSprite(load_image("Attack1_hero2.png"), 8, 1, 400, 300)
            my_menu.hero2 = AnimatedSprite(load_image("Attack2_hero2.png"), 8, 1, 400, 300)
            my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            del my_menu.player_image
            del my_menu.skel_image
        if my_menu.player_hero == 'hero3':
            my_menu.hero = AnimatedSprite(load_image("Attack1.png"), 8, 1, 400, 300)
            my_menu.hero2 = AnimatedSprite(load_image("Attack2.png"), 8, 1, 400, 300)
            my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            del my_menu.player_image
            del my_menu.skel_image
        my_menu.filename = 'None'
        if my_menu.w_press:
            skin_enemy_player()
    if my_menu.win == "win":
        qwe = 2
        my_menu.win = "None"

        if my_menu.filename == 'levels/test_map1':
            all_sprites = pygame.sprite.Group()
            del skel
            del player
            del my_menu.hero
            del my_menu.hero2
            del my_menu.enemy
            skel, player, level_x, level_y = generate_level(load_level(my_menu.filename))
            if my_menu.player_hero == 'hero1':
                my_menu.hero = AnimatedSprite(load_image("Attack1_hero1.png"), 8, 1, 400, 300)
                my_menu.hero2 = AnimatedSprite(load_image("Attack2_hero1.png"), 8, 1, 400, 300)
                my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            if my_menu.player_hero == 'hero2':
                my_menu.hero = AnimatedSprite(load_image("Attack1_hero2.png"), 8, 1, 400, 300)
                my_menu.hero2 = AnimatedSprite(load_image("Attack2_hero2.png"), 8, 1, 400, 300)
                my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            if my_menu.player_hero == 'hero3':
                my_menu.hero = AnimatedSprite(load_image("Attack1.png"), 8, 1, 400, 300)
                my_menu.hero2 = AnimatedSprite(load_image("Attack2.png"), 8, 1, 400, 300)
                my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            my_menu.filename = 'None'
            if my_menu.w_press:
                skin_enemy_player()
            my_menu.win = "los"
        if my_menu.filename == 'levels/test_map2':
            del skel
            del player
            del my_menu.hero
            del my_menu.hero2
            del my_menu.enemy
            skel, player, level_x, level_y = generate_level(load_level('play.txt'))
            if my_menu.player_hero == 'hero1':
                my_menu.hero = AnimatedSprite(load_image("Attack1_hero1.png"), 8, 1, 400, 300)
                my_menu.hero2 = AnimatedSprite(load_image("Attack2_hero1.png"), 8, 1, 400, 300)
                my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            if my_menu.player_hero == 'hero2':
                my_menu.hero = AnimatedSprite(load_image("Attack1_hero2.png"), 8, 1, 400, 300)
                my_menu.hero2 = AnimatedSprite(load_image("Attack2_hero2.png"), 8, 1, 400, 300)
                my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            if my_menu.player_hero == 'hero3':
                my_menu.hero = AnimatedSprite(load_image("Attack1.png"), 8, 1, 400, 300)
                my_menu.hero2 = AnimatedSprite(load_image("Attack2.png"), 8, 1, 400, 300)
                my_menu.enemy = AnimatedSprite(load_image("Runattack.png"), 8, 1, 400, 300)
            my_menu.filename = 'None'
            if my_menu.w_press:
                skin_enemy_player()
            my_menu.win = "los"
    if my_menu.lose == "lose":
        my_menu.no_go_level()
        my_menu.lose = "None"
    if qwe == 1:
        my_menu.no_go_level()

    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                count = 1
                for _ in range(8):
                    screen.blit(my_menu.bg, (0, 0))
                    count = 1
                    if my_menu.player_hero == 'hero1':
                        if my_menu.index_p - my_menu.index_e == 1:
                            if turn == 'left':
                                print(turn)
                                my_menu.hero.update()
                                atack_hero3.play()
                                all_sprites.draw(screen)
                                pygame.display.flip()
                                clock.tick(FPS)
                                my_menu.health_enemy -= my_menu.hit_1
                                print('урон врагу -1')
                                if my_menu.health_enemy <= 0:
                                    print('победа')
                                    my_menu.menu_level()
                            break
                        if my_menu.index_e - my_menu.index_p == 1:
                            if turn == 'right':
                                print(turn)
                                my_menu.hero.update()
                                atack_hero3.play()
                                all_sprites.draw(screen)
                                pygame.display.flip()
                                clock.tick(FPS)
                                my_menu.health_enemy -= my_menu.hit_1
                                print('урон врагу -1')
                                if my_menu.health_enemy <= 0:
                                    print('победа')
                                    my_menu.menu_level()
                            break

                    if my_menu.player_hero == 'hero2' or my_menu.player_hero == 'hero3':
                        if my_menu.index_p - my_menu.index_e >= 1:
                            if turn == 'left':
                                my_menu.hero.update()
                                atack_hero.play()
                                all_sprites.draw(screen)
                                pygame.display.flip()
                                clock.tick(FPS)
                                my_menu.health_enemy -= my_menu.hit_1
                                print(my_menu.hit_1)
                                print('урон врагу -1')
                                if my_menu.health_enemy <= 0:
                                    print('победа')
                                    my_menu.menu_level()
                                break
                        if my_menu.index_e - my_menu.index_p >= 1:
                            if turn == 'right':
                                my_menu.hero.update()
                                atack_hero.play()
                                all_sprites.draw(screen)
                                pygame.display.flip()
                                clock.tick(FPS)
                                my_menu.health_enemy -= my_menu.hit_1
                                print(my_menu.hit_1)
                                print('урон врагу -1')
                                if my_menu.health_enemy <= 0:
                                    print('победа')
                                    my_menu.menu_level()
                                break

                run = True
                if my_menu.index_p - my_menu.index_e == 1 or my_menu.index_e - my_menu.index_p == 1:
                    my_menu.health_player -= my_menu.hit_enemy
                    screen.blit(my_menu.bg, (0, 0))
                    my_menu.enemy.update()
                    atack_enemy.play()
                    all_sprites.draw(screen)
                    pygame.display.flip()
                    clock.tick(FPS)
                    print('урон игроку')
                    if my_menu.health_player <= 0:
                        print('поражение')
                        my_menu.defeat()
                    run = False
                if run:
                    if my_menu.index_p > my_menu.index_e:
                        my_menu.index_e += 1
                        skel.vx = STEP
                        enemy_group.update()
                    if my_menu.index_p < my_menu.index_e:
                        my_menu.index_e -= 1
                        skel.vx = -STEP
                        enemy_group.update()
                    run = False

            if event.key == pygame.K_e:
                if count == 1:
                    for _ in range(8):
                        if my_menu.player_hero == 'hero1':
                            if my_menu.index_p - my_menu.index_e == 1:
                                if turn == 'left':
                                    my_menu.hero.update()
                                    atack_hero4.play()
                                    all_sprites.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(FPS)
                                    my_menu.health_enemy -= my_menu.hit_2
                                    print('урон врагу -2')
                                    if my_menu.health_enemy <= 0:
                                        print('победа')
                                        my_menu.menu_level()
                                break
                            if my_menu.index_e - my_menu.index_p == 1:
                                if turn == 'right':
                                    my_menu.hero.update()
                                    atack_hero4.play()
                                    all_sprites.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(FPS)
                                    my_menu.health_enemy -= my_menu.hit_2
                                    print('урон врагу -2')
                                    if my_menu.health_enemy <= 0:
                                        print('победа')
                                        my_menu.menu_level()
                                break
                        if my_menu.player_hero == 'hero2' or my_menu.player_hero == 'hero3':
                            if my_menu.index_p - my_menu.index_e >= 1:
                                if turn == 'left':
                                    my_menu.hero.update()
                                    atack_hero2.play()
                                    all_sprites.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(FPS)
                                    my_menu.health_enemy -= my_menu.hit_2
                                    print(my_menu.hit_2)
                                    print('урон врагу -2')
                                    if my_menu.health_enemy <= 0:
                                        my_menu.menu_level()
                                        print('победа')
                                    break
                            if my_menu.index_e - my_menu.index_p >= 1:
                                if turn == 'right':
                                    my_menu.hero.update()
                                    atack_hero.play()
                                    all_sprites.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(FPS)
                                    my_menu.health_enemy -= my_menu.hit_2
                                    print(my_menu.hit_2)
                                    print('урон врагу -2')
                                    if my_menu.health_enemy <= 0:
                                        print('победа')
                                        my_menu.menu_level()
                                    break

                        run = True
                    if my_menu.index_p - my_menu.index_e == 1 or my_menu.index_e - my_menu.index_p == 1:
                        my_menu.health_player -= my_menu.hit_enemy
                        screen.blit(my_menu.bg, (0, 0))
                        my_menu.enemy.update()
                        atack_enemy.play()
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)
                        print('урон игроку')
                        if my_menu.health_player <= 0:
                            print('поражение')
                            my_menu.defeat()
                        run = False
                    if run:
                        if my_menu.index_p > my_menu.index_e:
                            my_menu.index_e += 1
                            skel.vx = STEP
                            enemy_group.update()
                        if my_menu.index_p < my_menu.index_e:
                            my_menu.index_e -= 1
                            skel.vx = -STEP
                            enemy_group.update()
                        run = False

            if 1 < my_menu.index_p < 9 and my_menu.index_p - my_menu.index_e != 1:
                if event.key == pygame.K_a:
                    my_menu.index_p -= 1
                    player.vx = -STEP
                    player_group.update()
                    run = True
                    if my_menu.index_p - my_menu.index_e == 1 or my_menu.index_e - my_menu.index_p == 1:
                        my_menu.health_player -= 1
                        screen.blit(my_menu.bg, (0, 0))
                        my_menu.enemy.update()
                        atack_enemy.play()
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)
                        print('урон игроку')
                        if my_menu.health_player <= 0:
                            print('поражение')
                            my_menu.defeat()
                        run = False
                    if run:
                        if my_menu.index_p > my_menu.index_e:
                            my_menu.index_e += 1
                            skel.vx = STEP
                            enemy_group.update()
                        if my_menu.index_p < my_menu.index_e:
                            my_menu.index_e -= 1
                            skel.vx = -STEP
                            enemy_group.update()
                        run = False

            if 1 <= my_menu.index_p < 9 and my_menu.index_e - my_menu.index_p != 1:
                if event.key == pygame.K_d:
                    my_menu.index_p += 1
                    player.vx = STEP
                    player_group.update()
                    run = True
                    if my_menu.index_p - my_menu.index_e == 1 or my_menu.index_e - my_menu.index_p == 1:
                        my_menu.health_player -= 1
                        screen.blit(my_menu.bg, (0, 0))
                        my_menu.enemy.update()
                        atack_enemy.play()
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)
                        print('урон игроку')
                        if my_menu.health_player <= 0:
                            print('поражение')
                            my_menu.defeat()
                        run = False
                    if run:
                        if my_menu.index_p > my_menu.index_e:
                            my_menu.index_e += 1
                            skel.vx = STEP
                            enemy_group.update()
                        if my_menu.index_p < my_menu.index_e:
                            my_menu.index_e -= 1
                            skel.vx = -STEP
                            enemy_group.update()
                        run = False

            if event.key == pygame.K_w:
                my_menu.w_press = False
                if my_menu.player_hero_turn == 111:
                    player_image = load_image('Idle22.png')
                    player.change_skin(player_image)
                    turn = 'left'
                if my_menu.player_hero_turn == 222:
                    player_image = load_image('Idle0.png')
                    player.change_skin(player_image)
                    turn = 'left'
                if my_menu.player_hero_turn == 333:
                    player_image = load_image('Idle32.png')
                    player.change_skin(player_image)
                    turn = 'left'
                run = True
                if my_menu.index_p - my_menu.index_e == 1 or my_menu.index_e - my_menu.index_p == 1:
                    my_menu.health_player -= my_menu.hit_enemy
                    screen.blit(my_menu.bg, (0, 0))
                    my_menu.enemy.update()
                    atack_enemy.play()
                    all_sprites.draw(screen)
                    pygame.display.flip()
                    clock.tick(FPS)
                    print('урон игроку')
                    if my_menu.health_player <= 0:
                        print('поражение')
                        my_menu.defeat()
                    run = False
                if run:
                    if my_menu.index_p > my_menu.index_e:
                        my_menu.index_e += 1
                        skel.vx = STEP
                        enemy_group.update()
                    if my_menu.index_p < my_menu.index_e:
                        my_menu.index_e -= 1
                        skel.vx = -STEP
                        enemy_group.update()
                    run = False

            if event.key == pygame.K_f:
                print('пропуск хода')
                run = True
                if my_menu.index_p - my_menu.index_e == 1 or my_menu.index_e - my_menu.index_p == 1:
                    my_menu.health_player -= my_menu.hit_enemy
                    screen.blit(my_menu.bg, (0, 0))
                    my_menu.enemy.update()
                    atack_enemy.play()
                    all_sprites.draw(screen)
                    pygame.display.flip()
                    clock.tick(FPS)
                    print('урон игроку')
                    if my_menu.health_player <= 0:
                        print('поражение')
                        my_menu.defeat()
                    run = False
                if run:
                    if my_menu.index_p > my_menu.index_e:
                        my_menu.index_e += 1
                        skel.vx = STEP
                        enemy_group.update()
                    if my_menu.index_p < my_menu.index_e:
                        my_menu.index_e -= 1
                        skel.vx = -STEP
                        enemy_group.update()
                    run = False

                if event.key == pygame.K_UP:
                    pass

    all_sprites.draw(screen)
    screen.blit(my_menu.bg, (0, 0))
    cell_group.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
    clock.tick(FPS1)
terminate()