import os
import sys
import time

# =================================================================
# 1. 环境固定配置 (遵循 README 规范)
# =================================================================
qgis_base = r"D:\GIS\QGIS3.40"

# =================================================================
# 2. 路径引导补丁 (解决 ModuleNotFoundError)
# =================================================================
# 必须包含 plugins 路径，否则无法导入 processing
python_path = os.path.join(qgis_base, "apps", "qgis-ltr", "python")
plugins_path = os.path.join(python_path, "plugins")
for path in [python_path, plugins_path]:
    if path not in sys.path:
        sys.path.append(path)

# =================================================================
# 3. DLL 加载修复 (解决 Windows 独立环境加载错误)
# =================================================================
os.add_dll_directory(os.path.join(qgis_base, "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "qgis-ltr", "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "Qt5", "bin"))

# =================================================================
# 4. 显式导入核心类 (规范 5：防止 NameError)
# =================================================================
from qgis.core import (
    QgsApplication, 
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsRasterBandStats,  # 栅格统计枚举
    QgsCoordinateReferenceSystem
)

# =================================================================
# 5. 实例化 QGIS 应用程序
# =================================================================
# [注意] VS Code 可能会提示 "无法解析导入 processing"，请忽略此虚假报错
try:
    import processing
    from processing.core.Processing import Processing
except ImportError:
    # 冗余检查：确保路径补丁生效
    print("❌ 路径补丁未生效，请检查 qgis_base 路径是否正确。")
    sys.exit(1)

qgs = QgsApplication([], False)
qgs.initQgis()

# 性能感知：任务计时开始
start_perf = time.perf_counter()

# =================================================================
# 6. 强制语法闭环 (规范 3)
# =================================================================
try:
    # 必须在此处初始化算法框架
    Processing.initialize()
    
    # -------------------------------------------------------------
    # --- 业务逻辑开始 (Business Logic Start) ---
    # 示例：print("✅ QGIS 3.40 独立脚本环境就绪！")
    
    # --- 业务逻辑结束 (Business Logic End) ---
    # -------------------------------------------------------------

except Exception as e:
    print(f"💥 运行过程中发生错误: {e}")

finally:
    # =============================================================
    # 7. 资源回收 (RTX 4060 显存释放)
    # =============================================================
    qgs.exitQgis()
    
    # 性能感知：输出耗时 (规范 9)
    end_perf = time.perf_counter()
    print("-" * 30)
    print(f"⏱️ 任务总耗时: {end_perf - start_perf:.4f} 秒")
    print("🔔 QGIS 资源已成功释放。")
