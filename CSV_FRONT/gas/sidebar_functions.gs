function onOpen() {
  SpreadsheetApp.getUi()
      .createMenu('カスタムフィルター')
      .addItem('検索サイドバー表示', 'showFilterSidebar')
      .addToUi();
}

function showFilterSidebar() {
  var html;
  try {
    html = HtmlService.createHtmlOutputFromFile('gas/sidebar_ui');
  } catch (e) {
    html = HtmlService.createHtmlOutputFromFile('sidebar_ui');
  }
  html.setTitle('シート内検索');
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * フィルターをすべて解除する
 */
function removeSheetFilters() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const filter = sheet.getFilter() || sheet.getDataRange().getFilter();
  if (filter) {
    filter.remove();
  }
}

/**
 * 列番号（1-based）から列のアルファベット（A, B, ..., Z, AA, AB, ...）を取得する
 */
function getColumnLetter(colIndex) {
  let temp = 0;
  let letter = '';
  while (colIndex > 0) {
    temp = (colIndex - 1) % 26;
    letter = String.fromCharCode(temp + 65) + letter;
    colIndex = Math.floor((colIndex - temp - 1) / 26);
  }
  return letter;
}

/**
 * ヘッダー一覧から指定された候補名に一致する列インデックス（1-based）を検索する
 */
function findColumnIndex(headers, candidates) {
  const normalizedCandidates = candidates.map(c =>
    c.toLowerCase().replace(/[\s_\.\/\-]/g, '')
  );

  for (let i = 0; i < headers.length; i++) {
    const raw = String(headers[i]).trim();
    if (!raw) continue;
    const normalized = raw.toLowerCase().replace(/[\s_\.\/\-]/g, '');
    if (candidates.includes(raw) || normalizedCandidates.includes(normalized)) {
      return i + 1;
    }
  }
  return null;
}

/**
 * 日付の範囲条件（開始日〜終了日）をカスタム数式として作成する
 * セル値が日付型・文字列型のいずれでも対応し、時刻が含まれていても正しく判定する
 */
function buildDateCriteria(colIdx, from, to) {
  if (!from && !to) return null;
  const colLetter = getColumnLetter(colIdx);
  const cellRef = `${colLetter}2`;
  // 時刻を除去した日付シリアル値を取得（文字列の場合はDATEVALUEでシリアル値に変換）
  const dateVal = `INT(IFERROR(DATEVALUE(${cellRef}), ${cellRef}))`;

  let formula = '';
  if (from && to) {
    const [fY, fM, fD] = from.split('-').map(Number);
    const [tY, tM, tD] = to.split('-').map(Number);
    formula = `=AND(${cellRef}<>"", ${dateVal}>=DATE(${fY},${fM},${fD}), ${dateVal}<=DATE(${tY},${tM},${tD}))`;
  } else if (from) {
    const [fY, fM, fD] = from.split('-').map(Number);
    formula = `=AND(${cellRef}<>"", ${dateVal}>=DATE(${fY},${fM},${fD}))`;
  } else if (to) {
    const [tY, tM, tD] = to.split('-').map(Number);
    formula = `=AND(${cellRef}<>"", ${dateVal}<=DATE(${tY},${tM},${tD}))`;
  }

  if (!formula) return null;
  return SpreadsheetApp.newFilterCriteria()
    .whenFormulaSatisfied(formula)
    .build();
}

/**
 * テキスト部分一致フィルター条件を作成する
 * 空白セルは自動的に非表示になり、大文字小文字の違いにも柔軟に対応する
 */
function buildTextContainsCriteria(value) {
  if (!value || typeof value !== 'string') return null;
  const trimmed = value.trim();
  if (trimmed === '') return null;
  return SpreadsheetApp.newFilterCriteria()
    .whenTextContains(trimmed)
    .build();
}

/**
 * テキスト完全一致フィルター条件を作成する
 */
function buildTextEqualToCriteria(value) {
  if (!value || typeof value !== 'string') return null;
  const trimmed = value.trim();
  if (trimmed === '') return null;
  return SpreadsheetApp.newFilterCriteria()
    .whenTextEqualTo(trimmed)
    .build();
}

/**
 * 検索フォームの入力値に基づいてシートにフィルターを適用する
 * @param {Object} formObject - HTMLフォームから送信された検索条件のオブジェクト
 */
