<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen.svg" alt="Dependencies">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README-zh-CN.md">简体中文</a> | 
  <a href="README-zh-TW.md">繁體中文</a>
</p>

<h1 align="center">🔄 RenameFlow</h1>

<p align="center">
  <b>轻量级批量文件重命名工具</b><br>
  <sub>零依赖 · 跨平台 · 安全可靠 · 功能强大</sub>
</p>

---

## 🎉 项目介绍

**RenameFlow** 是一款轻量级的命令行批量文件重命名工具，专为开发者和普通用户设计。它能够快速、安全地批量重命名文件和目录，支持多种重命名模式，所有操作默认预览，确保数据安全。

### 💡 灵感来源

在日常开发和管理文件时，经常需要批量重命名大量文件。现有的工具要么功能复杂难以使用，要么需要安装大量依赖。RenameFlow 的诞生就是为了解决这个问题——**零依赖、开箱即用、功能强大**。

### ✨ 自研差异化亮点

- 🚀 **零依赖设计** - 仅使用 Python 标准库，无需安装任何第三方包
- 👀 **安全第一** - 默认预览模式，所有操作先预览后执行
- ↩️ **支持撤销** - 内置历史记录，可随时撤销最近的操作
- 🎨 **交互式模式** - 提供友好的交互式界面，新手也能轻松使用
- 🌏 **中文友好** - 完善的中文支持和彩色输出

---

## ✨ 核心特性

### 🔧 多种重命名模式

| 模式 | 说明 | 示例 |
|------|------|------|
| **replace** | 字符串替换 | `old_file.txt` → `new_file.txt` |
| **regex** | 正则表达式 | `IMG_001.jpg` → `PHOTO_001.jpg` |
| **sequence** | 序号命名 | `file.txt` → `photo_001.txt` |
| **case** | 大小写转换 | `FileName.txt` → `filename.txt` |
| **prefix** | 添加前缀 | `file.txt` → `IMG_file.txt` |
| **suffix** | 添加后缀 | `file.txt` → `file_backup.txt` |
| **trim** | 删除字符 | `001file.txt` → `file.txt` |
| **date** | 日期命名 | `file.txt` → `20250508_001.txt` |
| **extension** | 扩展名修改 | `file.txt` → `file.md` |
| **csv** | CSV批量重命名 | 根据CSV映射批量重命名 |

### 🛡️ 安全特性

- ✅ **默认预览** - 所有操作默认为预览模式，确认无误后再执行
- ✅ **冲突检测** - 自动检测文件名冲突，避免覆盖
- ✅ **备份支持** - 可选择在重命名前创建备份文件
- ✅ **撤销功能** - 支持撤销最近的重命名操作

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8 或更高版本
- 无需任何第三方依赖

### 📦 安装方式

**方式一：直接下载（推荐）**
```bash
# 下载脚本
wget https://raw.githubusercontent.com/gitstq/RenameFlow/main/renameflow.py

# 添加执行权限
chmod +x renameflow.py

# 运行
python renameflow.py --help
```

**方式二：pip 安装**
```bash
pip install renameflow
```

**方式三：从源码安装**
```bash
git clone https://github.com/gitstq/RenameFlow.git
cd RenameFlow
pip install -e .
```

### 🎯 基本使用

```bash
# 查看帮助
renameflow --help

# 启动交互式模式
renameflow interactive

# 字符串替换（预览模式）
renameflow replace /path/to/files "old" "new"

# 执行实际替换
renameflow replace /path/to/files "old" "new" -e

# 正则表达式重命名
renameflow regex /path/to/files "\d{4}" "2024" -e

# 序号命名
renameflow sequence /path/to/files --prefix "photo_" --start 1 --padding 4 -e

# 大小写转换
renameflow case /path/to/files --type lower -e

# 添加前缀
renameflow prefix /path/to/files "IMG_" -e

# 添加后缀
renameflow suffix /path/to/files "_backup" -e

# 撤销最近操作
renameflow undo
```

---

## 📖 详细使用指南

### 🔧 重命名模式详解

