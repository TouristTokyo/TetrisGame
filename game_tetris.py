import pygame
from copy import deepcopy
from random import choice, randrange


class Game:
    def __init__(self, speed_game, music_play):
        pygame.init()
        self.weight, self.height = 10, 20
        self.tile = 45
        self.game_size = (self.weight * self.tile, self.height * self.tile)
        self.frame_size = (750, 940)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.font = None
        self.figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                            [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                            [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                            [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                            [(0, 0), (0, -1), (0, 1), (-1, -1)],
                            [(0, 0), (0, -1), (0, 1), (1, -1)],
                            [(0, 0), (0, -1), (0, 1), (-1, 0)]]
        self.figures = [[pygame.Rect(x + self.weight // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in
                        self.figures_pos]
        self.field = [[0 for _ in range(self.weight)] for _ in range(self.height)]
        self.get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
        self.grid = [pygame.Rect(x * self.tile, y * self.tile, self.tile, self.tile) for x in range(self.weight)
                     for y in range(self.height)]

        self.anim_fall_const, self.anim_speed_const, self.anim_interval_const = 0, speed_game, 2000

        self.game_music = music_play

        self.frame = None
        self.game_frame = None
        self.bg = None
        self.game_bg = None

    def start_game(self):
        self.__config_frame()
        if self.game_music:
            pygame.mixer.music.play(loops=-1)
        figure_rect = pygame.Rect(0, 0, self.tile - 2, self.tile - 2)
        figure, next_figure = deepcopy(choice(self.figures)), deepcopy(choice(self.figures))
        color, next_color = self.get_color(), self.get_color()
        dy = 1
        anim_fall, anim_speed, anim_interval = self.anim_fall_const, self.anim_speed_const, self.anim_interval_const
        score, lines = 0, 0
        scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
        record = int(self.__get_record())
        while True:
            dx, rotate = 0, False

            self.frame.blit(self.bg, (0, 0))
            self.frame.blit(self.game_frame, (20, 20))
            self.game_frame.blit(self.game_bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    if event.key == pygame.K_RIGHT:
                        dx = 1
                    if event.key == pygame.K_SPACE:
                        anim_interval = 100
                    if event.key == pygame.K_UP:
                        rotate = True

            # draw grid
            self.__draw_grid()

            # move x
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].x += dx
                if self.__check_boards(figure[i]):
                    figure = deepcopy(figure_old)
                    break

            # move y
            anim_fall += anim_speed
            if anim_fall > anim_interval:
                anim_fall = 0
                figure_old = deepcopy(figure)
                for i in range(4):
                    figure[i].y += dy
                    if self.__check_boards(figure[i]):
                        for j in range(4):
                            self.field[figure_old[j].y][figure_old[j].x] = color
                        figure, color = next_figure, next_color
                        next_figure, next_color = deepcopy(choice(self.figures)), self.get_color()
                        anim_interval = 2000
                        break

            # rotate
            center = figure[0]
            figure_old = deepcopy(figure)
            if rotate:
                for i in range(4):
                    x = figure[i].y - center.y
                    y = figure[i].x - center.x
                    figure[i].x = center.x - x
                    figure[i].y = center.y + y
                    if self.__check_boards(figure[i]):
                        figure = deepcopy(figure_old)
                        break

            # check Line
            score += scores[self.__check_lines()]

            # draw Figure
            for i in range(4):
                figure_rect.x = figure[i].x * self.tile
                figure_rect.y = figure[i].y * self.tile
                pygame.draw.rect(self.game_frame, color, figure_rect)

            # draw Next Figure
            for i in range(4):
                figure_rect.x = next_figure[i].x * self.tile + 380
                figure_rect.y = next_figure[i].y * self.tile + 185
                pygame.draw.rect(self.frame, next_color, figure_rect)

            # draw Field
            for y, row in enumerate(self.field):
                for x, col in enumerate(row):
                    if col:
                        figure_rect.x, figure_rect.y = x * self.tile, y * self.tile
                        pygame.draw.rect(self.game_frame, col, figure_rect)
            # game over
            for i in range(self.weight):
                if self.field[0][i]:
                    record = max(record, score)
                    self.__set_record(record)
                    self.field = [[0 for _ in range(self.weight)] for _ in range(self.height)]
                    anim_fall, anim_speed, anim_interval = self.anim_fall_const, self.anim_speed_const, self.anim_interval_const
                    score = 0
                    self.__game_over()

            self.frame.blit(self.label_nf, (485, 90))
            self.frame.blit(self.label_score, (525, 650))
            self.frame.blit(self.font.render(str(score), True, pygame.Color('gold')), (585, 710))
            self.frame.blit(self.label_record, (525, 780))
            self.frame.blit(self.font.render(str(record), True, pygame.Color('gold')), (585, 840))
            pygame.display.flip()
            self.clock.tick(self.fps)

    def __config_frame(self):
        pygame.display.set_icon(pygame.image.load("images/icon_tetris.png"))
        pygame.display.set_caption('Tetris[Game]')
        pygame.mixer.music.load("sound/tetris.mp3")
        self.frame = pygame.display.set_mode(self.frame_size)
        self.game_frame = pygame.Surface(self.game_size)
        self.bg = pygame.image.load('images/game_bg.jpg').convert()
        self.game_bg = pygame.image.load('images/field_bg.jpg').convert()
        self.font = pygame.font.Font('font/font.ttf', 35)
        self.label_nf = self.font.render('NEXT FIGURE', True, pygame.Color('red'))
        self.label_score = self.font.render('SCORE', True, pygame.Color('green'))
        self.label_record = self.font.render('RECORD', True, pygame.Color('purple'))

    def __check_boards(self, figure):
        if figure.x < 0 or figure.x > self.weight - 1:
            return True
        if figure.y > self.height - 1 or self.field[figure.y][figure.x]:
            return True
        return False

    def __draw_grid(self):
        [pygame.draw.rect(self.game_frame, (50, 50, 50), curr_rect, 1) for curr_rect in self.grid]

    def __check_lines(self):
        line, lines = self.height - 1, 0
        for row in range(self.height - 1, -1, -1):
            count = 0
            for col in range(self.weight):
                if self.field[row][col]:
                    count += 1
                self.field[line][col] = self.field[row][col]
            if count < self.weight:
                line -= 1
            else:
                lines += 1
        return lines

    def __game_over(self):
        for i_rect in self.grid:
            pygame.draw.rect(self.game_frame, self.get_color(), i_rect)
            self.frame.blit(self.game_frame, (20, 20))
            pygame.display.flip()
            self.clock.tick(200)

    def __get_record(self):
        try:
            with open('record.txt') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record.txt', 'w') as f:
                f.write('0')

    def __set_record(self, record):
        with open('record.txt', 'w') as f:
            f.write(str(record))
