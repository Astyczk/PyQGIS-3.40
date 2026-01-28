import os
import sys

# 1. 设置基础路径
qgis_base = r"D:\GIS\QGIS3.40"

# 2. 路径引导补丁：解决 ModuleNotFoundError
python_path = os.path.join(qgis_base, "apps", "qgis-ltr", "python")
plugins_path = os.path.join(python_path, "plugins")
for path in [python_path, plugins_path]:
    if path not in sys.path:
        sys.path.append(path)

# 3. DLL 加载修复：解决 Windows 环境 DLL 加载错误
os.add_dll_directory(os.path.join(qgis_base, "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "qgis-ltr", "bin"))
os.add_dll_directory(os.path.join(qgis_base, "apps", "Qt5", "bin"))

# 4. 导入核心类（必须在 DLL 修复之后）
from qgis.core import QgsApplication, QgsProject
import processing
from processing.core.Processing import Processing

# 5. 实例化 QGIS 应用程序
qgs = QgsApplication([], False)
qgs.initQgis()

# 6. 强制语法闭环：确保资源始终能被释放
try:
    # 必须在此处初始化算法框架
    Processing.initialize()
    
    # --- 业务逻辑开始 ---
    # 示例：print("QGIS 独立脚本环境就绪！")
    # --- 业务逻辑结束 ---

except Exception as e:
    print(f"❌ 运行过程中发生错误: {e}")

finally:
    # 7. 退出 QGIS，释放 RTX 4060 显存与 DLL 进程
    qgs.exitQgis()
