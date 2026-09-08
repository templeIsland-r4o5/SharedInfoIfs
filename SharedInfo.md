# SharedInfoシステム要件定義書

## 1. ドキュメント管理・概要

- **ドキュメントID / タイトル**: SPEC-CFG-MAINT-SharedInfo-001 / Shared Infoシステム後継機能 要件定義書
- **対象IFSバージョン**: IFS Cloud 25R2
- **対象モジュール / 画面名 (Component / Page)**:
  - Maint (Maintenance)
  - `AircraftTurnDetails.client`
  - （新規）`CustomShipMonitoring.client`
- **関連LU (Logical Unit) / Projection**:
  - `AircraftTurn`
  - `JtTask`
  - （新規）`CustomShipMonitoringHandling.projection`
- **目的・業務背景（Gapの概要と解決策）**:
  - **背景**: 現在の「Shared Info」システムは、インフラの老朽化、IFSとの分断による二重管理、高額な維持コストといった課題を抱えている。特に、整備記録として残せないグレーゾーンな情報（不具合の予兆、作業の補足事項等）の伝達・蓄積手段として利用されているが、これが本来あるべき整備記録の形骸化を招くリスクも指摘されている。
  - **目的**: IFS Cloudへの移行を機に、Shared Infoが担ってきた業務目的を再定義し、IFSの標準機能とコンフィグレーションを最大限活用した、安全で持続可能なソリューションを構築する。これにより、システム維持コストの削減、業務効率の向上、およびデータの一元管理を実現する。
- **採用するConfiguration機能一覧**:
  - Custom Page
  - Custom Entity / Custom Fields (Persistent)
  - Page Configuration (Custom Commands, Layout changes)
  - IFS Cloud BPA (Workflow)
  - Custom Events & Event Actions

## 2. ソリューション全体構造 & 連携シーケンス

Shared Infoが担う「①一時的な情報伝達」と「②継続的な事象監視」の2つの主要なユースケースを分離し、それぞれに最適化したソリューションをIFS Cloud内に構築する。

- **アーキテクチャ全体図（Mermaidダイアグラム）**:
  ```mermaid
  graph TD
      subgraph "IFS Cloud"
          A[整備士/Fleet] -- 1. 不明点をTurn Noteに記録 --> B(Aircraft Turn Details画面)
          A -- 2. 注視事象を起票 --> C{Ship Monitoring画面 (Custom Page)}
          C -- 3. 新規Monitoring Item作成 --> D[CustomShipMonitoring Entity]
          B -- 4. 画面上でTurn Noteを共有 --> B
          A -- 5. Monitoring Itemに対応する作業実施 --> E[JtTask / MaintFault]
          E -- 6. 作業完了イベント発火 --> F{BPA Workflow}
          F -- 7. Monitoring Itemの状態を更新 --> D
          G[技術/SE] -- 8. 過去の事象を検索 --> C
      end
  ```

- **処理シーケンス**:
  1.  **一時的な情報伝達 (Turn Note)**:
      - ユーザー（整備士・EST等）が `Aircraft Turn Details` 画面上のカスタム領域に、その整備機会限りの申し送り事項（Turn中の不明点問合せなど）を記録する。
      - 記録された情報は同画面で関係者に共有される。この情報は当該Turnに紐づき、長期的な蓄積は目的としない。
  2.  **継続的な事象監視 (Ship Monitoring)**:
      - ユーザー（整備士・Fleet等）が、予防整備や経過観察が必要な事象（SQ予備軍など）を、新設する「Ship Monitoring」カスタムページから「Monitoring Item」として起票する。
      - Fleetや技術部門は、起票されたItemをレビューし、必要に応じてIFS標準の`Task`や`Fault`を作成して対応を計画する。
      - 関連する`Task`が完了すると、BPAワークフローが起動し、対応する「Monitoring Item」のステータスを自動で更新する。
      - 過去のMonitoring Itemは検索・参照可能とし、ナレッジとして活用する。

## 3. データモデル & Custom Fields / Custom Entities

### 3.1. Turn Note (Aircraft Turn Detailsへの追加)

