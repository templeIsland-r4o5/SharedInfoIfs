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

### 2.1. DEMOデータ横断分析から分かる共通ルール

このワークスペースの `Items\Workflow-*.xml` に含まれるDEMO Workflowを横断確認すると、次の傾向がある。

| 観点 | DEMOで確認できる事実 | BPMN生成時の扱い |
|---|---|---|
| Workflow識別子 | `CUSTOM_OBJECT.NAME`、`WORKFLOW.PROCESS_KEY`、`bpmn:process id` は各DEMOで同一。例: `DemoValidateCustomerPONoExample`。 | IFSに登録・起動するWorkflow名は勝手に変更しない。新規作成時も、ユーザーが指定したKeyと `process id` と `BPMNPlane bpmnElement` を一致させる。 |
| `isExecutable` | エクスポート済みDEMO XML内のBPMNは多くが `isExecutable="false"`。一方、BPMN単体の実動作例 `TERA3_version_7.bpmn` は `isExecutable="true"`。 | `CUSTOM_OBJECT` 内のテンプレート/未デプロイWorkflowと、単体BPMNとして投入・実行するWorkflowを混同しない。 |
| Projection READ | `DemoValidateCustomerPONoExample`、`DemoAddCustomerPONoExample`、`DemoStateChangeExample` 等は、Projectionの項目を判定・更新に使う前に `IfsProjectionDelegate` の `READ` を置いている。 | DB/APIから最新値を取得して判定する場合は、原則READを入れる。ただし画面ボタンの起動コンテキストで既に値が渡される場合は、READなしで変数判定する実例もある。 |
| 条件式の形式 | 単純な変数比較は `${CustomerNo == "1010"}`、`${CustomerPoNo == null}`、`${BuyQtyDue < OldQty}`、`${executionSeq > 1}` のようなCamunda EL形式が多い。 | 単純条件は `${...}` を第一候補にする。 |
| JavaScript条件式 | `execution.getVariable("FormField_PoNo") != null`、`execution.getVariable("SupplySourceRef1") == null` のように、User Task後や特定変数確認で使用例がある。 | JavaScript条件式は使用可能だが、全条件の標準形ではない。単純な属性比較へ安易に適用しない。 |
| Script Task | 変数生成・加工に使用。例: `execution.setVariable('executionSeq', seq)`、`OrderSelection` 文字列からキー抽出、履歴配列のソート。 | 複雑な加工が必要な場合だけ使う。単純なGateway条件にScript Taskを増やさない。 |
| Validation Error | `DemoValidateCustomerPONoExample` は `Terminate End Event` + `IfsBpaFailureEndEventListener` + `ifsBpaValidationErrorMessages` で業務エラーを返す。 | 警告/検証エラーとして処理を止める場合はこの構造を使う。通常End Eventだけでは業務エラーにならない。 |
| Process Enrichment | `DemoSetDefaultValuesToUIExample`、`DetectRecursionExample` で、Workflow外へ返す変数を `ifsBpaEnrichmentRegisteredVariables` に登録している。 | UIや次回実行へ値を返す目的。起動時にどの変数が入ってくるかを保証する仕組みではない。 |

### 2.2. DEMOデータが多数あっても推測してはいけない領域

DEMOが多数あっても、次の情報はDEMOだけでは決定できない。これらを推測したことが、TestTERA Workflow生成ミスの直接原因になる。

| 推測してはいけない情報 | 理由 | 必要な確認 |
|---|---|---|
| 画面ボタン押下時に渡るBPA実行時変数名 | DEMOにある `CustomerNo`、`CustomerPoNo`、`WoNo`、`OrderSelection` は、それぞれの画面・Projection・イベントに固有。別画面の `AvFlight` では同じ命名規則とは限らない。 | 動作済みBPMN、IFSデバッグログ、実行時変数一覧、または一時的なメッセージ出力で確認する。 |
| Entity属性名と実行時変数名の一致 | `AvFlight.FlightTurnStatus` のような属性名が、そのまま `${FlightTurnStatus}` で参照できる保証はない。実動作版では `${FlightId == "Inbound"}` が使われている。 | 属性名ではなく、BPAエンジン上の変数名を確認する。 |
| ボタンに割り当て済みのWorkflow Key | DEMOでは `PROCESS_KEY` と `process id` が一致しているが、新規要件のボタンにどのKeyが割り当てられているかはDEMOから分からない。 | IFS画面側のボタン設定、Workflow登録名、Process Keyを確認する。 |
| 正常分岐を通常終了にするか失敗終了にするか | 業務要件上は正常終了に見えても、実験・検証用WorkflowではNot Inbound側にもメッセージを出して停止する場合がある。 | ユーザー要件と実動作版のどちらを優先するか確認する。 |
| BPMN単体で渡すか、`CUSTOM_OBJECT` XMLとして渡すか | DEMOは主にエクスポートXMLで、BPMNは `BPA_DIAGRAM` にHTMLエスケープされている。一方 `TERA3_version_7.bpmn` はBPMN単体。 | 投入先がIFSインポートなのか、モデラーへの貼り付けなのか、既存Workflow更新なのかを確認する。 |
| IFSモデラーが保持する空の拡張要素 | `camunda:properties` の空要素などは業務ロジックからは不要に見えるが、IFSモデラー保存後のBPMNには残る場合がある。 | 動作済みBPMNをベースにする場合は、不要と断定せず保持する。 |

