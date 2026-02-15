import os
import sys
import time

# 1. 设置基础路径 (按照 README 规范)
qgis_base = r"D:\GIS\QGIS3.40"

# 2. 路径引导补丁：解决独立脚本环境下 ModuleNotFoundError
python_path = os.path.join(qgis_base, "apps", "qgis-ltr", "python")
plugins_path = os.path.join(python_path, "plugins")
for path in [python_path, plugins_path]:
    if path not in sys.path:
        sys.path.append(path)

# 3. DLL 加载修复
os.add_dll_directory(os.path.join(qgis_base, "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "qgis-ltr", "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "Qt5", "bin"))

# 4. 显式导入核心类 (修正点：确保 QgsRasterBandStats 被导入)
from qgis.core import (
    QgsApplication, 
    QgsRasterLayer,
    QgsRasterBandStats
)

# 5. 实例化 QGIS 应用程序
qgs = QgsApplication([], False)
qgs.initQgis()

start_time = time.time()

try:
    # 6. 初始化 Processing 框架
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()

    # 7. 加载数据
    tif_path = r"D:\contextcapture\0wenjian\20260205_total\Productions\Production_2\Production_2_DSM_merge.tif"
    raster_layer = QgsRasterLayer(tif_path, "DSM_Analysis")

    if not raster_layer.isValid():
        print(f"❌ 无法加载图层: {tif_path}")
    else:
        # 8. 修正：使用 dataProvider().bandStatistics 获取极值
        # 虽有弃用警告，但在独立脚本环境中这是获取极值最稳健的方法
        provider = raster_layer.dataProvider()
        extent = raster_layer.extent()
        
        # 参数: 波段1, 统计全部指标, 范围, 采样规模(0为全量统计)
        stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0)

        # 9. 计算海拔差
        max_val = stats.maximumValue
        min_val = stats.minimumValue
        elevation_diff = max_val - min_val

        print("-" * 45)
        print(f"✅ 分析成功！")
        print(f"🏔️ 最高点: {max_val:.3f} 米 | 🕳️ 最低点: {min_val:.3f} 米")
        print(f"📊 海拔差: {elevation_diff:.3f} 米")
        print("-" * 45)

except Exception as e:
    print(f"💥 运行异常: {e}")

finally:
    # 10. 必须执行：释放资源与显存
    qgs.exitQgis()
    print(f"⏱️ 总耗时: {time.time() - start_time:.2f} 秒")
    print("🔔 QGIS 资源已释放。")
