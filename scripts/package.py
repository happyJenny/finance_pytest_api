# scripts/package.py
"""打包项目为 zip，排除 cache / venv / git 等。

用法：
    python scripts/package.py
    python scripts/package.py --output my_project.zip
"""
import argparse
import os
import sys
import zipfile
from datetime import datetime

# 排除的目录名（任意层级匹配）
EXCLUDE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "venv",
    ".venv",
    "env",
    ".env",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "htmlcov",
    ".coverage",
    "dist",
    "build",
    "*.egg-info",
}

# 排除的文件名（任意层级匹配）
EXCLUDE_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

# 排除的文件后缀
EXCLUDE_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".pyd",
    ".log",
    ".zip",
)

# 项目根目录（脚本的上一级）
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def should_exclude_dir(dir_name):
    return dir_name in EXCLUDE_DIRS


def should_exclude_file(file_name):
    if file_name in EXCLUDE_FILES:
        return True
    return file_name.endswith(EXCLUDE_SUFFIXES)


def collect_files(root):
    """遍历 root，返回要打包的文件绝对路径列表"""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # 原地修改 dirnames，跳过排除目录（os.walk 不会再进入）
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]

        for f in filenames:
            if should_exclude_file(f):
                continue
            files.append(os.path.join(dirpath, f))
    return files


def make_zip(root, output):
    files = collect_files(root)
    print(f"根目录: {root}")
    print(f"待打包: {len(files)} 个文件")

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            # 压缩包内用相对路径
            arcname = os.path.relpath(f, root)
            zf.write(f, arcname)
            print(f"  + {arcname}")

    size_mb = os.path.getsize(output) / 1024 / 1024
    print(f"\n输出: {output} ({size_mb:.2f} MB)")


def main():
    parser = argparse.ArgumentParser(description="打包项目为 zip")
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出 zip 路径（默认：../<项目名>_<时间戳>.zip）",
    )
    parser.add_argument(
        "--root", "-r",
        default=ROOT_DIR,
        help="要打包的根目录（默认：项目根目录）",
    )
    args = parser.parse_args()

    output = args.output
    if output is None:
        project_name = os.path.basename(args.root.rstrip(os.sep))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"{project_name}_{timestamp}.zip"

    make_zip(args.root, output)


if __name__ == "__main__":
    main()