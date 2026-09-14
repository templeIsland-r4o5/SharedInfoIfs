# IFS Cloud Business Process Automation (BPA / Workflow) 詳細解説

## 1. このドキュメントの目的

このドキュメントは、ワークスペース `C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA` に格納されている IFS Cloud の BPA（Business Process Automation / Workflow）デモデータを基に、BPA定義XMLの構造、IFS固有パラメータ、代表的な実装パターンを解説するものです。

対象ファイルは以下です。

| ファイル | 内容 |
|---|---|
| `DEMOWORKFLOWPACKFORMTERAJIMA.xml` | Application Configuration のパッケージ定義。含まれるWorkflow一覧を保持する。 |
| `Items\Workflow-DemoSplitPOLinesExample.xml` | 購買発注ライン分割デモ。履歴読取、数量差分計算、ネストエンティティ更新、Bound Action呼び出しを含む。 |
| `Items\Workflow-DemoCreateTaskPOExample.xml` | 作業指示の保守資材明細に対して購買要求を一括作成するデモ。コレクション取得とMulti-instance Loopを含む。 |
| `Items\Workflow-DemoAddCustomerPONoExample.xml` | 条件によりユーザーへCustomer PO No入力を促し、入力値で受注を更新するデモ。User TaskとUPDATEを含む。 |
| `Items\Workflow-DemoValidateCustomerPONoExample.xml` | Customer PO No必須チェックを行い、不備があればトランザクションを失敗終了させるデモ。Validation Errorを含む。 |
| `Items\Workflow-DetectRecursionExample.xml` | Workflowの再帰実行を検知・防止するデモ。Process Enrichmentとカウンタ変数を含む。 |
| `Items\Workflow-DemoStateChangeExample.xml` | 作業指示の状態変更デモ。READ後にBound ActionをCALLする。 |
| `Items\Workflow-DemoSetDefaultValuesToUIExample.xml` | UIへデフォルト値を返却するデモ。Script TaskとProcess Enrichmentを含む。 |

---

## 2. IFS Cloud BPAの概要

IFS CloudのBPAは、Camunda BPMN 2.0形式をベースにした業務プロセス自動化機能です。IFS CloudのProjection APIを呼び出すサービス処理、JavaScriptによる変数操作、ユーザー入力、条件分岐、ループ、検証エラーなどをBPMN上に定義できます。

このデモパッケージでは、主に以下の実装パターンを確認できます。

- Projection APIのREAD / UPDATE / CALL
- ETagを使った更新整合性制御
- EntitySetの単一レコード読取
- コレクション読取
- ネストエンティティ読取・更新
- Bound Action呼び出し
- JavaScriptによる変数加工
- User Taskによるユーザー入力
- Exclusive Gatewayによる条件分岐
- Terminate End Eventによる入力検証エラー
- Process EnrichmentによるUIまたは次回実行への変数返却
- Multi-instance Loopによる明細ごとの繰り返し処理
- 再帰実行防止

---

## 3. パッケージXMLの構造

### 3.1. `DEMOWORKFLOWPACKFORMTERAJIMA.xml`

最上位のパッケージ定義は次のような構造です。

```xml
<APPLICATION_CONFIGURATION>
  <EXPORT_DEF_VERSION>1</EXPORT_DEF_VERSION>
  <EXPORT_COMMENT>First</EXPORT_COMMENT>
  <PACKAGE_ID>...</PACKAGE_ID>
  <NAME>DEMOWORKFLOWPACKFORMTERAJIMA</NAME>
  <DESCRIPTION>DEMOのworkflowをまとめて出力する目的</DESCRIPTION>
  <AUTHOR>TERAJIMA</AUTHOR>
  <VERSION>V0.0</VERSION>
  <ITEMS>
    <ITEMS_ROW>
      <NAME>DemoSplitPOLinesExample</NAME>
      <TYPE>WORKFLOW</TYPE>
      <FILENAME>Workflow-DemoSplitPOLinesExample.xml</FILENAME>
    </ITEMS_ROW>
  </ITEMS>
</APPLICATION_CONFIGURATION>
```

| 要素 | 説明 |
|---|---|
| `APPLICATION_CONFIGURATION` | Application Configurationエクスポートのルート要素。 |
| `PACKAGE_ID` | パッケージ識別子。環境固有値。 |
| `NAME` | パッケージ名。 |
| `DESCRIPTION` | パッケージ説明。 |
| `AUTHOR` | 作成者。 |
| `VERSION` / `VERSION_TIME_STAMP` | パッケージバージョン情報。 |
| `ITEMS_ROW` | パッケージに含まれる個別オブジェクト。 |
| `TYPE` | このパッケージではすべて `WORKFLOW`。 |
| `FILENAME` | `Items` 配下のWorkflow定義ファイル名。 |

---

## 4. WorkflowエクスポートXMLの全体構造

各Workflowファイルは、IFS CloudのCustom Object形式でエクスポートされています。

```xml
<CUSTOM_OBJECT>
  <NAME>DemoStateChangeExample</NAME>
  <TYPE>WORKFLOW</TYPE>
  <DESCRIPTION>DemoStateChangeExample</DESCRIPTION>
  <WORKFLOW>
    <PROCESS_KEY>DemoStateChangeExample</PROCESS_KEY>
    <BPA_DIAGRAM>
      ... HTMLエスケープされたBPMN XML ...
    </BPA_DIAGRAM>
    <VERSION>version_1</VERSION>
    <DEPLOY_STATUS_DB>UNDEPLOYED</DEPLOY_STATUS_DB>
    <LOCKED_STATUS_DB>EDITING</LOCKED_STATUS_DB>
    <IS_TEMPLATE>TRUE</IS_TEMPLATE>
  </WORKFLOW>
</CUSTOM_OBJECT>
```

### 4.1. 主なメタデータ

