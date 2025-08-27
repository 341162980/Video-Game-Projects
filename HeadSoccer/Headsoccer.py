import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Head Soccer")

PADDLE_WIDTH, PADDLE_HEIGHT = 20,100
BALL_RADIUS = 20
FPS = 60
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

#Player options:
PLAYER_IMAGES = { "Messi": "Messi_head.png", "Ronaldo": "Ronaldo_head.png",
    "Neymar": "Neymar_head.png", "Lewa": "Lewa_head.png",
    "Robben": "Robben_head.png", "Hazard": "Hazard_head.png",
    "Aguero": "Aguero_head.png", "Bale": "Bale_head.png", "Buffon": "Buffon_head.png",
    "Griezmann": "Griezmann_head.png", "Iniesta": "Iniesta_head.png",
    "Modric": "Modric_head.png", "Ozil": "Ozil_head.png",  "Pogba": "Pogba_head.png",
    "Rooney": "Rooney_head.png", "Zlatan": "Zlatan_head.png", "Totti": "Totti_head.png",
    "Sanchez": "Sanchez_head.png", "Muller": "Muller_head.png", "DiMaria": "DiMaria_head.png"
}


class Player:       #class for paddles
    COLOR = (255,255,255)   #white
    VEL = 5     #paddle speed
    
    def __init__(self, x, y, width, height, image_path, flip=False):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

        #add player images
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        if flip:
            image = pygame.transform.flip(image, True, False)  # Flip horizontally
        self.image = image
    
    def draw(self,win):     #draws paddles
        #pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
        win.blit(self.image, (self.x, self.y))
    
    def move(self,dir):       #method for moving paddle
        if dir == "up":      #move up
            self.y -= self.VEL
        if dir == "down":        #move down
            self.y += self.VEL
        if dir == "left":       #move left
            self.x -= self.VEL
        if dir == "right":          #move right
            self.x += self.VEL
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:     #class for ball
    MAX_VEL = 5
    COLOR = "yellow"
    
    def __init__(self,x,y,radius):
        self.x = self.original_x = x     #x and y change later, originals stay the same
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL    #start x-vel as max
        self.y_vel = 0
        self.last_direction = 1  #1 = right, -1 = left (determines ball reset direction)
    
    def draw(self,win):     #draw ball
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self): #ball movement method
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):        #resets ball position after going out
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.last_direction *= -1
        self.x_vel = self.MAX_VEL * self.last_direction       #ball goes toward winner; reset ball speed
        
