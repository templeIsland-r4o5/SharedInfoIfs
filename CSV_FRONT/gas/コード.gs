const CACHE_KEY = 'csv_data';
const CACHE_EXPIRATION = 3600; // 1 hour in seconds
const SHEET_NAME = 'Data';

/**
 * Web App entry point.
 */
function doGet(e) {
  const htmlOutput = HtmlService.createTemplateFromFile('index');
  htmlOutput.data = getCsvData();
  return htmlOutput.evaluate()
      .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/**
 * Retrieves CSV data, using cache if available.
 * @returns {Array<Array<String>>} The CSV data as a 2D array.
 */
function getCsvData() {
  const cache = CacheService.getScriptCache();
  const cached = cache.get(CACHE_KEY);

  if (cached != null) {
    Logger.log('Serving from cache');
    const decompressed = Utilities.unzip(Utilities.base64Decode(cached));
    return JSON.parse(decompressed.getDataAsString());
  }

  Logger.log('Serving from Spreadsheet');
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    if (!sheet) {
      throw new Error(`Sheet "${SHEET_NAME}" not found.`);
    }
    const data = sheet.getDataRange().getValues();

    const jsonString = JSON.stringify(data);
    const compressed = Utilities.gzip(Utilities.newBlob(jsonString, 'application/json'));
    const base64Compressed = Utilities.base64Encode(compressed.getBytes());

    // Check if compressed data exceeds cache limit (100KB)
    if (base64Compressed.length > 100 * 1024) {
       Logger.log('Compressed data size exceeds 100KB limit. Not caching.');
    } else {
       cache.put(CACHE_KEY, base64Compressed, CACHE_EXPIRATION);
       Logger.log('Data stored in cache.');
    }

    return data;
  } catch (e) {
    Logger.log(e);
    return [['Error', `Failed to load data: ${e.message}`]];
  }
}
