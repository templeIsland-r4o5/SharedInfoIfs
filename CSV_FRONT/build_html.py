import json
import csv
import re

# 1. Data.csv の読み込み
with open('Data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

embedded_json = json.dumps(rows, ensure_ascii=False)

# 2. 既存の search.html のフォーム部分を読み込み（ベースとなるマークアップ）
# 元の search.html に日付 placeholder を付与
with open('search.html', 'r', encoding='utf-8') as f:
    original_html = f.read()

# フォーム部分の抽出
start_tag = '<div class="panel table-panel">'
end_tag = '<!-- /.panel-body -->\n</div>'
start_idx = original_html.find(start_tag)
end_idx = original_html.find(end_tag)

if start_idx != -1 and end_idx != -1:
    original_search_html = original_html[start_idx:end_idx + len(end_tag)]
else:
    original_search_html = original_html

# Bootstrap Select のメニューは初期状態で閉じる。クリック時のみ JS で親 .bootstrap-select に open を付与する。
original_search_html = original_search_html.replace('class="dropdown-menu open"', 'class="dropdown-menu"')

# 日付入力欄に placeholder="YYYY/MM/DD" を追加（再生成しても重複しないように制御）
for field_id in ['createDateFrom', 'createDateTo', 'updateDateFrom', 'updateDateTo']:
    id_name = f'id="{field_id}" name="{field_id}"'
    original_search_html = re.sub(
        rf'{id_name}(?: placeholder="YYYY/MM/DD")+',
        f'{id_name} placeholder="YYYY/MM/DD"',
        original_search_html
    )
    original_search_html = re.sub(
        rf'{id_name}(?! placeholder="YYYY/MM/DD")',
        f'{id_name} placeholder="YYYY/MM/DD"',
        original_search_html
    )

# モダンUIでは旧レイアウトの列見出しとチェックボックスが離れて見えるため、各チェックボックスに明示ラベルを付与
checkbox_label_map = {
    'importFromReportDone': 'Report',
    'importFromMightyDone': 'MntPLN',
    'notimportFromReportNone': 'Report',
    'notimportFromMightyNone': 'MntPLN',
    'exportFromReportDone': 'Report',
    'exportFromMightyDone': 'MntPLN',
    'notexportFromReportNone': 'Report',
    'notexportFromMightyNone': 'MntPLN',
}
for checkbox_id, checkbox_label in checkbox_label_map.items():
    original_search_html = re.sub(
        rf'<input type="checkbox" id="{checkbox_id}"(?: aria-label="[^"]*")?>\s*'
        rf'(?:<label class="control-label checkbox-field-label" for="{checkbox_id}">.*?</label>\s*)?',
        f'<input type="checkbox" id="{checkbox_id}" aria-label="{checkbox_label}">\n'
        f'                            <label class="control-label checkbox-field-label" for="{checkbox_id}">{checkbox_label}</label>',
        original_search_html,
        flags=re.S
    )

# 空白だけに見えるプルダウン項目を、用途ごとの明示ラベルに置換
blank_select_label_map = {
    'todayTr': 'All',
    'airportCode': 'All',
    'status': 'All',
    'keyword1': 'All',
    'ataNo': 'All',
    'priority': 'All',
    'recordLevel': 'All',
    'sortKey1': 'No Sort',
    'sortKey2': 'No Sort',
}
for select_name, blank_label in blank_select_label_map.items():
    select_match = re.search(
        rf'(<div class="btn-group bootstrap-select[\s\S]*?<select\b[^>]*name="{select_name}"[\s\S]*?</select>\s*</div>)',
        original_search_html
    )
    if not select_match:
        continue
    block = select_match.group(1)
    block = re.sub(
        r'<span class="filter-option pull-left">(?:&nbsp;|\s*)</span>',
        f'<span class="filter-option pull-left">{blank_label}</span>',
        block,
        count=1
    )
    block = re.sub(
        r'title="(?:&amp;nbsp;|&nbsp;|\s*)"',
        f'title="{blank_label}"',
        block,
        count=1
    )
    block = re.sub(
        r'<span class="text">(?:&nbsp;|\s*)</span>',
        f'<span class="text">{blank_label}</span>',
        block,
        count=1
    )
    block = re.sub(
        r'(<option\b[^>]*value=""[^>]*>)(?:&nbsp;|\s*)(</option>)',
        rf'\1{blank_label}\2',
        block,
        count=1
    )
    original_search_html = original_search_html[:select_match.start(1)] + block + original_search_html[select_match.end(1):]

# 旧レイアウトで余白扱いだった空ラベルを、モダンUIでは意味が分かる見出しに置換
original_search_html = original_search_html.replace(
    '<label class="control-label w100 "></label>\n                        <input type="radio" id="radioAND"',
    '<label class="control-label w100 ">Match Mode</label>\n                        <input type="radio" id="radioAND"'
)
original_search_html = original_search_html.replace(
    '<label class="control-label w100"></label>\n                        <button id="ShipMonitorListSearchBtn"',
    '<label class="control-label w100">Actions</label>\n                        <button id="ShipMonitorListSearchBtn"'
)

def replace_parent_form_group(html, marker, replacement):
    marker_idx = html.find(marker)
    if marker_idx == -1:
        return html
    start_idx = html.rfind('<div class="form-group', 0, marker_idx)
    if start_idx == -1:
        return html

    token_re = re.compile(r'</?div\b[^>]*>', re.I)
    depth = 0
    end_idx = None
    for token in token_re.finditer(html, start_idx):
        if token.group(0).lower().startswith('</div'):
            depth -= 1
            if depth == 0:
                end_idx = token.end()
                break
        else:
            depth += 1
    if end_idx is None:
        return html
    return html[:start_idx] + replacement + html[end_idx:]

def remove_parent_form_group(html, marker):
    return replace_parent_form_group(html, marker, '')

def io_filter_group(title, subtitle, mode_class, first_id, first_label, operator, second_id, second_label):
    return f'''<div class="form-group io-filter-group {mode_class}">
                        <div class="io-filter-title">
                            <span class="io-filter-title-main">{title}</span>
                            <span class="io-filter-title-sub">{subtitle}</span>
                        </div>
                        <div class="io-filter-options">
                            <label class="io-check-option" for="{first_id}">
                                <input type="checkbox" id="{first_id}" aria-label="{first_label}">
                                <span>{first_label}</span>
                            </label>
                            <span class="io-filter-operator">{operator}</span>
                            <label class="io-check-option" for="{second_id}">
                                <input type="checkbox" id="{second_id}" aria-label="{second_label}">
                                <span>{second_label}</span>
                            </label>
                        </div>
                    </div>'''

# 旧UIの列見出しだけのブロックは、チェックボックスカード内の見出しに統合
original_search_html = remove_parent_form_group(original_search_html, '<h3 class="panel-title">Import Filter</h3>')
original_search_html = remove_parent_form_group(original_search_html, '<h3 class="panel-title">Export Filter</h3>')

# Import / Export 系チェックボックスを、個別フィールドではなく1つのまとまったカードUIへ再構成
original_search_html = replace_parent_form_group(
    original_search_html,
    'id="importFromReportDone"',
    io_filter_group('Import Filter', 'Imported records', 'import-done-filter', 'importFromReportDone', 'Report', 'OR', 'importFromMightyDone', 'MntPLN')
)
original_search_html = replace_parent_form_group(
    original_search_html,
    'id="notimportFromReportNone"',
    io_filter_group('Not Import', 'Records not imported', 'import-none-filter', 'notimportFromReportNone', 'Report', 'OR', 'notimportFromMightyNone', 'MntPLN')
)
original_search_html = replace_parent_form_group(
    original_search_html,
    'id="exportFromReportDone"',
    io_filter_group('Export Filter', 'Exported records', 'export-done-filter', 'exportFromReportDone', 'Report', 'AND', 'exportFromMightyDone', 'MntPLN')
)
original_search_html = replace_parent_form_group(
    original_search_html,
    'id="notexportFromReportNone"',
    io_filter_group('Not Export', 'Records not exported', 'export-none-filter', 'notexportFromReportNone', 'Report', 'AND', 'notexportFromMightyNone', 'MntPLN')
)

# 3. 完全なHTMLドキュメントの構築
html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ship Monitor Search</title>
    <!-- Bootstrap 3.3.7 & FontAwesome 4.7.0 CDN -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    
    <style>

        :root {{
            --bg: #eef3fb;
            --bg-accent: #dbeafe;
            --surface: rgba(255, 255, 255, 0.92);
            --surface-solid: #ffffff;
            --surface-muted: #f8fafc;
            --text: #172033;
            --muted: #64748b;
            --line: #d8e2f0;
            --line-soft: #edf2f7;
            --primary: #2563eb;
            --primary-dark: #1e40af;
            --primary-soft: #e8f0ff;
            --success: #059669;
            --success-soft: #dcfce7;
            --danger: #dc2626;
            --warning: #f59e0b;
            --shadow-sm: 0 8px 22px rgba(15, 23, 42, 0.08);
            --shadow-md: 0 18px 45px rgba(15, 23, 42, 0.14);
            --radius: 18px;
            --radius-sm: 12px;
        }}

        * {{ box-sizing: border-box; }}

        html {{ min-height: 100%; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Meiryo", sans-serif;
            min-height: 100vh;
            margin: 0;
            padding: 24px;
            font-size: 13px;
            color: var(--text);
            background:
                radial-gradient(circle at 0% 0%, rgba(37, 99, 235, 0.18), transparent 28%),
                radial-gradient(circle at 100% 8%, rgba(14, 165, 233, 0.18), transparent 30%),
                linear-gradient(135deg, #f8fbff 0%, var(--bg) 52%, #f6f8fc 100%);
        }}

        body::before {{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(37, 99, 235, 0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(37, 99, 235, 0.04) 1px, transparent 1px);
            background-size: 36px 36px;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,0.75), transparent 75%);
        }}

        .container-fluid {{
            position: relative;
            max-width: 1680px;
            margin: 0 auto;
            padding: 0;
        }}

        .top-header-bar {{
            position: sticky;
            top: 16px;
            z-index: 20;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            min-height: 82px;
            margin-bottom: 22px;
            padding: 20px 24px;
            overflow: hidden;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(30, 64, 175, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 24px;
            box-shadow: var(--shadow-md);
            color: #fff;
        }}

        .top-header-bar::after {{
            content: "";
            position: absolute;
            right: -90px;
            top: -130px;
            width: 320px;
            height: 320px;
            border-radius: 999px;
            background: rgba(96, 165, 250, 0.22);
        }}

        .top-header-title {{
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 13px;
            margin: 0;
            color: #fff;
            font-size: 23px;
            font-weight: 800;
            letter-spacing: 0.01em;
        }}

        .top-header-title .fa {{
            display: inline-grid;
            place-items: center;
            width: 42px;
            height: 42px;
            color: #dbeafe;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.24);
            border-radius: 14px;
        }}

        .top-header-actions {{
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .data-status-badge {{
            display: inline-flex;
            align-items: center;
            max-width: min(520px, 72vw);
            min-height: 34px;
            padding: 7px 13px;
            overflow: hidden;
            border-radius: 999px;
            border: 1px solid rgba(191, 219, 254, 0.4);
            background: rgba(255, 255, 255, 0.14);
            color: #eff6ff;
            font-size: 12px;
            font-weight: 700;
            text-overflow: ellipsis;
            white-space: nowrap;
            backdrop-filter: blur(10px);
        }}

        .btn {{
            border-radius: 999px !important;
            border: 1px solid transparent;
            font-weight: 700;
            letter-spacing: 0.01em;
            transition: transform .15s ease, box-shadow .15s ease, background .15s ease, border-color .15s ease;
        }}

        .btn:hover:not(:disabled) {{
            transform: translateY(-1px);
            box-shadow: 0 10px 20px rgba(15, 23, 42, 0.12);
        }}

        .btn:active:not(:disabled) {{ transform: translateY(0); }}

        .btn-sm {{ padding: 7px 13px; }}
        .btn-xs {{ padding: 5px 10px; font-size: 11px; }}

        .btn-default {{
            color: #1f2a44;
            background: #fff;
            border-color: #d9e3f0;
        }}

        .btn-default:hover,
        .btn-default:focus {{
            color: var(--primary-dark);
            background: #f8fbff;
            border-color: #b7ccf5;
        }}

        .btn-primary {{
            color: #fff;
            background: linear-gradient(135deg, var(--primary), #1d4ed8);
            border-color: rgba(37, 99, 235, 0.6);
        }}

        .btn-success {{
            color: #fff;
            background: linear-gradient(135deg, #10b981, #059669);
            border-color: rgba(5, 150, 105, 0.7);
        }}

        .btn[disabled],
        button:disabled {{
            cursor: not-allowed !important;
            opacity: .52;
            box-shadow: none !important;
            transform: none !important;
        }}

        .panel.table-panel,
        .results-panel {{
            overflow: hidden;
            margin-bottom: 22px;
            background: var(--surface);
            border: 1px solid rgba(216, 226, 240, 0.88);
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(12px);
        }}

        .panel.table-panel,
        .panel.table-panel .panel-body,
        .panel.table-panel .collapse.in {{
            overflow: visible;
        }}

        .panel-heading,
        .results-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            min-height: 58px;
            padding: 15px 18px;
            border-bottom: 1px solid var(--line-soft);
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        }}

        .panel-title {{
            width: 100%;
            margin: 0;
            font-size: 15px;
            font-weight: 800;
        }}

        .panel-title a {{
            display: flex;
            align-items: center;
            gap: 9px;
            min-height: 34px;
            padding-right: 190px;
            color: #0f172a;
            text-decoration: none;
            cursor: pointer;
        }}

        .panel-title a::before {{
            content: "\\f002";
            display: inline-grid;
            place-items: center;
            width: 34px;
            height: 34px;
            color: var(--primary);
            background: var(--primary-soft);
            border-radius: 11px;
            font-family: FontAwesome;
            font-size: 14px;
        }}

        .panel-title a:hover {{ color: var(--primary-dark); }}

        .panel-title .pull-right {{
            order: 10;
            margin-left: auto;
            color: var(--muted);
        }}

        #ShipMonitorListRenewBtn {{
            top: 12px !important;
            left: auto !important;
            right: 18px !important;
            min-width: 118px;
            height: 36px;
            padding: 7px 16px;
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.18);
        }}

        .panel-body {{ padding: 20px; }}

        #submitForm {{
            display: flex;
            flex-wrap: wrap;
            align-items: flex-start;
            justify-content: center;
            gap: 14px 16px;
            max-width: 1280px;
            margin: 0 auto;
        }}

        .form-search-condition {{
            display: contents;
            flex-wrap: wrap;
            align-items: stretch;
            justify-content: center;
            gap: 12px;
            margin: 0;
            padding: 0;
        }}

        .form-group {{
            display: inline-flex;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 8px 10px;
            min-width: 280px;
            max-width: 100%;
            min-height: 78px;
            margin: 0;
            padding: 12px 14px;
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            border: 1px solid var(--line-soft);
            border-radius: var(--radius-sm);
            box-shadow: 0 7px 18px rgba(15, 23, 42, 0.05);
        }}

        .form-group:focus-within {{
            border-color: rgba(37, 99, 235, 0.45);
            background: #fff;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.08);
        }}

        .form-group.w480,
        .form-group.w430,
        .form-group.w400,
        .form-group.w380,
        .form-group.w360,
        .form-group.w330,
        .form-group.w310,
        .form-group.w300,
        .form-group.w290,
        .form-group.w280,
        .form-group.w270,
        .form-group.w260,
        .form-group.w250,
        .form-group.w240,
        .form-group.w230,
        .form-group.w220,
        .form-group.w210,
        .form-group.w200,
        .form-group.w190,
        .form-group.w180,
        .form-group.w170,
        .form-group.w160,
        .form-group.w150,
        .form-group.w140,
        .form-group.w130,
        .form-group.w120,
        .form-group.w110,
        .form-group.w100,
        .form-group.w90,
        .form-group.w80,
        .form-group.w70,
        .form-group.w60,
        .form-group.w50,
        .form-group.w40,
        .form-group.w30,
        .form-group.w20,
        .form-group.w10 {{
            width: auto !important;
        }}

        .control-label {{
            display: flex;
            align-items: center;
            flex: 0 0 100%;
            width: 100% !important;
            margin: 0 0 2px;
            padding: 0 0 7px;
            color: #1e3a8a;
            border-bottom: 1px dashed #d8e2f0;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: .03em;
            text-transform: uppercase;
            white-space: nowrap;
        }}

        .control-label::before {{
            content: "";
            width: 7px;
            height: 7px;
            margin-right: 7px;
            background: var(--primary);
            border-radius: 999px;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.11);
        }}

        .form-control,
        input.form-control,
        select.form-control,
        textarea.form-control,
        .btn-group.bootstrap-select.form-control > .btn {{
            min-height: 34px;
            padding: 7px 10px;
            color: #162033;
            background: #fff;
            border: 1px solid #cfd9e8;
            border-radius: 10px !important;
            box-shadow: none;
            font-size: 12px;
            transition: border-color .15s ease, box-shadow .15s ease, background .15s ease;
        }}

        .form-control:focus,
        .btn-group.bootstrap-select.open > .btn,
        .btn-group.bootstrap-select.form-control > .btn:focus {{
            border-color: var(--primary);
            outline: 0;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.11);
        }}

        input::placeholder {{ color: #94a3b8; }}

        .input-daterange {{ display: inline-flex; align-items: center; gap: 7px; }}
        .radio-inline, .checkbox-inline {{ font-weight: 600; color: #334155; }}
        input[type="radio"], input[type="checkbox"] {{ accent-color: var(--primary); }}

        .checkbox-field-label {{
            flex: 0 0 auto;
            width: auto !important;
            margin-left: 6px;
            margin-right: 0;
            padding: 0;
            color: #334155;
            border-bottom: 0;
            font-size: 11px;
            font-weight: 800;
            text-transform: none;
            letter-spacing: 0;
            cursor: pointer;
        }}

        .checkbox-field-label::before {{ content: none; }}

        .io-filter-group {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: nowrap;
            gap: 14px;
            min-width: 360px;
            padding: 12px 14px;
            background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
            border: 1px solid rgba(191, 219, 254, 0.9);
            border-radius: 16px;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.06);
        }}

        .io-filter-title {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            min-width: 112px;
        }}

        .io-filter-title-main {{
            color: #0f172a;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: .02em;
        }}

        .io-filter-title-sub {{
            color: #64748b;
            font-size: 10px;
            font-weight: 700;
        }}

        .io-filter-options {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }}

        .io-check-option {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            min-height: 34px;
            margin: 0;
            padding: 7px 10px;
            color: #1e293b;
            background: #fff;
            border: 1px solid #d8e2f0;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            cursor: pointer;
            transition: background .15s ease, border-color .15s ease, box-shadow .15s ease, transform .15s ease;
        }}

        .io-check-option:hover {{
            background: var(--primary-soft);
            border-color: #b7ccf5;
            transform: translateY(-1px);
        }}

        .io-check-option input {{
            margin: 0;
        }}

        .io-filter-operator {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 38px;
            min-height: 28px;
            padding: 4px 8px;
            color: #475569;
            background: #eef2f7;
            border-radius: 999px;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: .04em;
        }}

        .import-done-filter,
        .import-none-filter {{
            border-color: rgba(59, 130, 246, 0.32);
        }}

        .export-done-filter,
        .export-none-filter {{
            border-color: rgba(16, 185, 129, 0.32);
        }}

        .btn-group.bootstrap-select {{
            position: relative;
            display: inline-block;
            vertical-align: middle;
            background: transparent;
            border: 0;
            padding: 0;
            box-shadow: none;
        }}

        .btn-group.bootstrap-select.form-control {{ height: auto; min-height: 0; }}
        .btn-group.bootstrap-select > select.selectpicker,
        .btn-group.bootstrap-select > select.form-control {{
            display: none !important;
        }}
        .btn-group.bootstrap-select .dropdown-toggle {{ width: 100%; text-align: left; }}
        .btn-group.bootstrap-select .filter-option {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .btn-group.bootstrap-select .bs-caret {{ float: right; color: var(--muted); }}

        .btn-group.bootstrap-select .dropdown-menu {{
            display: none;
            position: absolute !important;
            top: calc(100% + 8px) !important;
            left: 0 !important;
            right: auto !important;
            bottom: auto !important;
            z-index: 3000;
            width: max(100%, min(420px, calc(100vw - 48px))) !important;
            min-width: min(280px, calc(100vw - 48px)) !important;
            max-width: calc(100vw - 48px) !important;
            max-height: min(720px, 82vh) !important;
            transform: none !important;
            padding: 10px;
            margin: 0;
            overflow: auto !important;
            background: #fff;
            border: 1px solid var(--line);
            border-radius: 16px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
        }}

        .btn-group.bootstrap-select.w60 .dropdown-menu,
        .btn-group.bootstrap-select.w80 .dropdown-menu,
        .btn-group.bootstrap-select.w100 .dropdown-menu,
        .btn-group.bootstrap-select.w120 .dropdown-menu,
        .btn-group.bootstrap-select.w130 .dropdown-menu {{
            width: min(360px, calc(100vw - 48px)) !important;
        }}

        .btn-group.bootstrap-select.w150 .dropdown-menu,
        .btn-group.bootstrap-select.w200 .dropdown-menu,
        .btn-group.bootstrap-select.w250 .dropdown-menu,
        .btn-group.bootstrap-select.w300 .dropdown-menu {{
            width: min(520px, calc(100vw - 48px)) !important;
        }}

        .btn-group.bootstrap-select.open > .dropdown-menu {{
            display: block !important;
            max-height: min(720px, 82vh) !important;
            overflow: auto !important;
        }}

        .btn-group.bootstrap-select .bs-searchbox {{ padding: 4px 4px 12px; }}
        .btn-group.bootstrap-select .bs-searchbox input {{ width: 100%; height: 40px; }}
        .btn-group.bootstrap-select .dropdown-menu.inner,
        .btn-group.bootstrap-select ul.dropdown-menu.inner,
        .dropdown-menu.inner {{
            position: static !important;
            display: block !important;
            width: 100% !important;
            max-height: min(620px, 70vh) !important;
            height: auto !important;
            padding: 0;
            margin: 0;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            border: 0;
            box-shadow: none;
        }}
        .dropdown-menu.inner li {{ list-style: none; }}
        .dropdown-menu.inner li a {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            min-height: 34px;
            padding: 8px 10px;
            color: #25324a;
            border-radius: 9px;
            text-decoration: none;
            cursor: pointer;
        }}
        .dropdown-menu.inner li a .text {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .dropdown-menu.inner li a:hover,
        .dropdown-menu.inner li.selected a {{ background: var(--primary-soft); color: var(--primary-dark); }}
        .dropdown-menu.inner .check-mark {{ color: var(--primary); }}

        .w10 {{ width: 10px !important; }}
        .w20 {{ width: 20px !important; }}
        .w30 {{ width: 30px !important; }}
        .w40 {{ width: 40px !important; }}
        .w50 {{ width: 50px !important; }}
        .w60 {{ width: 60px !important; }}
        .w70 {{ width: 70px !important; }}
        .w80 {{ width: 80px !important; }}
        .w90 {{ width: 90px !important; }}
        .w100 {{ width: 100px !important; }}
        .w110 {{ width: 110px !important; }}
        .w120 {{ width: 120px !important; }}
        .w130 {{ width: 130px !important; }}
        .w140 {{ width: 140px !important; }}
        .w150 {{ width: 150px !important; }}
        .w160 {{ width: 160px !important; }}
        .w170 {{ width: 170px !important; }}
        .w180 {{ width: 180px !important; }}
        .w190 {{ width: 190px !important; }}
        .w200 {{ width: 200px !important; }}
        .w210 {{ width: 210px !important; }}
        .w220 {{ width: 220px !important; }}
        .w230 {{ width: 230px !important; }}
        .w240 {{ width: 240px !important; }}
        .w250 {{ width: 250px !important; }}
        .w260 {{ width: 260px !important; }}
        .w270 {{ width: 270px !important; }}
        .w280 {{ width: 280px !important; }}
        .w290 {{ width: 290px !important; }}
        .w300 {{ width: 300px !important; }}
        .w310 {{ width: 310px !important; }}
        .w330 {{ width: 330px !important; }}
        .w360 {{ width: 360px !important; }}
        .w380 {{ width: 380px !important; }}
        .w400 {{ width: 400px !important; }}
        .w430 {{ width: 430px !important; }}
        .w480 {{ width: 480px !important; }}

        .inline-block {{ display: inline-block !important; }}
        .pull-right {{ float: right !important; }}
        .pull-left {{ float: left !important; }}
        .clearfix::after {{ content: ""; clear: both; display: table; }}
        .text-center {{ text-align: center !important; }}
        .text-right {{ text-align: right !important; }}
        .mr5 {{ margin-right: 5px !important; }}
        .mr10 {{ margin-right: 10px !important; }}
        .ml5 {{ margin-left: 5px !important; }}
        .mt-30 {{ margin-top: 30px !important; }}
        .mb-40 {{ margin-bottom: 40px !important; }}

        .submit-area,
        .button-area,
        .form-actions {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 18px;
            padding-top: 18px;
            border-top: 1px dashed var(--line);
        }}

        #ShipMonitorListSearchBtn,
        #ClearBtn {{
            min-width: 116px;
            min-height: 38px;
        }}

        .results-panel {{ background: var(--surface-solid); }}
        .results-header {{ padding: 16px 18px; }}
        .results-count {{
            display: inline-flex;
            align-items: center;
            gap: 9px;
            color: #0f172a;
            font-size: 16px;
            font-weight: 800;
        }}
        .results-count::before {{
            content: "\\f0ce";
            display: inline-grid;
            place-items: center;
            width: 32px;
            height: 32px;
            color: var(--success);
            background: var(--success-soft);
            border-radius: 10px;
            font-family: FontAwesome;
            font-size: 14px;
        }}
        .results-controls {{ display: flex; align-items: center; gap: 9px; color: var(--muted); font-weight: 700; }}
        .results-controls span {{ font-size: 12px !important; color: var(--muted) !important; }}
        #pageSizeSelect {{ width: 92px !important; height: 34px !important; padding: 6px 9px !important; font-size: 12px !important; }}

        .table-responsive-wrapper {{
            min-height: 260px;
            overflow-x: auto;
            background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
        }}

        .results-table {{
            width: 100%;
            min-width: 1120px;
            margin-bottom: 0;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 12px;
        }}

        .results-table thead th {{
            position: sticky;
            top: 0;
            z-index: 2;
            padding: 12px 10px;
            color: #475569;
            background: #f8fafc;
            border-bottom: 1px solid var(--line);
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .035em;
            white-space: nowrap;
        }}

        .results-table tbody td {{
            padding: 11px 10px;
            border-top: 1px solid #edf2f7;
            color: #25324a;
            vertical-align: middle;
        }}

        .results-table tbody tr {{ transition: background .12s ease, transform .12s ease; }}
        .results-table tbody tr:nth-child(even) {{ background: #fbfdff; }}
        .results-table tbody tr:hover {{ background: #eff6ff; }}
        .title-cell {{ max-width: 420px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 700; color: #172033; }}

        .status-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 54px;
            padding: 4px 8px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 800;
            line-height: 1;
            letter-spacing: .02em;
        }}
        .status-open {{ color: #075985; background: #e0f2fe; border: 1px solid #bae6fd; }}
        .status-close {{ color: #475569; background: #e2e8f0; border: 1px solid #cbd5e1; }}
        .priority-p1 {{ color: #991b1b; background: #fee2e2; border: 1px solid #fecaca; }}
        .priority-p2 {{ color: #92400e; background: #fef3c7; border: 1px solid #fde68a; }}
        .priority-p3 {{ color: #166534; background: #dcfce7; border: 1px solid #bbf7d0; }}

        .pagination-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            padding: 14px 18px;
            border-top: 1px solid var(--line-soft);
            background: #fff;
        }}
        .pagination-info {{ color: var(--muted); font-size: 12px; font-weight: 700; }}
        .pagination-nav {{ display: flex; flex-wrap: wrap; gap: 6px; padding: 0; margin: 0; list-style: none; }}
        .pagination-nav button {{
            min-width: 34px;
            min-height: 32px;
            padding: 5px 10px;
            color: #334155;
            background: #fff;
            border: 1px solid var(--line);
            border-radius: 10px;
            font-size: 12px;
            font-weight: 800;
            cursor: pointer;
            transition: all .14s ease;
        }}
        .pagination-nav button:hover:not(:disabled) {{ color: var(--primary-dark); background: var(--primary-soft); border-color: #b7ccf5; }}
        .pagination-nav button.active {{ color: #fff; background: var(--primary); border-color: var(--primary); box-shadow: 0 8px 16px rgba(37, 99, 235, 0.22); }}
        .pagination-nav button:disabled {{ opacity: 0.45; cursor: not-allowed; }}

        .custom-modal-backdrop {{
            display: none;
            position: fixed;
            inset: 0;
            z-index: 2000;
            align-items: center;
            justify-content: center;
            padding: 24px;
            background: rgba(15, 23, 42, 0.58);
            backdrop-filter: blur(8px);
        }}
        .custom-modal-backdrop.show {{ display: flex; }}
        .custom-modal-dialog {{
            width: min(1040px, 96vw);
            max-height: 92vh;
            overflow: hidden;
            background: #fff;
            border: 1px solid rgba(255,255,255,.4);
            border-radius: 22px;
            box-shadow: 0 28px 80px rgba(15, 23, 42, 0.38);
        }}
        .custom-modal-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            padding: 18px 22px;
            color: #fff;
            background: linear-gradient(135deg, #0f172a, #1d4ed8);
        }}
        .custom-modal-title {{ margin: 0; font-size: 18px; font-weight: 800; }}
        .custom-modal-close {{
            width: 36px;
            height: 36px;
            color: #fff;
            background: rgba(255,255,255,.14);
            border: 1px solid rgba(255,255,255,.24);
            border-radius: 12px;
            font-size: 24px;
            line-height: 1;
            cursor: pointer;
        }}
        .custom-modal-body {{ max-height: calc(92vh - 132px); padding: 20px 22px; overflow-y: auto; background: #f8fafc; }}
        .custom-modal-footer {{ padding: 14px 22px; text-align: right; background: #fff; border-top: 1px solid var(--line-soft); }}
        .detail-meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 10px;
            margin-bottom: 16px;
        }}
        .detail-meta-item {{
            padding: 11px 12px;
            background: #fff;
            border: 1px solid var(--line-soft);
            border-radius: 13px;
            font-size: 12px;
        }}
        .detail-meta-label {{ display: block; margin-bottom: 3px; color: var(--muted); font-size: 10px; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }}
        .detail-meta-value {{ color: #172033; font-weight: 800; }}
        .detail-block {{ margin-bottom: 16px; }}
        .detail-block-title {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            color: #172033;
            font-size: 13px;
            font-weight: 800;
        }}
        .detail-block-title::before {{ content: ""; width: 9px; height: 9px; border-radius: 999px; background: var(--primary); box-shadow: 0 0 0 4px rgba(37,99,235,.12); }}
        .detail-block-content {{
            max-height: 280px;
            overflow-y: auto;
            padding: 13px 14px;
            color: #25324a;
            background: #fff;
            border: 1px solid var(--line-soft);
            border-radius: 14px;
            font-size: 12px;
            line-height: 1.7;
            white-space: pre-wrap;
            word-break: break-word;
        }}

        body.dragover {{
            background:
                radial-gradient(circle at 50% 12%, rgba(37, 99, 235, 0.32), transparent 34%),
                linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        }}

        @media (max-width: 900px) {{
            body {{ padding: 14px; }}
            .top-header-bar {{ position: static; padding: 18px; border-radius: 20px; }}
            .top-header-title {{ font-size: 19px; }}
            .panel-title a {{ padding-right: 0; }}
            #ShipMonitorListRenewBtn {{ position: static !important; margin-top: 10px; }}
            .form-group {{ width: 100% !important; align-items: flex-start; }}
            .io-filter-group {{
                min-width: 0;
                align-items: flex-start;
                flex-direction: column;
            }}
            .io-filter-options {{ justify-content: flex-start; }}
            .btn-group.bootstrap-select .dropdown-menu,
            .btn-group.bootstrap-select.w60 .dropdown-menu,
            .btn-group.bootstrap-select.w80 .dropdown-menu,
            .btn-group.bootstrap-select.w100 .dropdown-menu,
            .btn-group.bootstrap-select.w120 .dropdown-menu,
            .btn-group.bootstrap-select.w130 .dropdown-menu,
            .btn-group.bootstrap-select.w150 .dropdown-menu,
            .btn-group.bootstrap-select.w200 .dropdown-menu,
            .btn-group.bootstrap-select.w250 .dropdown-menu,
            .btn-group.bootstrap-select.w300 .dropdown-menu {{
                width: min(420px, calc(100vw - 32px));
                min-width: min(260px, calc(100vw - 32px));
                max-width: calc(100vw - 32px);
            }}
            .control-label {{ width: 100% !important; }}
            .results-header, .pagination-container {{ align-items: flex-start; flex-direction: column; }}
        }}
    </style>
</head>
<body>

<div class="container-fluid">
    <!-- トップヘッダーバー -->
    <div class="top-header-bar">
        <h1 class="top-header-title">
            <i class="fa fa-plane" aria-hidden="true"></i> Ship Monitor CSV Search
        </h1>
        <div class="top-header-actions">
            <span id="dataStatusBadge" class="data-status-badge">
                <i class="fa fa-database mr5"></i>Loading Data...
            </span>
            <label class="btn btn-default btn-sm" style="margin: 0; cursor: pointer;">
                <i class="fa fa-folder-open-o mr5"></i>CSVファイル選択
                <input type="file" id="csvFileInput" accept=".csv" style="display: none;">
            </label>
            <button id="exportCsvBtn" type="button" class="btn btn-success btn-sm">
                <i class="fa fa-download mr5"></i>CSVエクスポート
            </button>
        </div>
    </div>

    <!-- 検索条件パネル (既存 search.html) -->
{original_search_html}

    <!-- 検索結果パネル -->
    <div class="results-panel">
        <div class="results-header">
            <div class="results-count" id="resultsCount">
                検索結果: 0 件
            </div>
            <div class="results-controls">
                <span style="font-size: 12px; color: #64748b;">表示件数:</span>
                <select id="pageSizeSelect" class="form-control" style="width: 80px; height: 28px; padding: 2px 5px; font-size: 12px;">
                    <option value="20" selected>20件</option>
                    <option value="50">50件</option>
                    <option value="100">100件</option>
                    <option value="all">全件</option>
                </select>
            </div>
        </div>
        
        <div class="table-responsive-wrapper">
            <table class="table results-table" id="resultsTable">
                <thead>
                    <tr>
                        <th style="width: 40px; text-align: center;">No.</th>
                        <th style="width: 100px;">Ship Monitor No</th>
                        <th style="width: 90px;">Ship Type</th>
                        <th style="width: 80px;">Ship No.</th>
                        <th style="width: 70px;">Station</th>
                        <th style="width: 60px;">ATA</th>
                        <th style="width: 60px;">Priority</th>
                        <th style="width: 60px;">Level</th>
                        <th style="width: 70px;">Status</th>
                        <th>Title</th>
                        <th style="width: 70px;">From</th>
                        <th style="width: 90px;">Created At</th>
                        <th style="width: 90px;">Updated At</th>
                        <th style="width: 60px; text-align: center;">Action</th>
                    </tr>
                </thead>
                <tbody id="resultsTableBody">
                    <!-- 動的行生成 -->
                </tbody>
            </table>
        </div>
        
        <div class="pagination-container">
            <div class="pagination-info" id="paginationInfo">
                0 - 0 / 0 件中
            </div>
            <ul class="pagination-nav" id="paginationNav">
                <!-- 動的ページネーションボタン -->
            </ul>
        </div>
    </div>
</div>

<!-- 詳細モーダルダイアログ -->
<div id="detailModal" class="custom-modal-backdrop">
    <div class="custom-modal-dialog">
        <div class="custom-modal-header">
            <h4 class="custom-modal-title" id="modalTitleText">
                <i class="fa fa-info-circle mr5"></i>Ship Monitor Detail
            </h4>
            <button type="button" class="custom-modal-close" id="modalCloseBtn">&times;</button>
        </div>
        <div class="custom-modal-body">
            <!-- メタ情報グリッド -->
            <div class="detail-meta-grid" id="modalMetaGrid">
                <!-- 動的生成 -->
            </div>
            
            <!-- タイトル -->
            <div class="detail-block">
                <div class="detail-block-title">Title</div>
                <div class="detail-block-content" id="modalDetailTitle" style="max-height: 80px; font-weight: bold;"></div>
            </div>

            <!-- 不具合・処置詳細 (Description) -->
            <div class="detail-block">
                <div class="detail-block-title">Description</div>
                <div class="detail-block-content" id="modalDetailDescription"></div>
            </div>

            <!-- メモ (Memo) -->
            <div class="detail-block">
                <div class="detail-block-title">Memo</div>
                <div class="detail-block-content" id="modalDetailMemo"></div>
            </div>
        </div>
        <div class="custom-modal-footer">
            <button type="button" class="btn btn-default" id="modalCloseFooterBtn">閉じる</button>
        </div>
    </div>
</div>

<!-- アプリケーションスクリプト -->
<script>
(function() {{
    'use strict';

    // 1. 初期内包データ (Data.csv 由来の1000レコード)
    const EMBEDDED_DATA = {embedded_json};

    // 状態管理変数
    let rawDataList = [];
    let filteredDataList = [];
    let currentPage = 1;
    let pageSize = 20;

    // DOM要素の参照
    const submitForm = document.getElementById('submitForm');
    const searchBtn = document.getElementById('ShipMonitorListSearchBtn');
    const clearBtn = document.getElementById('ClearBtn');
    const renewBtn = document.getElementById('ShipMonitorListRenewBtn');
    const toggleBtn = document.getElementById('ShipMonitorListToggle');
    const searchCollapse = document.getElementById('ShipMonitorSearch');
    const resultsTableBody = document.getElementById('resultsTableBody');
    const resultsCount = document.getElementById('resultsCount');
    const paginationInfo = document.getElementById('paginationInfo');
    const paginationNav = document.getElementById('paginationNav');
    const pageSizeSelect = document.getElementById('pageSizeSelect');
    const dataStatusBadge = document.getElementById('dataStatusBadge');
    const csvFileInput = document.getElementById('csvFileInput');
    const exportCsvBtn = document.getElementById('exportCsvBtn');

    // 詳細モーダル要素
    const detailModal = document.getElementById('detailModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalCloseFooterBtn = document.getElementById('modalCloseFooterBtn');
    const modalTitleText = document.getElementById('modalTitleText');
    const modalMetaGrid = document.getElementById('modalMetaGrid');
    const modalDetailTitle = document.getElementById('modalDetailTitle');
    const modalDetailDescription = document.getElementById('modalDetailDescription');
    const modalDetailMemo = document.getElementById('modalDetailMemo');

    // RFC 4180 準拠のCSVパーサー
    function parseCSV(text) {{
        if (text.charCodeAt(0) === 0xFEFF) {{
            text = text.slice(1);
        }}
        const rows = [];
        let row = [];
        let inQuotes = false;
        let token = '';

        for (let i = 0; i < text.length; i++) {{
            const c = text[i];
            const next = text[i + 1];

            if (inQuotes) {{
                if (c === '"' && next === '"') {{
                    token += '"';
                    i++;
                }} else if (c === '"') {{
                    inQuotes = false;
                }} else {{
                    token += c;
                }}
            }} else {{
                if (c === '"') {{
                    inQuotes = true;
                }} else if (c === ',') {{
                    row.push(token);
                    token = '';
                }} else if (c === '\\r' && next === '\\n') {{
                    row.push(token);
                    rows.push(row);
                    row = [];
                    token = '';
                    i++;
                }} else if (c === '\\n' || c === '\\r') {{
                    row.push(token);
                    rows.push(row);
                    row = [];
                    token = '';
                }} else {{
                    token += c;
                }}
            }}
        }}
        if (token || row.length > 0) {{
            row.push(token);
            rows.push(row);
        }}
        if (rows.length === 0) return [];

        const headers = rows[0].map(h => h.trim());
        const data = [];
        for (let i = 1; i < rows.length; i++) {{
            const r = rows[i];
            if (r.length === 1 && r[0] === '') continue;
            const obj = {{}};
            for (let j = 0; j < headers.length; j++) {{
                obj[headers[j]] = (r[j] !== undefined) ? r[j] : '';
            }}
            data.push(obj);
        }}
        return data;
    }}

    // データの読み込み初期化
    function loadInitialData() {{
        fetch('Data.csv')
            .then(res => {{
                if (!res.ok) throw new Error('HTTP status ' + res.status);
                return res.text();
            }})
            .then(text => {{
                const parsed = parseCSV(text);
                if (parsed.length > 0) {{
                    setData(parsed, 'Data.csv (Auto-fetched: ' + parsed.length + ' records)');
                }} else {{
                    fallbackToEmbedded();
                }}
            }})
            .catch(() => {{
                fallbackToEmbedded();
            }});
    }}

    function fallbackToEmbedded() {{
        setData(EMBEDDED_DATA, 'Embedded Data (' + EMBEDDED_DATA.length + ' records)');
    }}

    function setData(data, sourceLabel) {{
        rawDataList = data;
        dataStatusBadge.innerHTML = '<i class="fa fa-database mr5"></i>' + sourceLabel;
        if (renewBtn) renewBtn.removeAttribute('disabled');
        executeSearch();
    }}

    // CSVファイル選択時のハンドラ
    if (csvFileInput) {{
        csvFileInput.addEventListener('change', function(e) {{
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {{
                const text = evt.target.result;
                const parsed = parseCSV(text);
                setData(parsed, 'Loaded: ' + file.name + ' (' + parsed.length + ' records)');
            }};
            reader.readAsText(file, 'UTF-8');
        }});
    }}

    // ドラッグ＆ドロップによるCSV読み込み
    window.addEventListener('dragover', function(e) {{
        e.preventDefault();
        document.body.classList.add('dragover');
    }});
    window.addEventListener('dragleave', function(e) {{
        e.preventDefault();
        document.body.classList.remove('dragover');
    }});
    window.addEventListener('drop', function(e) {{
        e.preventDefault();
        document.body.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {{
            const file = e.dataTransfer.files[0];
            if (file.name.toLowerCase().endsWith('.csv')) {{
                const reader = new FileReader();
                reader.onload = function(evt) {{
                    const parsed = parseCSV(evt.target.result);
                    setData(parsed, 'Dropped: ' + file.name + ' (' + parsed.length + ' records)');
                }};
                reader.readAsText(file, 'UTF-8');
            }}
        }}
    }});

    // Bootstrap Select とネイティブ select の双方向連動 + Live Search
    function initBootstrapSelects() {{
        const btnGroups = document.querySelectorAll('.btn-group.bootstrap-select');
        btnGroups.forEach(group => {{
            const toggle = group.querySelector('.dropdown-toggle');
            const select = group.querySelector('select');
            const filterOption = group.querySelector('.filter-option');
            const items = group.querySelectorAll('ul.dropdown-menu.inner li');
            const searchInput = group.querySelector('.bs-searchbox input');

            if (toggle) {{
                toggle.addEventListener('click', function(e) {{
                    e.stopPropagation();
                    document.querySelectorAll('.btn-group.bootstrap-select.open').forEach(g => {{
                        if (g !== group) g.classList.remove('open');
                    }});
                    group.classList.toggle('open');
                    if (group.classList.contains('open') && searchInput) {{
                        setTimeout(() => searchInput.focus(), 50);
                    }}
                }});
            }}

            // ドロップダウン内インクリメンタル検索 (Live Search)
            if (searchInput) {{
                searchInput.addEventListener('click', function(e) {{
                    e.stopPropagation();
                }});
                searchInput.addEventListener('input', function(e) {{
                    const q = e.target.value.toLowerCase().trim();
                    items.forEach(li => {{
                        const text = (li.querySelector('.text')?.textContent || '').toLowerCase();
                        if (!q || text.includes(q)) {{
                            li.style.display = '';
                        }} else {{
                            li.style.display = 'none';
                        }}
                    }});
                }});
            }}

            if (items && select) {{
                items.forEach(li => {{
                    li.addEventListener('click', function(e) {{
                        e.stopPropagation();
                        const text = li.querySelector('.text') ? li.querySelector('.text').textContent.trim() : '';
                        
                        let matchedOption = null;
                        for (let opt of select.options) {{
                            if (opt.text.trim() === text || opt.value === text) {{
                                matchedOption = opt;
                                break;
                            }}
                        }}
                        if (matchedOption) {{
                            select.value = matchedOption.value;
                        }}
                        
                        items.forEach(i => i.classList.remove('selected'));
                        li.classList.add('selected');
                        if (filterOption) filterOption.textContent = text || '\u00A0';
                        if (toggle) toggle.title = text || '';
                        
                        group.classList.remove('open');
                        if (searchInput) {{
                            searchInput.value = '';
                            items.forEach(i => i.style.display = '');
                        }}

                        const event = new Event('change', {{ bubbles: true }});
                        select.dispatchEvent(event);
                    }});
                }});
            }}

            if (select) {{
                select.addEventListener('change', function() {{
                    const currentText = select.options[select.selectedIndex] ? select.options[select.selectedIndex].text.trim() : '';
                    if (filterOption) filterOption.textContent = currentText || '\u00A0';
                    if (toggle) toggle.title = currentText || '';
                    if (items) {{
                        items.forEach(li => {{
                            const t = li.querySelector('.text') ? li.querySelector('.text').textContent.trim() : '';
                            if (t === currentText) {{
                                li.classList.add('selected');
                            }} else {{
                                li.classList.remove('selected');
                            }}
                        }});
                    }}
                }});
            }}
        }});

        document.addEventListener('click', function() {{
            document.querySelectorAll('.btn-group.bootstrap-select.open').forEach(g => {{
                g.classList.remove('open');
            }});
        }});
    }}

    // 検索パネル開閉トグル
    if (toggleBtn && searchCollapse) {{
        toggleBtn.addEventListener('click', function(e) {{
            e.preventDefault();
            const isCollapsed = searchCollapse.classList.contains('in');
            if (isCollapsed) {{
                searchCollapse.classList.remove('in');
                searchCollapse.style.display = 'none';
                toggleBtn.classList.add('collapsed');
            }} else {{
                searchCollapse.classList.add('in');
                searchCollapse.style.display = 'block';
                toggleBtn.classList.remove('collapsed');
            }}
        }});
    }}

    // 日付正規化ヘルパー (YYYY/MM/DD or YYYY-MM-DD -> YYYY-MM-DD)
    function normalizeDate(str) {{
        if (!str) return '';
        const cleaned = str.trim().replace(/\\//g, '-');
        const parts = cleaned.split('-');
        if (parts.length === 3) {{
            const y = parts[0].padStart(4, '0');
            const m = parts[1].padStart(2, '0');
            const d = parts[2].padStart(2, '0');
            return `${{y}}-${{m}}-${{d}}`;
        }}
        return cleaned;
    }}

    // 検索処理
    function executeSearch() {{
        if (!rawDataList || rawDataList.length === 0) {{
            filteredDataList = [];
            renderTable();
            return;
        }}

        const createDateFrom = normalizeDate(document.getElementById('createDateFrom')?.value);
        const createDateTo = normalizeDate(document.getElementById('createDateTo')?.value);
        const updateDateFrom = normalizeDate(document.getElementById('updateDateFrom')?.value);
        const updateDateTo = normalizeDate(document.getElementById('updateDateTo')?.value);

        const shipTypeSelect = submitForm.querySelector('select[name="shipType"]')?.value || '';
        const shipTypeFreeText = (document.getElementById('shipTypeFreeText')?.value || '').trim().toLowerCase();

        const todayTr = submitForm.querySelector('select[name="todayTr"]')?.value || '';

        const shipNoGrpSelect = submitForm.querySelector('select[name="shipNoGrp"]')?.value || '';
        const grpFreeText = (document.getElementById('grpFreeText')?.value || '').trim().toLowerCase();

        const airportCode = (submitForm.querySelector('select[name="airportCode"]')?.value || '').trim();
        const notification = (submitForm.querySelector('input[name="notification"]')?.value || '').trim().toLowerCase();
        const status = submitForm.querySelector('select[name="status"]')?.value || '';

        const keyword1 = submitForm.querySelector('select[name="keyword1"]')?.value || '';
        const keyword2 = (submitForm.querySelector('input[name="keyword2"]')?.value || '').trim().toLowerCase();
        const ataNo = (submitForm.querySelector('select[name="ataNo"]')?.value || '').trim();

        const priority = submitForm.querySelector('select[name="priority"]')?.value || '';
        const recordLevel = submitForm.querySelector('select[name="recordLevel"]')?.value || '';

        const importReportDone = document.getElementById('importFromReportDone')?.checked;
        const importMightyDone = document.getElementById('importFromMightyDone')?.checked;
        const notimportReportNone = document.getElementById('notimportFromReportNone')?.checked;
        const notimportMightyNone = document.getElementById('notimportFromMightyNone')?.checked;

        const exportReportDone = document.getElementById('exportFromReportDone')?.checked;
        const exportMightyDone = document.getElementById('exportFromMightyDone')?.checked;
        const notexportReportNone = document.getElementById('notexportFromReportNone')?.checked;
        const notexportMightyNone = document.getElementById('notexportFromMightyNone')?.checked;

        const freeText = (submitForm.querySelector('input[name="freeText"]')?.value || '').trim().toLowerCase();
        const andOr = document.getElementById('radioOR')?.checked ? 'OR' : 'AND';

        const createFromChecked = Array.from(submitForm.querySelectorAll('input[name="createFrom"]:checked')).map(cb => cb.value);

        const sortKey1 = submitForm.querySelector('select[name="sortKey1"]')?.value || '';
        const sortValue1 = submitForm.querySelector('select[name="sortValue1"]')?.value || 'ASC';
        const sortKey2 = submitForm.querySelector('select[name="sortKey2"]')?.value || '';
        const sortValue2 = submitForm.querySelector('select[name="sortValue2"]')?.value || 'ASC';

        filteredDataList = rawDataList.filter(row => {{
            // 1. Create Date 比較
            const rowCreated = normalizeDate(row.createdAt);
            if (createDateFrom && rowCreated && rowCreated < createDateFrom) return false;
            if (createDateTo && rowCreated && rowCreated > createDateTo) return false;

            // 2. Update Date 比較
            const rowUpdated = normalizeDate(row.updatedAt);
            if (updateDateFrom && rowUpdated && rowUpdated < updateDateFrom) return false;
            if (updateDateTo && rowUpdated && rowUpdated > updateDateTo) return false;

            // 3. ShipType
            if (shipTypeSelect && shipTypeSelect !== 'freeText') {{
                const cleanType = shipTypeSelect.replace(/^CW_/, '').trim();
                const rowType = (row.shipType || '').trim();
                if (rowType !== shipTypeSelect && rowType !== cleanType) return false;
            }} else if (shipTypeFreeText) {{
                if (!(row.shipType || '').toLowerCase().includes(shipTypeFreeText)) return false;
            }}

            // 4. TODAY T/R
            if (todayTr) {{
                const matchStation = (row.airportCode || '').trim() === todayTr;
                if (!matchStation) return false;
            }}

            // 5. ShipNo. / GRP
            if (shipNoGrpSelect && shipNoGrpSelect !== 'freeText') {{
                if ((row.shipGroup || '').trim() !== shipNoGrpSelect) return false;
            }} else if (grpFreeText) {{
                if (!(row.shipGroup || '').toLowerCase().includes(grpFreeText)) return false;
            }}

            // 6. Create Station (airportCode)
            if (airportCode) {{
                if ((row.airportCode || '').trim() !== airportCode) return false;
            }}

            // 7. Notification No.
            if (notification) {{
                const rowNotif = (row.notification || '').toLowerCase();
                const rowMon = (row.shipMonitorNumber || '').toLowerCase();
                if (!rowNotif.includes(notification) && !rowMon.includes(notification)) return false;
            }}

            // 8. Status
            if (status) {{
                const statusCode = (row.statusCode || '').trim();
                const statusText = (row.status || '').toUpperCase().trim();
                if (status === '1') {{
                    if (statusCode !== '1' && statusText !== 'OPEN') return false;
                }} else if (status === '2') {{
                    if (statusCode !== '2' && statusText !== 'CLOSE') return false;
                }}
            }}

            // 9. Keyword1
            if (keyword1) {{
                const kw1Map = {{
                    '001': 'MEL', '002': 'MEL Fix', '003': 'C/O', '004': 'C/O Fix',
                    '005': 'CDL', '006': 'CDL Fix', '007': 'Watch', '008': 'Shortage',
                    '009': 'INFO', '010': 'Tail No.'
                }};
                const expectedText = kw1Map[keyword1] || '';
                const rowKwCode = (row.keyword1Code || '').trim();
                const rowKwText = (row.keyword1 || '').trim();
                if (rowKwCode !== keyword1 && rowKwText !== expectedText) return false;
            }}

            // 10. Keyword2
            if (keyword2) {{
                if (!(row.keyword2 || '').toLowerCase().includes(keyword2)) return false;
            }}

            // 11. ATA No.
            if (ataNo) {{
                const rowAta = (row.ataNo || '').trim();
                if (rowAta !== ataNo) return false;
            }}

            // 12. Priority
            if (priority) {{
                const priCodeMap = {{ '00': 'P1', '01': 'P2', '02': 'P3' }};
                const expectedPri = priCodeMap[priority] || '';
                const rowPriCode = (row.priorityCode || '').trim();
                const rowPri = (row.priority || '').trim();
                if (rowPriCode !== priority && rowPri !== expectedPri) return false;
            }}

            // 13. Record Level
            if (recordLevel) {{
                const rlMap = {{ '00': 'R1', '01': 'R2', '02': 'R3' }};
                const expectedRl = rlMap[recordLevel] || '';
                const rowRlCode = (row.recordLevelCode || '').trim();
                const rowRl = (row.recordLevel || '').trim();
                if (rowRlCode !== recordLevel && rowRl !== expectedRl) return false;
            }}

            // 14. Import Filter
            if (importReportDone && String(row.importReport) !== '1') return false;
            if (importMightyDone && String(row.importDeferralItem) !== '1') return false;
            if (notimportReportNone && String(row.importReport) !== '0') return false;
            if (notimportMightyNone && String(row.importDeferralItem) !== '0') return false;

            // 15. Export Filter
            if (exportReportDone && String(row.exportReport) !== '1') return false;
            if (exportMightyDone && String(row.exportMaintPlan) !== '1') return false;
            if (notexportReportNone && String(row.exportReport) !== '0') return false;
            if (notexportMightyNone && String(row.exportMaintPlan) !== '0') return false;

            // 16. Create From
            if (createFromChecked.length > 0) {{
                const rowFromCode = (row.createFromCode || '').trim();
                if (!createFromChecked.includes(rowFromCode)) return false;
            }}

            // 17. Free Text (AND / OR)
            if (freeText) {{
                const keywords = freeText.split(/[\\s\\u3000]+/).filter(Boolean);
                if (keywords.length > 0) {{
                    const fullTargetText = [
                        row.title || '',
                        row.description || '',
                        row.memo || '',
                        row.shipGroup || '',
                        row.shipMonitorNumber || '',
                        row.airportCode || ''
                    ].join(' ').toLowerCase();

                    if (andOr === 'AND') {{
                        const allMatch = keywords.every(kw => fullTargetText.includes(kw));
                        if (!allMatch) return false;
                    }} else {{
                        const someMatch = keywords.some(kw => fullTargetText.includes(kw));
                        if (!someMatch) return false;
                    }}
                }}
            }}

            return true;
        }});

        // ソート処理
        const sortKeyToField = {{
            'SHP.GROUP': 'shipGroup',
            'SHP.CREATED_AT': 'createdAt',
            'SHP.UPDATED_AT': 'updatedAt',
            'ATA_NO': 'ataNo'
        }};

        function compareBy(a, b, key, order) {{
            if (!key) return 0;
            const field = sortKeyToField[key] || key;
            const valA = (a[field] || '').trim();
            const valB = (b[field] || '').trim();
            if (valA === valB) return 0;
            let result = 0;
            if (key === 'SHP.CREATED_AT' || key === 'SHP.UPDATED_AT') {{
                const dateA = normalizeDate(valA);
                const dateB = normalizeDate(valB);
                result = dateA < dateB ? -1 : 1;
            }} else {{
                result = valA.localeCompare(valB, undefined, {{ numeric: true, sensitivity: 'base' }});
            }}
            return order === 'DESC' ? -result : result;
        }}

        if (sortKey1 || sortKey2) {{
            filteredDataList.sort((a, b) => {{
                let res1 = compareBy(a, b, sortKey1, sortValue1);
                if (res1 !== 0) return res1;
                return compareBy(a, b, sortKey2, sortValue2);
            }});
        }}

        currentPage = 1;
        renderTable();
    }}

    // テーブル描画処理
    function renderTable() {{
        const total = filteredDataList.length;
        resultsCount.textContent = `検索結果: ${{total.toLocaleString()}} 件 (全 ${{rawDataList.length.toLocaleString()}} 件中)`;

        const effectiveSize = pageSize === 'all' ? total : parseInt(pageSize, 10);
        const totalPages = effectiveSize > 0 ? Math.ceil(total / effectiveSize) : 1;
        if (currentPage > totalPages) currentPage = totalPages || 1;

        const startIndex = pageSize === 'all' ? 0 : (currentPage - 1) * effectiveSize;
        const endIndex = pageSize === 'all' ? total : Math.min(startIndex + effectiveSize, total);

        const currentSlice = filteredDataList.slice(startIndex, endIndex);

        resultsTableBody.innerHTML = '';

        if (currentSlice.length === 0) {{
            const tr = document.createElement('tr');
            tr.innerHTML = '<td colspan="14" style="text-align: center; padding: 30px; color: #94a3b8;">該当するデータが見つかりませんでした。</td>';
            resultsTableBody.appendChild(tr);
        }} else {{
            currentSlice.forEach((item, idx) => {{
                const tr = document.createElement('tr');
                const globalIndex = startIndex + idx + 1;

                const isClose = (item.status || '').toUpperCase() === 'CLOSE' || item.statusCode === '2';
                const statusBadge = isClose
                    ? '<span class="status-badge status-close">CLOSE</span>'
                    : '<span class="status-badge status-open">OPEN</span>';

                const pri = (item.priority || '').toUpperCase();
                let priBadge = pri;
                if (pri === 'P1') priBadge = '<span class="status-badge priority-p1">P1</span>';
                else if (pri === 'P2') priBadge = '<span class="status-badge priority-p2">P2</span>';
                else if (pri === 'P3') priBadge = '<span class="status-badge priority-p3">P3</span>';

                tr.innerHTML = `
                    <td style="text-align: center; color: #64748b;">${{globalIndex}}</td>
                    <td><strong>${{escapeHtml(item.shipMonitorNumber || '')}}</strong></td>
                    <td>${{escapeHtml(item.shipType || '')}}</td>
                    <td><span style="color: #1a4f8b; font-weight: bold;">${{escapeHtml(item.shipGroup || '')}}</span></td>
                    <td>${{escapeHtml(item.airportCode || '')}}</td>
                    <td>${{escapeHtml(item.ataNo || '')}}</td>
                    <td>${{priBadge}}</td>
                    <td>${{escapeHtml(item.recordLevel || '')}}</td>
                    <td>${{statusBadge}}</td>
                    <td class="title-cell" title="${{escapeHtml(item.title || '')}}">${{escapeHtml(item.title || '')}}</td>
                    <td>${{escapeHtml(item.createFrom || '')}}</td>
                    <td style="white-space: nowrap;">${{escapeHtml(item.createdAt || '')}}</td>
                    <td style="white-space: nowrap;">${{escapeHtml(item.updatedAt || '')}}</td>
                    <td style="text-align: center;">
                        <button type="button" class="btn btn-default btn-xs view-detail-btn" data-index="${{startIndex + idx}}">
                            <i class="fa fa-eye"></i> 詳細
                        </button>
                    </td>
                `;

                tr.addEventListener('click', function(e) {{
                    if (e.target.closest('.view-detail-btn') || e.target.tagName !== 'BUTTON') {{
                        openDetailModal(item);
                    }}
                }});

                resultsTableBody.appendChild(tr);
            }});
        }}

        if (total === 0) {{
            paginationInfo.textContent = '0 - 0 / 0 件中';
        }} else {{
            paginationInfo.textContent = `${{(startIndex + 1).toLocaleString()}} - ${{endIndex.toLocaleString()}} / ${{total.toLocaleString()}} 件中 (ページ ${{currentPage}} / ${{totalPages}})`;
        }}

        renderPagination(totalPages);
    }}

    // ページネーションボタン生成
    function renderPagination(totalPages) {{
        paginationNav.innerHTML = '';
        if (totalPages <= 1 || pageSize === 'all') return;

        const prevBtn = document.createElement('button');
        prevBtn.innerHTML = '&laquo; 前へ';
        prevBtn.disabled = (currentPage === 1);
        prevBtn.addEventListener('click', () => {{
            if (currentPage > 1) {{
                currentPage--;
                renderTable();
            }}
        }});
        paginationNav.appendChild(prevBtn);

        let startP = Math.max(1, currentPage - 3);
        let endP = Math.min(totalPages, startP + 6);
        if (endP - startP < 6) {{
            startP = Math.max(1, endP - 6);
        }}

        for (let p = startP; p <= endP; p++) {{
            const pageBtn = document.createElement('button');
            pageBtn.textContent = p;
            if (p === currentPage) pageBtn.classList.add('active');
            pageBtn.addEventListener('click', ((page) => () => {{
                currentPage = page;
                renderTable();
            }})(p));
            paginationNav.appendChild(pageBtn);
        }}

        const nextBtn = document.createElement('button');
        nextBtn.innerHTML = '次へ &raquo;';
        nextBtn.disabled = (currentPage === totalPages);
        nextBtn.addEventListener('click', () => {{
            if (currentPage < totalPages) {{
                currentPage++;
                renderTable();
            }}
        }});
        paginationNav.appendChild(nextBtn);
    }}

    // 詳細モーダル表示
    function openDetailModal(item) {{
        modalTitleText.innerHTML = `<i class="fa fa-info-circle mr5"></i>Ship Monitor No: ${{escapeHtml(item.shipMonitorNumber || '')}} - ${{escapeHtml(item.shipGroup || '')}} (${{escapeHtml(item.shipType || '')}})`;

        modalMetaGrid.innerHTML = `
            <div class="detail-meta-item"><span class="detail-meta-label">Ship Monitor No</span><span class="detail-meta-value">${{escapeHtml(item.shipMonitorNumber || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Ship Type</span><span class="detail-meta-value">${{escapeHtml(item.shipType || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Ship No. (GRP)</span><span class="detail-meta-value">${{escapeHtml(item.shipGroup || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Station</span><span class="detail-meta-value">${{escapeHtml(item.airportCode || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">ATA No</span><span class="detail-meta-value">${{escapeHtml(item.ataNo || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Priority</span><span class="detail-meta-value">${{escapeHtml(item.priority || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Record Level</span><span class="detail-meta-value">${{escapeHtml(item.recordLevel || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Status</span><span class="detail-meta-value">${{escapeHtml(item.status || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Keyword1</span><span class="detail-meta-value">${{escapeHtml(item.keyword1 || item.keyword1Code || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Keyword2</span><span class="detail-meta-value">${{escapeHtml(item.keyword2 || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Created From</span><span class="detail-meta-value">${{escapeHtml(item.createFrom || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Notification No</span><span class="detail-meta-value">${{escapeHtml(item.notification || '-')}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Created At</span><span class="detail-meta-value">${{escapeHtml(item.createdAt || '-')}} (${{escapeHtml(item.createUserId || '')}})</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Updated At</span><span class="detail-meta-value">${{escapeHtml(item.updatedAt || '-')}} (${{escapeHtml(item.updateUserId || '')}})</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Import Flags</span><span class="detail-meta-value">Report: ${{item.importReport}}, Deferral: ${{item.importDeferralItem}}</span></div>
            <div class="detail-meta-item"><span class="detail-meta-label">Export Flags</span><span class="detail-meta-value">Report: ${{item.exportReport}}, MntPlan: ${{item.exportMaintPlan}}</span></div>
        `;

        modalDetailTitle.textContent = item.title || '(なし)';
        modalDetailDescription.textContent = item.description || '(なし)';
        modalDetailMemo.textContent = item.memo || '(なし)';

        detailModal.style.display = 'block';
    }}

    function closeDetailModal() {{
        detailModal.style.display = 'none';
    }}

    if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeDetailModal);
    if (modalCloseFooterBtn) modalCloseFooterBtn.addEventListener('click', closeDetailModal);
    detailModal.addEventListener('click', function(e) {{
        if (e.target === detailModal) closeDetailModal();
    }});

    // クリア処理
    function clearFormConditions() {{
        submitForm.reset();
        document.querySelectorAll('.btn-group.bootstrap-select').forEach(group => {{
            const select = group.querySelector('select');
            const filterOption = group.querySelector('.filter-option');
            const items = group.querySelectorAll('ul.dropdown-menu.inner li');
            if (select) {{
                select.selectedIndex = 0;
                const defaultText = select.options[0] ? select.options[0].text.trim() : '';
                if (filterOption) filterOption.textContent = defaultText || '\u00A0';
                items.forEach((li, idx) => {{
                    if (idx === 0) li.classList.add('selected');
                    else li.classList.remove('selected');
                }});
            }}
        }});
        executeSearch();
    }}

    // CSVエクスポート処理
    function exportFilteredCSV() {{
        if (!filteredDataList || filteredDataList.length === 0) {{
            alert('エクスポートするデータがありません。');
            return;
        }}
        const headers = Object.keys(filteredDataList[0]);
        let csvContent = '\uFEFF';
        csvContent += headers.map(h => `"${{h.replace(/"/g, '""')}}"`).join(',') + '\\r\\n';

        filteredDataList.forEach(row => {{
            const line = headers.map(h => {{
                const val = (row[h] !== undefined && row[h] !== null) ? String(row[h]) : '';
                return `"${{val.replace(/"/g, '""')}}"`;
            }}).join(',');
            csvContent += line + '\\r\\n';
        }});

        const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `ShipMonitor_Export_${{new Date().toISOString().slice(0,10)}}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }}

    function escapeHtml(str) {{
        if (str === null || str === undefined) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }}

    // イベントバインド
    if (searchBtn) searchBtn.addEventListener('click', executeSearch);
    if (clearBtn) clearBtn.addEventListener('click', clearFormConditions);
    if (renewBtn) renewBtn.addEventListener('click', executeSearch);
    if (exportCsvBtn) exportCsvBtn.addEventListener('click', exportFilteredCSV);
    if (pageSizeSelect) {{
        pageSizeSelect.addEventListener('change', function(e) {{
            pageSize = e.target.value;
            currentPage = 1;
            renderTable();
        }});
    }}

    submitForm.addEventListener('keydown', function(e) {{
        if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {{
            e.preventDefault();
            executeSearch();
        }}
    }});

    // 初期化実行
    initBootstrapSelects();
    loadInitialData();

}})();
</script>

</body>
</html>
"""

# 出力ファイル書き込み
with open('search.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Generated search.html successfully! File size: {len(html_template)} characters.")
