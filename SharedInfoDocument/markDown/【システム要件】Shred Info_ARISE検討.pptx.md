# 【システム要件】Shred Info_ARISE検討.pptx

--- Slide 1 ---
[Notes]

Shared Infoの今後について
‹#›

現在IFSプロジェクトの方針としてはShared Infoについては継続する方向で検討している。
その際IFSからのデータ連動については廃止。外部から直接Shared Infoにデータを連動してもらう方式とする。

Shared Info継続の場合、AMOS過渡期の運用についても考慮する必要がある。※AMOS過渡期の際、SMARTはJ-AIR機についてはこれまで通り使用できることが前提となるため。
--- Slide 2 ---
[Notes]

機能毎まとめ
‹#›
--- Slide 3 ---
[Notes]

機能毎まとめ
‹#›
--- Slide 4 ---
[Notes]

機能毎まとめ
‹#›
--- Slide 5 ---
[Notes]

使用しているデータ一覧
‹#›
--- Slide 6 ---
[Notes]

使用しているデータ一覧
‹#›
--- Slide 7 ---
[Notes]

Shared Infoのシステム連動概要図
‹#›
機体情報(ZDMSMT_SHIP)
JAL Mightyから連動ではなく今後はShared Info画面からメンテナンス
便情報(ZDMSMT_AIS)
※MaintenanceOpp
App1/App2
ShareInfo
SOFIA
JAL Mighty(HR)
C/O Defect(ZDMSMT_DEFERRAL)
※廃止見込み
従業員(ZDMSMT_EMPLOYEE)
シフト：3日分
User Master人、人の名前、組織、権限を管理するようカラムを追加※
※赤文字項目を追加
✖
eJAL/勤務表
※eJALは停止するタイミングをAMOSに合わせる
Report、Flight Note
凡例：→ 既存
　　　→ IFS移行時に追加
Shared Info利用にZDMSMT_EMPLOYEEが前提となっているが、IFS以降に合わせてUser Masterデータを参照するよう修正
✖
Hermes
ACARS Free Text
※Reportで利用
eLog
Crew Report
FLEET Confirm
✖
✖
便情報(New)　
？
？
--- Slide 8 ---
[Notes]

各テーブルの移行方針、過渡期運用
‹#›
--- Slide 9 ---
[Notes]

各テーブルの移行方針、過渡期運用
‹#›

--- Slide 10 ---
[Notes]

AMOS過渡期時の運用について
‹#›
AMOS過渡期の期間、Shared InfoがIFS移行で新しいロジックに置き換わってしまうため、以下制約が発生します。
・App1/App2からReportの作成、参照は実施できません。
・Flight Noteの参照は実施できません。※下記画面ショット参照
・App2での整備士アサインおよびApp1/App2での便閲覧については実施可能
・Shared Info(Web App)について、AMOS便の表示は出来ますがApp1/App2とのReport連携については実施不可となる見込みです。


Flight Note画面表示(App2/App1)
--- Slide 11 ---
[Notes]

SMART Webアプリ 機能の削除
APP1がなくなるため不要となる機能
File Server機能(代替機能：Report機能)
Image機能(代替機能：不要)


削除
削除
--- Slide 12 ---
[Notes]

SMART Webアプリ 機能の削除
APP1がなくなるため不要となる機能
Seat Config機能(代替機能：不要)

削除
＊機能の概要Seat Config
　・App1/App2で飛行機の座席について画像で表示するのに使用している機能。

左画面ショットの飛行機の座席画像を表示するための機能。App1/App2が廃止されるため管理する必要がなくなる。
--- Slide 13 ---
[Notes]

SMART Webアプリ 機能の削除
eLogとの連動ががなくなるため不要
eLog-Crew Report(代替機能：不要)
FLEET Confirm(代替機能：不要)
＊機能の概要
eLog-Crew Report：eLogにて対象の航空機上でSQを発見、搭乗用航空日誌に記載、SQ Cardを発行したタイミングで利用しているが、eLogと通信しなくなるため不要となる。
FLEET Confirm：Shared InfoのReport Detailで編集する際、FLEET CONFIRMにチェックを入れるとeLogに対してデータ連携。地上のFleetが確認したことがeLogに通知される仕様だが、eLogと通信しなくなるため不要となる。
Reportの機能に影響あり。
--- Slide 14 ---
[Notes]

Shared Info ログイン後画面
タブレットモード As Is
タブレットモード To Be

Web版に存在する機能である「Report List」および、「Report Create」について、タブレットモードにも表示させる。
※表示させる順番は要検討


--- Slide 15 ---
[Notes]

【共通】Report List

eLogからの連携はなくなるのでリストから
「eLog」を削除
変更あり
Report list 検索

eLogと通信しなくなるため、削除？【要確認】
→業務上項目自体は必要であれば画面からは削除せず、裏で実行される機能については削除して動かないように対応する見込み。
--- Slide 16 ---
[Notes]

