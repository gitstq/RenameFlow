#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RenameFlow - Lightweight Batch File Renaming Tool
轻量级批量文件重命名工具

A cross-platform CLI tool for batch renaming files and directories quickly and safely.
"""

import os
import re
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import csv


__version__ = "1.0.0"
__author__ = "RenameFlow Team"
__license__ = "MIT"


class RenameMode(Enum):
    """重命名模式枚举"""
    REPLACE = "replace"           # 字符串替换
    REGEX = "regex"               # 正则表达式
    SEQUENCE = "sequence"         # 序号命名
    CASE = "case"                 # 大小写转换
    PREFIX = "prefix"             # 添加前缀
    SUFFIX = "suffix"             # 添加后缀
    TRIM = "trim"                 # 删除字符
    DATE = "date"                 # 日期命名
    EXTENSION = "extension"       # 扩展名修改
    CSV = "csv"                   # CSV批量重命名


class CaseType(Enum):
    """大小写类型"""
    UPPER = "upper"               # 全大写
    LOWER = "lower"               # 全小写
    TITLE = "title"               # 首字母大写
    CAMEL = "camel"               # 驼峰命名
    SNAKE = "snake"               # 蛇形命名
    KEBAB = "kebab"               # 短横线命名


@dataclass
class RenameOperation:
    """重命名操作数据类"""
    original_path: Path
    new_path: Path
    original_name: str
    new_name: str
    status: str = "pending"  # pending, success, failed, conflict
    error_message: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "original_path": str(self.original_path),
            "new_path": str(self.new_path),
            "original_name": self.original_name,
            "new_name": self.new_name,
            "status": self.status,
            "error_message": self.error_message
        }


@dataclass
class RenameConfig:
    """重命名配置数据类"""
    mode: RenameMode = RenameMode.REPLACE
    pattern: str = ""
    replacement: str = ""
    case_type: CaseType = CaseType.LOWER
    prefix: str = ""
    suffix: str = ""
    start_number: int = 1
    number_padding: int = 3
    trim_start: int = 0
    trim_end: int = 0
    date_format: str = "%Y%m%d"
    new_extension: str = ""
    csv_file: str = ""
    recursive: bool = False
    include_dirs: bool = False
    dry_run: bool = True
    overwrite: bool = False
    backup: bool = False


class ColorOutput:
    """彩色输出工具类"""
    
    # ANSI颜色代码
    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "dim": "\033[2m",
    }
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """为文本添加颜色"""
        if sys.stdout.isatty():
            return f"{cls.COLORS.get(color, '')}{text}{cls.COLORS['reset']}"
        return text
    
    @classmethod
    def success(cls, text: str) -> str:
        return cls.colorize(text, "green")
    
    @classmethod
    def error(cls, text: str) -> str:
        return cls.colorize(text, "red")
    
    @classmethod
    def warning(cls, text: str) -> str:
        return cls.colorize(text, "yellow")
    
    @classmethod
    def info(cls, text: str) -> str:
        return cls.colorize(text, "cyan")
    
    @classmethod
    def highlight(cls, text: str) -> str:
        return cls.colorize(text, "magenta")


class FileScanner:
    """文件扫描器"""
    
    def __init__(self, path: Path, config: RenameConfig):
        self.path = path
        self.config = config
    
    def scan(self) -> List[Path]:
        """扫描目标路径下的文件"""
        items = []
        
        if self.path.is_file():
            return [self.path]
        
        if self.config.recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        for item in self.path.glob(pattern):
            if item.is_file() or (self.config.include_dirs and item.is_dir()):
                # 跳过隐藏文件
                if item.name.startswith('.'):
                    continue
                items.append(item)
        
        # 按名称排序
        items.sort(key=lambda x: x.name.lower())
        return items


class RenameEngine:
    """重命名引擎"""
    
    def __init__(self, config: RenameConfig):
        self.config = config
        self.operations: List[RenameOperation] = []
        self.history_file = Path.home() / ".renameflow_history.json"
    
    def generate_new_name(self, original_name: str, index: int = 0) -> str:
        """根据配置生成新文件名"""
        name = original_name
        stem = Path(original_name).stem
        ext = Path(original_name).suffix
        
        if self.config.mode == RenameMode.REPLACE:
            name = original_name.replace(self.config.pattern, self.config.replacement)
        
        elif self.config.mode == RenameMode.REGEX:
            try:
                name = re.sub(self.config.pattern, self.config.replacement, original_name)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}")
        
        elif self.config.mode == RenameMode.SEQUENCE:
            num = self.config.start_number + index
            num_str = str(num).zfill(self.config.number_padding)
            name = f"{self.config.pattern}{num_str}{ext}"
        
        elif self.config.mode == RenameMode.CASE:
            stem = Path(original_name).stem
            ext = Path(original_name).suffix
            
            if self.config.case_type == CaseType.UPPER:
                name = stem.upper() + ext.lower()
            elif self.config.case_type == CaseType.LOWER:
                name = stem.lower() + ext.lower()
            elif self.config.case_type == CaseType.TITLE:
                name = stem.title() + ext.lower()
            elif self.config.case_type == CaseType.CAMEL:
                words = re.split(r'[_\-\s]+', stem.lower())
                name = words[0] + ''.join(w.capitalize() for w in words[1:]) + ext.lower()
            elif self.config.case_type == CaseType.SNAKE:
                s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', stem)
                name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower() + ext.lower()
            elif self.config.case_type == CaseType.KEBAB:
                s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1-\2', stem)
                name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s1).lower() + ext.lower()
        
        elif self.config.mode == RenameMode.PREFIX:
            name = self.config.prefix + original_name
        
        elif self.config.mode == RenameMode.SUFFIX:
            name = stem + self.config.suffix + ext
        
        elif self.config.mode == RenameMode.TRIM:
            start = self.config.trim_start
            end = len(stem) - self.config.trim_end if self.config.trim_end > 0 else len(stem)
            name = stem[start:end] + ext
        
        elif self.config.mode == RenameMode.DATE:
            date_str = datetime.now().strftime(self.config.date_format)
            name = f"{self.config.pattern}{date_str}_{index + 1:03d}{ext}"
        
        elif self.config.mode == RenameMode.EXTENSION:
            new_ext = self.config.new_extension
            if not new_ext.startswith('.'):
                new_ext = '.' + new_ext
            name = stem + new_ext
        
        return name
    
    def generate_csv_rename(self, original_name: str, csv_mapping: Dict[str, str]) -> str:
        """使用CSV映射生成新文件名"""
        return csv_mapping.get(original_name, original_name)
    
    def load_csv_mapping(self, csv_path: Path) -> Dict[str, str]:
        """加载CSV映射文件"""
        mapping = {}
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        mapping[row[0]] = row[1]
        except Exception as e:
            raise ValueError(f"Failed to load CSV file: {e}")
        return mapping
    
    def plan(self, files: List[Path]) -> List[RenameOperation]:
        """规划重命名操作"""
        self.operations = []
        
        # 如果是CSV模式，先加载映射
        csv_mapping = {}
        if self.config.mode == RenameMode.CSV and self.config.csv_file:
            csv_mapping = self.load_csv_mapping(Path(self.config.csv_file))
        
        for index, file_path in enumerate(files):
            original_name = file_path.name
            
            if self.config.mode == RenameMode.CSV:
                new_name = self.generate_csv_rename(original_name, csv_mapping)
            else:
                new_name = self.generate_new_name(original_name, index)
            
            if new_name == original_name:
                continue  # 跳过没有变化的文件
            
            new_path = file_path.parent / new_name
            
            operation = RenameOperation(
                original_path=file_path,
                new_path=new_path,
                original_name=original_name,
                new_name=new_name
            )
            self.operations.append(operation)
        
        return self.operations
    
    def detect_conflicts(self) -> List[RenameOperation]:
        """检测冲突"""
        conflicts = []
        new_paths = set()
        
        for op in self.operations:
            # 检测目标文件是否已存在
            if op.new_path.exists() and not self.config.overwrite:
                op.status = "conflict"
                op.error_message = "Target file already exists"
                conflicts.append(op)
                continue
            
            # 检测重命名后的文件名是否重复
            if op.new_path in new_paths:
                op.status = "conflict"
                op.error_message = "Duplicate target filename"
                conflicts.append(op)
                continue
            
            new_paths.add(op.new_path)
        
        return conflicts
    
    def execute(self) -> Tuple[int, int]:
        """执行重命名操作"""
        success_count = 0
        failed_count = 0
        
        # 先检测冲突
        conflicts = self.detect_conflicts()
        if conflicts and not self.config.overwrite:
            print(ColorOutput.warning(f"\n⚠️  Detected {len(conflicts)} conflicts. Use --overwrite to force rename."))
            return 0, len(conflicts)
        
        # 保存历史记录
        history = self._load_history()
        
        # 为整个批次生成一个唯一的时间戳
        batch_timestamp = datetime.now().isoformat()
        
        for op in self.operations:
            if op.status == "conflict" and not self.config.overwrite:
                continue
            
            try:
                # 备份
                if self.config.backup:
                    backup_path = op.original_path.with_suffix(op.original_path.suffix + '.bak')
                    shutil.copy2(op.original_path, backup_path)
                
                # 执行重命名
                op.original_path.rename(op.new_path)
                op.status = "success"
                success_count += 1
                
                # 记录到历史（使用相同的时间戳标记同一批次）
                history.append({
                    "timestamp": batch_timestamp,
                    "operation": op.to_dict()
                })
                
            except Exception as e:
                op.status = "failed"
                op.error_message = str(e)
                failed_count += 1
        
        # 保存历史
        self._save_history(history)
        
        return success_count, failed_count
    
    def undo(self) -> Tuple[int, int]:
        """撤销最近一次操作"""
        history = self._load_history()
        if not history:
            print(ColorOutput.warning("No history found to undo."))
            return 0, 0
        
        # 获取最近一次操作
        last_batch = []
        last_timestamp = history[-1]["timestamp"]
        
        # 找到同一批次的所有操作
        while history and history[-1]["timestamp"] == last_timestamp:
            last_batch.append(history.pop())
        
        success_count = 0
        failed_count = 0
        
        for item in reversed(last_batch):
            op_data = item["operation"]
            original_path = Path(op_data["original_path"])
            new_path = Path(op_data["new_path"])
            
            try:
                if new_path.exists():
                    new_path.rename(original_path)
                    success_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                print(ColorOutput.error(f"Failed to undo: {e}"))
        
        self._save_history(history)
        return success_count, failed_count
    
    def _load_history(self) -> List[Dict]:
        """加载历史记录"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self, history: List[Dict]):
        """保存历史记录"""
        # 只保留最近100条记录
        if len(history) > 100:
            history = history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)