- **対象Logical Unit / View**: `AircraftTurn`
- **項目定義一覧**:
  - `AircraftTurnDetails`画面に、`CustomTurnNote` EntityをListとして表示する。

  **Custom Entity: `CustomTurnNote`**
  | 項目名 (Attribute Name) | 表示ラベル (Prompt) | データ型 (Type/Length) | 属性種別 (Persistent) | 必須 | 備考 |
  |---|---|---|---|---|---|
  | `TurnNoteId` | Turn Note ID | `NUMBER` | Persistent | YES | 主キー |
  | `TurnId` | Turn ID | `NUMBER` | Persistent | YES | `AircraftTurn`への外部キー |
  | `NoteText` | 申し送り内容 | `VARCHAR2(2000)` | Persistent | YES | |
  | `ReportedBy` | 登録者 | `VARCHAR2(30)` | Persistent | YES | |
  | `ReportedAt` | 登録日時 | `TIMESTAMP` | Persistent | YES | |
  | `Role` | 登録者ロール | `VARCHAR2(50)` | Persistent | NO | Technician, Fleet, ESTなど |

### 3.2. Ship Monitoring Item

- **Custom Entity: `CustomShipMonitoring`**
- **項目定義一覧**:

  | 項目名 (Attribute Name) | 表示ラベル (Prompt) | データ型 (Type/Length) | 属性種別 (Persistent) | 必須 | 読取専用 | デフォルト値 / 導出ロジック |
  |---|---|---|---|---|---|---|
  | `MonitoringId` | モニタリングID | `NUMBER` | Persistent | YES | NO | Sequenceによる自動採番 |
  | `ShipNo` | 機番 | `VARCHAR2(10)` | Persistent | YES | NO | |
  | `Title` | 件名 | `VARCHAR2(200)` | Persistent | YES | NO | |
  | `Description` | 詳細 | `VARCHAR2(4000)` | Persistent | NO | NO | |
  | `Status` | 状態 | `VARCHAR2(30)` | Persistent | YES | NO | デフォルト値: `OPEN` (OPEN, IN_PROGRESS, CLOSED) |
  | `ReportedBy` | 起票者 | `VARCHAR2(30)` | Persistent | YES | YES | |
  | `CreatedAt` | 起票日時 | `TIMESTAMP` | Persistent | YES | YES | `SYSTIMESTAMP` |
  | `ClosedBy` | クローズ者 | `VARCHAR2(30)` | Persistent | NO | YES | |
  | `ClosedAt` | クローズ日時 | `TIMESTAMP` | Persistent | NO | YES | |

- **関連エンティティ**:
  - `CustomShipMonitoring`と`JtTask` / `MaintFault`を関連付けるための関連エンティティ `MonitoringTaskLink` を作成する。

## 4. UI / Page Configurations & Commands

- **対象ページ: `AircraftTurnDetails.client`**
  - **レイアウト変更**:
    - 新規Groupを追加し、`CustomTurnNote`のListを表示する領域を設ける。
    - List内には、NoteText, ReportedBy, ReportedAt を表示する。
  - **Custom Commands**:
    - **コマンド名**: `CreateMonitoringItem`
    - **表示ラベル**: "注視事象を起票"
    - **アクション**: `CustomShipMonitoring.client`の新規作成画面にナビゲートする。その際、現在のTurnの機番をパラメータとして渡す。

- **対象ページ: `CustomShipMonitoring.client` (新規作成)**
  - **レイアウト・コンポーネント**:
    - **List View**: `MonitoringId`, `ShipNo`, `Title`, `Status`, `CreatedAt` を表示する一覧画面。ステータスや機番でのフィルタリング機能を提供する。
    - **Detail View**: 選択したMonitoring Itemの詳細情報を表示。関連するTaskやFaultの一覧、対応履歴（ステータス変更履歴）のタブを設ける。
  - **Custom Commands**:
    - **コマンド名**: `LinkTask`
    - **表示ラベル**: "関連タスクを追加"
    - **アクション**: `JtTask`のSelectorを開き、関連付けるタスクを選択させる。

## 5. ビジネスプロセス・自動化 (BPA / Workflow) 仕様

