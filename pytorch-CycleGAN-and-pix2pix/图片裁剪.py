from PIL import Image
import os
import shutil
from natsort import natsorted  # 导入natsort库，用于自然排序
# 禁用最大像素限制
Image.MAX_IMAGE_PIXELS = None  # 禁用最大像素限制

# 裁剪函数
def crop_center(image, target_size=3000):
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

# 处理图像函数
def process_images(input_folder, output_folder, target_size=3000):
    # 检查输出文件夹是否存在，如果存在则清空该文件夹
    if os.path.exists(output_folder):
        # 删除输出文件夹及其内容
        shutil.rmtree(output_folder)

    # 重新创建输出文件夹
    os.makedirs(output_folder)

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

                        # 将裁剪后的图像保存到指定文件夹，并使用原文件名
                        output_path = os.path.join(output_folder, filename)
                        cropped_image.save(output_path)
                        print(f"图像 '{filename}' 已成功裁剪并保存到 '{output_folder}'")
                    else:
                        print(f"图像 '{filename}' 尺寸太小，跳过裁剪")
            except Exception as e:
                print(f"无法处理图像 '{filename}': {e}")

def crop_images(input_folder, output_folder_map, output_folder_other, crop_width=600, crop_height=600):
    """
    裁剪指定文件夹中的所有图片，按600x600大小裁剪，并将结果保存到不同的文件夹中。

    :param input_folder: 输入文件夹路径，包含要裁剪的原图
    :param output_folder_map: 输出文件夹，存放以"map"开头的图片
    :param output_folder_other: 输出文件夹，存放其他图片
    :param crop_width: 裁剪宽度，默认值为600
    :param crop_height: 裁剪高度，默认值为600
    """

    # 创建map输出文件夹（如果不存在的话）
    if os.path.exists(output_folder_map):
        # 删除输出文件夹及其内容
        shutil.rmtree(output_folder_map)
    # 重新创建输出文件夹
    os.makedirs(output_folder_map)

    # 创建line输出文件夹（如果不存在的话）
    if os.path.exists(output_folder_other):
        # 删除输出文件夹及其内容
        shutil.rmtree(output_folder_other)
    # 重新创建输出文件夹
    os.makedirs(output_folder_other)

    # 获取输入文件夹中的所有图片文件
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))]

    # 使用natsorted进行自然排序（确保文件按照数字大小顺序排序）
    image_files = natsorted(image_files)

    # 初始化计数器
    map_counter = 1  # 用于map开头的图片编号
    other_counter = 1  # 用于其他图片编号

    # 遍历所有图片
    for image_file in image_files:
        input_image_path = os.path.join(input_folder, image_file)

        # 打开原图
        img = Image.open(input_image_path)
        img_width, img_height = img.size

        # 根据图片名判断输出文件夹
        if image_file.lower().startswith('map'):
            image_output_folder = output_folder_map  # 以'map'开头的图片
            counter = map_counter
        else:
            image_output_folder = output_folder_other  # 其他图片
            counter = other_counter

        # 从左上角开始裁剪
        # 遍历图片，按 crop_width x crop_height 大小裁剪
        for top in range(0, img_height, crop_height):
            for left in range(0, img_width, crop_width):
                # 确保裁剪区域在图片范围内
                right = left + crop_width
                bottom = top + crop_height

                # 如果裁剪区域超出了图片的边界，跳过
                if right > img_width or bottom > img_height:
                    continue

                # 裁剪区域
                crop_box = (left, top, right, bottom)
                cropped_img = img.crop(crop_box)

                # 保存裁剪后的图片到相应的文件夹中
                cropped_img.save(os.path.join(image_output_folder, f"{counter}.jpg"))
                counter += 1  # 增加编号

        # 更新主计数器
        if image_file.lower().startswith('map'):
            map_counter = counter  # 更新map开头的图片编号
        else:
            other_counter = counter  # 更新其他图片编号

        print(f"{image_file} 裁剪完成，结果已保存在 {image_output_folder}")

    print("========================所有图片裁剪完成！===============================")



