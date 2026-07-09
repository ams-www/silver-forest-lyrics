import glob
import os

# 現在のディレクトリのすべての.mdファイルを取得
files = glob.glob('*.md')

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 1行ずつ読み込んで、末尾に改行がなければ追加して、さらに空行を追加する
    new_lines = []
    for line in lines:
        stripped = line.rstrip()
        if stripped:
            new_lines.append(stripped + '\n\n')
        else:
            new_lines.append('\n')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("すべてのmdファイルの改行を調整したよ！")