- **Workflow ID**: `wf_UpdateMonitoringStatus`
- **トリガー条件**: Event Invoked (`JT_TASK_COMPLETED`)
- **インプットパラメータ**: `JtTask.Objkey`
- **プロセスフロー設計**:
  1. **開始**: `JT_TASK_COMPLETED`イベントでWF開始。
  2. **関連チェック**: `MonitoringTaskLink`テーブルを検索し、完了したTaskに紐づく`MonitoringId`を取得。
  3. **分岐**: `MonitoringId`が存在する場合のみ続行。
  4. **ステータス更新**: `CustomShipMonitoringHandling.projection` の `UpdateStatus`アクションを呼び出し、対象Monitoring Itemのステータスを `IN_PROGRESS` または `CLOSED` に変更する。（ロジックは要検討）
  5. **終了**

## 6. イベント & トリガー (Custom Events & Event Actions) 仕様

- **Event ID**: `JT_TASK_COMPLETED`
- **対象LU**: `JtTask`
- **Event Type**: Model Event
- **トリガータイミング**: After - Update
- **発火条件**: `NEW:Objstate = 'Finished'` AND `OLD:Objstate != 'Finished'`
- **Event Actions 詳細**:
  - **Action Type**: Execute Workflow
  - **実行パラメータ**: `Workflow ID: wf_UpdateMonitoringStatus`, `Parameters: { "task_objkey": "${Objkey}" }`

## 7. セキュリティ & 権限 (Permission Sets)

- **必要なProjection権限**:
  - `CustomShipMonitoringHandling.projection`: Full Access権限をFleet、技術、SEロールに付与。整備士ロールにはRead-onlyおよびCreate権限を付与。
  - `CustomTurnNoteHandling.projection`: Full Access権限を整備士、Fleet、ESTロールに付与。
- **対象Permission Set / ロール**:
  - `JAL_TECHNICIAN_ROLE`: `CustomTurnNote`の作成・参照、`CustomShipMonitoring`の作成・参照権限。
  - `JAL_FLEET_ROLE`: 上記に加え、`CustomShipMonitoring`の更新・クローズ権限。

## 8. 非機能要件・影響範囲分析

- **パフォーマンス考慮事項**:
  - 旧Shared Infoは大量データによる性能問題を抱えていた。`CustomShipMonitoring`の検索は、機番、ステータス、期間で効率的なインデックスを設定し、レスポンスを担保すること。
  - タブレットでの利用が主となるため、UIの表示速度や操作性を考慮した軽量な画面設計を行う。
- **他モジュール・標準機能への影響**:
  - IFS標準の`JtTask`, `AircraftTurn`と連携するが、標準テーブルの変更は行わない。すべての拡張はCustom Entityと関連付けによって実現する。
- **データ移行**:
  - 旧Shared Infoの過去データ（特にShip Monitor）は、新設する`CustomShipMonitoring`エンティティに移行する必要がある。移行ツールの開発とデータクレンジング計画が必須。

## 9. テストケース & 単体検証シナリオ

| No | シナリオ種別 | 前提条件 | 実施手順 | 期待される結果 |
|---|---|---|---|---|
| 1 | 正常系 (Turn Note) | 整備士が`Aircraft Turn Details`画面を開いている | 1. 画面上の「申し送り」セクションにテキストを入力し保存。<br>2. ESTが同画面を開く。 | 1. 入力した内容がリストに表示される。<br>2. ESTの画面でも同じ内容が参照できる。 |
| 2 | 正常系 (Monitoring) | Fleet担当者が「Ship Monitoring」画面を開いている | 1. 新規ボタンを押し、機番と件名を入力して保存。<br>2. 作成したItemに関連タスクを紐づける。 | 1. 新しいMonitoring Itemが作成され、ステータスが`OPEN`になる。<br>2. Detail画面で関連タスクが確認できる。 |
| 3 | 正常系 (BPA連携) | No.2で紐づけられたTaskが整備士により完了される | 1. 整備士が`JtTask`を完了ステータスにする。 | 1. BPAが起動し、Monitoring Itemのステータスが`IN_PROGRESS`等に自動更新される。 |
| 4 | 権限制御 | 整備士ロールのユーザーが、他人が起票した`CLOSED`のMonitoring Itemを開く | 1. 編集ボタンを押そうとする。 | 1. 編集ボタンが無効化されており、更新できない。 |