結論として、DEMOデータは「BPMN構造」「Projection API呼び出し」「Gateway条件式」「Validation Errorの書き方」を学ぶ材料として有効である。しかし、「今回の画面ボタンから実際にどの変数名が渡るか」「既に割り当てられているWorkflow Keyは何か」はDEMO横断では導けない。ここをAIが補完すると誤る。

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

### 12.8. TERA3_version_7 / TestTERAボタン検証Workflowの実環境差分

対象ファイル:

- 実環境で動作確認されたBPMN: `C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\TERA3_version_7.bpmn`
- AIが本ドキュメントを基に作成したBPMN: `C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\Items\Workflow-ValidateInboundFlightOnTesttera.bpmn`
- 元要件: `C:\Users\15511914\Documents\IFSshearedInfo\DEMOWORKFLOWPACKFORMTERAJIMA\要件.md`

目的:

- `MY_AIRCRAFT_TURNS` 画面の `TestTERA` ボタン押下時に、Aircraft Turn Statusが `Inbound` の場合は警告を出し、後続処理を中断する。
- 対象Projectionは `FlmAircraftTurnsDetailsHandling`、EntitySetは `AvFlightSet`、Entityは `AvFlight`。

#### 12.8.1. 実環境で動作したBPMNの重要構造

実動作した `TERA3_version_7.bpmn` は、次の構造を持つ。

```xml
<bpmn:process id="TERA3" isExecutable="true">
  <bpmn:startEvent id="StartEvent_1" name="TestTERA Button Pressed">
    <bpmn:outgoing>Flow_ReadAvFlight</bpmn:outgoing>
  </bpmn:startEvent>

  <bpmn:exclusiveGateway id="Gateway_CheckStatus"
                         name="Is Aircraft Turn Status Inbound?"
                         default="Flow_Is_Not_Inbound">
    <bpmn:incoming>Flow_ReadAvFlight</bpmn:incoming>
    <bpmn:outgoing>Flow_Is_Inbound</bpmn:outgoing>
    <bpmn:outgoing>Flow_Is_Not_Inbound</bpmn:outgoing>
  </bpmn:exclusiveGateway>

  <bpmn:sequenceFlow id="Flow_ReadAvFlight"
                     sourceRef="StartEvent_1"
                     targetRef="Gateway_CheckStatus">
    <bpmn:extensionElements>
      <camunda:properties>
        <camunda:property />
      </camunda:properties>
    </bpmn:extensionElements>
  </bpmn:sequenceFlow>

  <bpmn:sequenceFlow id="Flow_Is_Inbound"
                     name="Inbound"
                     sourceRef="Gateway_CheckStatus"
                     targetRef="Event_Terminate">
    <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${FlightId == "Inbound"}</bpmn:conditionExpression>
  </bpmn:sequenceFlow>

  <bpmn:endEvent id="Event_Terminate" name="Show Warning and Stop">
    <bpmn:extensionElements>
      <camunda:inputOutput>
        <camunda:inputParameter name="ifsBpaValidationErrorMessages">
          <camunda:map>
            <camunda:entry key="en">This Fligh Status[${fFlightId}] is Inbound !!</camunda:entry>
          </camunda:map>
        </camunda:inputParameter>
      </camunda:inputOutput>
      <camunda:executionListener class="com.ifsworld.fnd.bpa.process.validation.IfsBpaFailureEndEventListener" event="end" />
    </bpmn:extensionElements>
    <bpmn:incoming>Flow_Is_Inbound</bpmn:incoming>
    <bpmn:terminateEventDefinition id="TerminateEventDefinition_InboundFlight" />
  </bpmn:endEvent>

  <bpmn:sequenceFlow id="Flow_Is_Not_Inbound"
                     name="Not Inbound"
                     sourceRef="Gateway_CheckStatus"
                     targetRef="Event_Complete" />

  <bpmn:endEvent id="Event_Complete" name="Process Completion">
    <bpmn:extensionElements>
      <camunda:inputOutput>
        <camunda:inputParameter name="ifsBpaValidationErrorMessages">
          <camunda:map>
            <camunda:entry key="en">This Fligh Status [${fFlightId}] is  NOT Inbound !!</camunda:entry>
          </camunda:map>
        </camunda:inputParameter>
      </camunda:inputOutput>
      <camunda:executionListener class="com.ifsworld.fnd.bpa.process.validation.IfsBpaFailureEndEventListener" event="end" />
    </bpmn:extensionElements>
    <bpmn:incoming>Flow_Is_Not_Inbound</bpmn:incoming>
    <bpmn:terminateEventDefinition id="TerminateEventDefinition_0og4byf" />
  </bpmn:endEvent>
</bpmn:process>
```

