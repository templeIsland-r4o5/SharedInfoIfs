# SharedInfo関連の検討.docx

検討の概要
検討の背景
・SharedInfoは継続利用前提で進めてきた。IFSの移行スコープ外としていた。
・SharedInfoを継続利用するために必要なシステム対応は以下を想定しているが、コスト見積が想定よりも高くなることが判明した。
　❶インフラ改修（DBバージョンアップ対応）
　❷ アプリ改修（Mighty等からは切り離し、SharedInfo単体で利用できるようにする対応）
　❸ アプリ改修（iPad版アプリをブラウザ版相当に機能追加する対応）
・改めて、業務観点でSharedInfoが本当に必要なのかを再評価する必要ができた。


検討の目的
・SharedInfoの現行業務でのユースケースを洗い出し、業務目的を可視化する
・業務目的を満たす方法について、SharedInfo以外の代替方法も含め、IFS導入後の最適なソリューション案を検討する

検討対象の機能
・Report Create/List
・Ship Monitor Create/List
※上記以外の機能（Maintenance Plan/File Server）は、2026年2-3月時点の評価で、廃止可能な旨を判断済みのため除外


現行業務の整理
SharedInfoユースケース一覧

SharedInfoを使って管理している情報には、情報の性質（情報の寿命、整備記録か否か、蓄積要否）の観点で、いくつか種類があることがわかった。


詳細：
ARISE_SHIP_SharedInfo現行業務整理[業務まとめ]シート
対応方針の検討　概要
対応方針の検討

情報の種類によって、IFS導入後にどのように管理すべきかを検討する。

検討時の考慮事項：
できるだけIFS上で管理できる方法を探る。
IFS上で管理できるほうが、複数システムを使い分ける必要がなく、整備士目線では都合がよいと考えるため。
整備記録として残すべき情報は、整備記録としてIFSに記録されるようにする。
全社的に、品質事象が継続して発生している状況がある。現行の運用では、SharedInfoのReport機能が汎用的に作られているが故に、本来ならばSQ Upすべき情報も、SharedInfoのReport機能で記録し、飛行機を飛ばせてしまうという安全上のリスクをはらんでいた。そのような余地は残さないようにして、整備記録として記録すべき情報は、整備記録に記録される体験設計となるよう留意する。

ARISE_SHIP_SharedInfo現行業務整理[対応方針の検討]シート参照






対応方針の検討　詳細①
対応方針の検討

①機番に紐づく情報のコミュニケーション

業務目的：
情報の伝達
業務要件：
・整備士・技術・SE・Fleet・ESTが、情報を登録する。登録された情報を参照する。
・情報のやりとりは、1 Turn中に完結する場合もあれば、複数Turnをまたいで継続する場合もある。
・伝えたい情報自体は、整備士が読んだら用が済み、機番に紐づけて蓄積する必要はない。
・モバイルで見られる。

取り扱う情報の具体例：
整備士からFleetへのTurn中の不明点問い合わせ
→Google Chat
[確認ポイント] Google Chatだと事足りないことがあるか？
Crewからの申し送り（耐空性に影響ない事象）
→Aircraft Turn Details に画面項目追加
技術/SE/Fleetから整備士への整備作業依頼（単発）
→Aircraft Turn Details に画面項目追加
技術/SE/Fleetから整備士への整備作業依頼（継続/複数Turnをまたぐ）
 [確認ポイント]このようなケースは、Ship Monitoringを起点とした整備作業依頼のみだろうか？Yesであれば、対応方針検討詳細②にマージする。



対応案イメージ
Aircraft Turn Detailsに画面項目追加（C-JAL-MEX019に要件追加）

管理すべき情報項目案
登録者のロール（Technician・SE・Fleet・EST）
※誰からの情報かわかるようにする
伝達したい情報

画面イメージ
機能の配置は想像に基づく。要は、Aircraft Turn Details画面で登録・参照できるようにしたい。
※細かい項目の定義は別途検討





9/8 議論メモ
このソリューション案で、要件は満たせる理解をしている。（寺嶋さん・仲摩さん）
画面に入力項目を用意するということは、データ保管先のテーブルも作成が必要となるはず。「C-JAL-MEX019の要件追加」という取り扱いで済むのか懸念される。（寺嶋さん）
C-JAL-MEX019と要件の目的は合致している理解をしている。実装がConfigで済むのかは不明。（領家さん）
MMでも拾うべき要件と考えている。
アクションプラン
C-JAL-MEX019に追加する方向で動く
C-JAL-MEX019に項目追加できないか、IFSに問い合わせる（川上）★




