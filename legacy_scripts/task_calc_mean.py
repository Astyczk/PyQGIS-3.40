import os
import sys

# 1. 设置基础路径
qgis_base = r"D:\GIS\QGIS3.40"

# 2. 路径引导补丁：确保 Python 发现 QGIS 内部包（解决 ModuleNotFoundError）
python_path = os.path.join(qgis_base, "apps", "qgis-ltr", "python")
plugins_path = os.path.join(python_path, "plugins")
for path in [python_path, plugins_path]:
    if path not in sys.path:
        sys.path.append(path)

# 3. DLL 加载修复：确保 Windows 独立脚本环境正常运行
os.add_dll_directory(os.path.join(qgis_base, "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "qgis-ltr", "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "Qt5", "bin"))

# 导入 QGIS 核心模块
from qgis.core import (
    QgsApplication, 
    QgsVectorLayer, 
    QgsProject
)

# 4. 初始化 QGIS 资源
qgs = QgsApplication([], False)
qgs.initQgis()

# 5. 强制执行 try...finally 语法闭环
try:
    # 6. 初始化 Processing 框架（算法避坑指南要求）
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()

    # 7. 加载数据（使用原始字符串路径）
    vector_layer_path = r"D:\gis\测试数据\获嘉县村镇建筑.shp"
    layer = QgsVectorLayer(vector_layer_path, "获嘉县村镇建筑", "ogr")

    if not layer.isValid():
        print(f"❌ 错误：无法加载图层，请检查路径: {vector_layer_path}")
    else:
        # 8. 字段检索与安全检查
        fields = layer.fields()
        field_idx = fields.indexFromName("Height")
        
        if field_idx == -1:
            print("❌ 错误：在属性表中未找到 'Height' 字段（请检查大小写是否一致）。")
        else:
            total_height = 0.0
            valid_count = 0
            
            print(f"🔍 正在统计字段 'Height' 的数据...")
            
            # 9. 遍历计算逻辑
            for feature in layer.getFeatures():
                val = feature[field_idx]
                # 检查空值并尝试转换为浮点数
                if val is not None:
                    try:
                        total_height += float(val)
                        valid_count += 1
                    except (ValueError, TypeError):
                        continue # 跳过非数值坏数据
            
            # 10. 输出最终结果
            if valid_count > 0:
                average = total_height / valid_count
                print("-" * 30)
                print(f"✅ 统计完成！")
                print(f"📊 有效要素总数: {valid_count}")
                print(f"📏 Height 字段平均值: {average:.4f}")
                print("-" * 30)
            else:
                print("⚠️ 警告：该字段内没有可计算的数值数据。")

except Exception as e:
    print(f"💥 脚本执行过程中发生异常: {e}")

finally:
    # 11. 资源回收：确保脚本结束时释放显存并卸载 DLL 进程
    qgs.exitQgis()
    print("🔔 QGIS 资源已成功释放。")