【共通】Report List


DefaultでFieldが入るように設定
→Web版も合わせて対応してよい？タブレット版だけFieldがデフォルト表示が必要？
共通の前提で検討　
→タブレット版はField。Web版は別※がよい。
個別制御が無理なら両方ブランクとしてほしい。
※Web版はなにがよい？ブランクがよい？
 →Web版はブランク。
To Stationについて、ログインしているユーザーの所属組織に紐付く空港コードを初期値提案する。
→組織に紐付く空港については別途管理できるようConfigを作成する必要あり。

--- Slide 17 ---
[Notes]

Report List





Default 今の日付
→Fromブランク、To翌日のうちToを今日の日付に変更すること。


赤枠の項目を上に
それ以外をdetailed searchタブ配下に
Ship TypeタブとShip Noタブから選択式に
Ship Monitor List検索欄


--- Slide 18 ---
[Notes]

Report List
Ship Monitor Listと同じロジックで機種、機番を選択できるようにする。


P15にて確認中。不要であれば削除。
--- Slide 19 ---
[Notes]

タブレット版 Report Create
TimeZoneについて配置の変更。

タブレット版画面案
Web版画面

--- Slide 20 ---
[Notes]

タブレット版 Report List-検索結果
以下はWeb版のReport List検索結果。タブレット版にする際不要な項目を削る or 縦に配置することで表示させる必要がある。
--- Slide 21 ---
[Notes]

タブレット版 Report List-検索結果
項目名
項目値
以降繰り返しのため、省略


横画面の検索結果・・赤枠の単位で1レコードとみなす。
縦画面の検索結果・・緑枠の単位で1レコードとみなす。


以降繰り返しのため、省略
--- Slide 22 ---
[Notes]

タブレット版 Report Details
Web版画面
タブレット版のReport Detailsの画面について次ページにて検討

FLEET Confirmのチェックボックスについて不要となる。(画面から削除)
--- Slide 23 ---
[Notes]

タブレット版 Report Details
タブレット版画面案(横画面)
CTG
Ship No.
FLT No.
From Station
Title
Fleet
JA508J
JL5126
GUM
TEST Create
Description
Test Create SATO
To Station
NRT
Status
OPEN
Report
Original Report
Reported By
99900011
AMJ
Taro JAL
Report Date
2026/06/01 11:53:06(Japan)
Attached File
画像.png
画像2.png
ALL Download
Revise
Delete
Memo List(x)
User-ID
Name
99900011
Taro JAL
Sent To
NRT
UpdateTime 
2026/06/01 13:25:49
Add MEMO
TEST
--- Slide 24 ---
[Notes]

タブレット版 Report Details
タブレット版画面案(横画面)
Add MEMO

Add MEMO
Attached File
縦画面と横画面で項目の並べ方が若干変わる程度を想定。今回の例は横画面を想定
--- Slide 25 ---
[Notes]

Ship Monitor Create

Deferral Item


変更あり
Ship Monitor Create 表示
Mightyと連携したDeferral ItemからのImport機能なくす
Deferral ItemのMonitorを作る場合のチェックボックス設置
→チェックボックスのみ。チェックボックスにチェックを入れて登録すると、List、Detailを表示する際Import Item Deferral Itemにチェックが設定される仕様とする。

Status*がCLOSEだと隠れていたRecord Level*欄が表示されるため、Deferral Itemのチェックボックスをずらす必要あり。
--- Slide 26 ---
[Notes]

Ship Monitor List、Ship Monitor Details
‹#›
Ship Monitor Listおよび、Ship Monitor Details画面Deferral Item


Ship Monitor CreateでDeferral itemにチェックを入れるとShip Monitor ListおよびDetailでもチェックが設定される。
--- Slide 27 ---
[Notes]

Maintenance Plan List

検討中
Maint Plan List 検索
SMART APP1のFLT NOTEへの表示の際に利用。
→今後もARR便に対してMaintenance Planを紐付ける必要があるため継続利用。詳細な区分については要確認
→Category分け自体不要の可能性あり。Miantenance Plan作成の際にCategoryを選択しないと便を紐付けることができないため、Categoryわけが不要となった場合は便を紐付けるロジックを変更する必要がある。
→Category分けは不要。
--- Slide 28 ---
[Notes]

Maintenance Plan List
Maint Plan List 検索
変更あり

FLT NOTE Category について画面から削除。
そのため赤枠項目についてFLT NOTE Categoryの場所に移すかもしくは他項目については触らないかは要検討。
→移動させるなら Free TextおよびAND/ORのラジオボタンを移すのがよさそう。(枠のサイズの問題)

--- Slide 29 ---
[Notes]

Maintenance Plan Create

変更あり
Reportを作成するための
チェックボックス設置
Report Create