| 要素 | 説明 |
|---|---|
| `NAME` | Workflow名。BPMNのprocess idと同じ名称になっている。 |
| `TYPE` | `WORKFLOW`。 |
| `PROCESS_KEY` | 実行時・登録時にWorkflowを識別するキー。 |
| `BPA_DIAGRAM` | BPMN 2.0定義本体。XMLタグが `&lt;` / `&gt;` / `&quot;` などでエスケープされて格納される。 |
| `VERSION` | Workflowバージョン。 |
| `DEPLOY_STATUS_DB` | デプロイ状態。このデモでは `UNDEPLOYED`。 |
| `LOCKED_STATUS_DB` | 編集ロック状態。このデモでは `EDITING`。 |
| `IS_TEMPLATE` | テンプレート扱いかどうか。このデモでは `TRUE`。 |
| `BPMN_VERSION_ROWKEY` 等 | IFS内部管理用のキー・バージョン。移送先環境では変わり得る。 |

### 4.2. BPMN本体の基本形

`BPA_DIAGRAM` 内をデコードすると、概ね次の構造になります。

```xml
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:camunda="http://camunda.org/schema/1.0/bpmn"
  id="sample-diagram"
  targetNamespace="http://bpmn.io/schema/bpmn">

  <bpmn:process id="DemoStateChangeExample" isExecutable="false">
    <bpmn:startEvent id="StartEvent_1" />
    <bpmn:serviceTask ... />
    <bpmn:endEvent ... />
    <bpmn:sequenceFlow ... />
  </bpmn:process>

  <bpmndi:BPMNDiagram>...</bpmndi:BPMNDiagram>
</bpmn:definitions>
```

| 要素 | 説明 |
|---|---|
| `bpmn:definitions` | BPMN定義全体。BPMN、Camunda拡張、ダイアグラム表示用名前空間を宣言する。 |
| `bpmn:process` | 実際のプロセス定義。`id` はWorkflowの識別子。 |
| `isExecutable="false"` | デモXMLでは `false`。IFS Cloud側でWorkflowとして管理される。 |
| `bpmndi:BPMNDiagram` | モデラー上の配置・線の座標情報。ロジック自体には直接関与しない。 |

---

## 5. BPMN要素の基本構文

### 5.1. Start Event / End Event

```xml
<bpmn:startEvent id="StartEvent_1" name="Process Start">
  <bpmn:outgoing>Flow_14t0fb1</bpmn:outgoing>
</bpmn:startEvent>

<bpmn:endEvent id="Event_0ccdktv" name="Process End">
  <bpmn:incoming>Flow_0e46kda</bpmn:incoming>
</bpmn:endEvent>
```

- `startEvent` はプロセス開始点です。
- `endEvent` は通常終了点です。
- `incoming` / `outgoing` は `sequenceFlow` のIDと対応します。

### 5.2. Sequence Flow

```xml
<bpmn:sequenceFlow
  id="Flow_14t0fb1"
  sourceRef="StartEvent_1"
  targetRef="Activity_0f93d25" />
```

- `sourceRef` は遷移元要素IDです。
- `targetRef` は遷移先要素IDです。
- 条件付き分岐では `conditionExpression` を持ちます。

### 5.3. Exclusive Gateway

```xml
<bpmn:exclusiveGateway id="Gateway_16676tt" default="Flow_0if5c8e">
  <bpmn:incoming>Flow_1ixlahd</bpmn:incoming>
  <bpmn:outgoing>Flow_0if5c8e</bpmn:outgoing>
  <bpmn:outgoing>Flow_0u1xsne</bpmn:outgoing>
</bpmn:exclusiveGateway>

<bpmn:sequenceFlow id="Flow_0u1xsne"
                   sourceRef="Gateway_16676tt"
                   targetRef="Activity_0g2o82j">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
    ${CustomerNo == "1010"}
  </bpmn:conditionExpression>
</bpmn:sequenceFlow>
```

- `exclusiveGateway` は条件に一致した1本の経路へ分岐します。
- `default` は、どの条件にも一致しない場合の遷移先Flowです。
- 条件式は `${...}` 形式の式、または `language="JavaScript"` を指定したJavaScript式で書かれています。

デモ内の条件例:

```xml
${CustomerNo == "1000"}
${CustomerNo == "1010"}
${CustomerPoNo == null}
${BuyQtyDue &lt; OldQty}
${executionSeq &gt; 1}
```

JavaScript条件の例:

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression" language="JavaScript">
  execution.getVariable("SupplySourceRef1") == null
</bpmn:conditionExpression>
```

---

## 6. Service Task: Projection API呼び出し

IFS CloudのProjection APIを呼び出す中心要素は `bpmn:serviceTask` です。IFS固有のDelegateとして `com.ifsworld.fnd.bpa.IfsProjectionDelegate` を指定します。

```xml
<bpmn:serviceTask id="Activity_0f93d25"
                  name="Read Work Order"
                  camunda:class="com.ifsworld.fnd.bpa.IfsProjectionDelegate">
  <bpmn:extensionElements>
    <camunda:inputOutput>
      <camunda:inputParameter name="ifsBpaProjectionAction">READ</camunda:inputParameter>
      <camunda:inputParameter name="ifsBpaProjectionType">Standard</camunda:inputParameter>
      <camunda:inputParameter name="ifsBpaProjectionName">PrepareWorkOrderHandling</camunda:inputParameter>
      <camunda:inputParameter name="ifsBpaProjectionEntitySetName">ActiveSeparateSet</camunda:inputParameter>
      <camunda:inputParameter name="ifsBpaProjectionParameters">
        <camunda:map>
          <camunda:entry key="WoNo">${WoNo}</camunda:entry>
        </camunda:map>
      </camunda:inputParameter>
    </camunda:inputOutput>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

### 6.1. IFS Projection Delegateの主要パラメータ

