from typing import Optional
from pdf2image import convert_from_path
import os
from tesseract2dict import TessToDict
from PIL import Image
import cv2
import numpy as np

td=TessToDict()


def pdf_to_image(
    path_to_file: str = "hat_1.pdf", path_to_store: Optional[str] = None
) -> bool:
    if not path_to_store:
        path_to_store = f"./{path_to_file.split('/')[-1].split('.pdf')[0]}"
        if not os.path.exists(path_to_store):
            os.makedirs(path_to_store)
    images = convert_from_path(path_to_file)
    for i in range(len(images)):
        images[i].save(f"{path_to_store}/page_{i}.jpg", "JPEG")
    return True



def image_to_text(pic_name str)):
    img = cv2.imread(pic_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(gray,kernel,iterations = 2)
    kernel = np.ones((4,4),np.uint8)
    dilation = cv2.dilate(erosion,kernel,iterations = 2)
    edged = cv2.Canny(dilation, 30, 200)
    cnt, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(cnt)):

        area = cv2.contourArea(cnt[i])
        if area>36000 and area<100000:
#             print(i, area)
            x,y,w,h = cv2.boundingRect(cnt[i])
            crop= img[ y:h+y,x:w+x]
    #         cv2.imwrite('cropped' + str(i) + '_'+ '.jpg', crop)
    #         plt.figure(figsize= (5,5))
    #         plt.imshow(crop)
    #         plt.show()
            word_dict=td.tess2dict(crop,'out','outfolder')
            text_plain=td.word2text(word_dict,(0,0,crop.shape[1],crop.shape[0]))
            #to do - save text_plain in pandas df
            return text_plain

pdf_to_image()
image_to_text('./hat_1/page_15.jpg')





