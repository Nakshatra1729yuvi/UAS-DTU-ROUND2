import cv2
import numpy as np
import math

image_by_priority_ratio={}

#Keep typingAny key for next image


for raw_img in range(10):
    print(f'For Image {raw_img+1}')

    img=cv2.imread(f'UAS DTU\\task_images\\{raw_img+1}.png')



    rows,columns,channels=img.shape

    yellow_img=np.zeros((rows,columns,3),dtype=np.uint8)

    cv2.rectangle(yellow_img,(0,0),(rows,columns),(0,255,255),-1)

    # print(rows,columns)

    lower_range=np.array([0,165,0])
    upper_range=np.array([75,255,170])

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(hsv,lower_range,upper_range)
    mask_inv=cv2.bitwise_not(mask)

    masked=cv2.bitwise_and(img,img,mask=mask)
    masked_inv=cv2.bitwise_and(img,img,mask=mask_inv)
    masked_yellow=cv2.bitwise_and(yellow_img,yellow_img,mask=mask)

    result=masked_yellow+masked_inv

    # cv2.imshow('Original',img)
    # cv2.imshow('HSV',hsv)
    # cv2.imshow('Mask',mask)
    # cv2.imshow('Masked_inv',masked_inv)
    # cv2.imshow('Yellow',yellow_img)
    # cv2.imshow('Yellow Masked',masked_yellow)
    cv2.imshow('Final',result)



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
            return 2        #2 for red
        else:
            return 1        #1 for yellow

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
                # print(img[cy,cx])



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
                # print(c)
                # print(color)
                # print(img[cy,cx])
            


    get_casualities(template_star,star,0.8)
    get_casualities(template_triangle,triangle,0.8)
    get_casualities(template_square,square,0.7)
        

    # print(star) 
    # print(triangle) 
    # print(square) 



    # print(len(star[0])+len(star[1])+len(star[2]))
    # print(len(triangle[0])+len(triangle[1])+len(triangle[2]))
    # print(len(square[0])+len(square[1])+len(square[2]))


    get_cicles()
    # print(circle)
    arrange_circle()
    # print(circle_arranged)

    # cv2.imshow('Final',img)



    dict_casualty={}   #In form {PtNo.:[Age,Color,Position]}

    pt=1

    for i in range(3):
        for j in range(len(star[i])):
            dict_casualty[f'pt{pt}']=[3,i+1,star[i][j]]
            pt+=1

    for i in range(3):
        for j in range(len(triangle[i])):
            dict_casualty[f'pt{pt}']=[2,i+1,triangle[i][j]]
            pt+=1


    for i in range(3):
        for j in range(len(square[i])):
            dict_casualty[f'pt{pt}']=[1,i+1,square[i][j]]
            pt+=1

    # print(dict_casualty)


    casualty_list=[]
    unique_list=[]

    for j in dict_casualty:
        casualty_list.append(dict_casualty[j][0:2])


    total_unique=0
    for i in casualty_list:
        if i not in unique_list:
            unique_list.append(i)
            total_unique+=1
            



    print(f'\tTotal No. of Unique Combination of casualties {total_unique}')
    print(f'\tTotal No. of casualties {len(casualty_list)}')


    def distance(pt1,pt2):
        return math.sqrt(((pt1[0]-pt2[0])**2)+((pt1[1]-pt2[1])**2))

    blue_dist={f'pt{i+1}':distance(circle_arranged[0],dict_casualty[f'pt{i+1}'][2]) for i in range(len(casualty_list))}
    pink_dist={f'pt{i+1}':distance(circle_arranged[1],dict_casualty[f'pt{i+1}'][2]) for i in range(len(casualty_list))}
    grey_dist={f'pt{i+1}':distance(circle_arranged[2],dict_casualty[f'pt{i+1}'][2]) for i in range(len(casualty_list))}
    # print(blue_dist)
    # print(pink_dist)
    # print(grey_dist)



    def casualty_score(casualty_list):
        return casualty_list[0]*casualty_list[1]


    arranged_casualty={f'pt{i+1}':[casualty_score(dict_casualty[f'pt{i+1}']),dict_casualty[f'pt{i+1}'][1]]for i in range(len(casualty_list))}
    # print(arranged_casualty)
    arranged_casualty=sorted(arranged_casualty.items(),key=lambda t:(t[1][0],t[1][1]),reverse=True)
    # print(arranged_casualty)


    pad_capacity = {"blue": 4, "pink": 3, "grey": 2}
    pad_assignments = {"blue": [], "pink": [], "grey": []}
    pad_priority = {"blue": 0, "pink": 0, "grey": 0}



    for id,(pr_score,emergency) in arranged_casualty:
        dist_blue=blue_dist[id]
        dist_pink=pink_dist[id]
        dist_grey=grey_dist[id]

        scores = {
            "blue":pr_score/(dist_blue),
            "pink":pr_score/(dist_pink),
            "grey":pr_score/(dist_grey)
        }

        best_pads=sorted(scores.items(),key=lambda x:x[1],reverse=True)

        for pad, _ in best_pads:
            if len(pad_assignments[pad])<pad_capacity[pad]:
                pad_assignments[pad].append((pr_score, emergency))
                pad_priority[pad]+=pr_score
                break


    total_priority=sum(pad_priority.values())
    priority_ratio=total_priority/len(arranged_casualty)

    # print(pad_assignments.values())
    print('\tAssignments of Pads',pad_assignments)
    print('\tPriority of Pads',pad_priority)
    print('\tPriority Ratio',priority_ratio)
    image_by_priority_ratio[f'img{raw_img+1}']=priority_ratio


    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_by_priority_ratio=dict(sorted(image_by_priority_ratio
                                    .items(),key=lambda x:x[1],reverse=True))
print('Image by Priority Ratio is ',image_by_priority_ratio)




