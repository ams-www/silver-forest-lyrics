import re
import os
from collections import defaultdict

lyrics_dir = "/workspace/Lyrics"
vocal_counts = defaultdict(int)

# パターンの定義
patterns = [
    r'^歌：\s*(.+)$',
    r'^vocal[：:]\s*(.+)$'
]

# 除外パターン（括弧書きなど）
exclude_patterns = [
    r'^\(.*\)$',  # 括弧のみのもの
    r'^[A-Z][a-z]*\)$',  # 閉じ括弧で終わるもの
    r'^先手必勝一撃必殺$',
    r'^SOUND$',
    r'^HOLIC\)$',
    r'^Silver$',
    r'^FataMorgana\)$',
    r'^Dolphin$',
    r'^Time\)$',
    r'^ロリコンの地位向上\)$',
    r'^Alternative$',
    r'^ending\)$',
    r'^ichiko\)$',
]

def should_exclude(name):
    for pattern in exclude_patterns:
        if re.match(pattern, name):
            return True
    return False

for filename in os.listdir(lyrics_dir):
    if not filename.endswith('.md'):
        continue
    
    filepath = os.path.join(lyrics_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for line in content.split('\n'):
        for pattern in patterns:
            match = re.match(pattern, line.strip())
            if match:
                vocal_str = match.group(1).strip()
                
                # カンマ、全角スペース、半角スペース、タブで分割
                vocals = re.split(r'[, 　\t]+', vocal_str)
                
                for vocal in vocals:
                    vocal = vocal.strip()
                    # 括弧を除去
                    vocal = re.sub(r'\([^)]*\)', '', vocal).strip()
                    
                    if vocal and not should_exclude(vocal):
                        vocal_counts[vocal] += 1
                break

# ソートして出力
sorted_vocals = sorted(vocal_counts.items(), key=lambda x: -x[1])

print("=== ボーカル一覧（出現回数順） ===")
print(f"総計 {len(sorted_vocals)} 名のボーカリスト")
print(f"延べ {sum(vocal_counts.values())} 回の歌唱参加\n")

for i, (name, count) in enumerate(sorted_vocals, 1):
    print(f"{i:3}. {name}: {count}回")