#### 12.8.2. AI生成版との主な差分

| 観点 | AI生成版 `Workflow-ValidateInboundFlightOnTesttera.bpmn` | 実動作版 `TERA3_version_7.bpmn` | 影響 |
|---|---|---|---|
| process id | `wf_validate_inbound_flight_on_testtera2` | `TERA3` | IFS側で登録・起動されるWorkflowキーと一致しない可能性がある。ボタン割当済みWorkflow名と不一致なら起動対象にならない。 |
| Start直後のFlow ID | `Flow_CheckStatus` | `Flow_ReadAvFlight` | ロジック上は同等だが、実環境で作成・保存されたモデルとは異なる。 |
| Start→GatewayのextensionElements | なし | `<camunda:properties><camunda:property /></camunda:properties>` | IFSモデラーが保持する空プロパティがなく、再インポートや編集時に差異になる可能性がある。 |
| Gateway条件式 | `language="JavaScript"` + `execution.hasVariable("FlightTurnStatus") && execution.getVariable("FlightTurnStatus") == "Inbound"` | `${FlightId == "Inbound"}` | 実環境でボタン押下時に渡っている変数名・評価方式と不一致。AIは要件上の属性名をそのまま実行時変数名と誤認した。 |
| 条件に使う変数 | `FlightTurnStatus` | `FlightId` | 最大の相違点。要件に書かれたEntity属性名と、IFS BPA起動コンテキストで実際に参照できる変数名が一致するとは限らない。 |
| メッセージ内変数 | なし | `${fFlightId}` | 実環境版は表示用に別変数 `fFlightId` を参照している。変数名の大文字小文字も含めて要確認。 |
| Inbound側End Event | Terminate + Failure Listener | Terminate + Failure Listener | この点は一致。 |
| Not Inbound側End Event | 通常End Event | Terminate + Failure Listener + Validation Error Message | 要件上は「Inbound時だけ警告」と読めるが、実動作版はNot Inbound側もFailure Listener付きTerminateとして作られている。テスト目的またはボタン処理を常に止める目的がある可能性が高い。 |
| BPMNDI座標 | Gateway/End位置が実動作版より左寄り | IFS保存後の座標 | 実行ロジックには通常影響しないが、IFSモデラーでの見た目・再編集差分になる。 |
| TextAnnotation | View/Component/Buttonまで含めた説明 | Projection APIでRead後に検証する説明 | 注釈は実行に影響しないが、AI生成版は「選択行から変数が供給される」と推測している。 |

#### 12.8.3. なぜAI生成版が大きく誤ったか

原因はBPMN構文の知識不足ではなく、IFS BPA固有の「実行時コンテキスト」と「登録済みWorkflow実体」の情報不足である。

1. **Entity属性名とBPA実行時変数名を同一視した**
   - 要件には `attribute: FlightTurnStatus` とある。
   - しかし実動作版では条件式が `${FlightId == "Inbound"}` になっている。
   - IFS BPAでは、画面ボタン・Projection・イベント・設定方法によって、Workflowへ渡される変数名がEntity属性名そのものとは限らない。
   - ドキュメントには「起動コンテキスト変数は画面・イベントから渡される」としかなく、「属性名から推測してはいけない」「実環境の変数名を確認する必要がある」という制約が不足していた。