## 10. 未決定事項 & 要確認事項 (TBD)

- **User情報**: スタンドアロン化した場合のUser情報の取得元（MatriX連携 or 手動管理）の最終決定。
- **データ移行**: 旧Shared Infoからの具体的なデータ移行範囲、手順、および移行ツールの詳細仕様。
- **BPAロジック**: Task完了時にMonitoring Itemのステータスをどのように更新するかの詳細ロジック（例：すべての関連タスクが完了したら`CLOSED`にするのか、など）。
- **画面詳細仕様**: 各カスタムページのワイヤーフレームと詳細な項目定義。
- **代替コミュニケーションツール**: Turn中の簡易的な問い合わせにGoogle Chat等のツールを公式に利用するか、IFS内のTurn Note機能に一本化するかの最終判断。

---
---

# SharedInfo関連の検討.docx

## 検討の概要
### 検討の背景
- SharedInfoは継続利用前提で進めてきた。IFSの移行スコープ外としていた。
- SharedInfoを継続利用するために必要なシステム対応は以下を想定しているが、コスト見積が想定よりも高くなることが判明した。
  - ❶インフラ改修（DBバージョンアップ対応）
  - ❷ アプリ改修（Mighty等からは切り離し、SharedInfo単体で利用できるようにする対応）
  - ❸ アプリ改修（iPad版アプリをブラウザ版相当に機能追加する対応）
- 改めて、業務観点でSharedInfoが本当に必要なのかを再評価する必要ができた。

### 検討の目的
- SharedInfoの現行業務でのユースケースを洗い出し、業務目的を可視化する
- 業務目的を満たす方法について、SharedInfo以外の代替方法も含め、IFS導入後の最適なソリューション案を検討する

### 検討対象の機能
- Report Create/List
- Ship Monitor Create/List
※上記以外の機能（Maintenance Plan/File Server）は、2026年2-3月時点の評価で、廃止可能な旨を判断済みのため除外

---

## 現行業務の整理
### SharedInfoユースケース一覧
SharedInfoを使って管理している情報には、情報の性質（情報の寿命、整備記録か否か、蓄積要否）の観点で、いくつか種類があることがわかった。

詳細は、`ARISE_SHIP_SharedInfo現行業務整理.xlsx.md` を参照。

---

## 対応方針の検討
### 概要
情報の種類によって、IFS導入後にどのように管理すべきかを検討する。

**検討時の考慮事項:**
- できるだけIFS上で管理できる方法を探る。
  - IFS上で管理できるほうが、複数システムを使い分ける必要がなく、整備士目線では都合がよいと考えるため。
- 整備記録として残すべき情報は、整備記録としてIFSに記録されるようにする。
  - 全社的に、品質事象が継続して発生している状況がある。現行の運用では、SharedInfoのReport機能が汎用的に作られているが故に、本来ならばSQ Upすべき情報も、SharedInfoのReport機能で記録し、飛行機を飛ばせてしまうという安全上のリスクをはらんでいた。そのような余地は残さないようにして、整備記録として記録すべき情報は、整備記録に記録される体験設計となるよう留意する。

`ARISE_SHIP_SharedInfo現行業務整理.xlsx.md` の[対応方針の検討]シートも参照。

---

### 詳細①：機番に紐づく情報のコミュニケーション
- **業務目的**: 情報の伝達
- **業務要件**:
  - 整備士・技術・SE・Fleet・ESTが、情報を登録する。登録された情報を参照する。
  - 情報のやりとりは、1 Turn中に完結する場合もあれば、複数Turnをまたいで継続する場合もある。
  - 伝えたい情報自体は、整備士が読んだら用が済み、機番に紐づけて蓄積する必要はない。
  - モバイルで見られる。

- **取り扱う情報の具体例**:
  - 整備士からFleetへのTurn中の不明点問い合わせ -> **Google Chat**
    - [確認ポイント] Google Chatだと事足りないことがあるか？
  - Crewからの申し送り（耐空性に影響ない事象） -> **Aircraft Turn Details に画面項目追加**
  - 技術/SE/Fleetから整備士への整備作業依頼（単発） -> **Aircraft Turn Details に画面項目追加**
  - 技術/SE/Fleetから整備士への整備作業依頼（継続/複数Turnをまたぐ）
    - [確認ポイント]このようなケースは、Ship Monitoringを起点とした整備作業依頼のみだろうか？Yesであれば、対応方針検討詳細②にマージする。

