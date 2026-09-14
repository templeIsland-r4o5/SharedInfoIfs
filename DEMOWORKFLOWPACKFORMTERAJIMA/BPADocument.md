# IFS Cloud Business Process Automation (BPA) 解説

## 1. 概要

IFS CloudのBPA（Workflow）は、Camunda BPMNエンジンをベースにしており、業務プロセスをグラフィカルに定義し、自動化するための強力なツールです。BPAを使用することで、Projection APIの呼び出し、カスタムロジックの実行、ユーザー操作の要求などを組み合わせ、複雑な業務フローを構築できます。

本文書は、サンプルとして提供されるBPA定義（`Workflow-*.xml`）を基に、その構文と典型的なユースケースを解説します。

## 2. 基本的な記述方法

BPAの定義はXML形式で行われ、BPMN 2.0標準に準拠しています。特に重要な要素は以下の通りです。

### 2.1. Service Task (サービス・タスク)

Projection APIの呼び出し（READ, UPDATE, CREATE, DELETE, CALL）を実行します。IFS CloudのBPAでは、`com.ifsworld.fnd.bpa.IfsProjectionDelegate` Javaクラスがこの役割を担います。

**記法例:**
```xml
<bpmn:serviceTask id="Activity_0f93d25" name="Read Work Order" camunda:class="com.ifsworld.fnd.bpa.IfsProjectionDelegate">
  <bpmn:extensionElements>
    <camunda:inputOutput>
      <camunda:inputParameter name="ifsBpaProjectionAction">READ</camunda:inputParameter>
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

- `camunda:class`: 常に `com.ifsworld.fnd.bpa.IfsProjectionDelegate` を指定します。
- `ifsBpaProjectionAction`: `READ`, `UPDATE`, `CREATE`, `DELETE`, `CALL` のいずれかを指定します。
- `ifsBpaProjectionName`: 対象のProjection名を指定します。
- `ifsBpaProjectionEntitySetName`: 対象のEntitySet名を指定します。
- `ifsBpaProjectionParameters`: API呼び出しのキーやパラメータを `<camunda:map>` を使って渡します。`${変数名}` の形式でワークフロー内の変数を参照できます。

### 2.2. Script Task (スクリプト・タスク)

JavaScriptを使用して、変数操作や簡単な計算、文字列処理などのカスタムロジックを実行します。

**記法例:**
```xml
<bpmn:scriptTask id="Activity_0l7lcni" name="Add default values to execution" scriptFormat="JavaScript">
  <bpmn:script>
    execution.setVariable('OrganizationSite', 31);
    execution.setVariable('Description', 'Track product levels &amp; orders');
  </bpmn:script>
</bpmn:scriptTask>
```
- `scriptFormat`: `JavaScript` を指定します。
- `<bpmn:script>`: 実行したいJavaScriptコードを記述します。
- `execution.setVariable('変数名', 値)`: ワークフローに変数を設定します。
- `execution.getVariable('変数名')`: ワークフローから変数を取得します。

### 2.3. User Task (ユーザー・タスク)

プロセスを一時停止し、ユーザーに入力を求めるダイアログを表示します。ユーザーが入力した値はワークフロー変数として後続のタスクで利用できます。

**記法例:**
```xml
<bpmn:userTask id="Activity_1ybqtct" name="User Enter Customer PO Number" camunda:formKey="CustomerPONo">
  <bpmn:extensionElements>
    <camunda:formData>
      <camunda:formField id="FormField_PoNo" type="string" />
    </camunda:formData>
  </bpmn:extensionElements>
</bpmn:userTask>
```
- `camunda:formKey`: ユーザー・タスクのフォームを識別するキーです。
- `camunda:formField`: ユーザーに入力を求めるフィールドを定義します。`id`が変数名になります。

### 2.4. Exclusive Gateway (排他ゲートウェイ)

条件に基づいてプロセスのフローを分岐させます。

**記法例:**
```xml
<bpmn:exclusiveGateway id="Gateway_16676tt">
  <bpmn:outgoing>Flow_0if5c8e</bpmn:outgoing>
  <bpmn:outgoing>Flow_0u1xsne</bpmn:outgoing>
</bpmn:exclusiveGateway>

