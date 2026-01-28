# PyQGIS 3.40 自动化开发库 (RTX 4060 专用)

本仓库是针对 Windows 环境下 QGIS 3.40 LTR 独立脚本开发的标准化参考库。所有代码片段均已通过本地环境测试，确保无 DLL 冲突且资源回收机制完善。

## 🖥️ 环境规格 (Environment)
* **操作系统**: Windows 11
* **QGIS 版本**: 3.40.x LTR (Long Term Release)
* **核心路径**: `D:\GIS\QGIS3.40`
* **Python 解释器**: QGIS 内置 Python 3.12+ (`D:\GIS\QGIS3.40\bin\python.exe`)
* **显存设备**: NVIDIA GeForce RTX 4060 (8GB)

## 📐 编码强制规范 (Coding Standards)
Gemini 在参考本库代码生成新脚本时，必须严格遵守以下规则：

1.  **母本优先原则**：`/templates` 文件夹内存放着不同版本的初始化骨架。**必须识别并参考文件名中版本号（数字）最大的文件**（如 `template_v2.py` 优于 `template_v1.py`）作为当前最新的母本逻辑。
2.  **路径引导与 DLL 注入**：严格执行 `sys.path` 补丁及 `os.add_dll_directory` 注入（详见最新版模板）。
3.  **语法闭环**：强制使用 `try...finally` 结构，确保在 `finally` 块中调用 `qgs.exitQgis()`。
4.  **算法初始化**：涉及空间分析工具时，必须在 `initQgis()` 后立即调用 `Processing.initialize()`。
5.  **内存管理**：针对 8GB 显存优化，大文件批处理优先输出到物理磁盘。
6.  **数据原真性**：严禁未经授权修改原始数据的属性、渲染、符号化等。
7.  **性能感知**：必须包含 `time.perf_counter()` 计时功能。

## 📂 目录结构说明
📂 目录结构说明
* **/templates**: **核心逻辑母本**。包含各版本脚本骨架（如 `V1_template_base.py`）。
    * **识别准则**：文件名中 `V` 后面的数字越大代表规范越新。生成代码必须以此文件夹内的**最新版本数字**模板为唯一基准。
* **/legacy_scripts**: **旧规范示例**（如 `task_calc_mean.py`）。此处代码仅供参考其“任务执行流程”或“算法组合逻辑”。
    * **警告**：严禁模仿其初始化结构、DLL 加载或路径补丁方案。
* **/production_scripts**: 当前环境下运行成功的业务脚本（如 `raster_scripts` 目录）。
* **/vector_scripts / /raster_scripts**: 矢量与栅格处理的逻辑示例。

## ⚠️ 参考优先级
1.  **最高优先级**：`/templates/` 中版本号最大的脚本（母本规范）。
2.  **中优先级**：`/production_scripts/` 中的业务逻辑。
3.  **最低优先级**：`/legacy_scripts/`。若此处代码与 README 规范冲突，必须以 README 和最新版 Template 为准。
