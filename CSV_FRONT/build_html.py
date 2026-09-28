import json
import csv

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

# 日付入力欄に placeholder="YYYY/MM/DD" を追加
original_search_html = original_search_html.replace(
    'id="createDateFrom" name="createDateFrom"',
    'id="createDateFrom" name="createDateFrom" placeholder="YYYY/MM/DD"'
).replace(
    'id="createDateTo" name="createDateTo"',
    'id="createDateTo" name="createDateTo" placeholder="YYYY/MM/DD"'
).replace(
    'id="updateDateFrom" name="updateDateFrom"',
    'id="updateDateFrom" name="updateDateFrom" placeholder="YYYY/MM/DD"'
).replace(
    'id="updateDateTo" name="updateDateTo"',
    'id="updateDateTo" name="updateDateTo" placeholder="YYYY/MM/DD"'
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
        /* オフライン＆単体動作のための包括的フォールバック・スタイル */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Meiryo", sans-serif;
            background-color: #f4f6f9;
            color: #333;
            margin: 0;
            padding: 15px;
            font-size: 13px;
        }}
        .top-header-bar {{
            background: #fff;
            padding: 12px 20px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .top-header-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1a4f8b;
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0;
        }}
        .top-header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .data-status-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            background-color: #e8f4fd;
            color: #0d6efd;
            border: 1px solid #b6d4fe;
        }}
        .panel.table-panel {{
            border: 1px solid #d2d6de;
            border-radius: 4px;
            background: #fff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }}
        .panel-heading {{
            background-color: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
            padding: 10px 15px;
            position: relative;
        }}
        .panel-title {{
            font-size: 15px;
            font-weight: bold;
            margin: 0;
        }}
        .panel-title a {{
            color: #333;
            text-decoration: none;
            display: block;
            cursor: pointer;
        }}
        .panel-title a:hover {{
            color: #23527c;
        }}
        .panel-body {{
            padding: 15px 20px;
        }}
        
        /* 検索フォームのレイアウトと幅ユーティリティ */
        .form-search-condition {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            margin-bottom: 10px;
            gap: 6px 15px;
        }}
        .form-group {{
            display: inline-flex;
            align-items: center;
            margin-bottom: 0;
            vertical-align: middle;
        }}
        .control-label {{
            font-size: 12px;
            font-weight: 600;
            color: #495057;
            margin-bottom: 0;
            margin-right: 8px;
            white-space: nowrap;
        }}
        .form-control {{
            height: 30px;
            padding: 4px 8px;
            font-size: 12px;
            border: 1px solid #ccc;
            border-radius: 3px;
            background-color: #fff;
            color: #333;
            display: inline-block;
            vertical-align: middle;
        }}
        .form-control:focus {{
            border-color: #66afe9;
            outline: 0;
            box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6);
        }}
        
        /* 固定幅ユーティリティ */
        .w50 {{ width: 50px !important; }}
        .w60 {{ width: 60px !important; }}
        .w70 {{ width: 70px !important; }}
        .w80 {{ width: 80px !important; }}
        .w90 {{ width: 90px !important; }}
        .w100 {{ width: 100px !important; }}
        .w110 {{ width: 110px !important; }}
        .w120 {{ width: 120px !important; }}
        .w130 {{ width: 130px !important; }}
        .w150 {{ width: 150px !important; }}
        .w160 {{ width: 160px !important; }}
        .w300 {{ width: 300px !important; }}
        .w340 {{ width: 340px !important; }}
        .w380 {{ width: 380px !important; }}
        .w480 {{ width: 480px !important; }}
        .w500 {{ width: 500px !important; }}
        .w800 {{ width: 800px !important; }}
        
        /* マージン・パディング */
        .mr5 {{ margin-right: 5px !important; }}
        .mr10 {{ margin-right: 10px !important; }}
        .mb-5 {{ margin-bottom: 5px !important; }}
        .mb-40 {{ margin-bottom: 40px !important; }}
        .mt-30 {{ margin-top: 30px !important; }}
        .vat {{ vertical-align: top !important; }}
        .inline-block {{ display: inline-block !important; }}
        .pull-right {{ float: right !important; }}
        .pull-left {{ float: left !important; }}
        .clearfix::after {{ content: ""; clear: both; display: table; }}
        .text-center {{ text-align: center !important; }}
        .text-right {{ text-align: right !important; }}
        
        /* ボタン */
        .btn {{
            display: inline-block;
            margin-bottom: 0;
            font-weight: 400;
            text-align: center;
            vertical-align: middle;
            touch-action: manipulation;
            cursor: pointer;
            border: 1px solid transparent;
            white-space: nowrap;
            padding: 5px 12px;
            font-size: 12px;
            line-height: 1.42857143;
            border-radius: 3px;
            user-select: none;
            transition: all 0.2s ease;
        }}
        .btn-primary {{
            color: #fff;
            background-color: #337ab7;
            border-color: #2e6da4;
        }}
        .btn-primary:hover {{
            background-color: #286090;
            border-color: #204d74;
        }}
        .btn-info {{
            color: #fff;
            background-color: #5bc0de;
            border-color: #46b8da;
        }}
        .btn-info:hover {{
            background-color: #31b0d5;
            border-color: #269abc;
        }}
        .btn-default {{
            color: #333;
            background-color: #fff;
            border-color: #ccc;
        }}
        .btn-default:hover {{
            background-color: #e6e6e6;
            border-color: #adadad;
        }}
        .btn-success {{
            color: #fff;
            background-color: #5cb85c;
            border-color: #4cae4c;
        }}
        .btn-success:hover {{
            background-color: #449d44;
            border-color: #398439;
        }}
        .btn-sm {{
            padding: 3px 8px;
            font-size: 11px;
            line-height: 1.5;
            border-radius: 3px;
        }}
        
        /* Bootstrap-select ドロップダウンのスタイル */
        .btn-group.bootstrap-select {{
            position: relative;
            display: inline-block;
            vertical-align: middle;
        }}
        .btn-group.bootstrap-select > .btn.dropdown-toggle {{
            width: 100%;
            height: 30px;
            padding: 4px 8px;
            font-size: 12px;
            text-align: left;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #fff;
            border: 1px solid #ccc;
        }}
        .btn-group.bootstrap-select .filter-option {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            flex-grow: 1;
        }}
        .btn-group.bootstrap-select .caret {{
            margin-left: 5px;
            border-top: 4px solid;
            border-right: 4px solid transparent;
            border-left: 4px solid transparent;
            display: inline-block;
            vertical-align: middle;
        }}
        .btn-group.bootstrap-select .dropdown-menu {{
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            z-index: 1000;
            min-width: 160px;
            padding: 5px 0;
            margin: 2px 0 0;
            font-size: 12px;
            text-align: left;
            background-color: #fff;
            border: 1px solid rgba(0,0,0,.15);
            border-radius: 4px;
            box-shadow: 0 6px 12px rgba(0,0,0,.175);
            max-height: 250px;
            overflow-y: auto;
        }}
        .btn-group.bootstrap-select.open .dropdown-menu {{
            display: block;
        }}
        .btn-group.bootstrap-select .dropdown-menu ul.inner {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .btn-group.bootstrap-select .dropdown-menu li a {{
            display: block;
            padding: 5px 15px;
            clear: both;
            font-weight: 400;
            line-height: 1.42857143;
            color: #333;
            white-space: nowrap;
            text-decoration: none;
            cursor: pointer;
        }}
        .btn-group.bootstrap-select .dropdown-menu li a:hover,
        .btn-group.bootstrap-select .dropdown-menu li.selected a {{
            color: #262626;
            background-color: #f5f5f5;
        }}
        .btn-group.bootstrap-select .check-mark {{
            float: right;
            display: none;
        }}
        .btn-group.bootstrap-select li.selected .check-mark {{
            display: inline-block;
        }}
        .btn-group.bootstrap-select select.selectpicker {{
            display: none !important;
        }}
        .bs-searchbox {{
            padding: 4px 8px;
            border-bottom: 1px solid #eee;
        }}
        .bs-searchbox input {{
            margin-bottom: 0;
        }}
        
        /* 検索結果パネルとテーブル */
        .results-panel {{
            background: #fff;
            border: 1px solid #d2d6de;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 25px;
        }}
        .results-header {{
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            background: #fdfdfd;
        }}
        .results-count {{
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .results-controls {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .table-responsive-wrapper {{
            overflow-x: auto;
            min-height: 200px;
        }}
        .results-table {{
            width: 100%;
            margin-bottom: 0;
            border-collapse: collapse;
            font-size: 12px;
        }}
        .results-table th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 600;
            border: 1px solid #e2e8f0;
            padding: 8px 10px;
            white-space: nowrap;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        .results-table td {{
            border: 1px solid #e2e8f0;
            padding: 7px 10px;
            vertical-align: middle;
            color: #333;
        }}
        .results-table tr:nth-child(even) {{
            background-color: #fbfcfe;
        }}
        .results-table tr:hover {{
            background-color: #eef6ff !important;
            cursor: pointer;
        }}
        .results-table .title-cell {{
            max-width: 320px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        /* バッジ表示 */
        .status-badge {{
            display: inline-block;
            padding: 2px 7px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 3px;
            text-align: center;
        }}
        .status-open {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .status-close {{
            background-color: #e2e3e5;
            color: #383d41;
            border: 1px solid #d6d8db;
        }}
        .priority-p1 {{
            background-color: #f8d7da;
            color: #721c24;
            font-weight: bold;
        }}
        .priority-p2 {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .priority-p3 {{
            background-color: #d1ecf1;
            color: #0c5460;
        }}
        
        /* ページネーション */
        .pagination-container {{
            padding: 12px 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            background: #fff;
            border-top: 1px solid #e2e8f0;
        }}
        .pagination-info {{
            font-size: 12px;
            color: #64748b;
        }}
        .pagination-nav {{
            display: flex;
            gap: 4px;
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .pagination-nav button {{
            padding: 4px 10px;
            font-size: 12px;
            border: 1px solid #cbd5e1;
            background: #fff;
            color: #334155;
            border-radius: 3px;
            cursor: pointer;
        }}
        .pagination-nav button:hover:not(:disabled) {{
            background-color: #f1f5f9;
            border-color: #94a3b8;
        }}
        .pagination-nav button.active {{
            background-color: #337ab7;
            color: #fff;
            border-color: #2e6da4;
        }}
        .pagination-nav button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        /* 詳細モーダル */
        .custom-modal-backdrop {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 1050;
            overflow-y: auto;
            padding: 20px;
        }}
        .custom-modal-dialog {{
            background: #fff;
            width: 100%;
            max-width: 900px;
            margin: 30px auto;
            border-radius: 6px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}
        .custom-modal-header {{
            padding: 15px 20px;
            border-bottom: 1px solid #e2e8f0;
            background: #f8fafc;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .custom-modal-title {{
            font-size: 16px;
            font-weight: bold;
            color: #1a4f8b;
            margin: 0;
        }}
        .custom-modal-close {{
            background: transparent;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: #888;
        }}
        .custom-modal-close:hover {{
            color: #000;
        }}
        .custom-modal-body {{
            padding: 20px;
            max-height: 75vh;
            overflow-y: auto;
        }}
        .custom-modal-footer {{
            padding: 12px 20px;
            border-top: 1px solid #e2e8f0;
            text-align: right;
            background: #f8fafc;
        }}
        .detail-meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            background: #f8fafc;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
        }}
        .detail-meta-item {{
            font-size: 12px;
        }}
        .detail-meta-label {{
            font-weight: bold;
            color: #64748b;
            display: block;
            margin-bottom: 2px;
        }}
        .detail-meta-value {{
            color: #1e293b;
            font-weight: 500;
        }}
        .detail-block {{
            margin-bottom: 15px;
        }}
        .detail-block-title {{
            font-size: 13px;
            font-weight: bold;
            color: #334155;
            margin-bottom: 6px;
            border-left: 3px solid #337ab7;
            padding-left: 8px;
        }}
        .detail-block-content {{
            background: #fdfdfd;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 10px 12px;
            font-size: 12px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 250px;
            overflow-y: auto;
        }}
        
        /* ドラッグ＆ドロップ用ハイライト */
        body.dragover {{
            background-color: #e0f2fe;
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