#Select players before game starts
def select_players():
    background_color = (50, 205, 50)
    head_size = 70
    margin = 60
    cols = 5
    clock = pygame.time.Clock()

    # Preload all heads
    heads = []
    for i, (name, path) in enumerate(PLAYER_IMAGES.items()):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (head_size, head_size))
        row = i // cols
        col = i % cols
        x = 100 + col * (head_size + margin)
        y = 100 + row * (head_size + margin)
        heads.append((name, path, img, pygame.Rect(x, y, head_size, head_size)))

    selected = []
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(background_color)

        # Draw soccer field background
        pygame.draw.rect(WIN, (50, 205, 50), (10, 10, WIDTH - 20, HEIGHT - 20))
        pygame.draw.circle(WIN, "white", (WIDTH//2, HEIGHT//2), 75, 2)
        pygame.draw.rect(WIN, "white", (WIDTH//2 - 5, 0, 10, HEIGHT))

        # Draw heads
        for name, path, img, rect in heads:
            WIN.blit(img, rect.topleft)
            if path in selected:
                pygame.draw.rect(WIN, "yellow", rect, 3)

        # Show instruction based on selection progress
        if len(selected) == 0:
            text = "Left Player: Choose Your Player"
        elif len(selected) == 1:
            text = "Right Player: Choose Your Player"
        else:
            text = "Click anywhere to start"        
        
        instr = SCORE_FONT.render(text, True, "yellow")
        WIN.blit(instr, (WIDTH//2 - instr.get_width()//2, 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(selected) < 2:
                    for name, path, img, rect in heads:
                        if rect.collidepoint(event.pos) and path not in selected:
                            selected.append(path)
                else:
                    run = False

    return selected[0], selected[1]


def draw(win, paddles, ball, left_score, right_score):
    win.fill("white")   #background
    pygame.draw.rect(win, (50,205,50), (10, 10, WIDTH - 20, HEIGHT - 20)) #field
    
    pygame.draw.circle(win, "white", (WIDTH//2, HEIGHT//2), 75)
    pygame.draw.circle(win, (50,205,50), (WIDTH//2, HEIGHT//2), 65)
    pygame.draw.rect(win,"white", (WIDTH//2 - 5, 0, 10, HEIGHT))    #half line + center circle

    #nets
    pygame.draw.rect(win, (225,225,225), (10, 100, 20, 10))     #left net
    pygame.draw.rect(win, (225,225,225), (10, 500, 20, 10))
    pygame.draw.rect(win, (225,225,225), (0, 100, 10, 410))
    pygame.draw.rect(win, (225,225,225), (WIDTH - 30, 100, 20, 10))     #right net
    pygame.draw.rect(win, (225,225,225), (WIDTH -  30, 500, 20, 10))
    pygame.draw.rect(win, (225,225,225), (WIDTH - 10, 100, 10, 410))
    
    #render score
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, "white")
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, "white")
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, ((WIDTH *3)//4 - right_score_text.get_width()//2, 20))
    
    for paddle in paddles:      #draw paddles
        paddle.draw(win)
    
    ball.draw(win)
    
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):      #handles collision between ball and paddles
    #add kicking:
    keys = pygame.key.get_pressed()
    kick_left = keys[pygame.K_LALT]
    kick_right = keys[pygame.K_RALT]

    # Top and bottom wall collision
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    # Prevent ball from escaping the sides unless it's a goal
    if ball.x - ball.radius < 0:
        if not (120 <= ball.y <= 490):
            ball.x = ball.radius
            ball.x_vel *= -1
    elif ball.x + ball.radius > WIDTH:
        if not (120 <= ball.y <= 490):
            ball.x = WIDTH - ball.radius
            ball.x_vel *= -1
    
    if ball.x_vel < 0:      #check if ball collides wth left paddle
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if left_paddle.x < ball.x < left_paddle.x + left_paddle.width + ball.radius:
                ball.x_vel *= -1
                
                #bounce
                middle_y = left_paddle.y + left_paddle.height / 2   #mid-y coordinate of left_paddle
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL      #how much y_vel decreases depending on where it hits paddle
                y_vel = difference_in_y / reduction_factor      #has range -5 to 5
                ball.y_vel = -1 * y_vel
                
                # kick
                if kick_left:
                    ball.x_vel *= 1.5
                    ball.y_vel *= 1.2
                
    if ball.x_vel > 0:      #check if ball collides wth left paddle
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if right_paddle.x < ball.x < right_paddle.x + right_paddle.width + ball.radius:
                ball.x_vel *= -1
            
                #bounce
                middle_y = right_paddle.y + right_paddle.height / 2   #mid-y coordinate of right_paddle
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL      #how much y_vel decreases depending on where it hits paddle
                y_vel = difference_in_y / reduction_factor      #has range -5 to 5
                ball.y_vel = -1 * y_vel
                
                #kick
                if kick_right:
                    ball.x_vel *= 1.5
                    ball.y_vel *= 1.2
    #cap max velocity
    max_speed = 10
    ball.x_vel = max(-max_speed, min(ball.x_vel, max_speed))
    ball.y_vel = max(-max_speed, min(ball.y_vel, max_speed))

def handle_paddle_movement(keys, left_paddle, right_paddle):
    
    #left paddle movement and bounds
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >=0:    
        left_paddle.move("up")
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move("down")
    if keys[pygame.K_a] and left_paddle.x - left_paddle.VEL>= 0:
        left_paddle.move("left")
    if keys[pygame.K_d] and left_paddle.x + left_paddle.VEL + left_paddle.width <= WIDTH:
        left_paddle.move("right")
        
    #right paddle movement and bounds
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >=0 :    
        right_paddle.move("up")
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move("down")
    if keys[pygame.K_LEFT] and right_paddle.x - right_paddle.VEL>= 0:
        right_paddle.move("left")
    if keys[pygame.K_RIGHT] and right_paddle.x + right_paddle.VEL + right_paddle.width <= WIDTH:
        right_paddle.move("right")

def main(left_img, right_img):    #main game running
    run = True
    clock = pygame.time.Clock()
    
    #load characters
    left_paddle = Player(30, HEIGHT//2 - PADDLE_HEIGHT//2, 70, 70, left_img)
    right_paddle = Player(WIDTH - 30 - 60, HEIGHT//2 - PADDLE_HEIGHT//2, 70, 70, right_img, flip=True)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    
    left_score = 0
    right_score = 0
    
    while run:
        clock.tick(FPS)     #regulate game speed
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        
        for event in pygame.event.get():        #window closed
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)        #function for #paddle movement using keys  

        ball.move()
        handle_collision(ball,left_paddle, right_paddle)
        
        if ball.x < 0 and ball.y >= 120 and ball.y <= 490:      #when someone scores
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)  
            pygame.time.delay(750)
        elif ball.x > WIDTH and ball.y >= 120 and ball.y <= 490:
            left_score+=1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
            pygame.time.delay(750)
            
        if left_score >= WINNING_SCORE:     #when left wins
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            
            win_text = "Left Player Won!"       #left player win msg
            text = SCORE_FONT.render(win_text, 1, "yellow")
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 - 150))
            pygame.display.update()
            pygame.time.delay(4000)
            pygame.quit()
            exit()
            
        elif right_score>= WINNING_SCORE: #when right wins
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            
            win_text = "Right Player Won!"       #right player win msg
            text = SCORE_FONT.render(win_text, 1, "yellow")
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 - 150))
            pygame.display.update()
            pygame.time.delay(4000)
            pygame.quit()
            exit()
            
    pygame.quit()

if __name__ == '__main__':      #ensure file doesn't run when imported
    left_img, right_img = select_players()  #select players at the start
    main(left_img, right_img)
