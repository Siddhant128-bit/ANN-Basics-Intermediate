import pygame
import random

def get_inputs(player_cords,flag,vel):
    if flag==0:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_cords[0]-=vel

        elif keys[pygame.K_RIGHT]:
            player_cords[0]+=vel
        
        elif keys[pygame.K_UP]:
            player_cords[1]-=vel
        
        elif keys[pygame.K_DOWN]:
            player_cords[1]+=vel
        
    return player_cords

def halt_cords(player_cords):
    
    if player_cords[0]<=0:
        player_cords[0]=0
    elif player_cords[0]>=470:
        player_cords[0]=470
    
    if player_cords[1]<=30:
        player_cords[1]=30
    elif player_cords[1]>=470:
        player_cords[1]=470
    return player_cords

def check_if_collision(cords1,cords2):
    d=((cords1[0]-cords2[0])**2+(cords1[1]-cords2[1])**2)**0.5
    if int(d)<=30:
        return 1
    else: 
        return 0

def move_opponent(cords1,cords2,score):
    o_vel_increase=3+(score/1000)
    print(o_vel_increase)
    if cords1[0]<cords2[0]:
        cords2[0]-=o_vel_increase
    elif cords1[0]>cords2[0]:
        cords2[0]+=o_vel_increase
    
    if cords1[1]<cords2[1]:
        cords2[1]-=o_vel_increase
    elif cords1[1]>cords2[1]:
        cords2[1]+=o_vel_increase
    return cords2

def start_game(flag):
    run=True
    vel=5
    pygame.init()
    win=pygame.display.set_mode((500,500))

    player_cords=[255,255]
    opp_cords=[random.randrange(0,470),random.randrange(30,470)]
    power_cords=[random.randrange(0,470),random.randrange(30,470)]
    score=0
    font = pygame.font.Font('freesansbold.ttf', 25)
    health=100

    while run: 

        with open('Score\\high_score.txt','r')as f:
            h_score=f.read()
        if h_score=='':
            h_score=0
            
        text = font.render('            Score: '+str(score)+'   Health:  '+str(health)+'    High Score: '+str(h_score), True, (255,255,255), (0,0,0))
        textRect = text.get_rect()
        textRect.center=(200,15)
        win.blit(text, textRect)

        
        #Player character: 
        pygame.draw.rect(win,(0,0,255),(player_cords[0],player_cords[1],30,30))

        #Opponent character: 
        pygame.draw.rect(win,(255,0,0),(opp_cords[0],opp_cords[1],30,30))

        #Power character: 
        pygame.draw.rect(win,(0,255,0),(power_cords[0],power_cords[1],30,30))

        player_cords=get_inputs(player_cords,flag,vel) #When flag==1 we will decide based on decision by AI
        opp_cords=move_opponent(player_cords,opp_cords,score) #Move opponent towards 

        player_cords=halt_cords(player_cords)
        
        o_collision=check_if_collision(player_cords,opp_cords)
        p_collision=check_if_collision(player_cords,power_cords)
        #print(f'Opp collision: {o_collision} , Power Collision: {p_collision}')

        if p_collision==1:
            vel=100
            score+=p_collision*10
            health+=p_collision*5
            power_cords[0]=random.randrange(0,470)
            power_cords[1]=random.randrange(30,470)
        else: 
            vel=5
        #p_collision=check_if_collision(player_cords,power_cords)

        if o_collision==1:
            health-=o_collision*1
            #print(health)


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        pygame.display.update()
        win.fill((0,0,0))
        pygame.time.delay(20)
        if health==0:
            run=False
    
    if int(h_score)<int(score):
        h_score=score
        with open('Score\\high_score.txt','w') as f:
            f.write(str(h_score))
    pygame.quit()


if __name__=='__main__':
    start_game(0)