2. **条件式の形式を実環境パターンに寄せず、JavaScript式を推測採用した**
   - 既存ドキュメントでは `${...}` と `language="JavaScript"` の両方を紹介していた。
   - AI生成版は安全確認のつもりで `execution.hasVariable()` を使ったが、実動作版はCamunda EL形式 `${FlightId == "Inbound"}` を使っている。
   - 画面ボタン連携やIFSモデラーで保存済みの単純条件では、既存実例に合わせて `${...}` を優先すべきだった。

3. **Workflowキー・process idを要件の任意記述から作成した**
   - 要件には `FlowIDはwf_validate_inbound_flight_on_testtera としても良い` とあるが、実環境版の `process id` は `TERA3`。
   - IFSではWorkflowの登録名、ボタン割当、Process Keyが起動可否に関係するため、実環境で既に動作しているWorkflow名がある場合は、それを最優先する必要がある。

4. **「警告後に後続処理を中断」をInbound側だけと解釈した**
   - 要件文からはInbound時のみ中断と読める。
   - 実動作版ではNot Inbound側もFailure Listener付きTerminate End Eventになっている。
   - これは業務要件としては不自然だが、実験用Workflowとして「どちらの分岐でもメッセージを返して処理を止める」設計にした可能性がある。
   - ドキュメントには、実動作例と業務要件が矛盾する場合は勝手に合理化せず、どちらを優先するか確認するルールが必要だった。

5. **BPMN単体ファイルとIFSエクスポートXMLの違いが明確でなかった**
   - 本ドキュメントは主に `CUSTOM_OBJECT` XML内の `BPA_DIAGRAM` を説明していた。
   - 今回AIが作成したのはBPMN単体ファイルであり、IFSへ投入する単位・登録名・既存Workflowとの置換関係が曖昧だった。
   - BPMN単体を作る場合でも、IFSに登録済みの `process id` / `BPMNPlane bpmnElement` / Workflow Key と整合させる必要がある。

#### 12.8.4. 今後AIにBPMNを生成させる時の必須ルール

1. **実環境で動作したBPMNがある場合は、それを正とする**
   - 新規生成よりも、動作済みBPMNをベースに最小変更する。
   - `process id`、`sequenceFlow id`、`Gateway id`、End Event構造、条件式の記法は、特別な理由がない限り変更しない。

2. **起動コンテキスト変数名を推測しない**
   - Entity属性名、画面表示名、Projection属性名、BPA変数名は別物として扱う。
   - 要件に `FlightTurnStatus` と書かれていても、実行時に参照できる変数が `FlightTurnStatus` とは限らない。
   - 実環境で使う変数名は、動作済みBPMN、IFSデバッグログ、Process Enrichment、または一時的なメッセージ出力で確認する。

3. **条件式は既存実例の形式を優先する**
   - 単純なGateway条件は原則として次の形式を優先する。

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${FlightId == "Inbound"}</bpmn:conditionExpression>
```

   - `language="JavaScript"` と `execution.getVariable()` は、既存BPMNで同じ文脈の使用例がある場合、またはJavaScriptが必要な複雑条件の場合だけ使用する。

4. **End Eventの失敗終了仕様を勝手に単純化しない**
   - IFSでメッセージを表示し、後続処理を止める場合は、Terminate End Event + `IfsBpaFailureEndEventListener` + `ifsBpaValidationErrorMessages` が必要。
   - 実動作版がNot Inbound側にも同じFailure Listenerを持つ場合、業務上不要に見えても勝手に通常End Eventへ変更しない。

5. **IFSモデラーが付与した空の拡張要素を不用意に削らない**
   - 例: Start→GatewayのsequenceFlowに付与された以下の空プロパティ。

```xml
<bpmn:extensionElements>
  <camunda:properties>
    <camunda:property />
  </camunda:properties>
