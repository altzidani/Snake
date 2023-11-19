import pygame
import random
import functions
import os
import json
from Settings import *


class SnakeUnit:
    def __init__(self,rectangle,image,direction,turn_image):
        self.rectangle=rectangle
        self.image=image
        self.direction=direction
        self.rotated_image=image
        self.turn_image=turn_image
    def rotate(self):
        if self.direction == (1, 0):
            self.rotated_image = self.image
        if self.direction == (0, -1):
            self.rotated_image=pygame.transform.rotate(self.image,90)
        if self.direction == (-1, 0):
            self.rotated_image = pygame.transform.rotate(self.image, 180)
        if self.direction == (0, 1):
            self.rotated_image = pygame.transform.rotate(self.image, 270)
    def turn(self):

        if right_turning:
            if self.direction == (1, 0):
                self.rotated_image = self.turn_image
            if self.direction == (0, -1):
                self.rotated_image=pygame.transform.rotate(self.turn_image,90)
            if self.direction == (-1, 0):
                self.rotated_image = pygame.transform.rotate(self.turn_image, 180)
            if self.direction == (0, 1):
                self.rotated_image = pygame.transform.rotate(self.turn_image, 270)
        if left_turning:
            if self.direction == (1, 0):
                self.rotated_image = pygame.transform.rotate(self.turn_image, 90)
            if self.direction == (0, -1):
                self.rotated_image = pygame.transform.rotate(self.turn_image, 180)
            if self.direction == (-1, 0):
                self.rotated_image = pygame.transform.rotate(self.turn_image, 270)
            if self.direction == (0, 1):
                self.rotated_image = self.turn_image

