PyQGIS 3.40 自动化开发库 (RTX 4060 专用)
本仓库是针对 Windows 环境下 QGIS 3.40 LTR 独立脚本开发的标准化参考库。所有代码片段均已通过本地环境测试，确保无 DLL 冲突且资源回收机制完善。

🖥️ 环境规格 (Environment)
操作系统: Windows 11

QGIS 版本: 3.40.x LTR (Long Term Release)

核心路径: D:\GIS\QGIS3.40

Python 解释器: QGIS 内置 Python 3.12+ (D:\GIS\QGIS3.40\bin\python.exe)

显存设备: NVIDIA GeForce RTX 4060 (8GB)

📐 编码强制规范 (Coding Standards)
Gemini 在参考本库代码生成新脚本时，必须严格遵守以下规则：

路径引导优先: 所有脚本必须包含 sys.path 补丁，以指向 apps\qgis-ltr\python\plugins 目录，否则 import processing 会失败。

DLL 注入: 必须使用 os.add_dll_directory 注入 bin、apps\qgis-ltr\bin 和 apps\Qt5\bin 三个路径。

语法闭环: 强制使用 try...finally 结构。无论业务逻辑是否成功，必须在 finally 块中调用 qgs.exitQgis() 以释放显存。

算法初始化: 涉及空间分析工具时，必须在 initQgis() 后立即调用 Processing.initialize()。

内存管理: 针对 8GB 显存优化，批量处理大文件时，优先将 OUTPUT 参数设为物理磁盘路径而非 memory: 图层。

数据原真性原则：严禁在未获得任务明确授权的情况下修改原始数据的任何属性（包括像素值、颜色梯度、符号化设定或最大/最小值）。

性能感知：所有业务逻辑必须包含计时功能，使用 time.perf_counter() 记录并输出任务耗时，确保开发过程可感知。

📂 目录结构说明
/templates: 存放独立脚本的基础初始化骨架 (template_base.py)。

/vector_scripts: 属性统计、矢量裁剪、缓冲区等矢量数据处理示例。

/raster_scripts: 地形分析、栅格计算、重采样等栅格处理示例。

/symbology: 图层渲染、标注设置及地图自动化导出示例。

💡 为什么这样写 README 对你有好处？
消除歧义：当你问 Gem“帮我写个脚本”时，Gem 会先读 README。看到 D:\GIS\QGIS3.40，它就不会再写出 C:\Program Files 这种错误路径了。

强化记忆：明确提到 RTX 4060，会让 Gem 在写复杂的地形分析脚本时，更倾向于使用节省显存的写法（如直接写盘而不是暂存内存）。

自动修复：它解释了为什么需要 sys.path 补丁，这能防止 Gem 以后为了偷懒而删掉那几行关键代码。

⚠️ 参考优先级：生成代码时，请以 /templates 中最新版本的模板和最近在 /production_scripts 中更新的脚本为最高准则。若 /legacy_scripts 中的代码与 README 规范冲突，必须以 README 为准。

legacy_scripts 往期运行成功的代码版本

production_scripts 最新版本运行成功的代码版本

templates 各个版本的代码模板（随时更新，同最新版本的代码）