| パラメータ | 使用例 | 説明 |
|---|---|---|
| `ifsBpaProjectionAction` | `READ`, `UPDATE`, `CALL` | 実行するProjection操作種別。このデモでは主にREAD/UPDATE/CALL。 |
| `ifsBpaProjectionType` | `Standard` | Projection種別。指定があるデモとないデモがある。 |
| `ifsBpaProjectionName` | `CustomerOrderHandling` | 対象Projection名。 |
| `ifsBpaProjectionEntitySetName` | `CustomerOrderSet` | 対象EntitySet名。READ/UPDATEで使用。CALLのみの場合は省略されることがある。 |
| `ifsBpaProjectionParameters` | `<camunda:map>` | キー項目、更新項目、Action引数をMapで指定する。値には `${変数名}` を利用できる。 |
| `ifsBpaProjectionETagVariableName` | `ETag`, `CustomerOrderHandling_ETag` | READで取得したETag、またはUPDATE/CALLで使用するETag変数名。 |
| `ifsBpaProjectionIsETag` | `true` または空要素 | ETagを扱う指定。デモでは `true` と空要素の両方がある。 |
| `ifsBpaProjectionCollectionVariableName` | `Reference_MaintMaterialReqLine_Set` | コレクションREAD結果を格納する変数名。 |
| `ifsBpaProjectionIsCollection` | `true` または空要素 | READ結果を複数件として扱う指定。 |
| `ifsBpaProjectionNestedEntityName` | `LinePartArray` | 親Entity配下のネストEntityを対象にする場合に指定。 |
| `ifsBpaProjectionNestedEntityParameters` | `<camunda:map>` | ネストEntityのキーや更新値を指定する。 |
| `ifsBpaProjectionCallSignature` | `ActiveSeparate_StartOrder():Void` | CALL対象Actionのシグネチャ。 |
| `ifsBpaCallReturnValueName` | `CreateNewReq` | CALL戻り値を格納・識別する名前。Voidでも指定されている。 |
| `ifsBpaProjectionErrorLogVariableName` | `CustomerOrderHandling_Error_Log` | エラーログ変数名。 |
| `ifsBpaProjectionIsErrorLog` | 空要素 | エラーログ出力を有効化する指定。 |

### 6.2. READ: 単一レコード取得

例: `Workflow-DemoValidateCustomerPONoExample.xml` / `Workflow-DemoAddCustomerPONoExample.xml`

```xml
<camunda:inputParameter name="ifsBpaProjectionAction">READ</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionETagVariableName">CustomerOrderHandling_ETag</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionName">CustomerOrderHandling</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionEntitySetName">CustomerOrderSet</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionParameters">
  <camunda:map>
    <camunda:entry key="OrderNo">${OrderNo}</camunda:entry>
  </camunda:map>
</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionIsETag">true</camunda:inputParameter>
```

目的:

- `OrderNo` をキーに `CustomerOrderSet` を読み取る。
- 後続UPDATEで利用するため、ETagを `CustomerOrderHandling_ETag` に保持する。
- 読み取った項目（例: `CustomerNo`, `CustomerPoNo`）を後続のGateway条件で参照する。

### 6.3. READ: コレクション取得

例: `Workflow-DemoCreateTaskPOExample.xml`

```xml
<camunda:inputParameter name="ifsBpaProjectionAction">READ</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionName">MaintenanceMaterialRequisitionHandling</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionEntitySetName">Reference_MaintMaterialReqLine</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionParameters">
  <camunda:map>
    <camunda:entry key="WoNo">${WoNo}</camunda:entry>
  </camunda:map>
</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionCollectionVariableName">Reference_MaintMaterialReqLine_Set</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionIsCollection">true</camunda:inputParameter>
```

目的:

- 作業指示番号 `WoNo` に紐づく保守資材要求明細を複数件取得する。
- 結果を `Reference_MaintMaterialReqLine_Set` というコレクション変数に格納する。
- 後続のMulti-instance Loopで1件ずつ処理する。

### 6.4. READ / UPDATE: ネストエンティティを扱う

例: `Workflow-DemoSplitPOLinesExample.xml`

```xml
<camunda:inputParameter name="ifsBpaProjectionAction">READ</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionName">PurchaseOrderHandling</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionEntitySetName">PurchaseOrderSet</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionParameters">
  <camunda:map>
    <camunda:entry key="OrderNo">${OrderNo}</camunda:entry>
  </camunda:map>
</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionNestedEntityName">LinePartArray</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionNestedEntityParameters">
  <camunda:map>
    <camunda:entry key="OrderNo">${OrderNo}</camunda:entry>
    <camunda:entry key="LineNo">${LineNo}</camunda:entry>
    <camunda:entry key="ReleaseNo">${ReleaseNo}</camunda:entry>
  </camunda:map>
</camunda:inputParameter>
```

ポイント:

- 親は `PurchaseOrderSet`。
- 明細は `LinePartArray`。
- 親キー `OrderNo` と明細キー `LineNo`, `ReleaseNo` を指定する。
- UPDATE時は `ifsBpaProjectionNestedEntityParameters` に更新値も含める。

更新例:

```xml
<camunda:entry key="BuyQtyDue">${OldQty - BuyQtyDue}</camunda:entry>
<camunda:entry key="OrderNo">${OrderNo}</camunda:entry>
<camunda:entry key="LineNo">${LineNo}</camunda:entry>
<camunda:entry key="ReleaseNo">${ReleaseNo}</camunda:entry>
```

### 6.5. UPDATE: レコード更新

例: `Workflow-DemoAddCustomerPONoExample.xml`

```xml
<camunda:inputParameter name="ifsBpaProjectionETagVariableName">CustomerOrderHandling_ETag</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionAction">UPDATE</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionName">CustomerOrderHandling</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionEntitySetName">CustomerOrderSet</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionParameters">
  <camunda:map>
    <camunda:entry key="CustomerPoNo">${FormField_PoNo}</camunda:entry>
  </camunda:map>
</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionIsETag">true</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionErrorLogVariableName">CustomerOrderHandling_Error_Log</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionIsErrorLog" />
```

