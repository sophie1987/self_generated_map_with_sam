import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
import math
from segment_anything import sam_model_registry, SamPredictor
from scipy.signal import convolve2d

def pre_process_img(IMG_PATH, pic_pixel_size=0.03):
    origin_img = cv2.imread(IMG_PATH, cv2.IMREAD_COLOR)
    width = origin_img.shape[1]
    height = origin_img.shape[0]
    ratio = 1/pic_pixel_size
    new_width = int(width/ratio)
    new_height = int(height/ratio)
    img = cv2.resize(origin_img, (new_width, new_height))
    return img

def init_image_array(img):
    passible = np.char.chararray((img.shape[0], img.shape[1]))
    passible[:] = '.'
    return passible

def init_terrain_classification():
    terrain_dict = {}
    terrain_dict[10] = "P" # 农田
    terrain_dict[20] = "F" # 森林
    terrain_dict[30] = "G" # 草地
    terrain_dict[40] = "T" # 灌丛
    terrain_dict[50] = "W" # 湿地
    terrain_dict[60] = "A" # 水体
    terrain_dict[70] = "G" # 苔原
    terrain_dict[80] = "I" # 不透水层
    terrain_dict[90] = "B" # 裸地 
    terrain_dict[100] = "C" # 冰雪
    return terrain_dict

def find_pixel_from_prompt(prompt, terrain_type_number, select_number=10, min_select_number=3):
    result_index = np.where(prompt == terrain_type_number)
    x=result_index[0]
    y=result_index[1]
    result = list(zip(y,x))
    if len(result) < min_select_number: # 特征点少于指定个数，不计算
        return []
    elif len(result) > select_number: # 特征点大于指定个数，取指定个数
        return random.sample(result,select_number)
    else:
        return result

def change_prompt_pixel_to_pic_pixel(prompt_point_list, prompt_pixel_size=8.98):
    tmp = np.array(prompt_point_list)
    result = np.rint(np.dot(tmp, prompt_pixel_size))
    input_point = np.array(result, dtype=int)
    input_label = np.ones(input_point.shape[0],dtype=int)
    return [input_point, input_label]

def sam_predict(image, input_point, input_label):
    #image = cv2.imread(image_path)    
    sam_checkpoint = "sam_vit_b_01ec64.pth"
    model_type = "vit_b"
    
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    
    predictor = SamPredictor(sam)
    predictor.set_image(image)
      
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    return list(zip(masks,scores))

def fill_passible(image_array, classification_list):
    classification_list.sort(key=lambda x:x[1])
    for mask, score, value in classification_list:
        image_array[mask] = value
    return image_array     