- **対応案イメージ**:
  - **Aircraft Turn Detailsに画面項目追加（C-JAL-MEX019に要件追加）**
  - **管理すべき情報項目案**:
    - 登録者のロール（Technician・SE・Fleet・EST）※誰からの情報かわかるようにする
    - 伝達したい情報
  - **画面イメージ**:
    - 機能の配置は想像に基づく。要は、Aircraft Turn Details画面で登録・参照できるようにしたい。
    - ※細かい項目の定義は別途検討

- **9/8 議論メモ**:
  - このソリューション案で、要件は満たせる理解をしている。（寺嶋さん・仲摩さん）
  - 画面に入力項目を用意するということは、データ保管先のテーブルも作成が必要となるはず。「C-JAL-MEX019の要件追加」という取り扱いで済むのか懸念される。（寺嶋さん）
  - C-JAL-MEX019と要件の目的は合致している理解をしている。実装がConfigで済むのかは不明。（領家さん）
  - MMでも拾うべき要件と考えている。
  - **アクションプラン**:
    - C-JAL-MEX019に追加する方向で動く
    - C-JAL-MEX019に項目追加できないか、IFSに問い合わせる（川上）★

---

### 詳細②：機番に紐づく注視事象（整備記録外）の情報記録・蓄積
- **業務目的**: 情報蓄積・時系列に合わせた情報の参照
- **業務要件**:
  - 整備士やFleetが、Turn中もしくはTurn後に、注視すべき事象の情報を登録する
  - 過去に登録された情報に対し、次Turn以降も、情報を追加登録できる（例：経過観察結果の記録）
  - 過去の登録情報を参照できる
  - 過去の登録情報に対して、特定のキーワードや条件で検索できる（例：類似SQの検索）
  - モニタリングが済んだら、クローズ処理ができる

- **取り扱う情報の具体例**:
  - 潜在的故障に対する対応記録
  - トラブルシューティング対応の記録
  - Chronic SQの観察記録
  - 予防整備の作業計画
  - ★補足資料：Shared Infoで管理している情報

- **今後の検討ステップ**:
  - 案2は、IFSに開発規模の見積依頼をする必要がありそう。インプットはワイヤーフレーム。Configで済むのか否か。
  - 案2、案3のノックアウトは何なのか？それは、運用の工夫や機能削減で回避できるのか？を評価する深掘りが必要になりそう
  - 案2 Configで済む範囲にした場合、運用上耐えられるのかしら？
  - 案3 何が運用上きついのか？

- **9/8のゴール**:
  - 案の全体像を理解いただく
  - SharedInfoでカバーしていた業務が、IFSのどの機能でカバーされるのかの理解をすり合わせる
  - 案2・案3のノックアウトがあるか、運用上の工夫/機能削減で回避できるのか？の深掘り
  - 案2は、IFS側への確認事項をとりまとめて、USI問い合わせ
  - 案3は、作りを改善するなら、その検討を宿題にする

- **議論メモ**:
  - Ship Monitoring起点の作業依頼があったとき、必ずしも強制力がないと理解した。必ずOn-condition Task/Faultを起票するような運用でよいのだろうか？（領家さん）
  - 部品交換をする際は、必ずFaultを起票するだろうが。
  - 作業を実施する時は、必ずTask/Faultを起票する。
  - On-condition TaskはFleetが起票するのか、整備士が起票するのか？
    - 現行運用では、整備士が作業直前にやっている。ただ、TaskであればUnassignすればよいので、Fleetが事前に起票していてもよい。
  - 不具合対応ではないため、eLog（整備記録）に入っていなくてもよい。
  - 長期的に見て、eLogにも記録しなさい、という流れになったときにも耐えうるか？
  - Taskで起票しておいて、Taskで、必要ならばFaultを起票しなさいと指示しておく。
  - RCM（Reliability Centered Maintenance） PFカーブ
  - **案の優先度**:
    - 案3: 表記ゆれ、属地ツールの誘発が懸念される。スプレッドシート管理は、それ用の運用整備も必要となってくる。
    - 案2 Configのみ＞案3
    - 案2: FaultやTaskのデータと、Monitoring Itemのデータを関連づけるところがModくさい
  - **アクションプラン**:
    - 大きな方向としては、案2をIFSに見積してもらう。Modification/Configurationで仕分けしてもらい、Mod部分を削ぎ落として、Configに着地させたい。
    - **IFSにインプットするにあたり**:
      - Modificationが要りそうなところとそうでないところの仮説を立てる。
      - 必要な改修を洗い出す
      - ワイヤーフレームを精緻化する
      - 機能要件を分解する（画面、ボタンの機能を明文化する）
      - 標準のデータとの接点になるところを示す
      - 上記機能要件一覧に対して、Modification Configurationの仕分けをIFSに依頼する

