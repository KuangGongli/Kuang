import os
from PIL import Image

# 禁用最大像素限制
Image.MAX_IMAGE_PIXELS = None  # 禁用最大像素限制


def crop_center(image, target_size=9300):
    # 获取原始图像的宽高
    width, height = image.size

    # 计算裁剪区域的左上角和右下角坐标
    left = (width - target_size) / 2
    upper = (height - target_size) / 2
    right = (width + target_size) / 2
    lower = (height + target_size) / 2

    # 裁剪图像
    cropped_image = image.crop((left, upper, right, lower))
    return cropped_image


def process_images(input_folder, target_size=9300):
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 只处理图片文件，常见的图片格式
        if filename.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
            # 获取图片的完整路径
            image_path = os.path.join(input_folder, filename)

            try:
                # 打开图像
                with Image.open(image_path) as image:
                    # 只有在图像尺寸大于裁剪尺寸时才进行裁剪
                    if image.width >= target_size and image.height >= target_size:
                        # 从中心裁剪图像
                        cropped_image = crop_center(image, target_size)

                        # 将裁剪后的图像直接保存回原文件路径
                        cropped_image.save(image_path)
                        print(f"图像 '{filename}' 已成功裁剪并保存")
                    else:
                        print(f"图像 '{filename}' 尺寸太小，跳过裁剪")
            except Exception as e:
                print(f"无法处理图像 '{filename}': {e}")


# 使用示例
input_folder = 'E:\mapstate\data\原图'  # 输入文件夹路径

process_images(input_folder)
