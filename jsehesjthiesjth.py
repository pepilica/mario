import pygame
import sys
import os


FPS = 50
clock = pygame.time.Clock()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((200, 200))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Ходить на стрелочки",
                  "прыгать нельзя"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(walls, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def left(self):
        self.rect = self.rect.move(-10, 0)
        if pygame.sprite.spritecollideany(self, walls):
            self.rect = self.rect.move(10, 0)

    def right(self):
        self.rect = self.rect.move(10, 0)
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.rect = self.rect.move(-10, 0)

    def back(self):
        self.rect = self.rect.move(0, 10)
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.rect = self.rect.move(0, -10)

    def forward(self):
        self.rect = self.rect.move(0, -10)
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.rect = self.rect.move(0, 10)


def main():
    player, level_x, level_y = generate_level(load_level('map.txt'))
    screen = pygame.display.set_mode((level_x * 50, level_y * 50))
    running = True
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    player.forward()
                if i.key == pygame.K_DOWN:
                    player.back()
                if i.key == pygame.K_LEFT:
                    player.left()
                if i.key == pygame.K_RIGHT:
                    player.right()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    start_screen()
    main()