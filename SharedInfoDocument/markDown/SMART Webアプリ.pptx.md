# SMART Webアプリ.pptx

--- Slide 1 ---

SMART Webアプリの単独利用について　

2025/02/24


--- Slide 2 ---

SMART Webアプリの単独運用

SAMRT Webアプリを独立して運用する

IFSとのIntegrationは行わないWebアプリの運用に関して必要なデータはIFSを介せず連携させるAPP1がなくなることで不要になる機能を削除するSMART Webアプリ タブレット版をFiledでは利用する（Report List, Report Createを追加)


--- Slide 3 ---

AsIs-ToBe比較

追加

SMART Webアプリ

SMART Webアプリ タブレット版

＋

Fleet/EST

Back Office

Fleet/EST

Back Office

SMART Webアプリ

現在の使用イメージ

IFS移行後SMART Webアプリのみでの運用イメージ

SMART Webアプリ タブレット版 (改修)

アサインされたSHIPのReport情報はタブレット版を用いて検索・閲覧・記入


--- Slide 4 ---

データ連携に関して

データの使用目的従業員情報：ログイン、アクセス権限→MatrixShip/FLT Data:情報とShip, 便情報を結びつけるため→SOFIA連携 DD:APP1側にDefect List, Defect History 表示のため→IFSで確認できるので連携不要　  　  Ship Monitor CreateでDeferral ItemからImportされる→手動入力にする連携不要Log：SQ up通知のため→IFSに同様の機能を持たせる連携不要

他にもデータ連携があれば使用目的を確認し連携要否を決める

現在のデータ連携Mighty/AMOS:従業員情報・Ship Data・FLT Data・DDLog？：SQ UP情報ももらっている？（Log起票のReport作成用）


--- Slide 5 ---

APP1で表示されるデータの行先

Flight Notes

…

IFS 

SMART Webアプリ タブレット版 

Report List機能Report Create機能の追加


--- Slide 6 ---

タブレット版 Report List

Default 今の日付

赤枠の項目を上にそれ以外をdetailed searchタブ配下に

Ship TypeタブとShip Noタブから選択式に

Ship Monitor List検索欄


--- Slide 7 ---

タブレット版 Report Create

DefaultでFieldが入るように設定　


--- Slide 8 ---

SMART Webアプリ 機能の削除

APP1がなくなるため不要となる機能File Server機能(代替機能：Report機能)Image機能(代替機能：不要)

削除

削除


--- Slide 9 ---

SMART Webアプリ Report List

eLogからの連携はなくなるので削除

変更あり

Report list 検索


--- Slide 10 ---

MART Webアプリ Report List

変更なし

Report list 検索結果表示


--- Slide 11 ---

SMART Webアプリ Report List

Maint Plan

変更なし

Report  Detail 内容表示


--- Slide 12 ---

SMART Webアプリ Report Create

変更なし


--- Slide 13 ---

SMART Webアプリ Ship Monitor List

変更なし

Ship Monitor List 検索


--- Slide 14 ---

SMART Webアプリ Ship Monitor List

変更なし

Ship Monitor List 検索結果表示


--- Slide 15 ---

SMART Webアプリ Ship Monitor List

変更なし

Ship Monitor Detail 内容表示

変更なし

Ship Monitor Edit 画面表示


--- Slide 16 ---

SMART Webアプリ Ship Monitor Create

Deferral Item

変更あり

Ship Monitor Create 表示

Mightyと連携したDeferral ItemからのImport機能なくす

Deferral ItemのMonitorを作る場合のチェックボックス設置


--- Slide 17 ---

SMART Webアプリ Maintenance Plan List

検討中

Maint Plan List 検索

SMART APP1のFLT NOTEへの表示の際に利用


--- Slide 18 ---

SMART Webアプリ Maintenance Plan List

変更なし

Maint Plan List 検索結果表示

変更なし

Maint Plan Detail 表示


--- Slide 19 ---

SMART Webアプリ Maintenance Plan Create

変更あり

Reporを作成するためのチェックボックス設置

Report Create


--- Slide 20 ---

他現場からの要望

簡単にアクセスできるようにしてほしい動作を軽くしてほしいログインが長い間保持されてほしい


--- Slide 21 ---

SMART Web アプリ タブレット版の改修

Report List機能Report Create機能の追加


--- Slide 22 ---

TodoWebアプリと何を連携させるか（DXさん）App１のための機能（不要となる機能）は何か（SHIPチーム）タブレット版に求められる機能（SHIPチーム）→網羅性をもとに確認→Webアプリとapp１の内容比較確認　　web アプリの情報はAPP１のどこに表示されているのか



