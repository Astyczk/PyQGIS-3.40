# PyQGIS 3.40 自动化开发库 (RTX 4060 专用)

本仓库是针对 Windows 环境下 **QGIS 3.40+** 独立脚本开发的标准化参考库。针对新版 QGIS 引入的 **Qt6** 架构进行了深度适配，确保无 DLL 冲突且资源回收机制完善。

---

## 🚀 快速开始 (Quick Start)

1. **环境检查**：确保 QGIS 安装于 `D:\app\GIS\QGIS`。若路径不同，请右键编辑 `vscode_qgis_V2.bat` 修改 `QGIS_HOME`。
2. **启动项目**：**双击**根目录下的 `vscode_qgis_V2.bat` 启动 VS Code。
3. **验证环境**：在 VS Code 中打开 `templates/V2_template_base.py`，右键选择 **“在终端中运行 Python 文件”**。若输出 `✅ QGIS 内核启动成功`，则环境配置完成。

---

## 🖥️ 环境规格 (Environment)

### 核心软件环境
* **操作系统**: Windows 11
* **QGIS 版本**: 3.40.x (最新版/LTR)
* **核心路径**: `D:\app\GIS\QGIS` 
* **Python 解释器**: QGIS 内置 Python 3.12.x (`D:\app\GIS\QGIS\bin\python3.exe`)
* **图形框架**: **Qt 6.x** (适配新版 API)

### 硬件加速配置
* **显存设备**: NVIDIA GeForce RTX 4060 (8GB) —— 建议在大数据量栅格处理时开启计时监控。

---

## 📐 编码强制规范 (Coding Standards)

### 1. 启动入口规范
* **唯一启动方式**：必须通过 `vscode_qgis_V2.bat` 注入环境变量。
* **环境变量锁定**：脚本已锁定 `PYTHONHOME`，严禁删除此设置，否则会导致 `ModuleNotFoundError: No module named 'encodings'`。

### 2. 逻辑骨架准则
* **母本优先原则**：参考 `/templates` 文件夹中版本号最大的文件（如 `V2`）。
* **V2 模板特性**：支持 `os.getenv('QGIS_HOME')` 动态探测，具备极强的路径兼容性。

### 3. 环境初始化规范
* **DLL 注入顺序**：`bin` -> `apps\qgis\bin` -> `apps\Qt6\bin` (顺序不可调换)。
* **资源闭环**：强制使用 `try...finally` 结构，确保 `qgs.exitQgis()` 永远被执行，防止显存溢出。

---

## 📂 目录结构说明

* **[/templates]**: 存放各版本初始化骨架，建议新脚本基于 `V2_template_base.py` 创建。
* **[/production_scripts]**: 
    * `Memory_Layer_Test.py`: 纯内核唤醒校验工具。
    * `/vector_scripts`: 矢量属性操作。
    * `/raster_scripts`: 栅格极值统计与裁剪。
* **[.vscode]**: 包含 `settings.json`，已配置 `extraPaths` 以消除虚假报错。

---

## ⚖️ 参考优先级
1. **最高优先级**：适配 **Qt6** 与 **Python 3.12** 路径的 `V2` 模板。
2. **中优先级**：`/production_scripts/` 下的业务逻辑。
3. **最低优先级**：包含旧路径 `D:\GIS\QGIS3.40` 或引用 `Qt5` 的旧脚本。

---

## 💡 维护提醒 (Maintenance)
* **路径迁移**：若更换电脑，只需修改 `.bat` 文件中的 `set QGIS_HOME=你的新路径`，代码无需改动。
* **依赖更新**：若 QGIS 升级导致 Python 版本变动（如 3.12 升至 3.13），需同步更新 `.bat` 中的 `PYTHONHOME` 路径。
