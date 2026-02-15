PyQGIS 3.40 自动化开发库 (RTX 4060 专用)
本仓库是针对 Windows 环境下 QGIS 3.40 LTR 独立脚本开发的标准化参考库。所有代码片段均已通过本地环境测试，确保无 DLL 冲突且资源回收机制完善。

🖥️ 环境规格 (Environment)
核心软件环境
操作系统: Windows 11

QGIS 版本: 3.40.x LTR (Long Term Release)

核心路径: D:\GIS\QGIS3.40

Python 解释器: QGIS 内置 Python 3.12+ (D:\GIS\QGIS3.40\bin\python.exe)

硬件加速配置
显存设备: NVIDIA GeForce RTX 4060 (8GB)

📐 编码强制规范 (Coding Standards)
注意：Gemini 在参考本库代码生成新脚本时，必须严格遵守以下规则：

1. 逻辑骨架准则
母本优先原则：/templates 文件夹内存放着不同版本的初始化骨架。必须识别并参考文件名中版本号（数字）最大的文件（如 V2 优于 V1）作为当前最新的母本逻辑。

2. 环境初始化规范
路径引导与 DLL 注入：严格执行 sys.path 补丁（需包含 plugins 路径）及 os.add_dll_directory 注入。

算法初始化：涉及空间分析工具时，必须在 initQgis() 后立即调用 Processing.initialize()。

3. 代码健壮性与安全
语法闭环：强制使用 try...finally 结构，确保在 finally 块中调用 qgs.exitQgis() 以回收资源。

显式导入增强：严禁模糊导入。所有枚举类（如 QgsRasterBandStats）必须在 from qgis.core import ... 中显式声明，以防运行时出现 NameError。

API 前瞻性：针对 QGIS 3.40 弃用警告，栅格统计应优先评估 statistics() 方法的可行性。

4. 性能与资源管理
内存管理：针对 8GB 显存优化，大文件批处理优先输出到物理磁盘，避免使用 memory: 图层。

数据原真性：严禁未经授权修改原始数据的属性、渲染、符号化等。

性能感知：必须包含 time 模块进行耗时统计，任务结束时输出 ⏱️ 任务总耗时: X.XX 秒。

⚠️ VS Code 开发避坑 (FAQ)
虚假报错 (Pylance)
现象：由于 processing 等模块是运行阶段通过 sys.path 动态注入的，VS Code 可能会显示 无法解析导入 "processing"。

对策：只要终端控制台输出正常且脚本能运行，请忽略“问题”面板中的此类提示。严禁为了消除警告而删除脚本头部的动态路径补丁。

📂 目录结构说明
/templates
核心逻辑母本：包含各版本脚本骨架（如 V2_template_base.py）。

识别准则：文件名中 V 后面的数字越大代表规范越新。

/legacy_scripts
旧规范示例：如 task_calc_mean.py。

使用限制：仅供参考其“算法组合逻辑”，严禁模仿其初始化结构或 DLL 加载方案。

/production_scripts
当前环境下运行成功的业务脚本：

[/vector_scripts]：shp 文件属性表操作。

[/raster_scripts]：栅格数据按范围裁剪、极值统计。

⚖️ 参考优先级
最高优先级：/templates/ 中版本号最大的脚本（母本规范）。

中优先级：/production_scripts/ 中的业务逻辑。

最低优先级：/legacy_scripts/。若此处代码与最新规范冲突，必须以最新版 Template 为准。