Old


対応案


Google Chatでもやっているケースも聞いたが、それじゃ足らないのか？を問うてみる。足らない部分がある場合、SharedInfoの強みだから、そこをどう対応すべきか考える必要がある。

関連Jira: https://jaldx.atlassian.net/browse/NEXTMNTPJ-2588
SERはタスクで管理する。



対応方針の検討　詳細②
対応方針の検討



②機番に紐づく注視事象（整備記録外）の情報記録・蓄積

業務目的：
情報蓄積・時系列に合わせた情報の参照
業務要件：
・整備士やFleetが、Turn中もしくはTurn後に、注視すべき事象の情報を登録する
・過去に登録された情報に対し、次Turn以降も、情報を追加登録できる（例：経過観察結果の記録）
・過去の登録情報を参照できる
・過去の登録情報に対して、特定のキーワードや条件で検索できる（例：類似SQの検索）
・モニタリングが済んだら、クローズ処理ができる

取り扱う情報の具体例：
・潜在的故障に対する対応記録
・トラブルシューティング対応の記録
・Chronic SQの観察記録
・予防整備の作業計画
★補足資料：Shared Infoで管理している情報

対応案






対応案の具体的な作業手順イメージ







今後の検討ステップ
案2は、IFSに開発規模の見積依頼をする必要がありそう。インプットはワイヤーフレーム。Configで済むのか否か。
案2、案3のノックアウトは何なのか？それは、運用の工夫や機能削減で回避できるのか？を評価する深掘りが必要になりそう
案2 Configで済む範囲にした場合、運用上耐えられるのかしら？
案3 何が運用上きついのか？

9/8のゴール
案の全体像を理解いただく
SharedInfoでカバーしていた業務が、IFSのどの機能でカバーされるのかの理解をすり合わせる
案2・案3のノックアウトがあるか、運用上の工夫/機能削減で回避できるのか？の深掘り
案2は、IFS側への確認事項をとりまとめて、USI問い合わせ
案3は、作りを改善するなら、その検討を宿題にする


議論メモ
Ship Monitoring起点の作業依頼があったとき、必ずしも強制力がないと理解した。必ずOn-condition Task/Faultを起票するような運用でよいのだろうか？（領家さん）
部品交換をする際は、必ずFaultを起票するだろうが。
作業を実施する時は、必ずTask/Faultを起票する。
On-condition TaskはFleetが起票するのか、整備士が起票するのか？
 現行運用では、整備士が作業直前にやっている。ただ、TaskであればUnassignすればよいので、Fleetが事前に起票していてもよい。
不具合対応ではないため、eLog（整備記録）に入っていなくてもよい。
長期的に見て、eLogにも記録しなさい、という流れになったときにも耐えうるか？
Taskで起票しておいて、Taskで、必要ならばFaultを起票しなさいと指示しておく。
RCM（Reliability Centered Maintenance）　PFカーブ
案の優先度
案3
表記ゆれ、属地ツールの誘発が懸念される。
スプレッドシート管理は、それ用の運用整備も必要となってくる。
案2 Configのみ＞案3
案2
FaultやTaskのデータと、Monitoring Itemのデータを関連づけるところがModくさい
アクションプラン
大きな方向としては、案2をIFSに見積してもらう。Modification/Configurationで仕分けしてもらい、Mod部分を削ぎ落として、Configに着地させたい。
IFSにインプットするにあたり：
Modificationが要りそうなところとそうでないところの仮説を立てる。
必要な改修を洗い出す
ワイヤーフレームを精緻化する
機能要件を分解する（画面、ボタンの機能を明文化する）
標準のデータとの接点になるところを示す
上記機能要件一覧に対して、Modification Configurationの仕分けをIFSに依頼する

川上検討メモ

IFSソリューション案(※)/Google Spreadsheet案を具体化してみる。★
業務影響はユーザー視点で変わるはず。例えば、整備士は情報へのアクセスのしやすさも比較ポイントになる。
※ワイヤーフレームを描いてみる。見積のインプットにも使えそう。



 比較対象の案より有利 /   比較対象の案より不利  /   案1, 2で優劣なし



上記2つでもIFS化に優先順位があるはず。
推奨案と妥協案





めも
Memo
[潜在的故障の対応]
・SQ予備軍連絡、予防整備

[Deferred Faultの詳細]
・Deferred Faultに対する補足情報

