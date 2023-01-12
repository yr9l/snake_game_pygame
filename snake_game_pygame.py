import pygame
from sys import exit
from random import randint

pygame.init()
pygame.font.init()

# ---------------- modif vars ----------------
# general
grid = (20, 16)
tick = 4
input_tick = 32
border = 20
field_bg_color = (40, 40, 120)
field_color = "black"
base_button_color = "white"
hovering_button_color = (255, 255, 80)
top_color = "black"
button_font_size = 30
scoreboard_font_size = 15

# player
player_res = 20
player_gap = 2
player_direction = "u"
player_initial_mass = 3
player_color = "green"
player_eye_color = "black"

# food
food_res = 16
food_color = "red"

# ---------------- comp vars ----------------
# player
player_eye_res = player_res / 4
player_eye_gap = player_res // 8
player_move_with = player_res + player_gap
with open("options.txt", "r") as file:
    try: best_score = int(file.readlines()[-1].split("=")[-1])
    except ValueError: best_score = 0

# general
clock = pygame.time.Clock()
tick_div = int(input_tick / tick)

scoreboard_font_size_height = pygame.font.Font("assets/font.ttf", scoreboard_font_size).render("Ass", True, base_button_color).get_height()

field_res = (grid[0] * player_move_with + player_gap, grid[1] * player_move_with + player_gap)

resolution = (field_res[0] + 2 * border, field_res[1] + 2 * border + scoreboard_font_size_height * 3 // 2)
field_pos = (border, border + scoreboard_font_size_height * 3 / 2)
field_end = (field_pos[0] + field_res[0], field_pos[1] + field_res[1])
middle_pos = (resolution[0] // 2, resolution[1] // 2)


window = pygame.display.set_mode(resolution)
pygame.display.set_caption("Snake Game")


class Button():
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.pos, self.text_input, self.font, self.base_color, self.hovering_color = pos, text_input, font, base_color, hovering_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.pos)

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def CheckForInput(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        else: return False

    def ChangeColor(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else: self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def best_write():
    with open("options.txt", "r") as filer:
        with open("options.txt", "w") as filew:
            filew.write("".join(filer.readlines()[:-1]) + "best=%d" % best_score)

'''
b_play = Button((middle_pos[0], middle_pos[1]), "PLAY", get_font(font_size), base_button_color, hovering_button_color)
b_options = Button((0, 0), "OPTIONS", get_font(font_size), base_button_color, hovering_button_color)
b_quit = Button((0, 0), "QUIT", get_font(font_size), base_button_color, hovering_button_color)
b_resume = Button((0, 0), "RESUME", get_font(font_size), base_button_color, hovering_button_color)
b_main_menu = Button((0, 0), "MAIN MENU", get_font(font_size), base_button_color, hovering_button_color)
b_new_game = Button((0, 0), "NEW GAME", get_font(font_size), base_button_color, hovering_button_color)
'''

class Player():
    def __init__(self):
        # modif vars
        self.res, self.gap, self.direction, self.mass, self.color, self.eye_color = player_res, player_gap, player_direction, player_initial_mass, player_color, player_eye_color

        # comp vars
        self.eye_res, self.eye_gap, self.move_with = player_eye_res, player_eye_gap, player_move_with
        self.score = 0
        self.pos = []
        x = grid[0] // 2 * self.move_with + self.gap + field_pos[0]
        y = grid[1] // 2 * self.move_with + self.gap + field_pos[1]
        for i in range(self.mass):
            self.pos.append([x, y])

    def draw(self):
        # body drawing
        for i in self.pos:
            pygame.draw.rect(window, self.color, pygame.Rect(i[0], i[1], self.res, self.res))

        # eye drawing
        if self.direction == "u":
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.eye_gap, self.pos[-1][1] + self.eye_gap, self.eye_res, self.eye_res))
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.res - (self.eye_res + self.eye_gap), self.pos[-1][1] + self.eye_gap, self.eye_res, self.eye_res))
        elif self.direction == "r":
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.res - (self.eye_res + self.eye_gap), self.pos[-1][1] + self.eye_gap, self.eye_res, self.eye_res))
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.res - (self.eye_res + self.eye_gap), self.pos[-1][1] + self.res - (self.eye_res + self.eye_gap), self.eye_res, self.eye_res))
        elif self.direction == "d":
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.res - (self.eye_res + self.eye_gap), self.pos[-1][1] + self.res - (self.eye_res + self.eye_gap), self.eye_res, self.eye_res))
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.eye_gap, self.pos[-1][1] + self.res - (self.eye_res + self.eye_gap), self.eye_res, self.eye_res))
        elif self.direction == "l":
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.eye_gap, self.pos[-1][1] + self.res - (self.eye_res + self.eye_gap), self.eye_res, self.eye_res))
            pygame.draw.rect(window, self.eye_color, pygame.Rect(self.pos[-1][0] + self.eye_gap, self.pos[-1][1] + self.eye_gap, self.eye_res, self.eye_res))

    def update(self):
        self.__init__()

