# -*- coding: utf-8 -*-
with open('search.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. <head> に <base target="_top"> を追加
if '<base target="_top">' not in content:
    content = content.replace('<head>', '<head>\n    <base target="_top">', 1)

# 2. loadInitialData に gasData の処理を追加
old_load = """    // データの読み込み初期化
    function loadInitialData() {
        fetch('Data.csv')"""

new_load = """    // GASテンプレート変数（GAS実行時に渡される）
    let gasData = null;
    try {
        gasData = <?!= (typeof data !== 'undefined' && data) ? JSON.stringify(data) : 'null' ?>;
    } catch(e) {
        gasData = null;
    }

    // データの読み込み初期化
    function loadInitialData() {
        if (gasData && Array.isArray(gasData) && gasData.length > 0) {
            if (Array.isArray(gasData[0])) {
                const headers = gasData[0].map(h => String(h).trim());
                const parsed = [];
                for (let i = 1; i < gasData.length; i++) {
                    const row = gasData[i];
                    if (row.length === 1 && row[0] === '') continue;
                    const item = {};
                    for (let j = 0; j < headers.length; j++) {
                        item[headers[j]] = (row[j] !== undefined && row[j] !== null) ? String(row[j]) : '';
                    }
                    parsed.push(item);
                }
                setData(parsed, 'Spreadsheet Data (' + parsed.length + ' records)');
                return;
            } else if (typeof gasData[0] === 'object') {
                setData(gasData, 'Spreadsheet Data (' + gasData.length + ' records)');
                return;
            }
        }

        fetch('Data.csv')"""

if old_load in content:
    content = content.replace(old_load, new_load, 1)
    print("old_load replaced successfully")
else:
    # 改行コードの差異 (CRLF vs LF) を考慮
    old_load_crlf = old_load.replace('\n', '\r\n')
    new_load_crlf = new_load.replace('\n', '\r\n')
    if old_load_crlf in content:
        content = content.replace(old_load_crlf, new_load_crlf, 1)
        print("old_load_crlf replaced successfully")
    else:
        print("ERROR: old_load not found in search.html")
        exit(1)

with open('gas/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("gas/index.html updated successfully")