ポイント:

- 更新前に同じProjection/EntitySetをREADしてETagを取得している。
- `FormField_PoNo` はUser Taskのフォーム入力値。
- ETagを使うことで、更新対象の整合性を担保する。
- `ifsBpaProjectionIsErrorLog` と `ifsBpaProjectionErrorLogVariableName` により、失敗時のログ変数を扱える。

### 6.6. CALL: Action呼び出し

例: `Workflow-DemoCreateTaskPOExample.xml`

```xml
<camunda:inputParameter name="ifsBpaProjectionAction">CALL</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionName">WorkTaskHandling</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionCallSignature">CreateNewReq(MaintMaterialOrderNo,LineNo):Void</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaCallReturnValueName">CreateNewReq</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionParameters">
  <camunda:map>
    <camunda:entry key="MaintMaterialOrderNo">${MaintMaterialOrderNo}</camunda:entry>
    <camunda:entry key="LineNo">${LineItemNo}</camunda:entry>
  </camunda:map>
</camunda:inputParameter>
```

ポイント:

- `ifsBpaProjectionCallSignature` にAction名、引数、戻り値型を指定する。
- `ifsBpaProjectionParameters` のキー名はAction引数名に合わせる。
- この例では戻り値型は `Void`。

### 6.7. CALL: Bound Actionによる状態変更

例: `Workflow-DemoStateChangeExample.xml`

```xml
<camunda:inputParameter name="ifsBpaProjectionAction">CALL</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionName">PrepareWorkOrderHandling</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionCallSignature">ActiveSeparate_StartOrder():Void</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaCallReturnValueName">ActiveSeparate_StartOrder</camunda:inputParameter>
<camunda:inputParameter name="ifsBpaProjectionParameters">
  <camunda:map />
</camunda:inputParameter>
```

このデモの重要点:

1. 先に `PrepareWorkOrderHandling.ActiveSeparateSet` を `WoNo` でREADする。
2. READで対象EntityをBPA実行コンテキストに載せる。
3. その後、引数なしで `ActiveSeparate_StartOrder():Void` をCALLする。

コメントにもある通り、状態変更は対象Entityに対するBound Actionです。BPAのAPI TaskではEntity自体をAction引数として直接渡せないため、先に対象EntityをREADしてからBound Actionを呼び出す構成になります。

---

## 7. Script Task: JavaScriptによる変数操作

Script TaskはWorkflow変数の設定、取得、文字列処理、配列処理などに使います。

```xml
<bpmn:scriptTask id="Activity_0l7lcni"
                 name="Add default values to execution"
                 scriptFormat="JavaScript">
  <bpmn:script>
    execution.setVariable('OrganizationSite', 31);
    execution.setVariable('Description', 'Track product levels &amp; orders');
    execution.setVariable('EarliestStart', '2024-01-01-23.30.00.0000000');
    execution.setVariable('AllowMultipleVisits', true);
  </bpmn:script>
</bpmn:scriptTask>
```

### 7.1. よく使うAPI

| 構文 | 説明 |
|---|---|
| `execution.setVariable('Name', value)` | Workflow変数を設定する。後続タスクや条件式で参照できる。 |
| `execution.getVariable('Name')` | Workflow変数を取得する。 |
| `execution.hasVariable('Name')` | 変数が存在するか判定する。 |

### 7.2. デモ内のスクリプト例

#### UIデフォルト値設定

`Workflow-DemoSetDefaultValuesToUIExample.xml`:

```javascript
execution.setVariable('OrganizationSite', 31);
execution.setVariable('Description', 'Track product levels & orders');
execution.setVariable('EarliestStart', '2024-01-01-23.30.00.0000000');
execution.setVariable('AllowMultipleVisits', true);
```

#### 再帰実行カウンタ

`Workflow-DetectRecursionExample.xml`:

```javascript
var seq = 1
if(execution.hasVariable('executionSeq')){
  seq = execution.getVariable('executionSeq') + 1
}
execution.setVariable('executionSeq', seq);
```

#### 購買発注ライン選択文字列からキー抽出

`Workflow-DemoSplitPOLinesExample.xml`:

```javascript
var text = execution.getVariable("OrderSelection")[0];

var pos_start = text.indexOf("ORDER_NO=") + 9;
var pos_end = text.indexOf("^", pos_start);
var orderNo = text.substr(pos_start, pos_end-pos_start);

pos_start = text.indexOf("LINE_NO=") + 8;
pos_end = text.indexOf("^", pos_start);
var lineNo = text.substr(pos_start, pos_end-pos_start);

pos_start = text.indexOf("RELEASE_NO=") + 11;
pos_end = text.indexOf("^", pos_start);
var releaseNo = text.substr(pos_start, pos_end-pos_start);

execution.setVariable("OrderNo", orderNo);
execution.setVariable("LineNo", lineNo);
execution.setVariable("ReleaseNo", releaseNo);
```

#### 履歴から変更前数量を取得

`Workflow-DemoSplitPOLinesExample.xml`:

```javascript
function compare(a, b) {
  if (a.HistoryNo < b.HistoryNo) {
    return 1;
  }
  if (a.HistoryNo > b.HistoryNo) {
    return -1;
  }
  return 0;
}

var histLines = execution.getVariable("PurchaseOrderLineHistorySet_Set");
histLines.sort(compare);

var lastLine = null;
for (i=0; (i < histLines.length && lastLine == null); i++){
  if (histLines[i].MessageText.startsWith("Quantity changed ")){
    lastLine = histLines[i];
  }
}

var text = lastLine.MessageText.replace("Quantity changed ","");
var oldQty = text.substr(0,text.indexOf(" => "));

execution.setVariable("LastLine", lastLine);
execution.setVariable("OldQty", oldQty);
```

