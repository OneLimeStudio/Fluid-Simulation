import math
import pygame
import random

cal = 1
N = 50
size = (N+2) * (N+2)

def SWAP(x0,x):
    temp  = x0
    x0 = x
    x = temp

def IX(i,j):
    return ((i)+(N+2)*(j))

u ,v,u_prev,v_prev = [],[],[0] * size ,[0] * size
dens,dens_prev = [0] * size,[0] * size

def set_bnd(N,b,x):
    for i in range(1,N+1):
        if(b == 1):
            x[IX(0,i)] = -x[IX(1,i)]
            x[IX(N+1,i)] = -x[IX(N,i)]
        else:
            x[IX(0,i)] = x[IX(1,i)]
            x[IX(N+1,i)] = x[IX(N,i)]
        if b == 2:
            x[IX(i,0)] = -x[IX(i,1)]
            x[IX(i,N+1)] = -x[IX(i,N)]
        else:
            x[IX(i,0)] =   x[IX(i,1)]
            x[IX(i,N+1)] = x[IX(i,N)]
        
        
    x[IX(0,0)] = 0.5*(x[IX(1,0)] + x[IX(0,1)] )
    x[IX(0,N+1)] = 0.5*(x[IX(1,N+1)] + x[IX(0,N)] )
    x[IX(N+1,0)] = 0.5*(x[IX(N,0)] + x[IX(N+1,1)] )
    x[IX(N+1,N+1)] = 0.5*(x[IX(N,N+1)] + x[IX(N+1,N)] )
def add_src(N,x,s,dt):
    for i in range(0,size):
        x[i] += dt*s[i]
        
def diffuse(N,b,x,x0,diff,dt):
    a = dt * diff * N * N
    for k in range(0,20):
        for i in range(0,N+1):
            for j in range(0,N+1):
                x[IX(i,j)] = (x0[IX(i,j)] + a*(x[IX(i-1,j)] + x[IX(i+1,j)] + x[IX(i,j-1)] + x[IX(i,j+1)]))/(1+4*a)
                
        set_bnd(N,b,x)
        

def advect(N,b,d,d0,u,v,dt):
    dt0 =  dt*N
    for i in range(1,N+1):
        for j in range(1,N+1):
            x = i - dt0*u[IX(i,j)]
            y = j - dt0*v[IX(i,j)]
            
            if(x < 0.5):
                x = 0.5
            if x > N+0.5:
                x  =N +0.5
            i0 = int(x)
            i1 = i0 + 1
            
            
            if(y < 0.5):
                y = 0.5
            if y > N+0.5:
                y  = N +0.5
            j0 = int(y)
            j1 = j0 + 1
            
            
            s1 = x - i0
            s0 = 1 - s1           
                            
            t1 = y- j0
            t0 = 1 - t1
            
            d[IX(i,j)] = s0*(t0*d0[IX(i0,j0)] + t1*d0[IX(i0,j1)]) + s1*(t0*d0[IX(i1,j0)] + t1*d0[IX(i1,j1)])
            
    set_bnd(N,b,d)
def project(N,u,v,p,div):
    h = 1/N
    for i in range(1,N+1):
        for j in range(1,N+1):
            div[IX(i,j)] = -0.5*h*(u[IX(i+1,j)]-u[IX(i-1,j)]+v[IX(i,j+1)]-v[IX(i,j-1)]);
            p[IX(i,j)] = 0
    set_bnd ( N, 0, div )
    set_bnd ( N, 0, p )
    for k in range(0,20):
        for i in range(1,N+1):
            for j in range(1,N+1):
                p[IX(i,j)] = (div[IX(i,j)]+p[IX(i-1,j)]+p[IX(i+1,j)]+p[IX(i,j-1)]+p[IX(i,j+1)])/4
                
    set_bnd ( N, 0, p );
    for i in range(1,N+1):
        for j in range(1,N+1):
            u[IX(i,j)] -= 0.5*(p[IX(i+1,j)]-p[IX(i-1,j)])/h  
            v[IX(i,j)] -= 0.5*(p[IX(i,j+1)]-p[IX(i,j-1)])/h     
    set_bnd ( N, 1, u ) 
    set_bnd ( N, 2, v );               
