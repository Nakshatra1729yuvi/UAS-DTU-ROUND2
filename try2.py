import cv2
import numpy as np
import math

img=cv2.imread('UAS DTU\\task_images\\10.png')


img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
template_star=cv2.imread('star.png',0)
template_triangle=cv2.imread('triangle.png',0)
template_square=cv2.imread('square.png',0)
template_circle=cv2.imread('circle.png',0)


star=[[],[],[]]              #In order green , red , yellow
triangle=[[],[],[]]
square=[[],[],[]]
circle=[]
circle_arranged=[None]*3


def circle_colour(color):
    if color[0]>=210 and color[1]>=210 and color[2]>=210:
        return 2     # for grey
    elif color[0]>=210 and color[1]<=210 and color[2] >= 210:
        return 1     # for pink
    else:
        return 0      # for blue


def check_colour(color):
    if color[1]>220 and color[2]<200:
        return 0        #0 for green
    elif color[2]>220 and color[1]<200:
        return 1        #1 for red
    else:
        return 2        #2 for yellow

def arrange_circle():
    for t in circle:
        order=circle_colour(img[t[0],t[1]])
        circle_arranged[order]=t



def get_cicles():
    w,h=template_circle.shape[::-1]
    result=cv2.matchTemplate(img_gray,template_circle,cv2.TM_CCOEFF_NORMED)

    threshold=0.7

    loc=np.where(result>=threshold)

    # print(loc[::-1])
    for pt in zip(*loc[::-1]):
        #cv2.rectangle(img,pt,(pt[0]+w,pt[1]+h),(0,255,0),1)
        cx,cy=pt[0]+w//2,pt[1]+h//2
        c=[cy.item(),cx.item()]
        #print(img[cy,cx])
        a=True
        for t in circle:
            if math.sqrt(((t[0]-c[0])**2)+((t[1]-c[1])**2))<=100:
                a=False
                break
            else:
                a=True
        if a:
            circle.append(c)
            cv2.rectangle(img,pt,(pt[0]+w,pt[1]+h),(0,255,0),1)
            print(img[cy,cx])



def get_casualities(template,list_shape,threshold):
    w,h=template.shape[::-1]

    result=cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

    loc=np.where(result>=threshold)

    # print(loc[::-1])
    for pt in zip(*loc[::-1]):
        #cv2.rectangle(img,pt,(pt[0]+w,pt[1]+h),(0,255,0),1)
        cx,cy=pt[0]+w//2,pt[1]+h//2
        c=[cy.item(),cx.item()]
        # print(img[cy,cx])
        color=check_colour(img[cy,cx])
        a=True
        for t in list_shape[color]:
            if math.sqrt(((t[0]-c[0])**2)+((t[1]-c[1])**2))<=100:
                a=False
                break
            else:
                a=True

        if a:    
            list_shape[color].append(c)
            #img[cy,cx]=(0,0,0)
            cv2.rectangle(img,pt,(pt[0]+w,pt[1]+h),(0,255,0),1)
            print(c)
            print(color)
            print(img[cy,cx])
        


get_casualities(template_star,star,0.8)
get_casualities(template_triangle,triangle,0.8)
get_casualities(template_square,square,0.7)
    

print(star) 
print(triangle) 
print(square) 



print(len(star[0])+len(star[1])+len(star[2]))
print(len(triangle[0])+len(triangle[1])+len(triangle[2]))
print(len(square[0])+len(square[1])+len(square[2]))


get_cicles()
print(circle)
arrange_circle()
print(circle_arranged)

cv2.imshow('Final',img)



cv2.waitKey(0)
cv2.destroyAllWindows()