注意点:

- XML内では `<`, `>`, `&&`, `&` は `&lt;`, `&gt;`, `&amp;&amp;`, `&amp;` のようにエスケープされます。
- スクリプト内で設定した変数は後続のProjection ParameterやGateway条件で参照できます。

---

## 8. User Task: ユーザー入力

例: `Workflow-DemoAddCustomerPONoExample.xml`

```xml
<bpmn:userTask id="Activity_1ybqtct"
               name="User Enter Customer PO Number"
               camunda:formKey="CustomerPONo">
  <bpmn:extensionElements>
    <camunda:inputOutput>
      <camunda:inputParameter name="ifsBpaUserTaskIsHeader">true</camunda:inputParameter>
      <camunda:inputParameter name="ifsBpaUserTaskHeaderValue">Enter Customer PO Number</camunda:inputParameter>
      <camunda:inputParameter name="ifsBpaImplFormField_PoNo">
        <camunda:map>
          <camunda:entry key="en">New Customer PO Number</camunda:entry>
        </camunda:map>
      </camunda:inputParameter>
    </camunda:inputOutput>
    <camunda:formData>
      <camunda:formField id="FormField_PoNo" type="string" />
    </camunda:formData>
  </bpmn:extensionElements>
</bpmn:userTask>
```

| 項目 | 説明 |
|---|---|
| `camunda:formKey` | フォーム識別子。 |
| `ifsBpaUserTaskIsHeader` | ヘッダー表示の有無。 |
| `ifsBpaUserTaskHeaderValue` | ユーザーへ表示するヘッダー文言。 |
| `ifsBpaImplFormField_PoNo` | フィールド表示名の多言語定義。ここでは英語 `New Customer PO Number`。 |
| `camunda:formField id="FormField_PoNo"` | 入力項目。IDがWorkflow変数名になる。 |
| `type="string"` | 入力型。 |

このUser Taskは重要なトランザクション境界になります。デモ内コメントでは、User Taskは「最初のトランザクションの完了」と「次のトランザクションの開始」を表すと説明されています。

---

## 9. Process Enrichment: 変数を外部へ返す

Process Enrichmentは、Workflow内で設定した変数をUIや呼び出し元コンテキストへ返すために使われます。

```xml
<bpmn:serviceTask id="Activity_0a88o5s"
                  name="Enrich variables"
                  camunda:class="com.ifsworld.fnd.bpa.process.enrichment.IfsBpaProcessEnrichmentDelegate">
  <bpmn:extensionElements>
    <camunda:inputOutput>
      <camunda:inputParameter name="ifsBpaEnrichmentRegisteredVariables">
        <camunda:list>
          <camunda:value>OrganizationSite</camunda:value>
          <camunda:value>Description</camunda:value>
          <camunda:value>EarliestStart</camunda:value>
          <camunda:value>AllowMultipleVisits</camunda:value>
        </camunda:list>
      </camunda:inputParameter>
    </camunda:inputOutput>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

| 項目 | 説明 |
|---|---|
| `camunda:class` | `com.ifsworld.fnd.bpa.process.enrichment.IfsBpaProcessEnrichmentDelegate` を指定する。 |
| `ifsBpaEnrichmentRegisteredVariables` | 返却・引継ぎ対象の変数名を `camunda:list` で列挙する。 |

使用例:

- `DemoSetDefaultValuesToUIExample`: UIへデフォルト値を返す。
- `DetectRecursionExample`: `executionSeq` を呼び出し元のユーザーアクションに返し、次回実行で再利用する。

---

## 10. Validation Error / Terminate End Event

入力検証でエラーにしたい場合、Terminate End EventとIFSのFailure Listenerを組み合わせます。

例: `Workflow-DemoValidateCustomerPONoExample.xml`

```xml
<bpmn:endEvent id="Event_07hazm6" name="Process Termination">
  <bpmn:extensionElements>
    <camunda:inputOutput>
      <camunda:inputParameter name="ifsBpaValidationErrorMessages">
        <camunda:map>
          <camunda:entry key="en">A PO Number is required for this Customer</camunda:entry>
        </camunda:map>
      </camunda:inputParameter>
    </camunda:inputOutput>
    <camunda:executionListener
      class="com.ifsworld.fnd.bpa.process.validation.IfsBpaFailureEndEventListener"
      event="end" />
  </bpmn:extensionElements>
  <bpmn:terminateEventDefinition id="TerminateEventDefinition_13psxxl" />
</bpmn:endEvent>
```

動作:

1. Gatewayでエラー条件に一致する。
2. Terminate End Eventへ遷移する。
3. `IfsBpaFailureEndEventListener` が `end` イベントで実行される。
4. `ifsBpaValidationErrorMessages` のメッセージをユーザーへ返す。
5. トランザクションを失敗・ロールバック扱いにする。

---

## 11. Multi-instance Loop: 複数明細の繰り返し処理

例: `Workflow-DemoCreateTaskPOExample.xml`

```xml
<bpmn:subProcess id="Activity_1oinajr">
  <bpmn:multiInstanceLoopCharacteristics
    isSequential="true"
    camunda:collection="Reference_MaintMaterialReqLine_Set"
    camunda:elementVariable="MaintMaterialReqLine" />

  <bpmn:startEvent id="Event_1ke7jhx" name="Loop Start" />
  ...
</bpmn:subProcess>
```

| 属性 | 説明 |
|---|---|
| `isSequential="true"` | 1件ずつ順番に処理する。 |
| `camunda:collection` | ループ対象のコレクション変数。READで取得した `Reference_MaintMaterialReqLine_Set`。 |
| `camunda:elementVariable` | ループ中の現在行を表す変数。ここでは `MaintMaterialReqLine`。 |

デモでは、各明細に対して `SupplySourceRef1` が未設定の場合のみ `CreateNewReq` をCALLします。

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression" language="JavaScript">
  execution.getVariable("SupplySourceRef1") == null
</bpmn:conditionExpression>
```