class Button:
    def __init__(self, x, y, image, hover_image, scale):
        width = image.get_width()
        heigth = image.get_height()
        self.image=pygame.transform.scale(image, (int(width * scale), int(heigth*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.hover_image = hover_image
        self.hovered = False
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 0:
            self.hovered=True
            screen.blit(self.hover_image, (self.rect.x, self.rect.y))
        if not self.rect.collidepoint(pos):self.hovered=False
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.hovered:
            self.clicked = True
            action = True
        if self.hovered==False:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
    
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, init_val,text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        self.color = YELLOW
        self.text=text
        self.border_color = BLACK
        self.handle_color = BLUE
        self.min_value = min_val
        self.max_value = max_val
        self.value = init_val  # Initial value
        self.handle_rect = pygame.Rect((self.x+(((self.value-self.min_value)*self.width)/(self.max_value-self.min_value))-self.height//2),self.rect.top,self.height,self.height)
        self.clicked = False

    def draw(self):
        # Draw slider background
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw slider border
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 4)
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.handle_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if self.clicked:
            self.handle_rect.centerx=pos[0]
            if self.handle_rect.centerx<=self.x:
                self.handle_rect.centerx=self.x
            if self.handle_rect.centerx>=self.x+self.width:
                self.handle_rect.centerx=self.x+self.width
        self.value=round(self.min_value+((self.handle_rect.centerx-self.x)/self.width)*(self.max_value-self.min_value))
    
        # Draw the handle
        pygame.draw.rect(screen, self.handle_color, self.handle_rect)
        functions.draw_text(screen,str(self.value), font_large, BLACK, self.rect.centerx-20,self.rect.top)
        functions.draw_text(screen,self.text, font_large, BLACK, self.rect.left,self.rect.top-self.height)
    
        
if __name__ == '__main__':
    # initialize pygame
    pygame.init()

    #clock
    clock = pygame.time.Clock()

    #load json settings
    with open("settings.json", "r") as file:
        settings_file = json.load(file)
    
    grid_size=settings_file["grid_size"]
    x_grids=settings_file["x_grids"]
    y_grids=settings_file["y_grids"]
    SCREEN_WIDTH=settings_file["SCREEN_WIDTH"]
    SCREEN_HEIGHT=settings_file["SCREEN_HEIGHT"]
    VOLUME = settings_file["VOLUME"]
    FPS = settings_file["FPS"]

    # create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Title and Icon
    pygame.display.set_caption('Snake')
    icon = pygame.image.load('img/Kígyó.PNG')
    pygame.display.set_icon(icon)
    
    
    #load images
    snake_horizontal_unit = pygame.image.load("img/horizontal_unit.png")
    snake_vertical_unit = pygame.image.load("img/vertical_unit.png")
    snake_head=pygame.image.load("img/Snake_head_idle.png")
    snake_turn=pygame.image.load("img/right_turn.png")
    snake_tail=pygame.image.load("img/tail_horizontal.png")
    apple=pygame.image.load("img/apple.png")
    apple_eaten=pygame.image.load("img/apple_eaten.png")
    fat_turn=pygame.image.load("img/fat_turn.png")
    grass_texture = pygame.image.load("img/grass_texture.png")
    resume_image = pygame.image.load("img/resume.png")
    options_image = pygame.image.load("img/options.png")
    quit_image = pygame.image.load("img/quit.png")
    resume_hover = pygame.image.load("img/resume_hover.png")
    options_hover = pygame.image.load("img/options_hover.png")
    quit_hover = pygame.image.load("img/quit_hover.png")
    back_hover = pygame.image.load("img/back_hover.png")
    back = pygame.image.load("img/back.png")

    #resize images
    resized_snake_vertical_unit = pygame.transform.scale(snake_vertical_unit, (grid_size, grid_size))
    resized_snake_horizontal_unit = pygame.transform.scale(snake_horizontal_unit, (grid_size, grid_size))
    resized_snake_head = pygame.transform.scale(snake_head, (grid_size, grid_size))
    resized_snake_turn = pygame.transform.scale(snake_turn, (grid_size, grid_size))
    resized_snake_tail = pygame.transform.scale(snake_tail, (grid_size, grid_size))
    resized_apple=pygame.transform.scale(apple,(grid_size,grid_size))
    resized_eaten_apple=pygame.transform.scale(apple_eaten,(grid_size,grid_size))
    resized_fat_turn = pygame.transform.scale(fat_turn, (grid_size, grid_size))
    resized_grass_texture = pygame.transform.scale(grass_texture, (grid_size, grid_size))
    
    #music
    pygame.mixer.music.load("Slower-Tempo-2020-03-22_-_A_Bit_Of_Hope_-_David_Fesliyan.mp3")
    pygame.mixer.music.set_volume(VOLUME)  # Adjust the volume as needed
    pygame.mixer.music.play(loops=-1)

    #button instances
    resume_button=Button(SCREEN_WIDTH//4,(SCREEN_HEIGHT//6)*2,resume_image,resume_hover,1)
    options_button=Button(SCREEN_WIDTH//4,(SCREEN_HEIGHT//6)*3, options_image,options_hover,1)
    quit_button=Button(SCREEN_WIDTH//4,(SCREEN_HEIGHT//6)*4, quit_image,quit_hover,1)
    back_button = Button(SCREEN_WIDTH//10,(SCREEN_HEIGHT//6)*5,back,back_hover,1)
    
    
    #slider instances
    volume_slider = Slider(SCREEN_WIDTH//2-200,(SCREEN_HEIGHT//6),400,40,0,100,VOLUME*100,"VOLUME")
    game_speed_slider = Slider(SCREEN_WIDTH//2-200,(SCREEN_HEIGHT//6)*2,400,40,5,15,FPS,"GAME SPEED")
    window_size_x_slider = Slider(SCREEN_WIDTH//2-200,(SCREEN_HEIGHT//6)*3,400,40,15,40,x_grids,"WINDOW SIZE X")
    window_size_y_slider = Slider(SCREEN_WIDTH//2-200,(SCREEN_HEIGHT//6)*4,400,40,10,20,y_grids,"WINDOW SIZE Y")

    # fonts
    font_small = pygame.font.SysFont('Lucida Sans', 18)
    font_large = pygame.font.SysFont('Lucida Sans', 24)
    score_font = pygame.font.Font(None, 36)
    pause_font = pygame.font.Font(None,50)

    # high scores
    if os.path.exists('high_scores.txt')==False :
        with open('high_scores.txt', 'w') as file:
            file.write(str(0))
    with open('high_scores.txt', 'r') as file:
        prev_high_score = int(file.read())

    
    
    #game variables
    setup = True
    x_cord_change = 0
    y_cord_change = 0
    snake = []
    prev_positions = []
    food_list = []
    score = 0
    game_over = False
    snake_unit_count = 3
    max_food = 1
    food_count = 1
    fade_counter = 0
    start_x = (x_grids//2) #max x_grids-5
    start_y = (y_grids//2) #max y_grids
    right_turning=False
    left_turning=False
    swallowed_apple=False
    pause=False
    pause_already_pressed=False
    settings=False
    showgrid=False
    #circular linked list for movement directions
    movement_directions = functions.create_circular_linked_list(1, 0, -1, 0)
    move_x = movement_directions[0]
    move_y = movement_directions[3]

    #Functions
    def spawn_food(max_food, food_count, x_grids, grid_size, y_grids, food_list):
        for i in range(max_food - (food_count - 1)):
            food = pygame.Rect(((random.randint(0, x_grids - 1)) * (grid_size)+1),
                               ((random.randint(2, y_grids + 1)) * (grid_size)+1), grid_size, grid_size)
            if food not in food_list:
                food_list.append(food)

    #create top panel
    top_rect = pygame.Rect(0, 0, SCREEN_WIDTH, ((grid_size+1)*2)-1)
    pause_rect = pygame.Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//4, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    #Create grids
    grids = []
    for x in range(x_grids):
        grids.append([])
        for y in range(y_grids):
            rect = pygame.Rect(1+x * (grid_size),(2*grid_size)+ 1+y * (grid_size), grid_size, grid_size)
            grids[x].append(rect)

    # assign the starting positions of the starting tail elements


    snake_units = []
    def Setup():
        prev_positions.append(grids[start_x + x_cord_change - 2][start_y + y_cord_change])
        prev_positions.append(grids[start_x + x_cord_change - 1][start_y + y_cord_change])
        prev_positions.append(grids[start_x + x_cord_change][start_y + y_cord_change])
        for i in range(snake_unit_count):

            unit_rect = pygame.Rect(i, i, grid_size, grid_size)
            relocated_unit_rect = unit_rect.clamp(prev_positions[i])


            snake_units.append(SnakeUnit(relocated_unit_rect, resized_snake_horizontal_unit, (move_x.val, move_y.val),resized_snake_turn))

    # Game loop
    running = True
    while running:

        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, LIGHT_BLUE, top_rect, 100)
        clock.tick(FPS)
        occupied_grids=[]

        if setup:
            #spawn food
            spawn_food(max_food, food_count, x_grids, grid_size, y_grids, food_list)
            Setup()

        for list in grids:
            for rect in list:
                screen.blit(resized_grass_texture, rect)
                if showgrid:
                    pygame.draw.rect(screen, BLUE, rect, 1)


        #draw food
        food_count = len(food_list)
        for food in food_list:
            #pygame.draw.rect(screen, RED, food, 20)
            screen.blit(resized_apple,food)

        #build_snake
        #print(prev_positions)
        unit_rect = pygame.Rect(1, 1, grid_size, grid_size)
        relocated_unit_rect = unit_rect.clamp(prev_positions[- 1])
        if swallowed_apple==False:
            current_unit=SnakeUnit(relocated_unit_rect, resized_snake_horizontal_unit, (move_x.val, move_y.val),resized_snake_turn)
        else:
            current_unit = SnakeUnit(relocated_unit_rect, resized_eaten_apple, (move_x.val, move_y.val),
                                     resized_fat_turn)
            swallowed_apple=False

        current_unit.rotate()
        if left_turning or right_turning:
            current_unit.turn()
            left_turning=False
            right_turning=False
        if not setup:
            if not pause:
                if not game_over:
                    snake_units.append(current_unit)
        snake_units[0].image = resized_snake_tail
        snake_units[0].rotate()

        for unit in snake_units:
            screen.blit(unit.rotated_image,unit.rectangle)
        if not pause:
            if not game_over:
                snake_units.pop(0)

        if not pause:
            if not game_over:
                x_cord_change += move_x.val
                y_cord_change += move_y.val

        #if snake moves to side, it come back on the other side
        if start_x+x_cord_change==x_grids:
            x_cord_change= x_cord_change - x_grids
        if start_x+x_cord_change==-1:
            x_cord_change= x_cord_change + x_grids
        if start_y+y_cord_change==y_grids:
            y_cord_change= y_cord_change - y_grids
        if start_y+y_cord_change==-1:
            y_cord_change= y_cord_change + y_grids


        # Player movement

        player_rect = pygame.Rect(0, 0, grid_size, grid_size)
        new_player = player_rect.clamp(grids[start_x + x_cord_change][start_y + y_cord_change])
        #pygame.draw.rect(screen, GREEN, new_player, 10)
        if not pause:
            if not game_over:
                head_unit=SnakeUnit(new_player,resized_snake_head,(move_x.val,move_y.val),resized_snake_turn)
        head_unit.rotate()
        screen.blit(head_unit.rotated_image, head_unit.rectangle)
        # Assign positions of the tail for the next frame
        prev_positions.append(new_player)
        #dont let the prev_poz list get infinite long
        prev_positions = prev_positions[-(snake_unit_count + 5):]
        #collision with food
        for food in food_list:
            if new_player.colliderect(food):
                food_list.remove(food)
                score += 1
                snake_unit_count += 1
                swallowed_apple=True
                spawn_food(max_food, food_count, x_grids, grid_size, y_grids, food_list)
                snake_units.insert(0,snake_units[0])
        #collision with tail units list
        for unit in snake_units:
            if new_player.colliderect(unit.rectangle):
                game_over = True
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # keybinds
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if right_turning==False and left_turning==False:
                        move_x = move_x.prev
                        move_y = move_y.prev
                        left_turning=True
                if event.key == pygame.K_RIGHT:
                    if left_turning==False and right_turning==False:
                        move_x = move_x.next
                        move_y = move_y.next
                        right_turning=True
                #pause
                if event.key == pygame.K_ESCAPE:
                    if not game_over:
                        if pause_already_pressed==False and pause==False:
                            pause=True
                            pause_already_pressed = True
                        if pause_already_pressed==False and pause==True:
                            pause=False
                            pause_already_pressed=True
        #on the end of first turn:
        setup=False
        pause_already_pressed=False
        #on the end of all turns:
            #increase food spawn rate with score
        max_food=1+(score//10)


        # Create a text with the score on screen
        score_text = score_font.render("Score: " + str(score), True, GREEN)
        high_score_text = score_font.render("High score: " + str(prev_high_score), True, GREEN)
        screen.blit(score_text, ((SCREEN_WIDTH//2)-50, 10))
        screen.blit(high_score_text, ((SCREEN_WIDTH // 2) - 50, 30))
        #PAUSE MENU
        if pause:
            if settings:
                volume_slider.draw()
                VOLUME = round(volume_slider.value/100,1)
                pygame.mixer.music.set_volume(VOLUME)
                game_speed_slider.draw()
                FPS = game_speed_slider.value
                window_size_x_slider.draw()
                window_size_y_slider.draw()

                # settings_file["grid_size"]
                settings_file["x_grids"]=window_size_x_slider.value
                settings_file["y_grids"]=window_size_y_slider.value
                
                settings_file["SCREEN_WIDTH"]=1+window_size_x_slider.value*grid_size
                settings_file["SCREEN_HEIGHT"]=1+(window_size_y_slider.value+2)*grid_size
                if back_button.draw() or running == False:
                    settings=False
                    with open("settings.json", "w") as file:
                        json.dump(settings_file, file, indent=4)
                   
            else:            
                if resume_button.draw():
                    pause=False
                if options_button.draw():
                    settings=True
                if quit_button.draw():
                    running=False
        
            
            

        #GAME OVER
        if game_over:
            #blackening of screen
            if fade_counter <= SCREEN_HEIGHT:
                fade_counter += 20
            pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, fade_counter))
            pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - fade_counter, SCREEN_WIDTH, fade_counter))


            if score > prev_high_score:
                with open('high_scores.txt', 'w') as file:
                    file.write(str(score))

            #gameover text
            functions.draw_text(screen,'GAME OVER', font_large, YELLOW, (SCREEN_WIDTH//2)-70, (SCREEN_HEIGHT//2)-140)
            functions.draw_text(screen,'SCORE:' + str(int(score)), font_large, YELLOW, (SCREEN_WIDTH//2)-50, (SCREEN_HEIGHT//2)-100)
            functions.draw_text(screen,'PRESS SPACE', font_small, WHITE, (SCREEN_WIDTH//2)-55, (SCREEN_HEIGHT//2)-50)
            functions.draw_text(screen, 'TO PLAY AGAIN', font_small, WHITE, (SCREEN_WIDTH // 2)- 65, (SCREEN_HEIGHT // 2) -25)

            #press space to restart
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game_over=False
                #resfresh game variables
                score = 0
                fade_counter = 0
                snake_unit_count = 3
                max_food = 1
                food_count = 1
                food_list = []
                x_cord_change = 0
                y_cord_change = 0
                snake = []
                setup = True
                prev_positions = []
                # assign the starting positions of the starting tail elements
                prev_positions.append(grids[start_x + x_cord_change - 2][start_y + y_cord_change])
                prev_positions.append(grids[start_x + x_cord_change - 1][start_y + y_cord_change])
                prev_positions.append(grids[start_x + x_cord_change][start_y + y_cord_change])
                move_x = movement_directions[0]
                move_y = movement_directions[3]
                snake_units=[]
                with open('high_scores.txt','r') as file:
                    prev_high_score=int(file.read())
        #update screen
        pygame.display.update()