<bpmn:sequenceFlow id="Flow_0u1xsne" sourceRef="Gateway_16676tt" targetRef="Activity_0g2o82j">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${CustomerNo == "1000"}</bpmn:conditionExpression>
</bpmn:sequenceFlow>
```
- `<bpmn:conditionExpression>`: 分岐条件を式で記述します。`${変数名}` の形式でワークフロー変数を参照できます。

---

## 3. ユースケース別 実装例

### 3.1. 顧客発注番号(PO No.)の検証と入力要求 (Workflow-DemoValidateCustomerPONoExample, Workflow-DemoAddCustomerPONoExample)

- **シナリオ**: 特定の顧客（例: `CustomerNo == "1010"`）の場合、顧客発注番号が空であればエラーを返す。別の顧客（例: `CustomerNo == "1000"`）の場合は、ユーザーに入力を促す。
- **ポイント**:
    - **分岐**: `Exclusive Gateway`を使い、`CustomerNo`で処理を分岐。
    - **検証**: `Exclusive Gateway`の条件式 `${CustomerPoNo == null}` で項目が空かチェック。
    - **エラー通知**: `Terminate End Event` と `IfsBpaFailureEndEventListener` を使用して、トランザクションをロールバックし、ユーザーにエラーメッセージを表示。
    - **ユーザー入力**: `User Task` を使用して、ユーザーにPO番号の入力を求め、その結果を変数に格納。
    - **データ更新**: `Service Task` (UPDATE) を使用して、入力されたPO番号でレコードを更新。

### 3.2. UIへのデフォルト値設定 (Workflow-DemoSetDefaultValuesToUIExample)

- **シナリオ**: 新規レコード作成時に、特定の項目にデフォルト値を設定してUIに表示する。
- **ポイント**:
    - **値の設定**: `Script Task` で `execution.setVariable()` を使い、複数のデフォルト値を設定。
    - **値の引き渡し**: `com.ifsworld.fnd.bpa.process.enrichment.IfsBpaProcessEnrichmentDelegate` を持つ `Service Task` を使用して、ワークフロー内で設定した変数をUI側に引き渡す。`ifsBpaEnrichmentRegisteredVariables` で引き渡す変数名をリストアップする。

### 3.3. 複数レコードに対する一括処理 (Workflow-DemoCreateTaskPOExample)

- **シナリオ**: 特定の条件（例: 作業指示書に紐づく購買要求がない）を満たす複数の明細行に対して、一括で購買要求を作成する。
- **ポイント**:
    - **データ取得**: `Service Task` (READ) で `ifsBpaProjectionIsCollection="true"` を設定し、複数行のデータをコレクション（配列）として取得。
    - **ループ処理**: `Sub-Process` と `Multi-instance Loop` を組み合わせ、取得したコレクションの各要素に対して繰り返し処理を実行。
        - `camunda:collection`: ループ対象のコレクション変数を指定。
        - `camunda:elementVariable`: ループ内の各要素を格納する変数を指定。
    - **API呼び出し**: ループ内の`Service Task` (CALL) で、明細行ごとに購買要求作成API (`CreateNewReq`) を呼び出す。

### 3.4. 再帰呼び出しの防止 (Workflow-DetectRecursionExample)

- **シナリオ**: イベントトリガーなどで意図せずワークフローが繰り返し呼び出されてしまう（再帰ループ）のを防ぐ。
- **ポイント**:
    - **実行カウンター**: `Script Task` を使い、ワークフローの実行回数をカウントする変数を管理する (`executionSeq`)。
    - **カウンターの永続化**: `IfsBpaProcessEnrichmentDelegate` を使ってカウンター変数をワークフローの外部に渡し、次回の実行に引き継ぐ。
    - **分岐**: `Exclusive Gateway` でカウンターが1より大きいかをチェック (`${executionSeq > 1}`)。2回目以降の実行であれば、何もせずにプロセスを終了させることで再帰を防ぐ。

### 3.5. レコードの状態変更 (Workflow-DemoStateChangeExample)

- **シナリオ**: ワークフロー経由でレコードのステータスを変更する（例: `Released` から `Started` へ）。
- **ポイント**:
    - **事前読み込み**: 状態変更は対象エンティティに対するBound Actionであるため、まず `Service Task` (READ) で対象のレコードを読み込み、コンテキストにロードする。
    - **状態変更アクションの呼び出し**: 次の `Service Task` (CALL) で、引数なしで状態変更アクション（例: `ActiveSeparate_StartOrder()`）を呼び出す。これにより、事前にロードされたレコードに対してアクションが実行される。

### 3.6. 発注ラインの分割 (Workflow-DemoSplitPOLinesExample)
- **シナリオ**: 購買発注ラインの数量が変更された場合に、差分を新しいラインとして分割する。
- **ポイント**:
    - **変更履歴の読み取り**: `Service Task` を使用して、購買発注ラインの変更履歴(`PurchaseOrderLineHistorySet`)を読み取る。
    - **差分の計算**: `Script Task` で変更履歴を解析し、変更前の数量を特定する。
    - **条件分岐**: `Exclusive Gateway` を使用し、数量が減少した場合のみ分割処理を実行する (`${BuyQtyDue < OldQty}`
    - **ライン操作**: 複数の `Service Task` を使用して、元のラインの数量を更新し、新しいラインをコピーして作成し、最後に元のラインの数量を元に戻す、という複雑な操作を行う。