---

## 12. デモ別詳細

### 12.1. DemoValidateCustomerPONoExample

対象ファイル:

`C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-DemoValidateCustomerPONoExample.xml`

目的:

- 顧客番号が `1010` の場合、Customer PO Noが必須であることを検証する。
- Customer PO Noが未設定ならエラーメッセージを返し、処理を終了する。

処理フロー:

1. Start EventからGatewayへ進む。
2. `CustomerNo == "1010"` の場合のみ検証処理へ進む。
3. `CustomerOrderHandling.CustomerOrderSet` を `OrderNo` でREADする。
4. `CustomerPoNo == null` の場合、Terminate End Eventへ進む。
5. `ifsBpaValidationErrorMessages` により `A PO Number is required for this Customer` を返す。
6. 条件に一致しない場合は通常終了する。

主な構文:

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
  ${CustomerNo == "1010"}
</bpmn:conditionExpression>
```

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
  ${CustomerPoNo == null}
</bpmn:conditionExpression>
```

設計上のポイント:

- 更新イベントなどでは、変更された項目しかWorkflow変数に含まれない場合があるため、検証前に対象レコードをREADして必要項目を補完している。
- 入力検証で業務処理を止めたい場合は、通常End EventではなくTerminate End Event + Failure Listenerを使用する。

### 12.2. DemoAddCustomerPONoExample

対象ファイル:

`C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-DemoAddCustomerPONoExample.xml`

目的:

- 顧客番号が `1000` で、Customer PO Noが未設定の場合、ユーザーへ入力を求める。
- 入力されたPO番号でCustomer Orderを更新する。
- User Task後の再実行時に再度User Taskへ入らないようにする。

処理フロー:

1. Start EventからGatewayへ進む。
2. `CustomerNo == "1000"` の場合、Customer OrderをREADする。
3. READ結果の `CustomerPoNo` が `null` の場合、User Taskを表示する。
4. User Taskで `FormField_PoNo` を入力する。
5. `CustomerOrderHandling.CustomerOrderSet` をUPDATEし、`CustomerPoNo = ${FormField_PoNo}` を設定する。
6. 入力値が既に存在する実行では、`execution.getVariable("FormField_PoNo") != null` の条件により処理を終了し、再帰的な入力要求を避ける。

主な条件:

```xml
${CustomerNo == "1000"}
${CustomerPoNo == null}
```

再帰回避条件:

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression" language="JavaScript">
  execution.getVariable("FormField_PoNo") != null
</bpmn:conditionExpression>
```

設計上のポイント:

- User Taskはトランザクション境界になるため、後続UPDATEは別トランザクションとして動く。
- UPDATE前にREADしてETagを取得している。
- User Taskで入力した値は `camunda:formField` の `id`、つまり `FormField_PoNo` として参照する。

### 12.3. DemoSetDefaultValuesToUIExample

対象ファイル:

`C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-DemoSetDefaultValuesToUIExample.xml`

目的:

- 新規作成画面などで、UIへデフォルト値を返す。

処理フロー:

1. Script Taskで以下の変数を設定する。
   - `OrganizationSite = 31`
   - `Description = 'Track product levels & orders'`
   - `EarliestStart = '2024-01-01-23.30.00.0000000'`
   - `AllowMultipleVisits = true`
2. Process Enrichmentで上記変数を `ifsBpaEnrichmentRegisteredVariables` に登録する。
3. UI側へ変数が返され、デフォルト値として利用される。

重要な注意:

- 返却する変数名は、UIまたは呼び出し元が期待するレスポンス項目名と一致させる必要がある。
- デモ内コメントでは、`<Entity>_Default()` 呼び出しのレスポンス値と一致させる例が示されている。

### 12.4. DemoCreateTaskPOExample

対象ファイル:

`C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-DemoCreateTaskPOExample.xml`

目的:

- 作業指示番号 `WoNo` に紐づく保守資材明細を読み取り、購買要求が未作成の明細に対して購買要求を作成する。

処理フロー:

1. `MaintenanceMaterialRequisitionHandling.Reference_MaintMaterialReqLine` を `WoNo` でコレクションREADする。
2. 結果を `Reference_MaintMaterialReqLine_Set` に格納する。
3. Sub ProcessをMulti-instance Loopとして、`Reference_MaintMaterialReqLine_Set` を順番に処理する。
4. 各明細について `SupplySourceRef1 == null` の場合のみ購買要求作成へ進む。
5. `WorkTaskHandling.CreateNewReq(MaintMaterialOrderNo,LineNo):Void` をCALLする。

主な構文:

```xml
<bpmn:multiInstanceLoopCharacteristics
  isSequential="true"
  camunda:collection="Reference_MaintMaterialReqLine_Set"
  camunda:elementVariable="MaintMaterialReqLine" />
```

```xml
<camunda:inputParameter name="ifsBpaProjectionCallSignature">
  CreateNewReq(MaintMaterialOrderNo,LineNo):Void