</bpmn:extensionElements>
```

   - 実行に直接影響しない可能性はあるが、IFSモデラーで保存された実物との差分を減らすため保持する。

6. **動作確認済み例にない値を補完しない**
   - メッセージ文、変数名、Flow名、Process Key、End Event種別は「より自然だから」という理由で変更しない。
   - 修正する場合は、要件上の明示指示またはIFS実環境での確認結果を根拠にする。

#### 12.8.5. TestTERA系Workflow作成時の確認事項

TestTERAボタンのWorkflowを作る、または修正する場合は、次を確認してからBPMNを生成する。

| 確認項目 | 必要な理由 | 今回の実動作値・観測値 |
|---|---|---|
| IFSに登録するWorkflow Key / process id | ボタン割当や実行対象に関係する | `TERA3` |
| ボタン押下時に渡る実行時変数名 | Gateway条件で参照するため | `FlightId` が条件式に使われている |
| 表示メッセージで使う変数名 | メッセージ内展開に必要 | `${fFlightId}` が使われている |
| Inbound以外の分岐を失敗終了にするか | 業務上の正常終了/中断仕様に関係する | 実動作版はNot Inbound側もTerminate + Failure Listener |
| 条件式の記法 | Camunda/IFSで評価可否に影響する | `${FlightId == "Inbound"}` |
| BPMN単体かCUSTOM_OBJECT XMLか | IFSへの投入形式が異なる | 今回比較対象はBPMN単体 |

生成前に上記が不明な場合は、推測でBPMNを作らず質問する。特に、属性名 `FlightTurnStatus` と実行時変数 `FlightId` のように名前が一致しない例があるため、変数名は必ず確認対象にする。

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

重要:

- Entity属性名、Projection属性名、画面項目名、BPA実行時変数名は必ずしも一致しない。
- 例として、TestTERAボタン検証の実動作BPMNでは、要件上の判定属性は `AvFlight.FlightTurnStatus` だが、Gateway条件式では `${FlightId == "Inbound"}` が使用されている。
- BPMN生成時に「属性名 = 変数名」と推測してはならない。動作済みBPMN、IFSログ、デバッグ用メッセージ、Process Enrichment等で実際の変数名を確認する。

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

### 13.3. DEMO別の条件式・変数参照実例

DEMO横断で確認できるGateway条件式は次のとおり。

| Workflow | 条件式 | 形式 | 変数の由来 | 読み取り方 |
|---|---|---|---|---|
| `DemoValidateCustomerPONoExample` | `${CustomerNo == "1010"}` | Camunda EL | 起動コンテキストまたはREAD結果 | Customer Noが特定値なら後続チェックへ進む。 |
| `DemoValidateCustomerPONoExample` | `${CustomerPoNo == null}` | Camunda EL | READ結果 | Customer PO Noが未入力ならValidation Errorへ進む。 |
| `DemoAddCustomerPONoExample` | `${CustomerNo == "1000"}` | Camunda EL | 起動コンテキストまたはREAD結果 | Customer Noが特定値ならUser Taskへ進む。 |
| `DemoAddCustomerPONoExample` | `${CustomerPoNo == null}` | Camunda EL | READ結果 | Customer PO Noが未入力なら入力要求へ進む。 |
| `DemoAddCustomerPONoExample` | `execution.getVariable("FormField_PoNo") != null` | JavaScript | User Task入力 | User Taskで入力された値が存在するか確認する。 |
| `DemoCreateTaskPOExample` | `execution.getVariable("SupplySourceRef1") == null` | JavaScript | Multi-instance内のREAD/コレクション要素 | 供給元が未設定の明細だけAction対象にする。 |
| `DemoSplitPOLinesExample` | `${BuyQtyDue < OldQty}` | Camunda EL | Script Taskで算出した変数とREAD結果 | 数量差分がある場合のみ分割処理へ進む。 |
| `DetectRecursionExample` | `${executionSeq > 1}` / `${executionSeq == 1}` | Camunda EL | Script Task + Process Enrichment | 再帰実行回数で処理を分岐する。 |
| `TERA3_version_7` | `${FlightId == "Inbound"}` | Camunda EL | TestTERAボタンの実行時変数 | Aircraft Turn Status相当の判定。ただし変数名は属性名 `FlightTurnStatus` ではない。 |

この表から分かるルール:

- DEMOでは単純比較・null判定・大小比較にCamunda EL `${...}` が多用されている。
- JavaScript条件式は、User Task入力やMulti-instance中の変数確認など、`execution.getVariable()` が必要な文脈で使われている。
- Script Taskで `execution.setVariable()` した変数は、その後のGatewayで `${変数名 ...}` として参照できる。
- READ結果の項目名がそのまま変数として使われるケースはあるが、すべての画面起動コンテキストに一般化してはいけない。

BPMN生成時の判断基準:

1. **READ結果を判定する場合**
   - Projection READを先に置き、そのREADで取得される属性名を条件式に使う。
   - 例: `CustomerPoNo` をREADして `${CustomerPoNo == null}` で判定する。

2. **画面ボタンの起動コンテキストを判定する場合**
   - 画面・ボタンから渡る実行時変数名を確認する。
   - 属性名から条件式を作らない。
   - TestTERAの実動作例では、要件属性 `FlightTurnStatus` に対して条件式は `${FlightId == "Inbound"}` だった。

3. **User Taskの入力値を判定する場合**
   - `camunda:formField id` が後続の変数名になる。
   - JavaScript条件式の使用例があるが、Camunda ELで書ける場合もある。既存DEMOに合わせる。

4. **Script Taskで作った値を判定する場合**
   - `execution.setVariable('OldQty', value)` のように設定した変数名を後続Gatewayで使う。
   - スクリプト内変数名とBPMN変数名を混同しない。

### 13.4. DEMO別のProjection利用実例

| Workflow | Projection / EntitySet / Action | 用途 | 生成時の注意 |
|---|---|---|---|
| `DemoValidateCustomerPONoExample` | `CustomerOrderHandling` / `CustomerOrderSet` / `READ` | Customer Orderを読み、`CustomerPoNo` を検証する。 | 検証対象がDB上の最新値ならREADを入れる。 |
| `DemoAddCustomerPONoExample` | `CustomerOrderHandling` / `CustomerOrderSet` / `READ` + `UPDATE` | Customer PO Noを入力させて更新する。 | UPDATE前にREADし、必要に応じてETagを扱う。 |
| `DemoStateChangeExample` | `PrepareWorkOrderHandling` / `ActiveSeparateSet` / `READ` + `ActiveSeparate_StartOrder():Void` | Work Orderを読み、Bound Actionで状態変更する。 | Bound Actionは `ifsBpaProjectionCallSignature` を正確に書く。 |
| `DemoCreateTaskPOExample` | `MaintenanceMaterialRequisitionHandling` / `Reference_MaintMaterialReqLine` / Collection `READ` | 明細コレクションを読み、Multi-instanceでAction実行する。 | コレクション変数名とループ要素変数名を分ける。 |
| `DemoSplitPOLinesExample` | 複数Projectionの `READ` / `UPDATE` / `CALL` | POライン分割、履歴読取、コピーAction。 | 複数READ結果・ETag・ネストEntityキーを混同しない。 |
| `DetectRecursionExample` | `RegulatoryBodyHandling` / `RegulatoryBodySet` / `READ` + `UPDATE` | 再帰検出用に更新しつつ、Process Enrichmentで実行回数を戻す。 | 再帰防止変数は次回実行へ返す必要がある。 |
| `TERA3_version_7` | Projection情報は注釈にあるが、BPMN上にProjection Service Taskはない | ボタン起動時の変数だけでGateway判定する構造。 | Projection名が要件にあるだけで、必ずREAD Taskを生成するとは限らない。実行時変数確認が先。 |

このため、Projection情報が要件に書かれている場合でも、BPMN上でREADが必要かどうかは別判断になる。

- **READが必要なケース**: 判定・更新に使う値をDB/APIから取得する必要がある場合。
- **READが不要なケース**: ボタン押下時点で必要な値がBPA変数として渡され、動作済みBPMNでもREADなしで判定している場合。
- **不明なケース**: 推測せず、どの変数が起動時に渡るか、READして取得すべきかを確認する。

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

### 生成前の前提確認

- 実環境で動作したBPMNが存在する場合、それを正として差分最小で修正しているか。
- IFSに登録されるWorkflow Key / `bpmn:process id` / `bpmndi:BPMNPlane bpmnElement` が一致しているか。
- 画面ボタンやイベントから渡されるBPA実行時変数名を確認したか。Entity属性名から推測していないか。
- 要件上の属性名と実行時変数名が異なる可能性を明記・確認したか。
- BPMN単体ファイルを作るのか、`CUSTOM_OBJECT` XML内の `BPA_DIAGRAM` を更新するのかを確認したか。
- IFSモデラーが保存した空の `camunda:properties` など、動作済みBPMNに存在する拡張要素を不用意に削除していないか。

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
- 単純条件では、既存実例に合わせて `${変数名 == "値"}` 形式を優先しているか。
- `language="JavaScript"` / `execution.getVariable()` を使う場合、その文脈でIFS上の動作実績があるか。
- 条件式内の変数名は、Projection属性名ではなくBPA実行時変数名として確認済みか。

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
- 実動作BPMNで正常側分岐にもFailure Listener付きTerminate End Eventがある場合、業務上不要に見えても勝手に通常End Eventへ変更していないか。
- メッセージ内の `${...}` 変数名は、実行時に存在する変数名として確認済みか。

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