def densStep(N,x,x0,u,v,diff,dt):
    add_src(N,x,x0,dt)
    SWAP(x0,x)
    diffuse(N,0,x,x0,diff,dt)
    SWAP(x0,x)
    advect(N,0,x,x0,u,v,dt)
def vel_step (N, u, v, u0, v0,visc,  dt ):

    add_src( N, u, u0, dt ) 
    add_src( N, v, v0, dt )
    SWAP ( u0, u )
    diffuse ( N, 1, u, u0, visc, dt )
    SWAP ( v0, v )
    diffuse ( N, 2, v, v0, visc, dt )
    project ( N, u, v, u0, v0 )
    SWAP ( u0, u )
    SWAP ( v0, v )
    advect ( N, 1, u, u0, u0, v0, dt )
    advect ( N, 2, v, v0, u0, v0, dt )
    project ( N, u, v, u0, v0 )
R = 0
a = 0
x0 = size * [0]
for i in range(0,size):
    x0[i] = a
    
for i in range(IX(0,25), IX(50,50)):
    x0[i] = random.choice([1])
    u_prev[i] = 1

    

u = [0] * size
v = [0] * size
x = [0] * size
# for i in range(0,1000):


    
pygame.init()
SCREEN_WIDTH = 520 * 2 
SCREEN_HEIGHT = 520 * 2
window  = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Box:
    def __init__(self,x,y,window,color):
        self.x = x 
        self.y = y
        self.window = window
        self.color = color
        self.R = R
    def draw(self):
        pygame.draw.rect(self.window, (0,0,min(self.color*100, 255) ), (self.x,self.y,SCREEN_WIDTH/(N+2),SCREEN_HEIGHT/(N+2)))
        
      
def gameLoop(dt):
    vel_step ( N, u, v,u_prev, v_prev,1, dt*10)
    densStep(N,x,x0,u,v,0.01,dt*10)
    for i in range(0,N+1):
        for j in range(0,N+1,1):
            #print(abs(v[IX(i,j)]))
            
            boxes.append(Box(i*(SCREEN_WIDTH/(N+2)),j*(SCREEN_HEIGHT/(N+2)),window,x[IX(i,j)]))
            if(u_prev[IX(i,j)] != 0):
                pygame.draw.rect(window, (0,100,min(255, 255) ), (i*(SCREEN_WIDTH/(N+2)),j*(SCREEN_HEIGHT/(N+2)),SCREEN_WIDTH/(N+2),SCREEN_HEIGHT/(N+2)))
            #boxes.append(Box(i*(SCREEN_WIDTH/(N+2)),j*(SCREEN_HEIGHT/(N+2)),window,int(abs(v[IX(i,j)]))))
     
            #print(x[IX(i,j)],i,j)
            #print(SCREEN_WIDTH) int(abs(v[IX(i,j)])))
    
    for box in boxes:
        box.draw()
            
       
boxes = []
running = True
while running:
    dt = clock.tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("YESS")
            x_A,y_A = pygame.mouse.get_pos()
            x_A  = x_A / (SCREEN_WIDTH/(N+2))
            y_A  = y_A / (SCREEN_HEIGHT/(N+2))
           
            x0[IX(int(x_A),int(y_A))] = 1.5
            #u_prev[IX(int(x_A),int(y_A))] = 0.1
            print(int(abs(v[IX(int(x_A),int(y_A))])) * 10 )

    
            #u[IX(int(x_A),int(y_A))] = 1100

            
            
            
                   
        #elif event.type == pygame.KEYUP:
        #    if event.key == pygame.K_SPACE:
    gameLoop(dt)


    pygame.display.update()
                

    