def combine_images(folder_A, folder_B, output_folder, img_size=(600, 600)):
    """
    将文件夹A和文件夹B中的同名图片左右拼接，并保存到输出文件夹C。

    :param folder_A: 文件夹A的路径
    :param folder_B: 文件夹B的路径
    :param output_folder: 输出文件夹C的路径
    :param img_size: 要求图片的尺寸，默认为(600, 600)
    """

    # 创建输出文件夹，如果它不存在
    if os.path.exists(output_folder):
        # 删除输出文件夹及其内容
        shutil.rmtree(output_folder)
    # 重新创建输出文件夹
    os.makedirs(output_folder)


    # 获取 A 文件夹中的所有图片文件名
    images_A = sorted(os.listdir(folder_A))

    # 遍历 A 文件夹中的每张图片，确保 B 文件夹中有相同名称的图片
    for i, img_a in enumerate(images_A, start=1):
        # 构建对应的 B 文件夹中图片的文件名
        img_b = img_a  # 由于图片名称一一对应，B 文件夹中的图片名称和 A 文件夹相同

        # 拼接路径
        path_a = os.path.join(folder_A, img_a)
        path_b = os.path.join(folder_B, img_b)

        # 检查 B 文件夹中是否有同名文件
        if not os.path.exists(path_b):
            print(f"警告：B 文件夹中找不到名为 {img_a} 的文件，跳过此对图片。")
            continue

        # 打开两张图片
        img_a = Image.open(path_a)
        img_b = Image.open(path_b)

        # 确保两张图片的尺寸为 600x600
        if img_a.size != img_size or img_b.size != img_size:
            print(f"警告：图片 {img_a} 或 {img_b} 尺寸不符合要求，将跳过该对图片。")
            continue

        # 拼接图片（左右拼接）
        img_combined = Image.new('RGB', (img_size[0] * 2, img_size[1]))  # 拼接后的尺寸
        img_combined.paste(img_a, (0, 0))  # 将 A 图片放在左边
        img_combined.paste(img_b, (img_size[0], 0))  # 将 B 图片放在右边

        # 保存拼接后的图片，命名为数字 1, 2, 3...
        output_path = os.path.join(output_folder, f'{i}.jpg')
        img_combined.save(output_path)
        # print(f"已保存拼接图片：{output_path}")

    print("=====================图片拼接完成！==================================")


def split_and_copy_images(source_folder, folder_A, folder_B, folder_C):
    """
    将 source_folder 中的图片按照比例分成三部分，分别复制到 folder_A, folder_B 和 folder_C 中。
    图片按顺序重命名为从1开始的数字。

    :param source_folder: 源文件夹路径
    :param folder_A: 存放前45%图片的文件夹路径
    :param folder_B: 存放中间40%图片的文件夹路径
    :param folder_C: 存放最后15%图片的文件夹路径
    """

    # 获取源文件夹中的所有图片文件
    images = sorted(os.listdir(source_folder))

    # 计算各部分图片的数量
    total_images = len(images)
    first_split = int(total_images * 0.45)
    second_split = int(total_images * 0.85)  # 中间部分的结束位置

    # 创建目标文件夹，如果它们不存在，或者清空现有文件夹
    for folder in [folder_A, folder_B, folder_C]:
        if os.path.exists(folder):
            # 如果文件夹已存在，清空文件夹
            shutil.rmtree(folder)
        # 重新创建文件夹
        os.makedirs(folder)

    # 复制前45%的图片到 folder_A
    for i, img in enumerate(images[:first_split], start=1):
        img_path = os.path.join(source_folder, img)
        dest_path = os.path.join(folder_A, f"{i}.jpg")
        shutil.copy(img_path, dest_path)
    print(f"{folder_A}图片已复制完成")

    # 复制中间40%的图片到 folder_B
    for i, img in enumerate(images[first_split:second_split], start=1):
        img_path = os.path.join(source_folder, img)
        dest_path = os.path.join(folder_B, f"{i}.jpg")
        shutil.copy(img_path, dest_path)
    print(f"{folder_B}图片已复制完成")

    # 复制最后15%的图片到 folder_C
    for i, img in enumerate(images[second_split:], start=1):
        img_path = os.path.join(source_folder, img)
        dest_path = os.path.join(folder_C, f"{i}.jpg")
        shutil.copy(img_path, dest_path)
    print(f"{folder_C}图片已复制完成")

    print("=============================图片分割和复制完成！================================")

# 使用示例


# 使用示例
input_folder = "E:\mapstate\山脊线数据"  # 输入文件夹路径
output_folder = "E:\mapstate\data\原图"  # 输出文件夹路径

output_folder_map = r'E:\mapstate\data\map_images'  # 输出文件夹（map开头的图片）
output_folder_line = r'E:\mapstate\data\line_images'  # 输出文件夹（其他图片）
pinjie_output_folder = r'E:\mapstate\data\pinjie'  #拼接图保存路径
folder_A = r'D:\研究生学习\论文\虚拟地形生成的论文\pytorch-CycleGAN-and-pix2pix\pytorch-CycleGAN-and-pix2pix\datasets\mymap\train'  # 存放前45%图片的文件夹
folder_B = r'D:\研究生学习\论文\虚拟地形生成的论文\pytorch-CycleGAN-and-pix2pix\pytorch-CycleGAN-and-pix2pix\datasets\mymap\val'  # 存放中间40%图片的文件夹
folder_C = r'D:\研究生学习\论文\虚拟地形生成的论文\pytorch-CycleGAN-and-pix2pix\pytorch-CycleGAN-and-pix2pix\datasets\mymap\test'  # 存放最后15%图片的文件夹

process_images(input_folder, output_folder, target_size=3000)    ###给定arcmap原图，从中心点开始裁剪，裁剪为9300*9300大小的正方形图
crop_images(output_folder, output_folder_map, output_folder_line, crop_width=600, crop_height=600)   ###将正方图裁剪为300*300的小图
combine_images(output_folder_map, output_folder_line, pinjie_output_folder)    ###将地图和山脊线图拼接
split_and_copy_images(pinjie_output_folder, folder_A, folder_B, folder_C)