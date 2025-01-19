import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

kose_noktalari =[
    [0,0,0],   
    [1,0,0],
    [1,1,0],
    [0,1,0],
    [0,0,1],
    [1,0,1],
    [1,1,1],    
    [0,1,1],
    [1,1,0.5],  
    [1,0.5,1], 
    [0.5,1,1]   
]

kenarlar =[
    (6,8),(6,9),(6,10),  
    (8,9),(9,10),(10,8),  
    (0,1),(1,2),(2,3),(3,0),  
    (4,5),(5,6),(6,7),(7,4),  
    (0,4),(1,5),(2,6),(3,7),  
    (8,2),(9,5),(10,7)  
]

eksenler =[
    [0,0,0],[2,0,0],
    [0,0,0],[0,2,0],
    [0,0,0],[0,0,2]
]

def matris_carpimi(matris,vektor):
    sonuc =[0]*4
    for i in range(4):
        sonuc[i] = (
            matris[i][0]*vektor[0]+
            matris[i][1]*vektor[1] +
            matris[i][2]*vektor[2] +
            matris[i][3]*vektor[3]
        )
    return sonuc

def donusum_uygula(noktalar,matris):
    donusen =[]
    for nokta in noktalar:
        vektor = nokta+[1] 
        sonuc = matris_carpimi(matris,vektor)
        donusen.append(sonuc[:3]) 
    return donusen

def kup_ciz(kose_noktalari, color):
    glColor3f(*color)
    glBegin(GL_LINES)
    for kenar in kenarlar:
        if 6 in kenar:
            continue
        for nokta in kenar:
            glVertex3f(*kose_noktalari[nokta])
    glEnd()

def eksenleri_ciz(eksenler):
    glBegin(GL_LINES)

    glColor3f(0,1,0)
    glVertex3f(*eksenler[0])
    glVertex3f(*eksenler[1])

    glColor3f(0,1,0)
    glVertex3f(*eksenler[2])
    glVertex3f(*eksenler[3])

    glColor3f(0,1,0)
    glVertex3f(*eksenler[4])
    glVertex3f(*eksenler[5])

    glEnd()

def main():
    pygame.init()
    ekran_boyutu=(800,600)
    pygame.display.set_mode(ekran_boyutu, DOUBLEBUF|OPENGL)

    gluPerspective(60,(ekran_boyutu[0]/ekran_boyutu[1]),0.1,50.0)
    glTranslatef(-2,-2,-10) 
    
    izometrik_matris =[
        [0.707,0.707,0,0],
        [-0.408,0.408,0.816,0],
        [0.577,-0.577,0.577,0],
        [0,0,0,1]
    ]

    kup1 = kose_noktalari
    oteleme_matris_z =[
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,2],
        [0,0,0,1]
    ]
    kup2 = donusum_uygula(kup1,oteleme_matris_z)

    olcek_matris =[
        [0.5,0,0,0],
        [0,0.5,0,0],
        [0,0,0.5,0],
        [0,0,0,1]
    ]
    oteleme_matris_xy =[
        [1,0,0,2],
        [0,1,0,2.5],
        [0,0,1,0],
        [0,0,0,1]
    ]
    olcekli_kup=donusum_uygula(kup1,olcek_matris)
    kup3=donusum_uygula(olcekli_kup,oteleme_matris_xy)

    eksenler_izometrik=donusum_uygula(eksenler,izometrik_matris)

    while True:
        for etkinlik in pygame.event.get():
            if etkinlik.type ==pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)

        kup1_izometrik =donusum_uygula(kup1,izometrik_matris)
        kup2_izometrik =donusum_uygula(kup2,izometrik_matris)
        kup3_izometrik =donusum_uygula(kup3,izometrik_matris)

        kup_ciz(kup1_izometrik,(1.0,0.75,0.8)) 
        kup_ciz(kup2_izometrik,(1.0,0.65,0.0)) 
        kup_ciz(kup3_izometrik,(0,0,1))  
    
        eksenleri_ciz(eksenler_izometrik)

        pygame.display.flip()
        pygame.time.wait(10)

main()



