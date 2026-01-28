import os
import sys
import time  # 新增：用于计时

# 1. 设置基础路径
qgis_base = r"D:\GIS\QGIS3.40"

# 2. 路径引导补丁
python_path = os.path.join(qgis_base, "apps", "qgis-ltr", "python")
plugins_path = os.path.join(python_path, "plugins")
for path in [python_path, plugins_path]:
    if path not in sys.path:
        sys.path.append(path)

# 3. DLL 加载修复
os.add_dll_directory(os.path.join(qgis_base, "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "qgis-ltr", "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "Qt5", "bin"))

from qgis.core import QgsApplication, QgsProject
import processing
from processing.core.Processing import Processing

qgs = QgsApplication([], False)
qgs.initQgis()

try:
    # 记录起始时间
    start_time = time.perf_counter() 
    
    Processing.initialize()
    
    # --- 业务逻辑开始 ---
    print("🔍 正在启动任务...")
    
    # [此处放置你的业务代码，严禁擅改原始数据样式]
    
    # --- 业务逻辑结束 ---

    # 输出耗时统计
    elapsed = time.perf_counter() - start_time
    print("-" * 30)
    print(f"✅ 任务处理完成！耗时: {elapsed:.2f} 秒")
    print("-" * 30)

except Exception as e:
    print(f"❌ 运行过程中发生错误: {e}")

finally:
    qgs.exitQgis()
    print("🔔 QGIS 资源已成功释放。")
