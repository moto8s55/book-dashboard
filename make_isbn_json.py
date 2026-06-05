import json
import pathlib

ph1 = pathlib.Path(r'C:\Users\moto8\OneDrive\ph')
ph2 = pathlib.Path(r'C:\Users\moto8\OneDrive\デスクトップ\興陽館共有フォルダ★★★2026_02_20\3 営業共有\営業\旧PCデスクトップ\ph')

files = list(ph1.glob('*.jpg')) + list(ph2.glob('*.jpg'))
isbns = list(set([f.stem for f in files]))

with open(r'C:\Users\moto8\Documents\GitHub\book-dashboard\docs\isbn_list.json', 'w') as fp:
    json.dump(sorted(isbns), fp)

print(f'完了: {len(isbns)}件')