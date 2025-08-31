import cv2 
import numpy as np

img=cv2.imread('UAS DTU\\task_images\\3.png')

rows,columns,channels=img.shape

yellow_img=np.zeros((rows,columns,3),dtype=np.uint8)

cv2.rectangle(yellow_img,(0,0),(rows,columns),(0,255,255),-1)

print(rows,columns)

lower_range=np.array([0,165,0])
upper_range=np.array([75,255,170])

hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

mask=cv2.inRange(hsv,lower_range,upper_range)
mask_inv=cv2.bitwise_not(mask)

masked=cv2.bitwise_and(img,img,mask=mask)
masked_inv=cv2.bitwise_and(img,img,mask=mask_inv)
masked_yellow=cv2.bitwise_and(yellow_img,yellow_img,mask=mask)

result=masked_yellow+masked_inv

cv2.imshow('Original',img)
cv2.imshow('HSV',hsv)
cv2.imshow('Mask',mask)
cv2.imshow('Masked_inv',masked_inv)
cv2.imshow('Yellow',yellow_img)
cv2.imshow('Yellow Masked',masked_yellow)
cv2.imshow('Final',result)

# cv2.imwrite('Final7.png',result)

px=img[0,0]
print(px)

cv2.waitKey(0)
cv2.destroyAllWindows()