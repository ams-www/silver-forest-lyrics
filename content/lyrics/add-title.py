import os
import glob

# カレントディレクトリのすべての .md ファイルを対象にする
for filepath in glob.glob("*.md"):
    # 拡張子を除いたファイル名をタイトルとして取得
    filename = os.path.basename(filepath)
    title = os.path.splitext(filename)[0]

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # すでにフロントマター（---で始まる）がついているかチェック
    if content.startswith("---"):
        print(f"Skipped (already has frontmatter): {filepath}")
        continue

    # 新しいフロントマター付きの内容を作成
    new_content = f"---\ntitle: \"{title}\"\n---\n\n{content}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Added title to: {filepath}")