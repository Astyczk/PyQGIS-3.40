# PyQGIS 3.40 自动化开发库 (RTX 4060 专用)

本仓库是针对 Windows 环境下 **QGIS 3.40+** 独立脚本开发的标准化参考库。针对新版 QGIS 引入的 **Qt6** 架构进行了深度适配，确保无 DLL 冲突且资源回收机制完善。

---

## 🖥️ 环境规格 (Environment)

### 核心软件环境
* **操作系统**: Windows 11
* **QGIS 版本**: 3.40.x (最新版/LTR)
* **核心路径**: `D:\app\GIS\QGIS` (请务必确认此路径，若变动需同步修改启动脚本)
* **Python 解释器**: QGIS 内置 Python 3.12.x (`D:\app\GIS\QGIS\bin\python3.exe`)
* **图形框架**: **Qt 6.x** (注意：3.34+ 版本已从 Qt5 迁移至 Qt6)

### 硬件加速配置
* **显存设备**: NVIDIA GeForce RTX 4060 (8GB)

---

## 📐 编码强制规范 (Coding Standards)

### 1. 启动入口规范 (核心变更)
* **唯一启动方式**：禁止直接在 VS Code 中运行脚本。必须通过仓库根目录的 `vscode_qgis_V2.bat` 启动器拉起 VS Code。
* **环境变量锁定**：启动脚本必须显式设置 `PYTHONHOME` 为 `%QGIS_HOME%\apps\Python312`，以防止 `ModuleNotFoundError: No module named 'encodings'` 错误。

### 2. 逻辑骨架准则 (模板优先级)
* **母本优先原则**：参考 `/templates` 文件夹。必须识别并参考文件名中**版本号（数字）最大**的文件（如 `V2` 优于 `V1`）。
* **V2 模板核心特性**：包含 `if os.path.exists` 的 DLL 路径自动探测逻辑，兼容不同的内部文件夹命名（如 `qgis` 或 `qgis-ltr`）。

### 3. 环境初始化规范
* **动态路径注入**：严格执行 `sys.path` 补丁，包含 `plugins` 路径。
* **DLL 注入顺序**：必须先注入 `bin`，再注入 `apps\qgis\bin`，最后注入 `apps\Qt6\bin`。
* **try...finally 闭环**：强制在 `finally` 块中执行 `qgs.exitQgis()`，确保脚本结束或报错时能够正常释放 GIS 引擎锁定的文件资源。

---

## 📂 目录结构说明

### [/templates](https://www.google.com/search?q=./templates)
* **V2_template_base.py**: 当前最新的母本逻辑，支持 Qt6 和 Python 3.12 路径自动适配。

### [/production_scripts](https://www.google.com/search?q=./production_scripts)
* **[Memory_Layer_Test.py]**: 无需外部数据的环境压力测试脚本（验证内核是否唤醒）。
* **[/vector_scripts]**: 包含矢量数据属性表操作及字段计算逻辑。

---

## ⚠️ VS Code 开发避坑 (FAQ)

### 1. 虚假报错处理 (Pylance/Pylint)
* **现象**：VS Code 显示 `No name 'QgsApplication' in module 'qgis.core'`。
* **解决**：已在 `.vscode/settings.json` 中配置 `extraPaths`。**只要终端控制台输出成功，请忽略编辑器内的红线提示**。

### 2. 运行方式差异
* **正确做法**：右键点击脚本 -> **“在终端中运行 Python 文件”**。
* **错误做法**：直接点击右上角的“三角形”按钮（Run Code），这会导致环境变量丢失。

---

## ⚖️ 参考优先级
1. **最高优先级**：使用了 `os.getenv('QGIS_HOME')` 且适配了 **Qt6** 路径的 `V2` 模板。
2. **中优先级**：`/production_scripts/`。
3. **最低优先级**：包含旧路径 `D:\GIS\QGIS3.40` 或引用 `Qt5` 的旧脚本。

---

### 💡 维护提醒
如果未来 QGIS 安装路径发生变化，请第一时间更新 `.bat` 启动器中的 `QGIS_HOME` 变量，否则整个开发环境将失效。
