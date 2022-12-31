import pygame
import random
import math
import os
from  model_train_test import train_model,predict_from_model

def get_inputs(player_cords,power_cords,opp_cords,flag,vel):
    if flag==1:
        print('Is it here')
        keys=pygame.key.get_pressed()
        
        #player_cords[2]=[0,0,0,0,1]
        
        if keys[pygame.K_LEFT]:
            player_cords[0]-=vel
            player_cords[2]=[0]

        elif keys[pygame.K_RIGHT]:
            player_cords[0]+=vel
            player_cords[2]=[1]
        
        elif keys[pygame.K_UP]:
            player_cords[1]-=vel
            player_cords[2]=[2]
        elif keys[pygame.K_DOWN]:
            print('Dkey pressed')
            player_cords[1]+=vel
            player_cords[2]=[3]
    else:
        if 'tf_model.h5' not in os.listdir(os.getcwd()):
            player_cords[0]+=vel
        else: 
            move=predict_from_model([[player_cords[0],player_cords[1],power_cords[0],power_cords[1],opp_cords[0],opp_cords[1]]])
            if move==0:
                player_cords[0]-=vel
            elif move==1:
                player_cords[0]+=vel  
            elif move==2: 
                player_cords[1]-=vel
            elif move==3:
                player_cords[1]+=vel
            else: 
                player_cords=player_cords
        
    return player_cords

def halt_cords(player_cords):
    
    if player_cords[0]<=0:
        player_cords[0]=0
    elif player_cords[0]>=270:
        player_cords[0]=270
    
    if player_cords[1]<=30:
        player_cords[1]=30
    elif player_cords[1]>=270:
        player_cords[1]=270
    return player_cords

def check_if_collision(cords1,cords2):
    d=((cords1[0]-cords2[0])**2+(cords1[1]-cords2[1])**2)**0.5
    if int(d)<=30:
        return 1
    else: 
        return 0

def move_opponent(cords1,cords2,score):
    o_vel_increase=3+(score/1000)
    if cords1[0]<cords2[0]:
        cords2[0]-=o_vel_increase
    elif cords1[0]>cords2[0]:
        cords2[0]+=o_vel_increase
    
    if cords1[1]<cords2[1]:
        cords2[1]-=o_vel_increase
    elif cords1[1]>cords2[1]:
        cords2[1]+=o_vel_increase
    return cords2

def dump_dataset(pl_cords,po_cords,op_cords):
    final_data=''
    player_cords=pl_cords[0:2]
    choices=pl_cords[-1]
    final_data=','.join([str(i)for i in player_cords])
    final_data=final_data+','+','.join([str(round(i,2)) for i in po_cords])+','+','.join([str(round(i,2)) for i in op_cords])+','+','.join([str(round(i,2)) for i in choices])

    try: 
        os.mkdir('Dataset')
    except:
        pass
    
    with open('Dataset\\data.csv','a') as f:
        f.write(final_data)
        f.write('\n')


def start_game(flag):
    run=True
    vel=5
    pygame.init()
    win=pygame.display.set_mode((300,300))

    player_cords=[150,150,[]]
    opp_cords=[random.randrange(0,270),random.randrange(30,270)]
    power_cords=[random.randrange(0,270),random.randrange(30,270)]
    score=0
    font = pygame.font.Font('freesansbold.ttf', 10)
    health=100

    while run: 

        with open('Score\\high_score.txt','r')as f:
            h_score=f.read()
        if h_score=='':
            h_score=0
            
        text = font.render('            Score: '+str(score)+'   Health:  '+str(health)+'    High Score: '+str(h_score), True, (255,255,255), (0,0,0))
        textRect = text.get_rect()
        textRect.center=(100,15)
        win.blit(text, textRect)

        
        #Player character: 
        pygame.draw.rect(win,(0,0,255),(player_cords[0],player_cords[1],20,20))

        #Opponent character: 
        pygame.draw.rect(win,(255,0,0),(opp_cords[0],opp_cords[1],20,20))

        #Power character: 
        pygame.draw.rect(win,(0,255,0),(power_cords[0],power_cords[1],20,20))

        player_cords=get_inputs(player_cords,power_cords,opp_cords,flag,vel) #When flag==2 we will decide based on decision by AI
        
        opp_cords=move_opponent(player_cords,opp_cords,score) #Move opponent towards 
        
        player_cords=halt_cords(player_cords)
        if flag==1:
            dump_dataset(player_cords,power_cords,opp_cords) #Function to create dataset that will generate dataset
        o_collision=check_if_collision(player_cords,opp_cords)
        p_collision=check_if_collision(player_cords,power_cords)

        if p_collision==1:
            vel=100
            score+=p_collision*10
            health+=p_collision*5
            power_cords[0]=random.randrange(0,270)
            power_cords[1]=random.randrange(30,270)
        else: 
            vel=5

        if o_collision==1:
            health-=o_collision*1


        for event in pygame.event.get():
            if event.type==pygame.QUIT: #To terminate the game press close button on the display
                run=False
            else: 
                keys=pygame.key.get_pressed() #To Terminate press Escape key on the keyboard
                if keys[pygame.K_ESCAPE]:
                    run=False
                    
        pygame.display.update()
        win.fill((0,0,0))
        
        if flag==1:
            pygame.time.delay(25)
        else: 
            pygame.time.delay(0)

        if health==0:
            run=False
    
    if int(h_score)<int(score):
        h_score=score
        with open('Score\\high_score.txt','w') as f:
            f.write(str(h_score))
    pygame.quit()


if __name__=='__main__':
    choice=2
    print(choice)
    if choice==1:
        start_game(1)
        
    else: 
        for i in range(0,choice*10):
            start_game(2)
            try:
                train_model()
            except:
                print('No Dataset found Please play the game once to generate dataset')