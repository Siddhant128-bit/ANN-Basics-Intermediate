import pygame

def get_inputs(player_cords,flag):
    if flag==0:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_cords[0]-=1

        elif keys[pygame.K_RIGHT]:
            player_cords[0]+=1
        
        elif keys[pygame.K_UP]:
            player_cords[1]-=1
        
        elif keys[pygame.K_DOWN]:
            player_cords[1]+=1
        
    return player_cords

def halt_cords(player_cords):
    
    if player_cords[0]<=0:
        player_cords[0]=0
    elif player_cords[0]>=470:
        player_cords[0]=470
    
    if player_cords[1]<=0:
        player_cords[1]=0
    elif player_cords[1]>=470:
        player_cords[1]=470
    return player_cords

def start_game(flag):
    run=True
    pygame.init()
    win=pygame.display.set_mode((500,500))

    player_cords=[255,255]
    opp_cords=[30,30]
    power_cords=[300,300]

    while run: 
        #Player character: 
        pygame.draw.rect(win,(0,0,255),(player_cords[0],player_cords[1],30,30))

        #Opponent character: 
        pygame.draw.rect(win,(255,0,0),(opp_cords[0],opp_cords[1],30,30))

        player_cords=get_inputs(player_cords,flag) #When flag==1 we will decide based on decision by AI
        player_cords=halt_cords(player_cords)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        pygame.display.update()
        win.fill((255,255,255))
        pygame.time.delay(20)
    pygame.quit()


if __name__=='__main__':
    start_game(0)