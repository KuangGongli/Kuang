import arcpy
from arcpy.sa import *

# 设置工作环境
arcpy.env.workspace = "C:/GIS_data"
arcpy.env.overwriteOutput = True  # 允许覆盖输出文件

# 输入栅格数据集
input_raster = "input_raster.tif"  # 替换为你的栅格数据文件路径

# 定义输出文件路径
output_raster = "C:/GIS_data/output_focalstat.tif"  # 输出结果路径

# 设置邻域大小（高度和宽度为10）
neighborhood = NbrRectangle(10, 10, "CELL")  # "CELL"表示单位为栅格单元

# 执行焦点统计操作
# 这里选择了"MEAN"作为统计方法，可以根据需要选择"MAXIMUM"、"MINIMUM"等
focal_stat_raster = FocalStatistics(input_raster, neighborhood, "MEAN")

# 保存输出结果
focal_stat_raster.save(output_raster)

print(f"焦点统计完成，结果保存在: {output_raster}")
