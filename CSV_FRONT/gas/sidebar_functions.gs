function onOpen() {
  SpreadsheetApp.getUi()
      .createMenu('カスタムフィルター')
      .addItem('検索サイドバー表示', 'showFilterSidebar')
      .addToUi();
}

function showFilterSidebar() {
  var html = HtmlService.createHtmlOutputFromFile('gas/sidebar_ui')
      .setTitle('シート内検索');
  SpreadsheetApp.getUi().showSidebar(html);
}

function removeSheetFilters() {
    const sheet = SpreadsheetApp.getActiveSheet();
    const filter = sheet.getDataRange().getFilter();
    if(filter){
        filter.remove();
    }
}

function applySheetFilters(formObject) {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getDataRange();
  
  removeSheetFilters();
  
  const filter = range.createFilter();

  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const colIndexMap = {};
  headers.forEach((header, i) => {
    colIndexMap[header.trim()] = i + 1;
  });

  const criteriaMap = {};

  function buildDateCriteria(from, to) {
    const criteria = SpreadsheetApp.newFilterCriteria();
    let fromDate, toDate;
    if (from) fromDate = new Date(from);
    if (to) toDate = new Date(to);

    if ((from && !isNaN(fromDate)) || (to && !isNaN(toDate))) {
        if (from && !isNaN(fromDate)) {
            const adjustedFrom = new Date(fromDate.getTime() - (24 * 60 * 60 * 1000));
            criteria.whenDateAfter(adjustedFrom);
        }
        if (to && !isNaN(toDate)) {
            const adjustedTo = new Date(to.getTime() + (24 * 60 * 60 * 1000));
            criteria.whenDateBefore(adjustedTo);
        }
        return criteria.build();
    }
    return null;
  }
  
  function getOtherValues(sheet, columnIndex, keepValues) {
    const allValues = sheet.getRange(2, columnIndex, sheet.getLastRow() - 1, 1).getValues();
    const uniqueValues = [...new Set(allValues.flat().map(v => String(v)))];
    return uniqueValues.filter(value => !keepValues.includes(value) && value !== "");
  }

  function buildTextCriteria(value, colIdx) {
     if (!value) return null;
     const hiddenValues = getOtherValues(sheet, colIdx, [value]);
     return SpreadsheetApp.newFilterCriteria().setHiddenValues(hiddenValues).build();
  }

  if (colIndexMap['Create Date'] && (formObject.createDateFrom || formObject.createDateTo)) {
    criteriaMap[colIndexMap['Create Date']] = buildDateCriteria(formObject.createDateFrom, formObject.createDateTo);
  }
  if (colIndexMap['Update Date'] && (formObject.updateDateFrom || formObject.updateDateTo)) {
    criteriaMap[colIndexMap['Update Date']] = buildDateCriteria(formObject.updateDateFrom, formObject.updateDateTo);
  }
  if (colIndexMap['ShipType'] && formObject.shipTypeFreeText) {
      criteriaMap[colIndexMap['ShipType']] = buildTextCriteria(formObject.shipTypeFreeText, colIndexMap['ShipType']);
  }
  if (colIndexMap['TODAY T/R'] && formObject.todayTr) {
      criteriaMap[colIndexMap['TODAY T/R']] = buildTextCriteria(formObject.todayTr, colIndexMap['TODAY T/R']);
  }
  if (colIndexMap['ShipNo. / GRP'] && formObject.grpFreeText) {
      criteriaMap[colIndexMap['ShipNo. / GRP']] = buildTextCriteria(formObject.grpFreeText, colIndexMap['ShipNo. / GRP']);
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
   if (colIndexMap['ATA No.'] && formObject.ataNo1) {
      const ataValue = formObject.ataNo1;
      if(ataValue && ataValue.toLowerCase() !== 'all') criteriaMap[colIndexMap['ATA No.']] = buildTextCriteria(ataValue, colIndexMap['ATA No.']);
  }
  
  for (const col in criteriaMap) {
    if (criteriaMap[col]) {
      filter.setColumnFilterCriteria(parseInt(col), criteriaMap[col]);
    }
  }
}