[コミュニケーション]
・パーツ番号問い合わせなど
・Crewからの連絡内容申し送り（ESTがCREWから連絡を受ける、相談しながら解決をした。この事実を整備士に共有する）
・ACARS情報の取り込み（ACARSの情報をReportとして起票する）

[情報共有]
・包括委託先が整備作業結果の報告をする
・カスタマー便の伝達事項を共有する

[ITMでの活用]
・不具合起票時に過去の類似事象を確認する。ReportではなくShip Monitorを使っている
・品質分析をするために、Shared InfoのShip Monitorの情報を使用して、不具合の分析をする


IFSと開発機能の相談をするときにまとめる資料
IFSと開発機能の相談をするときにまとめる資料


Target User: Fleets and Technicians
Purpose of Requirements:
There are information that JAL keeps records outside the official maintenance records, such as:
Potential Failure: monitoring the symptoms that suggest a fault and perform Precaution Maintenance
Troubleshooting: perform and records actions for identifying the root cause of afault. 
Chronic Failures
For these information, it is necessary to tag multiple Task and/or Fault records so that JAL can monitor the performed actions against one monitored issue.

Case
SharedInfoユースケース
情報の寿命
情報の内容
情報の使い方
1
❶整備士が、Fleetに、SQ予備軍として留意すべき事象を伝達する
❷Fleetが、予防整備を検討・計画し、実施結果をモニターする
❶複数機会にわたる
❷複数機会にわたる（作業完了まで継続）
❶整備記録ではない情報（予防整備のインプット）
❷整備記録として残すべき情報
❶蓄積が必要
❷蓄積が必要
2
整備士が、Fleetに、Turn Around中の不明点を問い合わせる
1整備機会で完結
整備記録ではない
蓄積不要
3
技術/SE/Fleetが、整備士に、実施してほしい作業を連絡する
例：整備機会には作業計画されていないが、実施できると望ましい作業、整備士の作業判断に役立つ情報（ETOPS or NON-ETOPSを判断するためのルート情報など）
1整備機会で完結
or 複数機会にわたる
整備記録ではない
蓄積不要
4
ESTが、Crewからの連絡内容・対応履歴を記録し、整備士に申し送る
1整備機会で完結
整備記録ではない
蓄積不要？
5
ESTが、Crewからの連絡内容を記録し、整備士に申し送る
1整備機会で完結
整備記録ではない
蓄積不要？
6
整備士が、Deferred Faultに関して画像で補足説明し、次StationのCrew/整備士に申し送る（従来のMAM）
※MEL適用した旨の申し送り
複数機会にわたる（Fault Closeまで継続）
整備記録ではない補足情報（だが本来は整備記録として残すべき助方）
蓄積不要
7
包括委託先の整備士が、ESTに、整備報告を実施する
1整備機会で完結
整備記録ではない
蓄積不要
8
カスタマー便の整備に関するカスタマー宛報告事項を記録する
1整備機会で完結
整備記録ではない
蓄積不要
9
【ITM固有】整備士やFleetが、新規SQについて、過去の類似事象を遡って調べる
就航来の長期蓄積
整備記録ではない補足情報
蓄積が必要
10
【ITM固有】Fleetが、品質分析（SQの発生傾向分析）を実施する
就航来の長期蓄積
整備記録ではない補足情報
蓄積が必要


現状維持
IFSで対応
IFS外対応
IFS外対応
IFS外対応
IFS外対応


案1 
SharedInfo
案2 
IFS 追加開発
案3
独自アプリ新規開発

案4 
Kintoneアプリ構築
案5
Google Chat 
案6
口頭/紙
内容の説明
内容の説明
SharedInfo Report機能を継続使用する。

機番に紐づくメモ登録・参照機能をIFSに追加開発する。
Aircraft Turnにメモ追加する
MEX019
NEXTMNTPJ-2808
機番に紐づくメモ登録・参照機能を持つ独自アプリを新規開発する。
JALDXに発注することを想定。
機番に紐づくメモ登録・参照機能を持つKintoneアプリを新規開発する。
JNZ DXチームに発注することを想定。
Google Chatを使用する。

バディカムや紙のメモを使用する。
業務影響
工数

ユーザビリティ
・操作するシステムを切り替える手間が増える（現状は、App1からシームレスにアクセスできるが、IFSメインで使う状態に変わるため、切り替え操作が発生する）
・操作すべきシステムがひとつにまとまる
・システム上の操作性はSharedInfo同等とする想定とし、変化なし
・操作するシステムを切り替える手間が増える
・システム上の操作性はSharedInfo同等とする想定とし、変化なし

