import os

# 指定文件夹路径
folder_path = r'E:\mapstate\山脊线数据'  # 修改为你的文件夹路径

# 获取文件夹中的所有文件
files = os.listdir(folder_path)

# 重命名文件
for i in range(1, 9):  # 遍历 yunnan1 到 yunnan8
    old_name = f'yunnan{i}'  # 原始文件名
    new_name = f'line{i}'  # 新的文件名

    # 找到匹配的文件并重命名
    for file in files:
        if old_name in file:
            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, file.replace(old_name, new_name))

            # 重命名
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{file}' to '{file.replace(old_name, new_name)}'")
