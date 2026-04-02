import os
import sys
import time

# =================================================================
# 1. 环境初始化与路径引导 (V2 规范：路径自适应 + DLL 注入)
# =================================================================

# 优先从环境变量获取路径，若未设置则使用当前本地路径
qgis_base = os.getenv('QGIS_HOME', r"D:\app\GIS\QGIS")

# 自动识别内部文件夹 (兼容 qgis 与 qgis-ltr)
qgis_app_path = os.path.join(qgis_base, "apps", "qgis")
if not os.path.exists(qgis_app_path):
    qgis_app_path = os.path.join(qgis_base, "apps", "qgis-ltr")

# 注入 PyQGIS 搜索路径
python_path = os.path.join(qgis_app_path, "python")
plugins_path = os.path.join(python_path, "plugins")
for p in [python_path, plugins_path]:
    if p not in sys.path:
        sys.path.append(p)

# 暴力加载 DLL (针对 Qt6 架构优化)
dll_folders = [
    "bin", 
    os.path.join("apps", "qgis", "bin"), 
    os.path.join("apps", "Qt6", "bin")
]
for folder in dll_folders:
    full_path = os.path.join(qgis_base, folder)
    if os.path.exists(full_path):
        os.add_dll_directory(full_path)

# =================================================================
# 2. 导入 QGIS 核心模块 (显式导入增强)
# =================================================================
from qgis.core import (
    QgsApplication, 
    QgsVectorLayer, 
    QgsProject,
    QgsFeatureRequest
)

# 初始化 QGIS 资源
qgs = QgsApplication([], False)
qgs.initQgis()

# =================================================================
# 3. 业务逻辑 (try...finally 闭环)
# =================================================================
start_time = time.time() # 性能感知：开始计时

try:
    # 初始化 Processing 框架
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()

    # 加载数据 (路径使用随机名称代替)
    vector_layer_path = r"D:\data\project_x\random_sample_data_v9.shp"
    layer = QgsVectorLayer(vector_layer_path, "Random_Test_Layer", "ogr")

    if not layer.isValid():
        print(f"❌ 错误：无法加载图层，请检查路径: {vector_layer_path}")
    else:
        print(f"✅ 图层已唤醒: {layer.name()}")
        
        # 字段检索与安全检查
        fields = layer.fields()
        target_field = "Height" # 假设字段名
        field_idx = fields.indexFromName(target_field)
        
        if field_idx == -1:
            print(f"❌ 错误：未找到字段 '{target_field}'。")
        else:
            total_val = 0.0
            valid_count = 0
            
            # 使用 Request 仅获取必要字段，优化内存性能
            request = QgsFeatureRequest().setSubsetOfAttributes([field_idx], fields)
            
            for feature in layer.getFeatures(request):
                val = feature[field_idx]
                if val is not None:
                    try:
                        total_val += float(val)
                        valid_count += 1
                    except (ValueError, TypeError):
                        continue 

            # 输出最终结果
            if valid_count > 0:
                average = total_val / valid_count
                print("-" * 35)
                print(f"📊 统计完成！有效要素: {valid_count}")
                print(f"📏 {target_field} 字段平均值: {average:.4f}")
            else:
                print("⚠️ 警告：该字段内没有可计算的数值数据。")

except Exception as e:
    print(f"💥 脚本执行过程中发生异常: {e}")

finally:
    # 资源回收与耗时统计
    qgs.exitQgis()
    end_time = time.time()
    print("-" * 35)
    print(f"⏱️ 任务总耗时: {end_time - start_time:.2f} 秒")
    print("🔔 QGIS 资源已成功释放。")
