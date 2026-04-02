import os
import sys
import time

# =================================================================
# 1. 环境初始化 (V2 规范：路径自适应 + Qt6 适配)
# =================================================================

# 优先读取 .bat 启动器设置的环境变量，否则使用当前本地默认路径
qgis_base = os.getenv('QGIS_HOME', r"D:\app\GIS\QGIS")

# 自动识别内部文件夹名
qgis_app_path = os.path.join(qgis_base, "apps", "qgis")
if not os.path.exists(qgis_app_path):
    qgis_app_path = os.path.join(qgis_base, "apps", "qgis-ltr")

# 注入 PyQGIS 搜索路径
python_path = os.path.join(qgis_app_path, "python")
plugins_path = os.path.join(python_path, "plugins")
for p in [python_path, plugins_path]:
    if p not in sys.path:
        sys.path.append(p)

# 暴力加载 DLL (适配新版 Qt6)
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
# 2. 显式导入核心类
# =================================================================
from qgis.core import (
    QgsApplication, 
    QgsRasterLayer,
    QgsRasterBandStats
)

# 实例化 QGIS 应用程序
qgs = QgsApplication([], False)
qgs.initQgis()

# 性能感知：开始计时
start_time = time.time()

try:
    # 3. 初始化 Processing 框架 (涉及栅格计算建议初始化)
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()

    # 4. 加载数据 (路径使用随机名称代替)
    tif_path = r"D:\workspace\output_raster_77a\random_dsm_data_992.tif"
    raster_layer = QgsRasterLayer(tif_path, "DSM_Analysis")

    if not raster_layer.isValid():
        print(f"❌ 无法加载图层: {tif_path}")
    else:
        # 5. 获取极值统计 (使用数据提供者)
        # 注意：此处遵循 README API 前瞻性规范
        provider = raster_layer.dataProvider()
        extent = raster_layer.extent()
        
        # 参数: 波段1, 统计全部指标, 范围, 采样规模(0为全量统计)
        # 针对 4060 显存优化：全量统计大图时，QGIS 内核会处理分块加载
        stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0)

        # 6. 计算海拔差
        max_val = stats.maximumValue
        min_val = stats.minimumValue
        elevation_diff = max_val - min_val

        print("-" * 45)
        print(f"✅ 分析成功！图层: {raster_layer.name()}")
        print(f"🏔️ 最高点: {max_val:.3f} 米 | 🕳️ 最低点: {min_val:.3f} 米")
        print(f"📊 海拔差: {elevation_diff:.3f} 米")
        print("-" * 45)

except Exception as e:
    print(f"💥 运行异常: {e}")

finally:
    # 7. 必须执行：释放资源与显存 (核心规范)
    qgs.exitQgis()
    
    # 性能统计
    end_time = time.time()
    print(f"⏱️ 任务总耗时: {end_time - start_time:.2f} 秒")
    print("🔔 QGIS 资源已成功安全回收。")
