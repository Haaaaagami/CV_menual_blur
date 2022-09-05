"""
CV_menual_blur_v2.1.1
20220830 하도겸 인턴
수동 비식별화 프로그램
코드 다듬기 전.. 코드 다듬는 작업 필요..
"""

"""
CV_menual_blur_v2.2.0
20220902 하도겸 인턴
현재 페이지/전체페이지 이미지명 표시 추가.
esc키 나가기 + 전체 이미지 저장 과정에서, 전체 이미지 저장 과정이 진행되지 않던 오류 수정 
"""

import cv2
import os
import keyboard
import copy
from tkinter import messagebox as mb


ksize = 30              
win_title = 'CV_menual_blur_v1.0.1'    

process_path = input('비식별화 처리 작업 대상 이미지 폴더 경로')
img_path_list = os.listdir(process_path)
img_path_list.sort()
img_path_list = [os.path.join(process_path,img) for img in img_path_list]
img_path_list.sort() 
result_path = input('비식별화 결과 이미지 저장 폴더 경로')

SELECTER = 0
img_dic_list = []

# 폰트 색상 설정
blue = (255, 0, 0)
green= (0, 255, 0)
red= (0, 0, 255)
white= (100, 255, 255)

# 폰트 설정
font =  cv2.FONT_HERSHEY_PLAIN

assert not os.listdir(result_path), '비식별화 결과 이미지 저장 폴더는 비어있어야 합니다.'
    
for img_path in img_path_list:
    dic = {}
    dic["name"] = os.path.basename(img_path)
    dic["path"] = img_path
    dic["xywh"] = []
    img_dic_list.append(dic)

    """ img_dic_list structure
[
{
    "name" = 이미지 파일명
    "path" = 이미지 파일 경로
    "xywh" = [[이미지 파일 내 블러 처리할 좌표1], [이미지 파일 내 블러 처리할 좌표2],[이미지 파일 내 블러 처리할 좌표n]]
}
]

    """

def xywh_apply(SELECTER):
    if img_dic_list[SELECTER]["xywh"]:
        img_data = cv2.imread(img_dic_list[SELECTER]["path"])
        for x,y,w,h in img_dic_list[SELECTER]["xywh"]:
            if w > 0 and h > 0:
                roi = img_data[y:y+h, x:x+w]
                roi = cv2.blur(roi, (ksize, ksize))
                img_data[y:y+h, x:x+w] = roi
    else:
        img_data = cv2.imread(img_dic_list[SELECTER]["path"])
    return img_data
    
cv2.namedWindow('image')
while True:
    img_path = img_dic_list[SELECTER]["path"]
    img_data = xywh_apply(SELECTER)
    img_name = img_dic_list[SELECTER]["name"]
    text = 'Page: {}/{}'.format(SELECTER+1,len(img_dic_list)) + '{}'.format(img_name)
    img_data_with_text = copy.deepcopy(img_data)
    img_data_with_text = cv2.putText(img_data_with_text, text, (0,10), font, 1, white, 1, cv2.LINE_AA) 
    cv2.imshow("image", img_data_with_text)
    key_inp = cv2.waitKey()
    if key_inp == 102:
        cv2.imwrite(os.path.join(result_path, img_name), img_data)
        print('{} 페이지 {}저장 되었습니다.'.format(SELECTER, img_name))
        if SELECTER < len(img_dic_list)-1:
            SELECTER += 1
            print('{} 페이지'.format(SELECTER))

    elif key_inp == 100:
        if SELECTER > 0:
            SELECTER -= 1
            print('{} 페이지'.format(SELECTER))

    elif key_inp == 110:
        x,y,w,h = cv2.selectROI('image', img_data_with_text, False)
        img_dic_list[SELECTER]["xywh"].append([x,y,w,h])
        print(img_dic_list[SELECTER]["xywh"])

    elif key_inp == 113:
        print("{}페이지 {} 초기화".format(SELECTER, img_name))
        img_dic_list[SELECTER]["xywh"] = []
        cv2.imwrite(os.path.join(result_path, img_name), img_data)

    elif key_inp == 27:
        break

cv2.destroyAllWindows()
for selecter in range(len(img_dic_list)):
    img_data = xywh_apply(selecter)
    cv2.imwrite(os.path.join(result_path, img_dic_list[selecter]["name"]), img_data)
mb.showwarning(title = "저장 완료", message = "모든 이미지가 저장 완료되었습니다")