---

## その他メモ

- **[潜在的故障の対応]**
  - SQ予備軍連絡、予防整備
- **[Deferred Faultの詳細]**
  - Deferred Faultに対する補足情報
- **[コミュニケーション]**
  - パーツ番号問い合わせなど
  - Crewからの連絡内容申し送り（ESTがCREWから連絡を受ける、相談しながら解決をした。この事実を整備士に共有する）
  - ACARS情報の取り込み（ACARSの情報をReportとして起票する）
- **[情報共有]**
  - 包括委託先が整備作業結果の報告をする
  - カスタマー便の伝達事項を共有する
- **[ITMでの活用]**
  - 不具合起票時に過去の類似事象を確認する。ReportではなくShip Monitorを使っている
  - 品質分析をするために、Shared InfoのShip Monitorの情報を使用して、不具合の分析をする

---

# その他のドキュメントからの抜粋

## Shared Infoで管理している情報.docx

Shared Infoでは、予防整備や潜在的SQに関する情報を取り扱っている。

1. **潜在的故障に対する対応**: 機器が提供している性能・機能の観点では故障ではないが、オイル消費量が多い、若干漏れが発生しているなど、正常な状態と比べると何か故障の兆候が観察される状況で、症状と対応を記録する。
   - **情報管理の目的**: 徐々に故障し始めている機器の状態の監視
2. **トラブルシューティング対応**: ある不具合に対して、原因を追求するための一連の活動での情報共有。
   - **情報管理の目的**: 不具合の根本原因を特定するために、これまで実施したアクションを記録することで、調査範囲を絞り込む
3. **繰り返し発生している不具合**: 機体のシステムで、不具合を示唆するメッセージが表示される。それに対して、Faultを起票して対応する。
   - **情報管理の目的**: 慢性的に発生する不具合への対症療法の把握
4. **AMM C/O SQのクローズ**: クローズできるSQをクローズする。

## Shared Info申し送り .docx

- **現状**: Shared Info（SMART Web アプリ 及び SMART Web アプリ タブレット版）をIFSとは独立して運用させる。
- **他システムとの連携**:
  - **FLT情報**: SOFIAと連携して取得
  - **User情報**: MatriX連携予定だったが、手動管理の提案あり。CSV一括登録も検討。
  - **Ship情報**: WebアプリのSettingから登録。
  - **C/O情報**: MightyからのImport機能は廃止。

- **やること**: User情報取得元の決定、Maint Plan FLT Noteカテゴリ要否確認、現業部門への説明、変更管理、スケジュール管理、リソース確保など。

- **現業部門に確認して欲しいこと**: App1/App2廃止に伴うタブレット版利用への変更、Customor機対象外、Report機能のSHIP検索方法変更、Ship MonitorのImport機能廃止、Maint PlanのFLT Note連携廃止、Ship/User情報の手動登録について。

## 20260824_shared info.docx

- **相談の背景**: SharedInfoの継続利用コスト（インフラ改修、アプリ改修）が高いため、業務的な必要性を再評価。
- **課題**: 整備記録に残せないグレーゾーンな情報（不具合の予兆など）の扱いや、品質事象の記録方法。
- **検討の方向性**: Report機能とShip Monitor機能の必要性を評価し、代替案を検討する。

---
上記内容を`SharedInfo.md`に統合しました。
ご確認の上、問題なければこの内容でファイルを更新し、コミットします。よろしいでしょうか？
