import json
import re
import shutil
import pathlib

# このスクリプトが置いてある場所 = リポジトリのルート
ROOT = pathlib.Path(__file__).resolve().parent
REPO_PH = ROOT / "ph"
REPO_PH.mkdir(exist_ok=True)

# 画像の元フォルダ（OneDrive）。存在するものだけ使う。
ONEDRIVE = [
    pathlib.Path(r"C:\Users\moto8\OneDrive\ph"),
    pathlib.Path(r"C:\Users\moto8\OneDrive\デスクトップ\興陽館共有フォルダ★★★2026_02_20\3 営業共有\営業\旧PCデスクトップ\ph"),
]

# 正しいファイル名＝13桁の数字（ISBN）だけを採用する
ISBN_RE = re.compile(r"^\d{13}$")

# 1) OneDrive の画像を、リポジトリの ph へコピー（まだ無いものだけ）
copied = 0
for folder in ONEDRIVE:
    if not folder.exists():
        continue
    for jpg in folder.glob("*.jpg"):
        dst = REPO_PH / jpg.name
        if not dst.exists():
            shutil.copy2(jpg, dst)
            copied += 1
            print(f"  + {jpg.name}")

# 2) 索引は repo の ph フォルダから作る。
#    ただし「13桁の数字」のファイル名だけを採用（_500px・12桁などの誤名は自動で無視）
valid = []
skipped = []
for f in REPO_PH.glob("*.jpg"):
    if ISBN_RE.match(f.stem):
        valid.append(f.stem)
    else:
        skipped.append(f.name)

isbns = sorted(set(valid))
(ROOT / "docs").mkdir(exist_ok=True)
with open(ROOT / "docs" / "isbn_list.json", "w", encoding="utf-8") as fp:
    json.dump(isbns, fp)

print(f"完了: 新規コピー {copied}件 / 索引 {len(isbns)}件（13桁ISBNのみ）")
if skipped:
    print(f"※ 誤ったファイル名のため索引から除外: {len(skipped)}件 -> {skipped}")
