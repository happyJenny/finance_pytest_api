from base64 import b64encode
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "all_files_record.txt"

SKIP_DIR_NAMES = {"api", "cache", "vscode", "venv","scripts"}
SKIP_SUFFIXES = {".apk"}  # 新增：跳过后缀
SCRIPT_FILE = Path(__file__).resolve()


def _is_cases_test5(p: Path) -> bool:
    """cases/ 目录下、文件名以 test_5_ 开头的文件"""
    try:
        rel = p.relative_to(ROOT)
    except ValueError:
        return False
    return (
        len(rel.parts) >= 2
        and rel.parts[0] == "cases"
        and rel.name.startswith("test_14_")
    )


def _should_skip(p: Path) -> bool:
    if p == SCRIPT_FILE:
        return True
    if p == OUTPUT:
        return True
    if not p.is_file():
        return True

    # 跳过 .apk 等后缀文件
    if p.suffix.casefold() in SKIP_SUFFIXES:
        return True

    rel = p.relative_to(ROOT)
    parts_lower = [part.casefold() for part in rel.parts]

    # 任意一层目录是 api / vscode / venv / cases1-3 / 含 cache → 跳过
    for part_lower in parts_lower:
        if part_lower in ("derpricatedapi", "deprecatedcases","vscode", "venv", "cases1-3","cases4_1_fixutre"):
            return True
        if "cache" in part_lower:
            return True

    # cases 目录特殊处理：只保留 test_5_ 开头的文件
    # if parts_lower[0] == "cases":
    #     return not _is_cases_test5(p)

    # 其余文件（项目根、utils、config、factories、data 等）照常收录
    return False


with OUTPUT.open("w", encoding="utf-8") as record:
    for path in sorted(ROOT.rglob("*")):
        if _should_skip(path):
            continue

        data = path.read_bytes()
        
        # 修改点 1：把原有的 \n 去掉，让每个文件块的标题紧凑相连
        record.write(f"{'=' * 80}\n文件：{path.relative_to(ROOT)}\n{'=' * 80}\n")

        try:
            text = data.decode("utf-8")
            
            # 修改点 2：按行处理，跳过空行，保留原有的缩进和逻辑
            for line in text.splitlines():
                if line.strip():  # 如果是空行（或只包含空格），就不写入
                    record.write(f"{line}\n")
                    
        except UnicodeDecodeError:
            record.write("[二进制文件，Base64 内容]\n")
            record.write(f"{b64encode(data).decode('ascii')}\n")

print(f"已完成，文件已写入：{OUTPUT}")