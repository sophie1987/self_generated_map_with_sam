import numpy as np
import cv2

origin_img = cv2.imread("./pic/prompt.tif", cv2.IMREAD_GRAYSCALE)
#new_img = np.array(origin_img)
#new_img[origin_img==40] = 90
#cv2.imwrite('./pic/prompt_new.tif', new_img)
print(origin_img)