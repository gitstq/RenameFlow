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
  <b>Lightweight Batch File Renaming Tool</b><br>
  <sub>Zero Dependencies · Cross-Platform · Safe & Reliable · Powerful</sub>
</p>

---

## 🎉 Introduction

**RenameFlow** is a lightweight command-line batch file renaming tool designed for developers and everyday users. It can quickly and safely rename files and directories in bulk, supporting multiple renaming modes with preview by default to ensure data safety.

### 💡 Inspiration

In daily development and file management, we often need to rename large numbers of files at once. Existing tools are either too complex to use or require installing numerous dependencies. RenameFlow was born to solve this problem — **zero dependencies, ready to use, powerful features**.

### ✨ Self-Developed Highlights

- 🚀 **Zero Dependencies** - Uses only Python standard library, no third-party packages required
- 👀 **Safety First** - Default preview mode, all operations are previewed before execution
- ↩️ **Undo Support** - Built-in history, undo recent operations anytime
- 🎨 **Interactive Mode** - User-friendly interactive interface, easy for beginners
- 🌏 **Internationalization** - Full multilingual support with colorful output

---

## ✨ Core Features

### 🔧 Multiple Renaming Modes

| Mode | Description | Example |
|------|-------------|---------|
| **replace** | String replacement | `old_file.txt` → `new_file.txt` |
| **regex** | Regular expression | `IMG_001.jpg` → `PHOTO_001.jpg` |
| **sequence** | Sequential numbering | `file.txt` → `photo_001.txt` |
| **case** | Case conversion | `FileName.txt` → `filename.txt` |
| **prefix** | Add prefix | `file.txt` → `IMG_file.txt` |
| **suffix** | Add suffix | `file.txt` → `file_backup.txt` |
| **trim** | Remove characters | `001file.txt` → `file.txt` |
| **date** | Date-based naming | `file.txt` → `20250508_001.txt` |
| **extension** | Change extension | `file.txt` → `file.md` |
| **csv** | CSV-based renaming | Rename based on CSV mapping |

### 🛡️ Safety Features

- ✅ **Preview by Default** - All operations default to preview mode, confirm before executing
- ✅ **Conflict Detection** - Automatically detect filename conflicts to avoid overwrites
- ✅ **Backup Support** - Option to create backup files before renaming
- ✅ **Undo Function** - Support undoing recent rename operations

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.8 or higher
- No third-party dependencies required

### 📦 Installation

**Option 1: Direct Download (Recommended)**
```bash
# Download the script
wget https://raw.githubusercontent.com/gitstq/RenameFlow/main/renameflow.py

# Add execute permission
chmod +x renameflow.py

# Run
python renameflow.py --help
```

**Option 2: pip Install**
```bash
pip install renameflow
```

**Option 3: Install from Source**
```bash
git clone https://github.com/gitstq/RenameFlow.git
cd RenameFlow
pip install -e .
```

### 🎯 Basic Usage

```bash
# Show help
renameflow --help

# Start interactive mode
renameflow interactive

# String replacement (preview mode)
renameflow replace /path/to/files "old" "new"

# Execute actual replacement
renameflow replace /path/to/files "old" "new" -e

# Regex renaming
renameflow regex /path/to/files "\d{4}" "2024" -e

# Sequential numbering
renameflow sequence /path/to/files --prefix "photo_" --start 1 --padding 4 -e

# Case conversion
renameflow case /path/to/files --type lower -e

# Add prefix
renameflow prefix /path/to/files "IMG_" -e

# Add suffix
renameflow suffix /path/to/files "_backup" -e

# Undo last operation
renameflow undo
```

---

## 📖 Detailed Usage Guide

### 🔧 Renaming Modes Explained

#### 1️⃣ String Replace (replace)

The simplest way to rename - replace a specified string with a new one.

```bash
# Replace "draft" with "final" in all filenames
renameflow replace ./documents "draft" "final"

# Process subdirectories recursively
renameflow replace ./documents "draft" "final" -r

# Execute actual replacement
renameflow replace ./documents "draft" "final" -e
```

#### 2️⃣ Regular Expression (regex)

Use regex for complex pattern matching and replacement.

```bash
# Change date format from YYYY-MM-DD to YYYYMMDD
renameflow regex ./photos "(\d{4})-(\d{2})-(\d{2})" "\1\2\3" -e

# Remove special characters from filenames
renameflow regex ./files "[^\w\-.]" "" -e
```

#### 3️⃣ Sequential Numbering (sequence)

Rename files with sequential numbers.

```bash
# Rename to photo_001.jpg, photo_002.jpg, ...
renameflow sequence ./photos --prefix "photo_" --start 1 --padding 3 -e

# Start from 100, use 5-digit numbers
renameflow sequence ./data --prefix "data_" --start 100 --padding 5 -e
```

#### 4️⃣ Case Conversion (case)

Supports multiple case conversion modes:

| Type | Description | Example |
|------|-------------|---------|
| `upper` | Uppercase | `FileName` → `FILENAME` |
| `lower` | Lowercase | `FileName` → `filename` |
| `title` | Title Case | `filename` → `Filename` |
| `camel` | Camel Case | `file_name` → `fileName` |
| `snake` | Snake Case | `FileName` → `file_name` |
| `kebab` | Kebab Case | `FileName` → `file-name` |

```bash
# Convert to lowercase
renameflow case ./files --type lower -e

# Convert to snake case
renameflow case ./files --type snake -e
```

#### 5️⃣ CSV Batch Renaming (csv)

Define rename mappings through a CSV file.

CSV file format:
```csv
old_name.txt,new_name.txt
draft_v1.doc,final_v1.doc
image_001.jpg,photo_001.jpg
```

```bash
renameflow csv ./files --csv mapping.csv -e
```

### 🎨 Interactive Mode

For users unfamiliar with command line, use interactive mode:

```bash
renameflow interactive
```

The system will guide you step by step:
1. Select target path
2. Select rename mode
3. Enter parameters
4. Preview changes
5. Confirm execution

---

## 💡 Design Philosophy & Roadmap

### 🏗️ Design Principles

RenameFlow follows these principles:

1. **Zero Dependencies First** - Uses Python standard library for simple installation and good compatibility
2. **Safety First** - Default preview mode to avoid accidental operations
3. **Complete Features** - Covers common batch renaming scenarios
4. **Easy to Use** - Interactive mode and detailed documentation

### 📅 Future Roadmap

- [ ] Support EXIF metadata variables (photo dates, etc.)
- [ ] Support ID3 tag variables (audio file info)
- [ ] Add file preview functionality
- [ ] Support more file attribute variables
- [ ] Add configuration file support
- [ ] Develop GUI version

### 🤝 Community Contributions

Issues and Pull Requests are welcome!

---

## 📦 Build & Deployment

### Build from Source

```bash
# Clone repository
git clone https://github.com/gitstq/RenameFlow.git
cd RenameFlow

# Install in development mode
pip install -e .

# Build distribution packages
pip install build
python -m build
```

### Cross-Platform Compatibility

RenameFlow supports:
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (all major distributions)

---

## 🤝 Contributing

All forms of contribution are welcome!

### Submitting Issues

- 🐛 Bug reports: Please describe the problem, reproduction steps, and environment in detail
- 💡 Feature suggestions: Please explain the use case and expected results

### Submitting PRs

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

You are free to:
- ✅ Commercial use
- ✅ Modify the code
- ✅ Distribute the code
- ✅ Private use

The only requirement is to retain the copyright notice.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">RenameFlow Team</a>
</p>
