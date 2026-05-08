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
  <b>輕量級批量檔案重新命名工具</b><br>
  <sub>零依賴 · 跨平台 · 安全可靠 · 功能強大</sub>
</p>

---

## 🎉 專案介紹

**RenameFlow** 是一款輕量級的命令列批量檔案重新命名工具，專為開發者和一般使用者設計。它能夠快速、安全地批量重新命名檔案和目錄，支援多種重新命名模式，所有操作預設預覽，確保資料安全。

### 💡 靈感來源

在日常開發和管理檔案時，經常需要批量重新命名大量檔案。現有的工具要麼功能複雜難以使用，要麼需要安裝大量依賴。RenameFlow 的誕生就是為了解決這個問題——**零依賴、開箱即用、功能強大**。

### ✨ 自研差異化亮點

- 🚀 **零依賴設計** - 僅使用 Python 標準函式庫，無需安裝任何第三方套件
- 👀 **安全第一** - 預設預覽模式，所有操作先預覽後執行
- ↩️ **支援復原** - 內建歷史記錄，可隨時復原最近的操作
- 🎨 **互動式模式** - 提供友善的互動式介面，新手也能輕鬆使用
- 🌏 **中文友善** - 完善的中文支援和彩色輸出

---

## ✨ 核心特性

### 🔧 多種重新命名模式

| 模式 | 說明 | 範例 |
|------|------|------|
| **replace** | 字串替換 | `old_file.txt` → `new_file.txt` |
| **regex** | 正規表示式 | `IMG_001.jpg` → `PHOTO_001.jpg` |
| **sequence** | 序號命名 | `file.txt` → `photo_001.txt` |
| **case** | 大小寫轉換 | `FileName.txt` → `filename.txt` |
| **prefix** | 新增前綴 | `file.txt` → `IMG_file.txt` |
| **suffix** | 新增後綴 | `file.txt` → `file_backup.txt` |
| **trim** | 刪除字元 | `001file.txt` → `file.txt` |
| **date** | 日期命名 | `file.txt` → `20250508_001.txt` |
| **extension** | 副檔名修改 | `file.txt` → `file.md` |
| **csv** | CSV批量重新命名 | 根據CSV映射批量重新命名 |

### 🛡️ 安全特性

- ✅ **預設預覽** - 所有操作預設為預覽模式，確認無誤後再執行
- ✅ **衝突檢測** - 自動檢測檔名衝突，避免覆蓋
- ✅ **備份支援** - 可選擇在重新命名前建立備份檔案
- ✅ **復原功能** - 支援復原最近的重新命名操作

---

## 🚀 快速開始

### 📋 環境要求

- Python 3.8 或更高版本
- 無需任何第三方依賴

### 📦 安裝方式

**方式一：直接下載（推薦）**
```bash
# 下載腳本
wget https://raw.githubusercontent.com/gitstq/RenameFlow/main/renameflow.py

# 新增執行權限
chmod +x renameflow.py

# 執行
python renameflow.py --help
```

**方式二：pip 安裝**
```bash
pip install renameflow
```

**方式三：從原始碼安裝**
```bash
git clone https://github.com/gitstq/RenameFlow.git
cd RenameFlow
pip install -e .
```

### 🎯 基本使用

```bash
# 查看幫助
renameflow --help

# 啟動互動式模式
renameflow interactive

# 字串替換（預覽模式）
renameflow replace /path/to/files "old" "new"

# 執行實際替換
renameflow replace /path/to/files "old" "new" -e

# 正規表示式重新命名
renameflow regex /path/to/files "\d{4}" "2024" -e

# 序號命名
renameflow sequence /path/to/files --prefix "photo_" --start 1 --padding 4 -e

# 大小寫轉換
renameflow case /path/to/files --type lower -e

# 新增前綴
renameflow prefix /path/to/files "IMG_" -e

# 新增後綴
renameflow suffix /path/to/files "_backup" -e

# 復原最近操作
renameflow undo
```

---

## 📖 詳細使用指南

### 🔧 重新命名模式詳解

#### 1️⃣ 字串替換 (replace)

最簡單的重新命名方式，將檔名中的指定字串替換為新字串。