Maintenance Plan Createの処理遷移イメージDeferral Item
■初期表示（作成画面）
■検索処理
(Flight Searchでフライト情報選択
Report Create
■Report Create
Report Createのチェックボックスが入力されていた場合、Report Create画面に遷移。
■登録処理
チェックなし
チェックあり

--- Slide 30 ---
[Notes]

Maintenance Plan Create



FLT NOTE CATEGORYに値を設定→ARR Dateを入力後にFlight Searchボタンを押下するとFlight Listに便が表示される。検索時にはMaitenance Opportunity番号は使用しておらずShip No.、Station、Planned Dateを使用して便を検索している。
→便を選択してMaintenance Planを作成すると、最終的にMaintenance Opportunity番号がDBに設定され、DetailおよびListの検索時に使用されてしまう。
--- Slide 31 ---
[Notes]

Maintenance Plan Create


現在の仕様はFLT NOTE CATEGORYを選択するとARR Dateが入力可能となり、緑枠情報も入力してからFlight Searchを押下すると便情報が表示される。
→今後はARR Dateグレーアウトせず、ARR Dateを入力したらFlight Search枠が表示され、必要に応じて紐付ける便を選択できるようにしてはどうか。
→ARR Dateを入力するとFlight Searchの枠が表示されるようにする。Maintenance Planに対して便を紐付けずに起票もするため、現在のFLT NOTE CATEGORYと似たようなロジックで便を紐付けられるようにする必要がある。


--- Slide 32 ---
[Notes]

Maintenance Plan List、Detail
Maint Plan List 検索結果表示
Maint Plan Detail 表示
FLT NOTE CATEGORYの項目がなくなる。
変更あり
変更あり




--- Slide 33 ---
[Notes]

User Maintenance
‹#›
現在従業員情報について、JAL Mightyから連動された情報+必要に応じてSMARTにて登録した情報を使ってSMART(Web App)を使用している。
その際、JAL MightyからSMART Cache DBに連動する従業員は、組織の情報をもって制御しており、連動対象外の組織(例えば技術部等)はストアドプロシージャを使ってSMARTで登録を行っている。
eJAL等の上流システム
JAL Mighty
SMART Cache DB
ZDMSMT_EMPLOYEE
ストアドプロシージャ
SP_SHARED_INFO
--- Slide 34 ---
[Notes]

User Maintenance
‹#›
JAL Mightyから従業員の情報を送る際、現在はApp2でのアサイン業務を実行する際に参照しているテーブルのため、前日、当日、翌日の計3日分有効な従業員を連動している。
※以下例は日付関係が分かりやすいよう、特定の従業員のみをフィルタリングして表示。
現在Web Appを使用するには以下ZDMSMT_EMPLOYEEに登録されていることが前提となっているが、後述するUser Masterの情報を使ってShared Infoを使用できるようロジックを改修する必要がある。



--- Slide 35 ---
[Notes]

User Maintenance
‹#›
その他Web Appにて権限登録を実施する必要がある。
User Maintenance機能の初期画面
--- Slide 36 ---
[Notes]

User Maintenance
‹#›
User Maintenance 検索結果画面

User-ID、Name、Deaprtmentについて、前述したZDMSMT_EMPLOYEEの情報を使用している。
今後はUSER_MASTERの情報を使って検索するようロジックを改修する必要がある。

--- Slide 37 ---
[Notes]

User Maintenance
‹#›
User Maintenance 編集画面
今後Web Appを使用できる権限について登録するのと同時に、以下画面に組織も入力して登録することで、ZDMSMT_EMPLOYEE(もしくは日付が不要となるため、別のテーブルを用意するか)にもデータを登録できる仕組みとする必要がある。
※User Maintenanceを実行すると、USER_MASTER にデータが登録されるが、USER_MASTERには所属組織および人の名前の情報がないため、USER_MASTERにカラムを追加する対応が必要となる見込み。
Organization
NLL/E2

USER_MASTERサンプル

--- Slide 38 ---
[Notes]

User Maintenance
‹#›
今後の申請については要相談となりますが、以下SMART権限申請フォームに所属組織の変更についても盛り込むことを検討しております。
・所属組織も一緒に申請が必要となる・所属組織は自動で変わらず変更が必要な場合は再度申請してもらう必要がある
　→権限に変更がない場合でも組織が変わる場合は申請をお願いすることとなる。
組織と権限が紐付いていると、組織が古いと問題が起こってしまう可能性はある。
申請について、eLogとShared Infoって分かれている？もし分かれているならそもそも申請方法含め運用を検討する必要があるかも。
→今後運用で検討。
--- Slide 39 ---
[Notes]

User Maintenance
‹#›
組織改正等で大量に所属組織の変更があった際、1件ずつのマニュアル対応では対応が難しいため、
ファイルを読み込ませての一括更新できる機能を作成する必要あり。
※権限ロール申請も一括処理できるよう機能開発することで、今後の権限申請反映についても簡略化できるか。要検討。

Upload
イメージはUser Mainteannce初期画面にcsvファイルを添付できる欄を追加、添付後Uploadボタンを押すことで、csvファイルの内容読み込み→USER_MASTER更新→処理結果を画面表示or csvファイルで出力
--- Slide 40 ---
[Notes]

User Maintenance
‹#›
User Maintenanceの処理遷移イメージ
■検索処理
■初期表示（一覧画面）
■登録処理
■更新処理
■初期表示（編集画面）
■一覧画面からの画面遷移
CSV Upload？
■csvアップロード
■登録/更新/削除 処理
■処理結果表示
赤枠部分について新規処理。それ以外は既存処理として記載。
--- Slide 41 ---
[Notes]

System-Ship Maintenance
‹#›
機体情報の登録について
　　登録画面をShared Infoに構築する場合、以下画面ショットイメージのSeat Config
　　Maintenanceと同じような形で開発を行うことが想定されます。
【参考機能】Seat Config Maintenance
　　出来ること：参照、登録、更新、削除
--- Slide 42 ---
[Notes]

System-Ship Maintenance
Report Create



Shipのメンテナンス機能※を追加
※新規開発が必要。

画面イメージはSeat Configと同様、
画面に表示された項目に入力した内容でCache DB：ZDMSMT_SHIPに登録/更新/削除できるようにする。
Ship Maintenanceへの画面遷移
--- Slide 43 ---
[Notes]

System-Ship Maintenance
‹#›
Ship Maintenanceの処理遷移イメージ
--- Slide 44 ---
[Notes]

System-Ship Maintenance
Report Create




Ship List(機材)の登録で必要となる項目。
STCON(Seat Config)はShared Infoで登録した座席の画像について表示するために必要となる。
※App2のアサイン時資格チェックおよび、AMOS過渡期期間はほかの項目を使う可能性があるため削除不可。
Ship Maintenanceにて必要となる情報
--- Slide 45 ---
[Notes]

System-Ship Maintenance
‹#›
Ship No
Aircraft Type
Flight Operator

Search Results
Ship No
Aircraft Type
Aircraft Type Detail
Flight Operator
Managed Flag
JA01XJ
350
350-900
JL
J
JA211J
ERJ170
ERJ170
JL
A
Ship Maintenance 一覧画面参考
画面遷移した直後は表示なし。
+Add ボタンを押下すると新規登録画面に遷移

Searchボタンを押して条件に合致するデータが表示されたのち、検索されたレコードをクリックすると編集画面に遷移
--- Slide 46 ---
[Notes]

System-Ship Maintenance
‹#›
Ship Maintenance 登録画面参考
Edit Ship
Ship No
Aircraft Type
Flight Operator



Aircraft Type Detail

Managed Flag

画面の項目にそれぞれ値を設定してSaveボタンを押下することでShipを新規登録可能。
--- Slide 47 ---
[Notes]

System-Ship Maintenance
‹#›
Ship Maintenance 編集画面参考
Edit Ship
Ship No
Aircraft Type
Flight Operator
JA10XJ
350
JL
Aircraft Type Detail
350-900
Managed Flag
J
画面にそれぞれ値が設定されているため、それを編集してSaveボタンを押すことでShipの更新。

なにも変更せずDeleteボタンを押すことでレコード削除

【業務運用変更】eLog登録に合わせてWebAppの対応も必要となる。
--- Slide 48 ---
[Notes]

他現場からの要望(非機能要件)
簡単にアクセスできるようにしてほしい
→必要なデータに早くアクセスしたい。
　よって各検索画面の初期値提案について検討する必要あり。
動作を軽くしてほしい
→Shared Infoで国内線はレポートの数が多い。数が多いためか読み込みに時間がかかるケースがある。タブレットで使えるようにするにあたって、読み込み方法の検討だったりしてほしい。
→過去Shred Infoのパフォーマンスについては検討がされており、その中での結論としてはマシンスペックの改善が必要で、SQLの改善については検討はしたものの効果が限定的かつリスクが高いため実装はされなかった。また、Cache DBはJAL Mightyのデータをキャッシュする思想で開発されたため、今後Shared Info単独で動作する場合はCache DBを廃止しShared DBに片寄することでほぼ確実に処理速度が向上する。
https://chat.google.com/room/AAAAa-xw7C0/XQtj3Ac-62k/XQtj3Ac-62k
MFPFのプロジェクトにてShared Info DBサーバーののスケールアップについて実施しない方向となっていたが維持管理で見る限り日中帯の負荷が非常に高い状況となっている。 https://jalec.atlassian.net/browse/SMWR-630
現在SJOプロジェクトにおいてサーバーのスケールアップ要否の検討を実施していただけないでしょうか。SharedDBは日中帯は比較的CPU高い状況です。SJO展開実施後はデータのやり取りが増えると思いますのでお願いします。
→SJOプロジェクトでスケールアップを行わない判断を下した場合は、維持管理側でもしばらくスケールアップは行われない見込み。
--- Slide 49 ---
[Notes]

他現場からの要望(非機能要件)
ログインが長い間保持されてほしい
→セキュリティ観点の懸念やネットワークの問題もあり、難しいのではないか。。基盤チームに検討を依頼する必要がありそう。
・バックオフィスで使ってる時等、何かしら操作していれば長時間ログイン情報が保持されるが、触っていない時間が続くとセッションが切れてしまう。整備士さんが使うタブレットの場合は触ってない時間が続くため、度々ログインが必要となってしまう。

→やはりセキュリティ観点の懸念があり、ご期待に沿うことは難しいという結論になりました。
--- Slide 50 ---
[Notes]

非機能要件：簡単にアクセスできるようにしてほしい
‹#›
すでに提案しているもの以外ですと、所属組織(空港)によって、検索画面のFromやToの空港を初期値提案してはどうか。
対象機能：Report(Create,List)、Maintenance Plan(Create,List)
　→ReportではTo Stationを設定。Maintenance PlanについてはBack Officeでの利用を前提としているため設定不要。

To Ttationの初期提案に所属組織に紐付く空港を設定してはどうか。(所属組織と空港の関係性についてConfig等で保持して、その情報を使って表示する見込み。)
→Report Listのみ対応希望
--- Slide 51 ---
[Notes]

非機能要件：ソフトウェアバージョン
ソフトウェアバージョンについて、Shared Infoを継続利用する場合検討する必要がある。以下が現在の構成である。(SMARTクラウド化プロジェクト計画書5章から抜粋)


松田さんに相談してから対処
→DB2じゃなくなったりでほぼほぼ作り替えのような状態になる想定である。
使用できるところはあまりないように思っている。
(松田さん)

--- Slide 52 ---
[Notes]

非機能要件：ソフトウェアバージョン
Jbossについて、そもそもJAL標準ではなくTOM CAT(トムキャット)がJAL標準となる。
IFS移行の際JAL標準に合わせるべくソフトウェアを一新する案 or これまでと方式は大きく変えずにソフトウェアのバージョンにのみ絞って検討を行う。
→JAL標準に一新する方向を本線として検討を進めてもらう様SMART担当に依頼済み。



--- Slide 53 ---
[Notes]

要望：Reportの添付ファイルコピー機能
Reportで写真を貼っている。
→Maintenance PlanにもReportで添付した写真をコピーしたい。(Reportから切り取りではなくコピー。ReportとMaintenance Plan両方に同じ写真が貼付されるようなイメージ。)
→実現可能性を確認すること。
確認結果：DBサーバーの容量圧迫によりパフォーマンス悪化の懸念もあり推奨できない。非機能要件で対応してもこれで悪化させたら意味がなくなる懸念があるため実施不可。


--- Slide 54 ---
[Notes]

Shared Infoの現状の課題
SMARTのマスタを更新した際、反映にはJBossの落とし上げが現在は必要だが、
維持管理する上でPSS/SSSでしか反映できない。
→仕組みを変えたい。

Access Keyが90日毎に変更が必要となるが、認証方法が標準的な方法ではなく時間がなかったことによる暫定処置で本番反映されてしまっている。
→是正策は複数存在する。以下案から選択。①
②
③
松田さんに相談してから対処
--- Slide 55 ---
[Notes]

その他検討事項、今後の進め方
‹#›
・受託便はShared Infoの対象便に含めるべきか？
→最悪なくてもよい。。。JAL便、ZIP、SJO、J-AIR(AMOS)は必要。
　現状使えるようになってるから、制限、制約がないなら既存に合わせてあげるべき？
　→確認する。
     →受託便は不要。JAL、ZIP、SJO、J-AIRの便について対象とすること。
　　 

・改修、開発のスケジュール感に関して。今後どのように進めていきますか。→ARISEのプロジェクトのスケジュール(周辺)に則って動くことになるとは思います。
　5月に概算、 7月に詳細の見積もりを出すような形になると思います。
--- Slide 56 ---
[Notes]

‹#›
後続ページは内部向け。


--- Slide 57 ---
[Notes]

SMART Webアプリ 便情報(As is)
‹#›
便情報について、これまでは以下経路で最終的にSMART Cache DBまで連動されている。
しかし、今後はJAL Mighty(IFS)を介さずに便情報を受信することとなる。
SOFIA
EPIC
JAL,JAL Group便の・当日便のﾘｱﾙﾀｲﾑ更新情報
・FSA(※)
SOFIA
他社便
Customer便の便情報
※航務部が入力したタイミングで連動
処理1(EA1001)
処理2(EA1002)
処理3’(EAB220)
処理3(EAB221)
eLog

eLog用XML
JAL Mighty
Adapter69
SAP Adapter
IDocData
JAL Mighty
Adapter57
SAP Adapter
IDocData
SMART Cache DB

--- Slide 58 ---
[Notes]

SMART Webアプリ 便情報(To be)-MQ案
‹#›
便情報について、これまでは以下経路で最終的にSMART Cache DBまで連動されている。
しかし、今後はJAL Mighty(IFS)を介さずに便情報を受信することとなる。※IFSについては別途SOFIAから連動されるが、SMART Cache DBとは通信しない。
SOFIA
EPIC
JAL,JAL Group便の・当日便のﾘｱﾙﾀｲﾑ更新情報
・FSA(※)
SOFIA
他社便
Customer便の便情報
※航務部が入力したタイミングで連動
処理1(EA1001)
処理2(EA1002)
処理3’(EAB220)
処理3(EAB221)
eLog

eLog用XML
SMART Cache DB


--- Slide 59 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
‹#›
SOFIAからEPICを介して連動するのと同時にSX-APIを使用してSahred Info(SMART Cache DB)に便情報を連動する方式について検討。Shared InfoからSX-APIにアクセスし必要なデータを抽出したのち、Cache DBに登録するイメージ。
Shared Info
SMART Cache DB
SX-API


1
2

3
JSONで出力
特定の条件で便情報を出力するようリクエスト
JSON形式で出力された情報でCache DBレコードの登録/更新/削除
SQSとかではなく、Shared Info APからコールして直接やり取りしてもらうイメージ。
--- Slide 60 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
‹#›
SX-APIについて、大まかに以下2つの機能がある。
①「一覧検索」
　指定した条件に一致した便の一般的に利用頻度の高い基本情報を一度に取得

②「詳細取得」
　「一覧検索」にて抽出した便について、サロゲートキー(意味を持たない自動生成した連番やIDでJAL MightyでいうMaintenance Opportunity番号)を使用して便の詳細情報を取得
上記①、②をセットで実行する必要がある。
--- Slide 61 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
‹#›
SX-APIで便情報を取得する際に必要となる項目は以下。
【一覧検索】
・originDateLocal/originDateUTC：運航基準日。運航基準日を指定して検索する場合、Local orUTCのどちらかが必須となり、どちらも入力した場合はLocalが優先される。
・carrierCode：航空会社コード。(JAL便：JL,NU,XM,ZG　他社便：IJ)
・updateTime：データの更新日時。リクエストパラメータにupdateTimeのみを指定した場合は指定した時刻以降に更新されたデータが抽出対象となる。(対象データが存在しなかった場合は空で返却される。)　　書式：YYYY-MM-DDThh:mm:ss.SSS(例：2024-10-08T12:00:00.000)
主にupdateTimeを使うことになる見込み。carrierCodeについては他社便の方では利用想定あり。(でないと余計な便情報を多く取得してしまうため。)【詳細取得】
・fltLeg-id：サロゲートキー。SX-APIで便の詳細情報を取得する際にはサロゲートキーを入力して抽出する必要がある。　JAL便：J-20241010-JL-0101-HND-ITM-0　SJO便：O-20241015-IJ-0026-HND-LAX-0
詳細取得時、1便毎に待ち時間を設けることは出来るか。→時間帯によりどの程度更新されるのかも観ておく必要あり。
--- Slide 62 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
【流入用制限】
　SX-APIについて、APIの呼び出し制限の設定が存在する。5分に一度便の最新情報をSX-APIから情報を取得しSMART Cache DBにデータの登録/更新を行う想定があるが、一覧取得から詳細取得の際複数の便情報を取得する必要があり、1日当たり1500便弱(受託便含む)+その更新をどのようにして取得するか方式を検討する必要がある。流入量制限に引っかからないかつ、負荷をかけすぎないよう検討を進めること。
→出発2日前以降のデータを5分に一度のリクエストであれば問題なし。

【件数制限】
　一度の抽出で最大300件のデータが抽出される。300を超える件数が存在する場合には、offsetという値を駆使してデータ抽出を行う必要がある。(よってLimitについては300固定でよい。)
例えば、1000件のデータを取得したい場合は、以下のように4回に分けてリクエストします。

1回目：offsetに0を指定し、1件目から300件目までを取得
2回目：offsetに300を指定し、301件目から600件目までを取得
3回目：offsetに600を指定し、601件目から900件目までを取得
4回目：offsetに900を指定し、901件目から1000件目までを取得
‹#›
便の削除(XLDではなく物理削除)した場合にはOffsetの番号がズレるので抽出できない便が発生する。
--- Slide 63 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
SX-APIの便情報一覧について、以下のようなデータの構造となっている。

‹#›
fltLeg
legInfoSummary
運航基準日、便冠(carrierCode+fltNumber)など、便を特定できる情報。
便の詳細な情報。主に運航した日時(Skd～ActualまでのDep,ARRの日時)や、Seat Config、PAX、離発着空港の実績等が確認できる。
※後述する詳細情報取得の際に取得できる項目ばかりなので、便情報一覧についてはfltLeg-id(サロゲートキー)を取得して詳細な情報を別途取得する方式になると想定している。
--- Slide 64 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
SX-APIの便詳細情報について、以下のようなデータの構造となっている。

‹#›
fltLeg
legInfoSummary
connectFltInfo
運航基準日、便冠(carrierCode+fltNumber)など、便を特定できる情報。
便の詳細な情報。主に運航した日時(Skd～ActualまでのDep,ARRの日時)や、Seat Config、PAX、離発着空港の実績等が確認できる。
※後述する詳細情報取得の際に取得できる項目ばかりなので、便情報一覧についてはfltLeg-id(サロゲートキー)を取得して詳細な情報を別途取得する方式になると想定している。
fltLeg便の前後便を管理している。
precFlt(前接続便区間キー(前便))、 succFlt(次接続便区間キー(後便))にてそれぞれ前後便の情報があり、fltLegと同じ構造で管理される。
--- Slide 65 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
SX-APIの区間便詳細情報について、以下のようなデータの構造となっている。
内容を見るに区間便検索を実施すれば概要→詳細と2回に分けて抽出せずとも必要な情報が取得できそう。

‹#›
fltLeg
LegInfoDetailLite
connectFltInfo
運航基準日、便冠(carrierCode+fltNumber)など、便を特定できる情報。
便詳細情報の簡易版。簡易版とはいえSMARTで必要な情報は持っている模様。
fltLeg便の前後便を管理している。
precFlt(前接続便区間キー(前便))、 succFlt(次接続便区間キー(後便))にてそれぞれ前後便の情報があり、fltLegと同じ構造で管理される。
--- Slide 66 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
connectFltInfoについて必ず設定されるわけではない模様。(特に他社便の場合)
理由：現在JAL Mightyにて他社便についてMaitenance Opportunityを作成/更新する際に前後便の情報を受信、Table：ZDMSMT_LEGに保存しているが設定されていないレコードが微量ながら存在している。JAL便についてはもともと編集してないので不明。ただしサンプルファイルを見る限り設定されると思われる。

その他SX-APIで便を抽出するにあたり詳細な定義については下記ファイルを参照してください。
https://drive.google.com/drive/folders/1gTro_KbrN3Uez04YpzsI4Nia-sWQGpFZFile名：SXAPI設定手順書.xlsx

また、サンプルファイルについては下記ファイルを参照してください。
File名：jsonファイルサンプル.xlsx

不明点などがあれば下記問合せ先にお願いします。
https://jaldx.atlassian.net/servicedesk/customer/portal/195

‹#›
--- Slide 67 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
‹#›
HTTPステータス(SX-API実行時のリターン値)
--- Slide 68 ---
[Notes]

SMART Webアプリ 便情報(To be)-SX-API案
SX-APIで便の詳細情報を取得した際、connectFltInfo-succFlt カラムが存在しており、そこに後続便を特定できる以下情報が格納されていることが分かった。現在と同じように後続便検索の際に利用できると思われる。
(データをDBに登録/更新するときの方法を工夫すれば現在のForwardのロジックとほぼほぼ同じような流れでFoward先の便が特定できると考えている。)

・connectFltInfo-succFlt-id(値の例を以下に記載。サロゲートキー。)　JAL便：J-20241010-JL-0101-HND-ITM-0　SJO便：O-20241015-IJ-0026-HND-LAX-0　
・connectFltInfo-succFlt-carrierCode(JL,NU,XM,ZG,IJ 等)
・connectFltInfo-succFlt-fltNumber(前ゼロあり4桁)
・connectFltInfo-succFlt-skdDepAirportCode(予定出発空港)※
・connectFltInfo-succFlt-skdArrAirportCode(予定到着空港)※
※イレギュラー運航(ATB,DVT)がなければ前便(Fowardする便)の到着空港と同じになるが、イレギュラー発生を考慮すると空港でのハンドリングは非推奨。idを使って便を特定、紐付けること。
‹#›
--- Slide 69 ---
[Notes]

SMART Webアプリ データ移行について
‹#›
Shared InfoのReport、Ship Monitor、Miantenance Plan等の過去データを参照するにあたり、既存のデータを移行するためのツールが必要となる。※Maintenance Opporutnityが廃止され、考え方が大幅に変わるため。
　→SX-APIの定義を確認したところ、同じようなデータの持ち方にすることもできるため、考え方としては大きく変わらないと思われる。

また、不要なデータについては移行前に削除をする必要がある。
→データ量を極力減らした状態で移行することでリスクを抑えたい。

WebAppのURL欄にMopp No.が設定されるケースがあるとのこと。
--- Slide 70 ---
[Notes]

SMART Webアプリ 便情報の考え方
‹#›
JAL Mightyで便情報(LEG)について、Maintenance Opportunityと呼ばれる整備機会に編集したうえで、現在はSMART Cache DBに連動しているが、SOFIAから直接受け取ることになるため、
今後はMaintenance Opportunity(以下イメージの緑枠)は廃止されるため、便毎(青枠)で処理するよう仕組みを変える必要がある。　
Maintenance Opportunityのイメージ(以下緑枠)
--- Slide 71 ---
[Notes]

SMART Webアプリ 便情報 (Report List)
‹#›
現在のShared Infoについて、Maintenance Opportunityを使った便の特定が前提となっているため、画面および検索ロジックを大きく変更する必要性がある。
以下Report Create画面でもMaintenance Opportunityは一見表示されていないが、Searchした際に取得、DBに登録しReportの検索時に裏で使用している。
Report Createの画面では、Maintenance Opportunityの項目自体は表示されていないが、Reportの登録、検索、削除などのKey情報として非表示で持っている。

--- Slide 72 ---
[Notes]

SMART Webアプリ 便情報(Report Create)
‹#›
Report Createの検索。便を特定できうる情報がFlight Listに並んでいるが、実際には裏にMaintenance Opportunityの番号を保持してしまっている。

StationにFrom-toの空港が表示されている。SX-APIのデータの場合後続便の情報が取得できるので、今と同様の方法でデータを管理すれば問題なく設定可能。
--- Slide 73 ---
[Notes]

SMART Webアプリ 便情報(Report Detail)
Report Detail画面。先送りするときにForward(緑ボタン)処理を行うが、その際次の便に引き継ぐために
便の情報が必要となるが、現在は以下「Maintenance Opportunityのイメージ」の緑枠のような形で情報を保持しているため、レコード内に次の便の情報が設定されるが、今後は青枠のような形でデータを保持するため、次の便を検索する処理を追加する必要がある。

上記青枠のデータイメージについては、以下添付ファイルを参照。
‹#›
--- Slide 74 ---
[Notes]

SMART Webアプリ 便情報(Report Detail)
Foward処理を行う際、後続便を確認する必要がある。これまでは後続便の情報を同じレコード内に保持していたが、今後IFS移行後は考え方が大きく変わり後続便については別途検索およびマッチングをかける必要があると思われる。
‹#›
後続便の情報が同一レコードに含まれているため、Foward対象の便を確認する際容易にFoward先が特定できた。
しかし今後は後続便の情報が同一レコードにないため、Foward先の便を検索する必要が出てくる。


--- Slide 75 ---
[Notes]

SMART Webアプリ 便情報(Report Detail)
しかしSX-APIで便の詳細情報を取得した際、connectFltInfo-succFlt カラムが存在しており、そこに後続便を特定できる以下情報が格納されていることが分かった。現在と同じように後続便検索の際に利用できると思われる。
(データ保持の方法を工夫すれば現在のForwardのロジックとほぼほぼ同じような流れでFoward先の便が特定できると考えている。)

・connectFltInfo-succFlt-id(値の例を以下に記載)　JAL便：J-20241010-JL-0101-HND-ITM-0　SJO便：O-20241015-IJ-0026-HND-LAX-0　
・connectFltInfo-succFlt-carrierCode(JL,NU,XM,ZG,IJ 等)
・connectFltInfo-succFlt-fltNumber(前ゼロあり4桁)
・connectFltInfo-succFlt-skdDepAirportCode(予定出発空港)※
・connectFltInfo-succFlt-skdArrAirportCode(予定到着空港)※
※イレギュラー運航(ATB,DVT)がなければ前便(Fowardする便)の到着空港と同じになるが、イレギュラー発生を考慮すると空港でのハンドリングは非推奨。idを使った検索が無難。
‹#›
--- Slide 76 ---
[Notes]

SMART Webアプリ 便情報(Maintenance Plan)
‹#›
一方、Maintenance Planの機能では画面には表示されていないが、実際にMaintenance Planを登録する際FLT NOTEを設定した場合、検索する際にMaintenance Opportunityを使用しているため、ロジックの改修が必要となる。(FLT NOTEを作成しないように改修)
SX-APIのfltLeg:id(サロゲートキー)を使用するようにして、ロジックをほぼほぼ流用する手もあると思われる。

--- Slide 77 ---
[Notes]

SMART Webアプリ 便情報(Maintenance Plan)
‹#›
もしくは現行と同じようにMaintenance PlanおよびFLT NOTEについてはfltLeg:id(サロゲートキー)を使って同じようにMaintenance Planに対して対して便を紐付けることは可能。
その場合テーブル定義の更新を実施する必要がある。現在のそれぞれのテーブル作りは以下の通り。これと同じようなテーブルを新たに用意するイメージ。




--- Slide 78 ---
[Notes]

EOF
‹#›