</camunda:inputParameter>
```

設計上のポイント:

- 一括処理は「コレクションREAD」+「Multi-instance Sub Process」で実装する。
- 条件式は「既に購買要求があるか」を見ている。実業務では品目、金額、供給方法などの追加条件を含める余地がある。
- 各明細が複数のタスクへ流れないよう、Gateway条件は排他的に設計する。

### 12.5. DetectRecursionExample

対象ファイル:

`C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-DetectRecursionExample.xml`

目的:

- Workflowが更新処理を行い、その更新が同じWorkflowを再度起動してしまう再帰実行を防止する。

処理フロー:

1. Script Taskで `executionSeq` を初期化またはインクリメントする。
2. Process Enrichmentで `executionSeq` を呼び出し元コンテキストへ返す。
3. Gatewayで `executionSeq > 1` の場合は即終了する。
4. `executionSeq == 1` の場合のみ本処理へ進む。
5. `RegulatoryBodyHandling.RegulatoryBodySet` を `RegulatoryBodyCode = AA` でREADする。
6. 同じEntityをUPDATEし、`RegulatoryBodyDesc = ATest2` を設定する。

主な条件:

```xml
${executionSeq > 1}
${executionSeq == 1}
```

設計上のポイント:

- Workflow内でUPDATEを行うと、更新イベントをトリガーに同じWorkflowが再度起動する可能性がある。
- `executionSeq` のようなカウンタをProcess Enrichmentで外部へ返し、同一ユーザーアクション内の後続実行で参照できるようにする。
- 2回目以降は処理せず終了することで再帰を止める。

### 12.6. DemoStateChangeExample

対象ファイル:

`C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-DemoStateChangeExample.xml`

目的:

- 作業指示を状態変更Actionで開始状態へ変更する。

処理フロー:

1. `PrepareWorkOrderHandling.ActiveSeparateSet` を `WoNo` でREADする。
2. ETagを `ETag` 変数に保持する。
3. `PrepareWorkOrderHandling.ActiveSeparate_StartOrder():Void` をCALLする。
4. 通常終了する。

主な構文:

```xml
<camunda:inputParameter name="ifsBpaProjectionCallSignature">
  ActiveSeparate_StartOrder():Void
</camunda:inputParameter>
```

設計上のポイント:

- 状態変更はBound Actionなので、対象Entityの事前READが必要。
- CALL自体の `ifsBpaProjectionParameters` は空Map。
- ETag変数名はREADとCALLで同じ `ETag` を指定している。

### 12.7. DemoSplitPOLinesExample

対象ファイル:

`C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-DemoSplitPOLinesExample.xml`

目的:

- 購買発注ラインの数量が減少した場合、減少分を新しいラインとして分割する。

処理フロー:

1. `ConfirmPurchaseOrderWithDifferences.ConfirmDifferencesSet` を `Objkey` でコレクションREADする。
2. `OrderSelection` から `ORDER_NO`, `LINE_NO`, `RELEASE_NO` をJavaScriptで抽出し、`OrderNo`, `LineNo`, `ReleaseNo` に設定する。
3. `PurchaseOrderHandling.PurchaseOrderSet` のネストEntity `LinePartArray` をREADし、現在の購買発注ライン情報を取得する。
4. `PurchaseOrderLinesHistoryAnalysis.PurchaseOrderLineHistorySet` をREADし、変更履歴をコレクションとして取得する。
5. JavaScriptで履歴を `HistoryNo` 降順にソートし、最新の `Quantity changed ...` メッセージから変更前数量 `OldQty` を抽出する。
6. Gatewayで `BuyQtyDue < OldQty`、つまり数量が減少した場合のみ分割処理へ進む。
7. 既存ラインの数量を一時的に `OldQty - BuyQtyDue` へUPDATEする。
8. `PurchaseOrderHandling.CopyPurchaseOrderLines(RecordSelection):Void` をCALLし、ラインをコピーする。
9. 既存ラインの数量を元の `BuyQtyDue` へ戻す。
10. 終了する。

主な条件:

```xml
${BuyQtyDue < OldQty}
```

主なProjection:

| 処理 | Projection | EntitySet / Action |
|---|---|---|
| 差分情報読取 | `ConfirmPurchaseOrderWithDifferences` | `ConfirmDifferencesSet` |
| 現在POライン読取 | `PurchaseOrderHandling` | `PurchaseOrderSet` + nested `LinePartArray` |
| 履歴読取 | `PurchaseOrderLinesHistoryAnalysis` | `PurchaseOrderLineHistorySet` |
| 旧ライン更新 | `PurchaseOrderHandling` | `PurchaseOrderSet` + nested `LinePartArray` |
| ラインコピー | `PurchaseOrderHandling` | `CopyPurchaseOrderLines(RecordSelection):Void` |
| 旧ライン復元 | `PurchaseOrderHandling` | `PurchaseOrderSet` + nested `LinePartArray` |

設計上のポイント:

- `OrderSelection` は選択行情報を含む文字列配列で、スクリプトでキーを抽出している。
- コピー対象ラインの値を直接変更できないため、既存ラインの数量を一時更新してからコピーし、その後既存ラインを戻すという手順になっている。
- 履歴メッセージの文字列 `Quantity changed ` に依存しているため、環境・言語・メッセージ形式が変わる場合は注意が必要。

---

## 13. 変数の扱い

### 13.1. 変数の発生源

| 発生源 | 例 | 説明 |
|---|---|---|
| 起動コンテキスト | `WoNo`, `OrderNo`, `CustomerNo`, `Objkey`, `OrderSelection` | UI操作、イベント、アシスタント等から渡される。 |
| Projection READ結果 | `CustomerPoNo`, `BuyQtyDue`, `SupplySourceRef1` | READ結果の項目がWorkflow変数として参照される。 |
| Script Task | `executionSeq`, `OldQty`, `LineNo` | JavaScriptで明示的に設定する。 |
| User Task | `FormField_PoNo` | `camunda:formField` の `id` が変数名になる。 |
| Projection設定 | `ETag`, `CustomerOrderHandling_ETag`, `Reference_MaintMaterialReqLine_Set` | ETagやコレクション結果の格納先として指定する。 |

### 13.2. 変数参照の書き方

Projection Parameterでは `${...}` を使います。

```xml
<camunda:entry key="WoNo">${WoNo}</camunda:entry>
<camunda:entry key="CustomerPoNo">${FormField_PoNo}</camunda:entry>
<camunda:entry key="BuyQtyDue">${OldQty - BuyQtyDue}</camunda:entry>
```

JavaScript条件では `execution.getVariable()` を使う例もあります。

```javascript
execution.getVariable("SupplySourceRef1") == null
execution.getVariable("FormField_PoNo") != null
```

---

## 14. XMLエスケープの注意点

`BPA_DIAGRAM` 内はXML文字列として格納されるため、BPMN本体のXMLはエスケープされています。

| 実際に表したい文字 | `BPA_DIAGRAM` 内の表記 |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&apos;` または通常文字として現れる場合あり |
| `&` | `&amp;` |
| `&&` | `&amp;&amp;` |
| `=>` | `=&gt;` |

