function onOpen() {
  SpreadsheetApp.getUi()
      .createMenu('カスタムメニュー')
      .addItem('サイドバーを表示', 'showSidebar')
      .addToUi();
}

function showSidebar() {
  var html = HtmlService.createHtmlOutputFromFile('gas/index').setTitle('検索');
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * フィルターをすべて解除する
 */
function removeFilters() {
    const sheet = SpreadsheetApp.getActiveSheet();
    const filter = sheet.getRange(1, 1, sheet.getLastRow(), sheet.getLastColumn()).getFilter();
    if(filter){
        filter.remove();
    }
}

/**
 * @param {Object} formObject - HTMLフォームから送信された検索条件のオブジェクト
 */
function applyFilters(formObject) {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getDataRange();
  
  removeFilters(); // 既存のフィルターを一旦解除
  
  const filter = range.createFilter();

  // 列名と列インデックスのマッピングを作成
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const colIndexMap = {};
  headers.forEach((header, i) => {
    colIndexMap[header.trim()] = i + 1;
  });

  const criteriaMap = {};

  // 日付範囲の条件を作成
  function buildDateCriteria(from, to) {
    const criteria = SpreadsheetApp.newFilterCriteria();
    let fromDate, toDate;
    if (from) fromDate = new Date(from);
    if (to) toDate = new Date(to);

    if (from && !isNaN(fromDate)) {
      criteria.whenDateAfter(fromDate);
    }
    if (to && !isNaN(toDate)) {
      criteria.whenDateBefore(toDate);
    }
    return criteria.build();
  }
  
  // テキスト（完全一致）の条件を作成
  function buildTextCriteria(value, colIdx) {
     if (!value) return null;
     const hiddenValues = getOtherValues(sheet, colIdx, [value]);
     return SpreadsheetApp.newFilterCriteria().setHiddenValues(hiddenValues).build();
  }

  // キーワード（部分一致）の条件を作成
  function buildKeywordCriteria(keyword) {
    if (!keyword) return null;
    return SpreadsheetApp.newFilterCriteria().whenTextContains(keyword).build();
  }


  // 各検索項目に対応するフィルター条件を構築
  if (colIndexMap['Create Date'] && (formObject.createDateFrom || formObject.createDateTo)) {
    criteriaMap[colIndexMap['Create Date']] = buildDateCriteria(formObject.createDateFrom, formObject.createDateTo);
  }
  if (colIndexMap['Update Date'] && (formObject.updateDateFrom || formObject.updateDateTo)) {
    criteriaMap[colIndexMap['Update Date']] = buildDateCriteria(formObject.updateDateFrom, formObject.updateDateTo);
  }
  if (colIndexMap['ShipType']) {
      const shipTypeValue = formObject.shipType !== 'freeText' ? formObject.shipType : formObject.shipTypeFreeText;
      if(shipTypeValue) criteriaMap[colIndexMap['ShipType']] = buildTextCriteria(shipTypeValue, colIndexMap['ShipType']);
  }
  if (colIndexMap['TODAY T/R'] && formObject.todayTr) {
      criteriaMap[colIndexMap['TODAY T/R']] = buildTextCriteria(formObject.todayTr, colIndexMap['TODAY T/R']);
  }
  if (colIndexMap['ShipNo. / GRP']) {
      const grpValue = formObject.shipNoGrp !== 'freeText' ? formObject.shipNoGrp : formObject.grpFreeText;
      if(grpValue) criteriaMap[colIndexMap['ShipNo. / GRP']] = buildTextCriteria(grpValue, colIndexMap['ShipNo. / GRP']);
  }
  if (colIndexMap['Create Station'] && formObject.airportCode) {
      criteriaMap[colIndexMap['Create Station']] = buildTextCriteria(formObject.airportCode, colIndexMap['Create Station']);
  }
  if (colIndexMap['Notification No.'] && formObject.notification) {
      criteriaMap[colIndexMap['Notification No.']] = buildTextCriteria(formObject.notification, colIndexMap['Notification No.']);
  }
  if (colIndexMap['Status'] && formObject.status) {
      let statusValue = '';
      if (formObject.status === '1') statusValue = 'OPEN';
      if (formObject.status === '2') statusValue = 'CLOSE';
      if(statusValue) criteriaMap[colIndexMap['Status']] = buildTextCriteria(statusValue, colIndexMap['Status']);
  }
   if (colIndexMap['ATA No.']) {
      const ataValue = formObject.ataNo1 !== 'freeText' ? formObject.ataNo1 : formObject.ataNo2;
      if(ataValue) criteriaMap[colIndexMap['ATA No.']] = buildTextCriteria(ataValue, colIndexMap['ATA No.']);
  }
  // Keyword1, Keyword2 はどの列を対象とするか不明なため、実装を保留
  
  // 構築した条件をフィルターに適用
  for (const col in criteriaMap) {
    if (criteriaMap[col]) {
      filter.setColumnFilterCriteria(parseInt(col), criteriaMap[col]);
    }
  }
}

/**
 * 指定された値以外を非表示にするためのヘルパー関数
 */
function getOtherValues(sheet, columnIndex, keepValues) {
  const allValues = sheet.getRange(2, columnIndex, sheet.getLastRow() - 1, 1).getValues();
  const uniqueValues = [...new Set(allValues.flat().map(String))];
  return uniqueValues.filter(value => !keepValues.includes(value));
}
