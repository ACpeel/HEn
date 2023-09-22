import cv2
import numpy as np
import os

def get_person_png(image_path:str)->None:
    '''
    抠出HEn,我们亲爱的iKUN
    '''
    # 读取原始图像
    image = cv2.imread(image_path)
    # 定义掩码
    mask = np.zeros(image.shape[:2], np.uint8)
    # 初始化背景和前景模型
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    # 定义矩形框，包含需要抠图的人形
    rect = (100, 55, 400, 533)
    # 使用GrabCut算法进行抠图
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 23, cv2.GC_INIT_WITH_RECT)
    # 将掩码中的可能的前景和肯定的前景设置为1
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    # 将原始图像与掩码相乘以获得抠图结果
    result = image * mask2[:, :, np.newaxis]

    # 保存抠图结果
    output_path = image_path.replace('.png', '_output.png')
    cv2.imwrite(output_path, result)


def check_and_add_alpha_channel(image_path: str) -> None:
    '''
    检测是否含有透明信道
    '''
    # 读取图像
    image = cv2.imread(image_path)    
    # 检查图像是否已经有Alpha通道
    if image.shape[-1] != 4:
        # 如果没有Alpha通道，添加一个全透明的Alpha通道
        image_with_alpha = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        # 保存带有Alpha通道的图像
        output_path = image_path.replace('.png', '_AC.png')
        cv2.imwrite(output_path, image_with_alpha)
    else:
        output_path = image_path.replace('.png', '_AC.png')
        cv2.imwrite(output_path, image_with_alpha)
    

def black_to_transparent(image_path: str, threshold: int) -> None:
    '''
    将黑色超过一定数值的转化为透明
    '''
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # 以包括Alpha通道的格式读取图像 
    if image is None:
        print(f"Error: Unable to read image from {image_path}")
        return
    # 获取图像的高度和宽度
    height, width, _ = image.shape
    # 遍历图像的每个像素
    for y in range(height):
        for x in range(width):
            # 获取像素的RGB通道值
            r, g, b, a = image[y, x]

            # 如果RGB通道的值都低于阈值，则将Alpha通道值设为0（变为透明）
            if r <= threshold and g <= threshold and b <= threshold:
                image[y, x, 3] = 0  # 将Alpha通道设为0

    # 保存处理后的图像
    output_path = image_path.replace('.png', '_transparent.png')
    cv2.imwrite(output_path, image)

def clear_cache(path:str)->None:
    for i in range(1,8):
        image_path_1 =f'{path}{i}_output.png'
        image_path_2 =f'{path}{i}_output_AC.png'
        if os.path.exists(image_path_1) and os.path.exists(image_path_2):
            os.remove(image_path_1)
            os.remove(image_path_2)
            print(f'del {image_path_1} , {image_path_2}')
        else:
            print(f'{image_path_1},{image_path_2} Not Found')
    for i in range(1, 8):
        old_image_path = f'{path}{i}_output_AC_transparent.png'
        new_image_path = f'{path}{i}_res.png'  # 设置新的文件名

        if os.path.exists(old_image_path):
            os.rename(old_image_path, new_image_path)

if __name__=="__main__":
    path = './imgs_HEn/'
    for i in range(1, 8):
        image_path = f'{path}{i}.png'
        get_person_png(image_path)
        print(f"{i}.png Scratched HEn!")
    for i in range(1,8):
        image_path = f'{path}{i}_output.png'
        check_and_add_alpha_channel(image_path) 
        print(f"{i}.png Alpha_Channel OK!") 
    for i in range(1,8):
        image_path = f'{path}{i}_output_AC.png'
        black_to_transparent(image_path,30)
        print(f"{i}.png Processed!")
    clear_cache(path)
    

        