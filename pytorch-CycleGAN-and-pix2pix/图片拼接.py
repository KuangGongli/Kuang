from PIL import Image
import os

# 设置文件夹路径
folder_A = 'E:\mapstate\data\map_images'  # A 文件夹路径
folder_B = 'E:\mapstate\data\line_images'  # B 文件夹路径
output_folder = 'E:\mapstate\data\D'  # C 文件夹路径

# 创建 C 文件夹，如果它不存在
if not os.path.exists(output_folder):
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
    if img_a.size != (600, 600) or img_b.size != (600, 600):
        print(f"警告：图片 {img_a} 或 {img_b} 尺寸不符合要求，将跳过该对图片。")
        continue

    # 拼接图片（左右拼接）
    img_combined = Image.new('RGB', (1200, 600))
    img_combined.paste(img_a, (0, 0))  # 将 A 图片放在左边
    img_combined.paste(img_b, (600, 0))  # 将 B 图片放在右边

    # 保存拼接后的图片，命名为数字 1, 2, 3...
    output_path = os.path.join(output_folder, f'{i}.jpg')
    img_combined.save(output_path)
    print(f"已保存拼接图片：{output_path}")

print("图片拼接完成！")