・操作するシステムを切り替える手間が増える
・システム上の操作性はSharedInfo同等とする想定とし、変化なし
・操作するシステムを切り替える手間が増える
・情報の参照性がわるい懸念がある（リアルタイムコミュニケーションには強みがあるが、つまり複数Turnをまたぐ申し送りには向いていない可能性がある）
・紙とデジタルを併用する手間が生まれる
ただし、現行業務でも、SharedInfoを使わず、紙/バディカムでやりとりしている拠点もあるため一部拠点にとっては現行から変化なし
業務影響
品質
整備品質リスク
現行と同等（変化なし）





プロジェクト
影響
開発・テスト
コスト規模
大
JALDX見積に基づく
要確認
中
金額は不明だが、案1より安価かもしれないと示唆されたと聞いている
要確認
なし
なし
プロジェクト
影響
業務運用
設計/教育
コスト規模
小
ユーザー操作や業務運用ルールは変化なしのため
中
業務運用ルールの設計、教育周知が必要
中
業務運用ルールの設計、教育周知が必要
中
業務運用ルールの設計、教育周知が必要
大
業務運用ルールの設計、チャネル作成などの運用準備、教育周知が必要
小
口頭/紙運用に戻す旨（SharedInfo以前）の教育・周知が必要
プロジェクト
影響
データ移行
コスト規模
なし
継続利用のため
なし
蓄積不要なデータのため、データ移行不要と判断
なし
蓄積不要なデータのため、データ移行不要と判断
なし
蓄積不要なデータのため、データ移行不要と判断
なし
蓄積不要なデータのため、データ移行不要と判断
なし
そもそもデータ移行不可能


現状維持
IFSで対応
IFS外対応


案1 
SharedInfo
案2 
IFS 追加開発
案3
Google Spreadsheet管理

内容の説明
内容の説明
Ship Monitor機能を継続使用する。

機番に紐づく注視事象の記録・蓄積機能をIFSに追加開発する。
Google Spreadsheetで管理する。
業務影響
工数

ユーザビリティ
・操作するシステムを切り替える手間が増える

・操作すべきシステムがひとつにまとまる
・操作するシステムを切り替える手間が増える

業務影響
品質

整備品質への
リスク有無
現行と同等（変化なし）
・IFS上の整備記録（Fault/Task記録）との紐付けがわかりにくい
・IFS上の整備記録（Fault/Task記録）との紐付けがわかりやすい
・意図しないデータ更新などのヒューマンエラーを防止できない
・IFS上の整備記録（Fault/Task記録）との紐付けがわかりにくい
プロジェクト
影響
開発・テスト
コスト規模
大
JALDX見積に基づく
大
2000-3000万（案1の半額）
なし

プロジェクト
影響
業務運用
設計/教育
コスト規模
小
ユーザー操作や業務運用ルールは変化なしのため
中
業務運用ルールの設計、教育周知が必要
大
業務運用ルールの設計、チGoogle Spreadsheet作成などの運用準備、教育周知が必要
プロジェクト
影響
データ移行
コスト規模
なし
継続利用のため
要確認

なし
そもそもデータ移行不可能?
総合評価
総合評価



Case
Step
現行業務の実施内容
実施者
実施する
場所
使用する
端末
案1 SharedInfo
継続
使用機能
案2.IFS追加開発
案3.Google Spreadsheet管理
1
1
ENG OILのにじみを検知する
整備士
機側
-