class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def print_preview(operations: List[RenameOperation], dry_run: bool = True):
        """打印预览"""
        if not operations:
            print(ColorOutput.info("\n📋 No files to rename."))
            return
        
        if dry_run:
            print(ColorOutput.info("\n📋 Dry run preview (no changes will be made):"))
            print("=" * 80)
        else:
            print(ColorOutput.info("\n📋 Rename operations:"))
            print("=" * 80)
        
        for i, op in enumerate(operations, 1):
            status_icon = "✓" if op.status == "pending" else "⚠"
            status_color = "success" if op.status == "pending" else "warning"
            
            print(f"\n{ColorOutput.colorize(status_icon, status_color)} [{i}]")
            print(f"  {ColorOutput.colorize('Original:', 'dim')} {op.original_name}")
            print(f"  {ColorOutput.colorize('New:', 'dim')}      {ColorOutput.highlight(op.new_name)}")
            
            if op.status == "conflict":
                print(f"  {ColorOutput.error('⚠ Conflict:')} {op.error_message}")
        
        print("\n" + "=" * 80)
        print(f"\n📊 Summary: {len(operations)} files to rename")
        
        conflicts = [op for op in operations if op.status == "conflict"]
        if conflicts:
            print(ColorOutput.warning(f"⚠️  {len(conflicts)} conflicts detected"))
    
    @staticmethod
    def print_result(success_count: int, failed_count: int):
        """打印执行结果"""
        print("\n" + "=" * 80)
        print(ColorOutput.success(f"✅ Successfully renamed: {success_count} files"))
        if failed_count > 0:
            print(ColorOutput.error(f"❌ Failed: {failed_count} files"))
        print("=" * 80 + "\n")