def show_result(image_array=None):    
    char_to_value = {
        '.': 0,
        'P': 50,
        'F': 100,
        'G': 150,
        'T': 200,
        'W': 250,
        'A': 20,
        'I': 70,
        'B': 120,
        'C': 170
    }

    array_int = np.zeros((image_array.shape[0],image_array.shape[1]))
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            array_int[i][j] = char_to_value[image_array[i][j]]

    plt.figure(figsize=(10, 10))
    plt.imshow(array_int, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.title('Terrain Classification Grayscale')
    plt.show()

def show_rgb_image(img):
    # 获取二维数组的形状
    height, width = img.shape
    
    # 创建一个三维数组，形状为 (height, width, 3)，初始值为0
    rgb_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # 遍历二维数组，根据字符设置RGB值
    for i in range(height):
        for j in range(width):
            if img[i, j] == '.':
                rgb_array[i, j] = [128, 128, 128]  # 灰色
            elif img[i, j] == 'F':
                rgb_array[i, j] = [0, 255, 0]     # 绿色
            elif img[i, j] == 'T':
                rgb_array[i, j] = [255, 255, 255] # 白色
            else:
                rgb_array[i, j] = [0, 0, 255] # 蓝色
    
    plt.figure(figsize=(10, 10))
    plt.imshow(rgb_array)
    plt.title('RGB Image')
    plt.axis('off')
    plt.show()
    

def generate_all_result(PROMPT_IMAGE_PATH="pic/prompt.tif", PREDICT_IMAGE_PATH="pic/pic.tif",RESULAT_PASSIBLE="result/passible.txt"):
    img = pre_process_img(PREDICT_IMAGE_PATH)
    prompt = cv2.imread(PROMPT_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread(PREDICT_IMAGE_PATH)
    terrian_dict = init_terrain_classification()
    image_array = init_image_array(img)
    classification_list = []
    for key,value in terrian_dict.items():
        result_index = find_pixel_from_prompt(prompt, key, 20)
        [input_point, input_label] = change_prompt_pixel_to_pic_pixel(result_index)
        if len(input_point)>0:
            terrian_result = sam_predict(img, input_point, input_label) # list[(masks, scores)], masks: (number_of_masks) x H x W, (3, 334, 128)
            terrian_result.sort(key=lambda x:x[1],reverse=True)
            for mask,score in terrian_result:
                if score>0.98: # 提示点不准确，做一定调整
                    continue
                classification_list.append([mask, score, value])
            
    fill_passible(image_array, classification_list)
    passible = image_array.astype(np.str_)
    unique,count = np.unique(passible, return_counts=True)
    data_count = dict(zip(unique,count))
    print("1. classification result:")
    print(data_count)
    print("2. show rgb image:")
    show_rgb_image(passible)
    print("3. show gray image:")
    show_result(passible)
    np.savetxt(RESULAT_PASSIBLE,passible, fmt='%s', delimiter='')
    # add width and height to top of the txt
    with open(RESULAT_PASSIBLE, 'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(f"height {img.shape[0]}\nwidth {img.shape[1]}\n"+content)
    # 增加卷积计算
    char_to_value = {
        '.': 0,
        'P': 0,
        'F': 1,
        'G': 0,
        'T': 0,
        'W': 1,
        'A': 1,
        'I': 1,
        'B': 0,
        'C': 0
    }

    array_int = np.zeros((passible.shape[0],passible.shape[1]))
    for i in range(passible.shape[0]):
        for j in range(passible.shape[1]):
            array_int[i][j] = char_to_value[passible[i][j]]
    kernel = np.ones((6,6))
    result_passible = convolve2d(array_int, kernel, mode='same')
    print(result_passible)
    np.savetxt("result/updated.txt",result_passible,delimiter=',',fmt='%d')

def get_updated_img(PROMPT_IMAGE_PATH="pic/prompt.tif", PREDICT_IMAGE_PATH="pic/pic.tif",UPDATED_PASSIBLE="result/passible_updated.txt"):
    '''
    通过卷积运算，计算每个点的可通行性
    '''
    img = pre_process_img(PREDICT_IMAGE_PATH)
    prompt = cv2.imread(PROMPT_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread(PREDICT_IMAGE_PATH)
    terrian_dict = init_terrain_classification()
    image_array = init_image_array(img)
    classification_list = []
    for key,value in terrian_dict.items():
        result_index = find_pixel_from_prompt(prompt, key, 20)
        [input_point, input_label] = change_prompt_pixel_to_pic_pixel(result_index)
        if len(input_point)>0:
            terrian_result = sam_predict(img, input_point, input_label) # list[(masks, scores)], masks: (number_of_masks) x H x W, (3, 334, 128)
            for mask,score in terrian_result:
                if score>0.98: # 提示点不准确，做一定调整
                    continue
                classification_list.append([mask, score, value])
            
    fill_passible(image_array, classification_list)
    passible = image_array.astype(np.str_)
    show_result(passible)
    char_to_value = {
        '.': 0,
        'P': 0,
        'F': 1,
        'G': 0,
        'T': 0,
        'W': 1,
        'A': 1,
        'I': 1,
        'B': 0,
        'C': 0
    }

    array_int = np.zeros((passible.shape[0],passible.shape[1]))
    for i in range(passible.shape[0]):
        for j in range(passible.shape[1]):
            array_int[i][j] = char_to_value[passible[i][j]]
    kernel = np.ones((3,3))
    result_passible = convolve2d(array_int, kernel, mode='same')
    print(result_passible)
    np.savetxt("test.txt",result_passible,delimiter=',',fmt='%d')