player = Player()

class FoodLine():
    def __init__(self):
        # modif vars
        self.res, self.color = food_res, food_color

        # comp vars
        self.res_dif = (player.res - self.res) / 2
        self.eaten()

    def eaten(self):
        self.real_pos = [(randint(0, grid[0] - 1) * player_move_with) + player_gap + field_pos[0],
                         (randint(0, grid[1] - 1) * player_move_with) + player_gap + field_pos[1]]
        while self.real_pos in player.pos:
            self.real_pos = [(randint(0, grid[0] - 1) * player_move_with) + player_gap + field_pos[0],
                             (randint(0, grid[1] - 1) * player_move_with) + player_gap + field_pos[1]]
        self.pos = [self.real_pos[0] + self.res_dif,
                    self.real_pos[1] + self.res_dif]

    def draw(self):
        pygame.draw.rect(window, self.color, pygame.Rect(self.pos[0], self.pos[1], self.res, self.res))

    def update(self):
        self.__init__()

food = FoodLine()


def MENU():
    window.fill(field_bg_color)
    while True:
        clock.tick(input_tick)

        pygame.draw.rect(window, field_color, pygame.Rect((border, border), (resolution[0] - 2 * border, resolution[1] - 2 * border)))

        b_play = Button((middle_pos[0], middle_pos[1] - 50), "PLAY", get_font(button_font_size), base_button_color, hovering_button_color)
        b_options = Button((middle_pos[0], middle_pos[1]), "OPTIONS", get_font(button_font_size), base_button_color, hovering_button_color)
        b_quit = Button((middle_pos[0], middle_pos[1] + 50), "QUIT", get_font(button_font_size), base_button_color, hovering_button_color)

        mouse_pos = pygame.mouse.get_pos()

        b_play.ChangeColor(mouse_pos)
        b_options.ChangeColor(mouse_pos)
        b_quit.ChangeColor(mouse_pos)

        b_play.update(window)
        b_options.update(window)
        b_quit.update(window)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b_play.CheckForInput(mouse_pos):
                    NEW_GAME()
                elif b_options.CheckForInput(mouse_pos):
                    OPTIONS()
                elif b_quit.CheckForInput(mouse_pos):
                    pygame.quit()
                    exit()

def OPTIONS():
    pass

def PAUSE():
    global last_key_esc
    alpha = pygame.Surface(resolution)
    alpha.fill(top_color)
    alpha.set_alpha(200)
    window.blit(alpha, (0, 0))
    while True:
        clock.tick(input_tick)

        b_resume = Button((middle_pos[0], middle_pos[1] - 50), "RESUME", get_font(button_font_size), base_button_color, hovering_button_color)
        b_main_menu = Button((middle_pos[0], middle_pos[1]), "MAIN MENU", get_font(button_font_size), base_button_color, hovering_button_color)
        b_quit = Button((middle_pos[0], middle_pos[1] + 50), "QUIT", get_font(button_font_size), base_button_color, hovering_button_color)

        mouse_pos = pygame.mouse.get_pos()

        b_resume.ChangeColor(mouse_pos)
        b_main_menu.ChangeColor(mouse_pos)
        b_quit.ChangeColor(mouse_pos)

        b_resume.update(window)
        b_main_menu.update(window)
        b_quit.update(window)

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and last_key_esc != keys[pygame.K_ESCAPE]:
            last_key_esc = True
            PLAY()
        elif not keys[pygame.K_ESCAPE]: last_key_esc = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b_resume.CheckForInput(mouse_pos):
                    PLAY()
                elif b_main_menu.CheckForInput(mouse_pos):
                    MENU()
                elif b_quit.CheckForInput(mouse_pos):
                    pygame.quit()
                    exit()