例:

```xml
&lt;bpmn:conditionExpression xsi:type=&quot;bpmn:tFormalExpression&quot;&gt;${BuyQtyDue &amp;lt; OldQty}&lt;/bpmn:conditionExpression&gt;
```

デコード後の意味:

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${BuyQtyDue < OldQty}</bpmn:conditionExpression>
```

---

## 15. 実装時のチェックリスト

### Projection API Task

- `camunda:class="com.ifsworld.fnd.bpa.IfsProjectionDelegate"` を指定しているか。
- `ifsBpaProjectionAction` は目的に合っているか。
- `ifsBpaProjectionName` と `ifsBpaProjectionEntitySetName` は正しいか。
- キー項目は `ifsBpaProjectionParameters` に不足なく指定しているか。
- UPDATEやBound Action前に必要なREADを行っているか。
- ETagが必要な更新で `ifsBpaProjectionETagVariableName` と `ifsBpaProjectionIsETag` を設定しているか。
- コレクションREADでは `ifsBpaProjectionCollectionVariableName` と `ifsBpaProjectionIsCollection` を設定しているか。
- ネストEntityでは親Entityキーと子Entityキーの両方を正しく設定しているか。

### Gateway / 条件式

- 条件が排他的になっているか。
- どの条件にも一致しない場合の `default` Flowを設定しているか。
- `null` 判定や型比較が実データ型と合っているか。
- XML内で `<`, `>`, `&&` などを正しくエスケープしているか。

### User Task

- `camunda:formKey` が設定されているか。
- `camunda:formField id` と後続で参照する変数名が一致しているか。
- User Task後に再帰的に同じUser Taskへ戻らない条件を設計しているか。

### Process Enrichment

- 外部へ返したい変数を `ifsBpaEnrichmentRegisteredVariables` に列挙しているか。
- UIが期待する項目名と変数名が一致しているか。
- 再帰防止など、次回実行に引き継ぎたい変数を登録しているか。

### Validation Error

- 業務エラーとして止める場合、通常End EventではなくTerminate End Eventを使用しているか。
- `IfsBpaFailureEndEventListener` を `event="end"` で設定しているか。
- `ifsBpaValidationErrorMessages` に必要な言語キーのメッセージを設定しているか。

---

## 16. デモから読み取れる設計パターンまとめ

| パターン | デモ | 使う要素 |
|---|---|---|
| 入力必須チェック | `DemoValidateCustomerPONoExample` | READ + Gateway + Terminate End Event |
| ユーザー入力後の更新 | `DemoAddCustomerPONoExample` | READ + User Task + UPDATE |
| UIデフォルト値返却 | `DemoSetDefaultValuesToUIExample` | Script Task + Process Enrichment |
| 複数明細一括処理 | `DemoCreateTaskPOExample` | Collection READ + Multi-instance Sub Process + CALL |
| 再帰実行防止 | `DetectRecursionExample` | Script Task + Process Enrichment + Gateway |
| 状態変更 | `DemoStateChangeExample` | READ + Bound Action CALL |
| 明細分割 | `DemoSplitPOLinesExample` | Collection READ + Script Task + Nested Entity UPDATE + CALL |

---

## 17. 補足: このデモパッケージで使われるProjection / Action一覧

| Workflow | Projection | EntitySet / Action | 用途 |
|---|---|---|---|
| `DemoValidateCustomerPONoExample` | `CustomerOrderHandling` | `CustomerOrderSet` | 受注情報読取。 |
| `DemoAddCustomerPONoExample` | `CustomerOrderHandling` | `CustomerOrderSet` | 受注情報読取、Customer PO No更新。 |
| `DemoSetDefaultValuesToUIExample` | - | - | Projection呼び出しなし。変数Enrichmentのみ。 |
| `DemoCreateTaskPOExample` | `MaintenanceMaterialRequisitionHandling` | `Reference_MaintMaterialReqLine` | 保守資材明細のコレクション読取。 |
| `DemoCreateTaskPOExample` | `WorkTaskHandling` | `CreateNewReq(MaintMaterialOrderNo,LineNo):Void` | 購買要求作成Action。 |
| `DetectRecursionExample` | `RegulatoryBodyHandling` | `RegulatoryBodySet` | Regulatory Bodyの読取・更新。 |
| `DemoStateChangeExample` | `PrepareWorkOrderHandling` | `ActiveSeparateSet` | 作業指示読取。 |
| `DemoStateChangeExample` | `PrepareWorkOrderHandling` | `ActiveSeparate_StartOrder():Void` | 作業指示開始Action。 |
| `DemoSplitPOLinesExample` | `ConfirmPurchaseOrderWithDifferences` | `ConfirmDifferencesSet` | PO差分情報読取。 |
| `DemoSplitPOLinesExample` | `PurchaseOrderHandling` | `PurchaseOrderSet` / `LinePartArray` | POライン読取・更新。 |
| `DemoSplitPOLinesExample` | `PurchaseOrderLinesHistoryAnalysis` | `PurchaseOrderLineHistorySet` | POライン履歴読取。 |
| `DemoSplitPOLinesExample` | `PurchaseOrderHandling` | `CopyPurchaseOrderLines(RecordSelection):Void` | POラインコピーAction。 |