```bash
# 將所有檔名中的 "draft" 替換為 "final"
renameflow replace ./documents "draft" "final"

# 遞迴處理子目錄
renameflow replace ./documents "draft" "final" -r

# 執行實際替換
renameflow replace ./documents "draft" "final" -e
```

#### 2️⃣ 正規表示式 (regex)

使用正規表示式進行複雜的模式匹配和替換。

```bash
# 將檔名中的日期格式從 YYYY-MM-DD 改為 YYYYMMDD
renameflow regex ./photos "(\d{4})-(\d{2})-(\d{2})" "\1\2\3" -e

# 移除檔名中的特殊字元
renameflow regex ./files "[^\w\-.]" "" -e
```

#### 3️⃣ 序號命名 (sequence)

按順序編號重新命名檔案。

```bash
# 將檔案重新命名為 photo_001.jpg, photo_002.jpg, ...
renameflow sequence ./photos --prefix "photo_" --start 1 --padding 3 -e

# 從 100 開始編號，使用 5 位數字
renameflow sequence ./data --prefix "data_" --start 100 --padding 5 -e
```

#### 4️⃣ 大小寫轉換 (case)

支援多種大小寫轉換模式：

| 類型 | 說明 | 範例 |
|------|------|------|
| `upper` | 全大寫 | `FileName` → `FILENAME` |
| `lower` | 全小寫 | `FileName` → `filename` |
| `title` | 首字母大寫 | `filename` → `Filename` |
| `camel` | 駝峰命名 | `file_name` → `fileName` |
| `snake` | 蛇形命名 | `FileName` → `file_name` |
| `kebab` | 短橫線命名 | `FileName` → `file-name` |

```bash
# 轉換為小寫
renameflow case ./files --type lower -e

# 轉換為蛇形命名
renameflow case ./files --type snake -e
```

#### 5️⃣ CSV 批量重新命名 (csv)

透過 CSV 檔案定義重新命名映射。

CSV 檔案格式：
```csv
old_name.txt,new_name.txt
draft_v1.doc,final_v1.doc
image_001.jpg,photo_001.jpg
```

```bash
renameflow csv ./files --csv mapping.csv -e
```

### 🎨 互動式模式

對於不熟悉命令列的使用者，可以使用互動式模式：

```bash
renameflow interactive
```

系統會逐步引導您：
1. 選擇目標路徑
2. 選擇重新命名模式
3. 輸入相關參數
4. 預覽變更
5. 確認執行

---

## 💡 設計思路與迭代規劃

### 🏗️ 設計理念

RenameFlow 的設計遵循以下原則：

1. **零依賴優先** - 使用 Python 標準函式庫，確保安裝簡單、相容性好
2. **安全第一** - 預設預覽模式，避免誤操作
3. **功能完整** - 覆蓋常見的批量重新命名場景
4. **易於使用** - 提供互動式模式和詳細的說明文件

### 📅 後續迭代計劃

- [ ] 支援 EXIF 元資料變數（照片拍攝日期等）
- [ ] 支援 ID3 標籤變數（音訊檔案資訊）
- [ ] 新增檔案預覽功能
- [ ] 支援更多檔案屬性變數
- [ ] 新增設定檔支援
- [ ] 開發 GUI 版本

### 🤝 社群貢獻

歡迎提交 Issue 和 Pull Request！

---

## 📦 打包與部署指南

### 從原始碼建構

```bash
# 複製儲存庫
git clone https://github.com/gitstq/RenameFlow.git
cd RenameFlow

# 安裝開發依賴
pip install -e .

# 建構分發套件
pip install build
python -m build
```

### 跨平台相容性

RenameFlow 支援以下平台：
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (所有主流發行版)

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 提交 Issue

- 🐛 錯誤報告：請詳細描述問題、重現步驟和環境資訊
- 💡 功能建議：請說明使用場景和預期效果

### 提交 PR

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

---

## 📄 開源授權說明

本專案採用 [MIT License](LICENSE) 開源授權。

您可以自由地：
- ✅ 商業使用
- ✅ 修改程式碼
- ✅ 分發程式碼
- ✅ 私人使用

唯一要求是保留版權聲明。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">RenameFlow Team</a>
</p>
