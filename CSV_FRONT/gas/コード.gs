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

/**
 * キャッシュで使用されているキーの数を走査して取得する。
 * 単一キー（CACHE_KEY）および連番キー（prefix_0, prefix_1, ...）の存在を確認する。
 * CacheService.getAll() を利用して1回のリクエストで効率的に取得。
 *
 * @param {string} [prefix=CACHE_KEY] 走査対象のキーのプレフィックス
 * @param {number} [maxScan=100] 連番の最大走査数
 * @returns {number} 使用中のキャッシュキー数
 */
function getUsedCacheKeyCount(prefix = CACHE_KEY, maxScan = 100) {
  const cache = CacheService.getScriptCache();

  // 調査対象のキー配列を作成（単一キー + 連番キー 0〜maxScan-1）
  const keysToCheck = [prefix];
  for (let i = 0; i < maxScan; i++) {
    keysToCheck.push(`${prefix}_${i}`);
  }

  // 存在するキーを一括取得
  const cachedEntries = cache.getAll(keysToCheck);
  const usedKeys = Object.keys(cachedEntries);
  const count = usedKeys.length;

  Logger.log(`使用中キャッシュキー数: ${count} 件 (${usedKeys.join(', ') || 'なし'})`);
  return count;
}

