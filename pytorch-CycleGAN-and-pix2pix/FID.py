import os
import shutil
import torch
from pytorch_fid import fid_score

def calculate_fid(real_images_path, fake_images_path):
    # 计算FID
    fid_value = fid_score.calculate_fid_given_paths(
        [real_images_path, fake_images_path],
        batch_size=50,
        device='cuda',
        dims=2048
        # num_workers=0  # 禁用多进程数据加载
    )
    print(f"FID值: {fid_value}")


if __name__ == '__main__':
    # 输入文件夹路径
    input_folder = r'D:\研究生学习\论文\虚拟地形生成的论文\pytorch-CycleGAN-and-pix2pix\pytorch-CycleGAN-and-pix2pix\results\mymap_pix2pix\test_latest\images'  # 替换成你的文件夹路径

    # 创建两个输出文件夹，如果它们不存在
    output_fake_folder = os.path.join(input_folder, 'generated_images')
    output_real_folder = os.path.join(input_folder, 'real_images')

    os.makedirs(output_fake_folder, exist_ok=True)
    os.makedirs(output_real_folder, exist_ok=True)

    # 分类图片：将fake_B和real_B图片分别移动到相应的文件夹
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        if os.path.isfile(file_path):
            if filename.endswith('fake_B.png'):
                # 移动到生成图像文件夹
                shutil.move(file_path, os.path.join(output_fake_folder, filename))
            elif filename.endswith('real_B.png'):
                # 移动到真实图像文件夹
                shutil.move(file_path, os.path.join(output_real_folder, filename))

    print("图片分类完成")
    # 输入文件夹路径
    real_images_path = r'D:\研究生学习\论文\虚拟地形生成的论文\pytorch-CycleGAN-and-pix2pix\pytorch-CycleGAN-and-pix2pix\results\mymap_pix2pix\test_latest\images\real_images'  # 替换为你的真实图像路径
    fake_images_path = r'D:\研究生学习\论文\虚拟地形生成的论文\pytorch-CycleGAN-and-pix2pix\pytorch-CycleGAN-and-pix2pix\results\mymap_pix2pix\test_latest\images\generated_images'  # 替换为你的生成图像路径

    # 检查路径是否正确并且文件夹不为空
    if len(os.listdir(real_images_path)) == 0:
        raise ValueError("The real images folder is empty!")
    if len(os.listdir(fake_images_path)) == 0:
        raise ValueError("The fake images folder is empty!")

    print("Real images path:", real_images_path)
    print("Fake images path:", fake_images_path)

    # 计算FID
    calculate_fid(real_images_path, fake_images_path)