def LOST():
    global best_score
    alpha = pygame.Surface(resolution)
    alpha.fill(top_color)
    alpha.set_alpha(200)
    window.blit(alpha, (0, 0))

    if player.score > best_score:
        best_score = player.score
        best_write()
        gm_text = "NEW BEST!"
    elif randint(0, 15) == 0:
        gm_text = "BONK!"
    else: gm_text = "GAME OVER!"

    score = get_font(20).render("Score: %d" % player.score, True, base_button_color)
    score_rect = score.get_rect(center=(middle_pos[0], middle_pos[1] - 70))
    game_over = get_font(45).render(gm_text, True, "orange")
    game_over_rect = game_over.get_rect(center=(middle_pos[0], middle_pos[1] - 110))
    window.blit(score, score_rect)
    window.blit(game_over, game_over_rect)
    while True:
        clock.tick(input_tick)

        b_new_game = Button((middle_pos[0], middle_pos[1] - 10), "NEW GAME", get_font(button_font_size), base_button_color, hovering_button_color)
        b_main_menu = Button((middle_pos[0], middle_pos[1] + 35), "MAIN MENU", get_font(button_font_size), base_button_color, hovering_button_color)
        b_quit = Button((middle_pos[0], middle_pos[1] + 80), "QUIT", get_font(button_font_size), base_button_color, hovering_button_color)

        mouse_pos = pygame.mouse.get_pos()

        b_new_game.ChangeColor(mouse_pos)
        b_main_menu.ChangeColor(mouse_pos)
        b_quit.ChangeColor(mouse_pos)

        b_new_game.update(window)
        b_main_menu.update(window)
        b_quit.update(window)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b_new_game.CheckForInput(mouse_pos):
                    NEW_GAME()
                elif b_main_menu.CheckForInput(mouse_pos):
                    MENU()
                elif b_quit.CheckForInput(mouse_pos):
                    pygame.quit()
                    exit()

def NEW_GAME():
    global moves, first_safety_moves, last_key_esc, direction
    player.update()
    food.update()

    moves = 0
    first_safety_moves = player.mass
    last_key_esc = False
    direction = player.direction

    PLAY()

def PLAY():
    global moves, first_safety_moves, last_key_esc, direction
    tick_counter = 0
    while True:
        clock.tick(input_tick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # verify which direction we apply
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.direction != "l":
            direction = "r"
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.direction != "r":
            direction = "l"
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and player.direction != "d":
            direction = "u"
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.direction != "u":
            direction = "d"

        if keys[pygame.K_ESCAPE] and last_key_esc != keys[pygame.K_ESCAPE]:
            last_key_esc = keys[pygame.K_ESCAPE]
            PAUSE()
        elif not keys[pygame.K_ESCAPE]: last_key_esc = False

        if tick_counter == input_tick: # reset the difference tickrate counter
            tick_counter = 0

        if tick_counter % tick_div == 0: # verify if its time to do a tick
            # apply the movement of the direction
            player.direction = direction
            if player.direction == "r":
                player.pos.append([player.pos[-1][0] + player_move_with, player.pos[-1][1]])
            elif player.direction == "l":
                player.pos.append([player.pos[-1][0] - player_move_with, player.pos[-1][1]])
            elif player.direction == "u":
                player.pos.append([player.pos[-1][0], player.pos[-1][1] - player_move_with])
            elif player.direction == "d":
                player.pos.append([player.pos[-1][0], player.pos[-1][1] + player_move_with])
            del player.pos[0]

            # verify if rules are respected
            rules_noncompliance = (player.pos[-1][0] < field_pos[0],
                                   player.pos[-1][1] < field_pos[1],
                                   player.pos[-1][0] > field_end[0] - player_move_with,
                                   player.pos[-1][1] > field_end[1] - player_move_with,
                                   player.pos[-1] in player.pos[:-1])
            if True in rules_noncompliance and moves > first_safety_moves:
                # game over
                LOST()

            if player.pos[-1] == food.real_pos: # verify if food is eaten
                food.eaten()
                player.pos.insert(0, player.pos[0])
                player.mass += 1
                player.score += 1

            # draw the window with all we need
            window.fill(field_bg_color)

            score = get_font(scoreboard_font_size).render("Score: %d" % player.score, True, base_button_color)
            window.blit(score, pygame.Rect((border, scoreboard_font_size_height // 2), score.get_size()))

            best = get_font(scoreboard_font_size).render("Best: %d" % best_score, True, base_button_color)
            window.blit(best, pygame.Rect((resolution[0] - (border + best.get_width()), scoreboard_font_size_height // 2), best.get_size()))

            pygame.draw.rect(window, field_color, pygame.Rect(field_pos, field_res))
            food.draw()
            player.draw()
            pygame.display.update()
            moves += 1
        tick_counter += 1

moves = 0
first_safety_moves = player.mass
last_key_esc = False
direction = player.direction

MENU()