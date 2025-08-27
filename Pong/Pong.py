import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

PADDLE_WIDTH, PADDLE_HEIGHT = 20,100
BALL_RADIUS = 10
FPS = 60
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

class Paddle:       #class for paddles
    COLOR = (255,255,255)   #white
    VEL = 4     #paddle speed
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self,win):     #draws paddles
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self,up = True):       #method for moving paddle
        if up:      #move up
            self.y -= self.VEL
        else:       #move down
            self.y += self.VEL
    
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
    
    def draw(self,win):     #draw ball
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self): #ball movement method
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):        #resets ball position after going out
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1        #ball goes toward winner
        
def draw(win, paddles, ball, left_score, right_score):
    win.fill("Black")   #background
    
    #render score
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, "white")
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, "white")
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, ((WIDTH *3)//4 - right_score_text.get_width()//2, 20))
    
    for paddle in paddles:      #draw paddles
        paddle.draw(win)
    
    for i in range(10, HEIGHT, HEIGHT//20):     #draw dotted line in middle
        if i %20 ==0:    #increment rectangles
            continue
        pygame.draw.rect(win,"White", (WIDTH//2 - 5, i, 10, HEIGHT//20))
    
    ball.draw(win)
    
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):      #handles collision between ball and paddles
    
    if ball.y + ball.radius >= HEIGHT:      #if ball hits floor, reverse y_vel
        ball.y_vel *= -1
    elif ball.y + ball.radius <=0:     #ball hits ceiling
        ball.y_vel *= -1
    
    if ball.x_vel <0:       #check if ball collide with left_paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2   #mid-y coordinate of left_paddle
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL      #how much y_vel decreases depending on where it hits paddle
                y_vel = difference_in_y / reduction_factor      #has range -5 to 5
                ball.y_vel = -1 * y_vel
                
    else:           #check if ball collide with right_paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
            
                middle_y = right_paddle.y + right_paddle.height / 2   #mid-y coordinate of right_paddle
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL      #how much y_vel decreases depending on where it hits paddle
                y_vel = difference_in_y / reduction_factor      #has range -5 to 5
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    
    #left paddle movement and bounds
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >=0:    
        left_paddle.move(up = True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up = False)
        
    #right paddle movement and bounds
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >=0 :    
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up = False)

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 -PADDLE_HEIGHT//2,  PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 -PADDLE_HEIGHT//2,  PADDLE_WIDTH, PADDLE_HEIGHT)
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
        
        if ball.x < 0:      #when ball goes out
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)  
            pygame.time.delay(750)
        elif ball.x > WIDTH:
            left_score+=1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
            pygame.time.delay(750)
            
        if left_score >= WINNING_SCORE:     #when someone wins
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            
            win_text = "Left Player Won!"       #left player win msg
            text = SCORE_FONT.render(win_text, 1, "green")
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 - 60))
            pygame.display.update()
            pygame.time.delay(5000)
            
        elif right_score>= WINNING_SCORE: #right player win msg
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            
            win_text = "Right Player Won!"       #left player win msg
            text = SCORE_FONT.render(win_text, 1, "green")
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 - 60))
            pygame.display.update()
            pygame.time.delay(5000)
            
    pygame.quit()

if __name__ == '__main__':      #ensure file doesn't run when imported
    main()
    