1
2
ENG OILのにじみを検知した旨を、記録する。
Leak Checkなどを実施したが、にじみの発生箇所は特定できず（機体としては健全）。
整備士
機側
iPhone
Report Create
Fleetへの申し送り
Aircraft Turn Detailsで入力
Fleetへの申し送り
Aircraft Turn Detailsで入力
1
3
起票されたReportの内容を確認する
Fleet
オフィス
PC
Report List
Aircraft Turn Detailsで確認
Aircraft Turn Detailsで確認
1
4
ENG OILのにじみをShip Monitor機能で新規起票する。にじみに対して、どう対応していくかを検討するため。
Fleet or
Ship Monitor担当の整備士(FE)
オフィス
PC
Ship Monitor Create
IFS追加機能「Ship Monitoring Item」（仮名）を新規起票
ARISE_SHIP_SharedInfo_IFS追加開発案.pdf
Spreadsheetで新規起票
ARISE_SHIP_SharedInfo_Spreadsheet管理案
1
5
Report Listを確認する。ウォークアラウンドチェック時に気にすべき箇所の事前確認する。
整備士
オフィス
iPhone
Report List
Aircraft Turn Detailsで確認
Aircraft Turn Detailsで確認
1
6
にじみ発生箇所を確認する。確認結果をReportに追記する。
整備士
機側
iPhone
Report List
Aircraft Turn Detailsで追記
Aircraft Turn Detailsで追記
1
7
ENG OILのにじみに対して、計画すべき作業を検討する
Fleet
オフィス
PC
Ship Monitor List
Ship Monitoring Itemを参照
Spreadsheetを参照
1
8
詳細なリークチェックの整備作業を計画する
Fleet
オフィス
PC
Maintenance Plan
On-Condition TaskもしくはFaultを起票 ※On-Condition Tasks.pdf
Ship Monitoring Itemに紐付け

※Fleetが起票するのか、整備士が起票するのか要精査。運用次第
→ 現行運用では、整備士が作業直前にやっている。ただ、TaskであればUnassignすればよいので、事前に起票していてもよい。
On-Condition TaskもしくはFaultを起票※
Ship Monitoring Itemに紐付け

※Fleetが起票するのか、整備士が起票するのか要精査。運用次第
1
9
詳細なリークチェックの整備作業を確認する
整備士
機側
iPhone
Ship Monitor List
On-Condition Taskを確認
On-Condition Taskを確認
1
10
詳細なリークチェックの整備作業を実施する。実施結果をReportに追記する。実施結果を紙に記録し、Fleetに共有する。
整備士
機側
iPhone
Report List
On-Condition Taskをクローズ
On-Condition Taskをクローズ
1
11
詳細なリークチェックの整備作業に紐づくFlight Noteをクローズする。
整備士
機側
iPhone
Maintenance Plan
N/A
N/A
1
12
実施結果の紙をふまえ、Ship Monitorアイテムのクローズ可否を決める。システム上でShip Monitorアイテムをクローズする。
Fleet
オフィス
PC
Ship Monitor List
On-Condition Taskを確認
Ship Monitoring Itemをクローズ
On-Condition Taskを確認
Spreadsheetでクローズ
L1
L2
Title
Functional Requirements 機能要件概要
Screen Illustration / 画面イメージ
2
-
Monitoring Items screen
Screen to list the registered Monitoring Items.

2
1
Monitoring Item list
List of registered Monitoring Items.

2
2
Details button
Button to navigate the user to an individual Monitoring Item Details screen for the selected Monitoring Item.
Activates when the user checks an Item in the Monitoring Item list. 

2
3
Create Task
Button to navigate the user to create a task associated with the selected Monitoring Item.

The navigated screen is the Create New Task screen of an on-condition task.

The created on-condition task via this screen flow has a link information with the corresponding Monitoring Item. 
Navigated screen:

3
-
Monitoring Item Details screen
Screen to confirm the details of a Monitoring Item.

2
1
Create Task button
Button to navigate the user to create a task associated with the selected Monitoring Item.

The navigated screen is the Create New Task screen of an on-condition task.
The created on-condition task via this screen flow has a link information with the corresponding Monitoring Item.
機能詳細を述べる
IFS標準機能のデータを登録するなら、それがわかるようにする。



2
Mark as Closed button
Button to mark the Monitoring Item as closed.


3
Record Performed Task button
Button to allow the user to select a performed Task or Fault to associate the information with the Monitoring Item. The selected Task or Fault will be listed in the Performed Tasks list.


4
Details section
Section to display the information entered at the time of  Monitoring Item creation.


5
Performed Tasks list
List of Tasks and/or Faults that are related to the Monitoring Item.


6
Monitoring Notes list
Section to allow the user to create a new record associated with the Monitoring Item and view the existing Note records associated with the Monitoring Item.
This feature allows the user to make a note of information across faults and across timelines.

1
-
Create Monitoring Item screen

Screen for user to create a new Monitoring Item.
Input fields include:
Aircraft
Pull-down
Title
Free text
e.g OIL LEAK
Category
Pulldown
Options include:
Potential Fault
Troubleshooting
Chronic Fault
This field will be utilized for a user to filter the Monitoring Items in the Monitoring Items list view.
Description
Free text

Save button triggers registering a new record of a Monitoring Item.

5




6