#### 1️⃣ 字符串替换 (replace)

最简单的重命名方式，将文件名中的指定字符串替换为新字符串。

```bash
# 将所有文件名中的 "draft" 替换为 "final"
renameflow replace ./documents "draft" "final"

# 递归处理子目录
renameflow replace ./documents "draft" "final" -r

# 执行实际替换
renameflow replace ./documents "draft" "final" -e
```

#### 2️⃣ 正则表达式 (regex)

使用正则表达式进行复杂的模式匹配和替换。

```bash
# 将文件名中的日期格式从 YYYY-MM-DD 改为 YYYYMMDD
renameflow regex ./photos "(\d{4})-(\d{2})-(\d{2})" "\1\2\3" -e

# 移除文件名中的特殊字符
renameflow regex ./files "[^\w\-.]" "" -e
```

#### 3️⃣ 序号命名 (sequence)

按顺序编号重命名文件。

```bash
# 将文件重命名为 photo_001.jpg, photo_002.jpg, ...
renameflow sequence ./photos --prefix "photo_" --start 1 --padding 3 -e

# 从 100 开始编号，使用 5 位数字
renameflow sequence ./data --prefix "data_" --start 100 --padding 5 -e
```

#### 4️⃣ 大小写转换 (case)

支持多种大小写转换模式：

| 类型 | 说明 | 示例 |
|------|------|------|
| `upper` | 全大写 | `FileName` → `FILENAME` |
| `lower` | 全小写 | `FileName` → `filename` |
| `title` | 首字母大写 | `filename` → `Filename` |
| `camel` | 驼峰命名 | `file_name` → `fileName` |
| `snake` | 蛇形命名 | `FileName` → `file_name` |
| `kebab` | 短横线命名 | `FileName` → `file-name` |

```bash
# 转换为小写
renameflow case ./files --type lower -e

# 转换为蛇形命名
renameflow case ./files --type snake -e
```

#### 5️⃣ CSV 批量重命名 (csv)

通过 CSV 文件定义重命名映射。

CSV 文件格式：
```csv
old_name.txt,new_name.txt
draft_v1.doc,final_v1.doc
image_001.jpg,photo_001.jpg
```

```bash
renameflow csv ./files --csv mapping.csv -e
```

### 🎨 交互式模式

对于不熟悉命令行的用户，可以使用交互式模式：

```bash
renameflow interactive
```

系统会逐步引导您：
1. 选择目标路径
2. 选择重命名模式
3. 输入相关参数
4. 预览更改
5. 确认执行

---

## 💡 设计思路与迭代规划

### 🏗️ 设计理念

RenameFlow 的设计遵循以下原则：

1. **零依赖优先** - 使用 Python 标准库，确保安装简单、兼容性好
2. **安全第一** - 默认预览模式，避免误操作
3. **功能完整** - 覆盖常见的批量重命名场景
4. **易于使用** - 提供交互式模式和详细的帮助文档

### 📅 后续迭代计划

- [ ] 支持 EXIF 元数据变量（照片拍摄日期等）
- [ ] 支持 ID3 标签变量（音频文件信息）
- [ ] 添加文件预览功能
- [ ] 支持更多文件属性变量
- [ ] 添加配置文件支持
- [ ] 开发 GUI 版本

### 🤝 社区贡献

欢迎提交 Issue 和 Pull Request！

---

## 📦 打包与部署指南

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/RenameFlow.git
cd RenameFlow

# 安装开发依赖
pip install -e .

# 构建分发包
pip install build
python -m build
```

### 跨平台兼容性

RenameFlow 支持以下平台：
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (所有主流发行版)

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 提交 Issue

- 🐛 Bug 报告：请详细描述问题、复现步骤和环境信息
- 💡 功能建议：请说明使用场景和预期效果

### 提交 PR

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 开源协议说明

本项目采用 [MIT License](LICENSE) 开源协议。

您可以自由地：
- ✅ 商业使用
- ✅ 修改代码
- ✅ 分发代码
- ✅ 私人使用

唯一要求是保留版权声明。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">RenameFlow Team</a>
</p>