function applySheetFilters(formObject) {
  const sheet = SpreadsheetApp.getActiveSheet();
  if (sheet.getLastRow() <= 1) {
    return;
  }

  // 既存のフィルターを一旦解除
  removeSheetFilters();

  const range = sheet.getDataRange();
  const filter = range.createFilter();

  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

  // 列名の候補リスト（CSVのカラム名、表示用ラベル、日本語名に対応）
  const columnCandidates = {
    createDate: ['Create Date', 'Created At', 'createdAt', '作成日時', '作成日'],
    updateDate: ['Update Date', 'Updated At', 'updatedAt', '更新日時', '更新日'],
    shipType: ['ShipType', 'Ship Type', 'shipType', '機種'],
    todayTr: ['TODAY T/R', 'Today T/R', 'todayTr', 'TODAY TR'],
    shipGroup: ['ShipNo. / GRP', 'ShipNo / GRP', 'Ship No.', 'Ship No', 'shipGroup', '機番', '機体番号'],
    airportCode: ['Create Station', 'Station', 'airportCode', '空港', 'ステーション'],
    notification: ['Notification No.', 'Notification', 'notification', '通知番号'],
    status: ['Status', 'status', 'ステータス'],
    statusCode: ['statusCode', 'Status Code'],
    ataNo: ['ATA No.', 'ATA', 'ataNo', 'ATA番号']
  };

  const criteriaMap = {};

  // 1. Create Date (作成日)
  if (formObject.createDateFrom || formObject.createDateTo) {
    const colIdx = findColumnIndex(headers, columnCandidates.createDate);
    if (colIdx) {
      const criteria = buildDateCriteria(colIdx, formObject.createDateFrom, formObject.createDateTo);
      if (criteria) criteriaMap[colIdx] = criteria;
    }
  }

  // 2. Update Date (更新日)
  if (formObject.updateDateFrom || formObject.updateDateTo) {
    const colIdx = findColumnIndex(headers, columnCandidates.updateDate);
    if (colIdx) {
      const criteria = buildDateCriteria(colIdx, formObject.updateDateFrom, formObject.updateDateTo);
      if (criteria) criteriaMap[colIdx] = criteria;
    }
  }

  // 3. ShipType
  if (formObject.shipTypeFreeText) {
    const colIdx = findColumnIndex(headers, columnCandidates.shipType);
    if (colIdx) {
      const criteria = buildTextContainsCriteria(formObject.shipTypeFreeText);
      if (criteria) criteriaMap[colIdx] = criteria;
    }
  }

  // 4. TODAY T/R
  if (formObject.todayTr) {
    const colIdx = findColumnIndex(headers, columnCandidates.todayTr);
    if (colIdx) {
      const criteria = buildTextContainsCriteria(formObject.todayTr);
      if (criteria) criteriaMap[colIdx] = criteria;
    }
  }

  // 5. ShipNo. / GRP
  if (formObject.grpFreeText) {
    const colIdx = findColumnIndex(headers, columnCandidates.shipGroup);
    if (colIdx) {
      const criteria = buildTextContainsCriteria(formObject.grpFreeText);
      if (criteria) criteriaMap[colIdx] = criteria;
    }
  }

  // 6. Create Station
  if (formObject.airportCode) {
    const colIdx = findColumnIndex(headers, columnCandidates.airportCode);
    if (colIdx) {
      const criteria = buildTextContainsCriteria(formObject.airportCode);
      if (criteria) criteriaMap[colIdx] = criteria;
    }
  }

  // 7. Notification No.
  if (formObject.notification) {
    const colIdx = findColumnIndex(headers, columnCandidates.notification);
    if (colIdx) {
      const criteria = buildTextContainsCriteria(formObject.notification);
      if (criteria) criteriaMap[colIdx] = criteria;
    }
  }

  // 8. Status
  if (formObject.status) {
    const statusCol = findColumnIndex(headers, columnCandidates.status);
    const statusCodeCol = findColumnIndex(headers, columnCandidates.statusCode);

    let statusText = '';
    if (formObject.status === '1' || formObject.status.toUpperCase() === 'OPEN') {
      statusText = 'OPEN';
    } else if (formObject.status === '2' || formObject.status.toUpperCase() === 'CLOSE') {
      statusText = 'CLOSE';
    }

    if (statusCol && statusText) {
      criteriaMap[statusCol] = buildTextEqualToCriteria(statusText);
    } else if (statusCodeCol && (formObject.status === '1' || formObject.status === '2')) {
      criteriaMap[statusCodeCol] = buildTextEqualToCriteria(formObject.status);
    }
  }

  // 9. ATA No.
  if (formObject.ataNo1) {
    const ataValue = String(formObject.ataNo1).trim();
    if (ataValue && ataValue.toLowerCase() !== 'all') {
      const colIdx = findColumnIndex(headers, columnCandidates.ataNo);
      if (colIdx) {
        const criteria = buildTextContainsCriteria(ataValue);
        if (criteria) criteriaMap[colIdx] = criteria;
      }
    }
  }

  // 各列にフィルター条件を適用
  for (const col in criteriaMap) {
    if (criteriaMap[col]) {
      filter.setColumnFilterCriteria(parseInt(col, 10), criteriaMap[col]);
    }
  }
}
