import numpy as np
import math
import matplotlib.pyplot as plt

def convert_number(number):
    if number <= 5:
        return 1
    elif number <= 10:
        return 0.6
    elif number <= 20:
        return 0.4
    elif number <= 35:
        return 0.2
    else:
        return 0

def change_height_value():
    # 原始数据
    data = """
    16.917 13.457 7.833 1.217 6.379
    16.229 12.536 6.629 1.068 7.141
    16.751 12.814 7.054 4.38 8.71
    17.89 13.406 9.107 8.111 11.499
    18.777 13.828 10.457 10.03 14.306
    19.788 14.621 10.436 9.583 15.332
    21.26 15.613 9.72 7.543 14.71
    21.955 15.616 8.407 4.059 11.709
    20.376 15.169 8.997 1.721 8.849
    16.666 14.277 10.643 1.968 8.544
    13.737 12.369 10.399 2.134 9.375
    12.689 11.127 7.973 0.477 9.921
    13.057 9.72 5.096 2.721 0.182
    """
   
    result_lines = [
        " ".join(str(convert_number(float(num))) for num in line.split())
        for line in data.strip().split("\n")
    ]

    with open("converted_height.txt", "w") as file:
        file.write("\n".join(result_lines))


def convert_terran(terran):
    if terran.lower() == 'b': # B，裸地
        return 0.8
    elif terran.lower() == 'g': # G，草地
        return 0.7
    elif terran.lower() == 't': # T，灌丛
        return 0.3
    else:
        return 0

def get_passible_with_height():
    # 读取原始数据
    with open("result/passible.txt") as f:
        height = int(f.readline().strip().split()[1])
        width = int(f.readline().strip().split()[1])
        print(f"map size: {height} x {width}")
        result_lines = []
        for i in range(height):
            line = f.readline().strip()
            result_line = [
                " ".join(str(convert_terran(num)) for num in line)
            ]
            result_lines.extend(result_line)

        with open("converted_terran.txt", "w") as file:
            file.write("\n".join(result_lines))
    
def mix_terran_with_height():
    height_num = np.loadtxt('converted_height.txt')
    terran_num = np.loadtxt('converted_terran.txt')
    # 获取height_num的形状
    height_rows, height_cols = height_num.shape
    
    # 初始化结果数组
    result_num = np.zeros_like(terran_num)
    
    # 计算每个元素的索引并进行乘法运算
    for i in range(terran_num.shape[0]):
        for j in range(terran_num.shape[1]):
            row_idx = math.floor(i // (terran_num.shape[0] // height_rows))
            col_idx = math.floor(j // (terran_num.shape[1] // height_cols))
            if col_idx >= height_cols:
                col_idx = height_cols - 1
            if row_idx >= height_rows:
                row_idx = height_rows - 1
            result_num[i, j] = terran_num[i, j] * height_num[row_idx, col_idx]
    
    # 将结果写入文件
    np.savetxt('mixed_result.txt', result_num, fmt='%.2f')

def show_mix_result(filename, png_name):
    with open(filename, 'r') as file:
        lines = file.readlines()

    data = [list(map(float, line.split())) for line in lines]

    array = np.array(data)

    array_uint8 = (array * 255).astype(np.uint8)

    plt.imshow(array_uint8, cmap='gray')
    #plt.axis('off')  # 关闭坐标轴
    plt.savefig(png_name)
    plt.show()

def calculate_new_result(input_file, output_file, kernel_size=5):
    data = np.loadtxt(input_file)
    rows, cols = data.shape
    result = np.zeros_like(data)
    
    for i in range(rows):
        for j in range(cols):
            row_start = max(0, i - kernel_size // 2)
            row_end = min(rows, i + kernel_size // 2 + 1)
            col_start = max(0, j - kernel_size // 2)
            col_end = min(cols, j + kernel_size // 2 + 1)
            
            sub_array = data[row_start:row_end, col_start:col_end]
            
            # 检查子数组的形状是否为5x5，如不是，说明有超出边界的情况，设置为0
            if sub_array.shape != (kernel_size, kernel_size):
                result[i, j] = 0
            else:
                if np.any(sub_array == 0):
                    result[i, j] = 0
                else:
                    result[i, j] = np.mean(sub_array)

    np.savetxt(output_file, result, fmt='%.2f')

#calculate_new_result('mixed_result.txt', 'result.txt')
show_mix_result('result.txt', 'result.png')
