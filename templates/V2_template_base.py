import os
import sys
import time

# =================================================================
# 1. 环境初始化 (V2 规范：路径自适应 + 环境注入)
# =================================================================
# 优先读取 .bat 启动器设置的环境变量，否则使用默认路径
qgis_base = os.getenv('QGIS_HOME', r"D:\app\GIS\QGIS")

# 自动识别内部文件夹 (兼容 qgis 与 qgis-ltr)
qgis_app_path = os.path.join(qgis_base, "apps", "qgis")
if not os.path.exists(qgis_app_path):
    qgis_app_path = os.path.join(qgis_base, "apps", "qgis-ltr")

# =================================================================
# 2. 路径引导补丁 (解决 ModuleNotFoundError)
# =================================================================
python_path = os.path.join(qgis_app_path, "python")
plugins_path = os.path.join(python_path, "plugins")
for path in [python_path, plugins_path]:
    if path not in sys.path:
        sys.path.append(path)

# =================================================================
# 3. DLL 加载修复 (针对 QGIS 3.40 / Qt6 架构优化)
# =================================================================
# 注入顺序：bin -> qgis_bin -> Qt6_bin
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
# 4. 显式导入核心类 (规范：防止运行时 NameError)
# =================================================================
from qgis.core import (
    QgsApplication, 
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsRasterBandStats,
    QgsCoordinateReferenceSystem
)

# =================================================================
# 5. 实例化 QGIS 应用程序
# =================================================================
# [注意] VS Code 提示 "无法解析导入 processing" 为虚假报错，请通过 .bat 启动以消除
try:
    import processing
    from processing.core.Processing import Processing
except ImportError:
    print("❌ 核心组件加载失败！请确保通过 .bat 脚本启动 VS Code。")
    sys.exit(1)

# GUI 参数设为 False 表示非 GUI 独立脚本运行
qgs = QgsApplication([], False)
qgs.initQgis()

# 性能感知：任务计时开始 (使用高精度计时器)
start_perf = time.perf_counter()

# =================================================================
# 6. 强制语法闭环 (try...finally 结构)
# =================================================================
try:
    # 必须在此处初始化算法框架 (Processing 避坑关键)
    Processing.initialize()
    
    # -------------------------------------------------------------
    # --- 业务逻辑开始 (Business Logic Start) ---
    # -------------------------------------------------------------
    
    print(f"✅ QGIS 3.40 (Qt6) 独立脚本环境就绪！")
    print(f"📍 当前工作路径: {os.getcwd()}")
    
    # 示例：创建内存图层进行压力测试
    # layer = QgsVectorLayer("Point?crs=EPSG:4326", "Test_Layer", "memory")
    # if layer.isValid(): print("🚀 内核响应正常")

    # -------------------------------------------------------------
    # --- 业务逻辑结束 (Business Logic End) ---
    # -------------------------------------------------------------

except Exception as e:
    print(f"💥 运行过程中发生异常: {e}")

finally:
    # =============================================================
    # 7. 资源回收 (RTX 4060 显存释放与 DLL 卸载)
    # =============================================================
    qgs.exitQgis()
    
    # 性能感知：输出耗时
    end_perf = time.perf_counter()
    duration = end_perf - start_perf
    print("-" * 35)
    print(f"⏱️ 任务总耗时: {duration:.4f} 秒")
    print("🔔 QGIS 资源已成功释放。")