class InteractiveMode:
    """交互式模式"""
    
    def __init__(self):
        self.config = RenameConfig()
        self.target_path = Path.cwd()
    
    def run(self):
        """运行交互式模式"""
        print(ColorOutput.info("\n🔄 RenameFlow Interactive Mode"))
        print("=" * 50)
        
        # 选择目标路径
        path_input = input(f"\n📁 Target path [{self.target_path}]: ").strip()
        if path_input:
            self.target_path = Path(path_input)
        
        if not self.target_path.exists():
            print(ColorOutput.error("Path does not exist!"))
            return
        
        # 选择重命名模式
        print("\n🔧 Select rename mode:")
        modes = list(RenameMode)
        for i, mode in enumerate(modes, 1):
            print(f"  {i}. {mode.value}")
        
        mode_choice = input("\nSelect mode [1]: ").strip()
        try:
            self.config.mode = modes[int(mode_choice) - 1] if mode_choice else modes[0]
        except (ValueError, IndexError):
            self.config.mode = modes[0]
        
        # 根据模式获取参数
        self._get_mode_params()
        
        # 其他选项
        recursive = input("\n🔄 Recursive? [y/N]: ").strip().lower()
        self.config.recursive = recursive == 'y'
        
        dry_run = input("👀 Dry run? [Y/n]: ").strip().lower()
        self.config.dry_run = dry_run != 'n'
        
        # 执行
        self._execute()
    
    def _get_mode_params(self):
        """根据模式获取参数"""
        if self.config.mode == RenameMode.REPLACE:
            self.config.pattern = input("🔍 Pattern to replace: ").strip()
            self.config.replacement = input("📝 Replacement: ").strip()
        
        elif self.config.mode == RenameMode.REGEX:
            self.config.pattern = input("🔍 Regex pattern: ").strip()
            self.config.replacement = input("📝 Replacement: ").strip()
        
        elif self.config.mode == RenameMode.SEQUENCE:
            self.config.pattern = input("📝 Name prefix: ").strip()
            self.config.start_number = int(input("🔢 Start number [1]: ").strip() or "1")
            self.config.number_padding = int(input("🔢 Number padding [3]: ").strip() or "3")
        
        elif self.config.mode == RenameMode.CASE:
            print("\n🔤 Select case type:")
            cases = list(CaseType)
            for i, case in enumerate(cases, 1):
                print(f"  {i}. {case.value}")
            case_choice = input("\nSelect case [1]: ").strip()
            try:
                self.config.case_type = cases[int(case_choice) - 1] if case_choice else cases[0]
            except (ValueError, IndexError):
                self.config.case_type = cases[0]
        
        elif self.config.mode == RenameMode.PREFIX:
            self.config.prefix = input("📝 Prefix to add: ").strip()
        
        elif self.config.mode == RenameMode.SUFFIX:
            self.config.suffix = input("📝 Suffix to add: ").strip()
        
        elif self.config.mode == RenameMode.TRIM:
            self.config.trim_start = int(input("✂️ Characters to trim from start [0]: ").strip() or "0")
            self.config.trim_end = int(input("✂️ Characters to trim from end [0]: ").strip() or "0")
        
        elif self.config.mode == RenameMode.DATE:
            self.config.pattern = input("📝 Name prefix: ").strip()
            self.config.date_format = input("📅 Date format [%Y%m%d]: ").strip() or "%Y%m%d"
        
        elif self.config.mode == RenameMode.EXTENSION:
            self.config.new_extension = input("📝 New extension (e.g., txt): ").strip()
        
        elif self.config.mode == RenameMode.CSV:
            self.config.csv_file = input("📄 CSV file path: ").strip()
    
    def _execute(self):
        """执行重命名"""
        scanner = FileScanner(self.target_path, self.config)
        files = scanner.scan()
        
        engine = RenameEngine(self.config)
        operations = engine.plan(files)
        
        OutputFormatter.print_preview(operations, self.config.dry_run)
        
        if self.config.dry_run:
            confirm = input("\n❓ Execute these changes? [y/N]: ").strip().lower()
            if confirm == 'y':
                self.config.dry_run = False
                success, failed = engine.execute()
                OutputFormatter.print_result(success, failed)
        else:
            success, failed = engine.execute()
            OutputFormatter.print_result(success, failed)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="renameflow",
        description="🔄 RenameFlow - Lightweight Batch File Renaming Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Replace string in filenames
  renameflow replace /path/to/files "old" "new"
  
  # Use regex pattern
  renameflow regex /path/to/files "\d{4}" "2024"
  
  # Sequential numbering
  renameflow sequence /path/to/files --prefix "photo_" --start 1 --padding 4
  
  # Change case
  renameflow case /path/to/files --type lower
  
  # Add prefix/suffix
  renameflow prefix /path/to/files "IMG_"
  renameflow suffix /path/to/files "_backup"
  
  # Date-based naming
  renameflow date /path/to/files --prefix "file_"
  
  # Change extension
  renameflow extension /path/to/files --ext "txt"
  
  # CSV-based renaming
  renameflow csv /path/to/files --csv mapping.csv
  
  # Undo last operation
  renameflow undo
  
  # Interactive mode
  renameflow interactive
        """
    )
    
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Replace command
    replace_parser = subparsers.add_parser("replace", help="Replace string in filenames")
    replace_parser.add_argument("path", help="Target directory or file")
    replace_parser.add_argument("pattern", help="Pattern to replace")
    replace_parser.add_argument("replacement", help="Replacement string")
    replace_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    replace_parser.add_argument("-d", "--dirs", action="store_true", help="Include directories")
    replace_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes (not dry run)")
    replace_parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite existing files")
    replace_parser.add_argument("-b", "--backup", action="store_true", help="Create backup files")
    
    # Regex command
    regex_parser = subparsers.add_parser("regex", help="Use regex pattern for renaming")
    regex_parser.add_argument("path", help="Target directory or file")
    regex_parser.add_argument("pattern", help="Regex pattern")
    regex_parser.add_argument("replacement", help="Replacement string")
    regex_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    regex_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    regex_parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite existing files")
    
    # Sequence command
    seq_parser = subparsers.add_parser("sequence", help="Sequential numbering")
    seq_parser.add_argument("path", help="Target directory")
    seq_parser.add_argument("--prefix", default="", help="Name prefix")
    seq_parser.add_argument("--start", type=int, default=1, help="Starting number")
    seq_parser.add_argument("--padding", type=int, default=3, help="Number padding")
    seq_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    seq_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # Case command
    case_parser = subparsers.add_parser("case", help="Change filename case")
    case_parser.add_argument("path", help="Target directory")
    case_parser.add_argument("--type", choices=["upper", "lower", "title", "camel", "snake", "kebab"],
                            default="lower", help="Case type")
    case_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    case_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # Prefix command
    prefix_parser = subparsers.add_parser("prefix", help="Add prefix to filenames")
    prefix_parser.add_argument("path", help="Target directory")
    prefix_parser.add_argument("prefix", help="Prefix to add")
    prefix_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    prefix_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # Suffix command
    suffix_parser = subparsers.add_parser("suffix", help="Add suffix to filenames")
    suffix_parser.add_argument("path", help="Target directory")
    suffix_parser.add_argument("suffix", help="Suffix to add")
    suffix_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    suffix_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # Trim command
    trim_parser = subparsers.add_parser("trim", help="Trim characters from filenames")
    trim_parser.add_argument("path", help="Target directory")
    trim_parser.add_argument("--start", type=int, default=0, help="Characters to trim from start")
    trim_parser.add_argument("--end", type=int, default=0, help="Characters to trim from end")
    trim_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    trim_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # Date command
    date_parser = subparsers.add_parser("date", help="Date-based naming")
    date_parser.add_argument("path", help="Target directory")
    date_parser.add_argument("--prefix", default="", help="Name prefix")
    date_parser.add_argument("--format", default="%Y%m%d", help="Date format")
    date_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    date_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # Extension command
    ext_parser = subparsers.add_parser("extension", help="Change file extension")
    ext_parser.add_argument("path", help="Target directory")
    ext_parser.add_argument("--ext", required=True, help="New extension")
    ext_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    ext_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # CSV command
    csv_parser = subparsers.add_parser("csv", help="CSV-based renaming")
    csv_parser.add_argument("path", help="Target directory")
    csv_parser.add_argument("--csv", required=True, help="CSV file path")
    csv_parser.add_argument("-r", "--recursive", action="store_true", help="Process recursively")
    csv_parser.add_argument("-e", "--execute", action="store_true", help="Execute changes")
    
    # Undo command
    subparsers.add_parser("undo", help="Undo last rename operation")
    
    # Interactive command
    subparsers.add_parser("interactive", help="Start interactive mode")
    
    return parser


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Interactive mode
    if args.command == "interactive":
        InteractiveMode().run()
        return
    
    # Undo
    if args.command == "undo":
        engine = RenameEngine(RenameConfig())
        success, failed = engine.undo()
        OutputFormatter.print_result(success, failed)
        return
    
    # Build config from args
    config = RenameConfig()
    config.dry_run = not getattr(args, 'execute', False)
    config.recursive = getattr(args, 'recursive', False)
    config.include_dirs = getattr(args, 'dirs', False)
    config.overwrite = getattr(args, 'overwrite', False)
    config.backup = getattr(args, 'backup', False)
    
    # Set mode-specific config
    if args.command == "replace":
        config.mode = RenameMode.REPLACE
        config.pattern = args.pattern
        config.replacement = args.replacement
    
    elif args.command == "regex":
        config.mode = RenameMode.REGEX
        config.pattern = args.pattern
        config.replacement = args.replacement
    
    elif args.command == "sequence":
        config.mode = RenameMode.SEQUENCE
        config.pattern = args.prefix
        config.start_number = args.start
        config.number_padding = args.padding
    
    elif args.command == "case":
        config.mode = RenameMode.CASE
        config.case_type = CaseType(args.type)
    
    elif args.command == "prefix":
        config.mode = RenameMode.PREFIX
        config.prefix = args.prefix
    
    elif args.command == "suffix":
        config.mode = RenameMode.SUFFIX
        config.suffix = args.suffix
    
    elif args.command == "trim":
        config.mode = RenameMode.TRIM
        config.trim_start = args.start
        config.trim_end = args.end
    
    elif args.command == "date":
        config.mode = RenameMode.DATE
        config.pattern = args.prefix
        config.date_format = args.format
    
    elif args.command == "extension":
        config.mode = RenameMode.EXTENSION
        config.new_extension = args.ext
    
    elif args.command == "csv":
        config.mode = RenameMode.CSV
        config.csv_file = args.csv
    
    # Execute
    target_path = Path(args.path)
    if not target_path.exists():
        print(ColorOutput.error(f"Error: Path '{args.path}' does not exist."))
        sys.exit(1)
    
    scanner = FileScanner(target_path, config)
    files = scanner.scan()
    
    if not files:
        print(ColorOutput.warning("No files found to rename."))
        return
    
    engine = RenameEngine(config)
    operations = engine.plan(files)
    
    OutputFormatter.print_preview(operations, config.dry_run)
    
    if config.dry_run:
        print(ColorOutput.info("\n💡 Run with -e/--execute to apply changes."))
    else:
        success, failed = engine.execute()
        OutputFormatter.print_result(success, failed)


if __name__ == "__main__":
    main()
