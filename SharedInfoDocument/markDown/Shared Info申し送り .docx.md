# Shared Info申し送り .docx

Shared Info

現状
Shared Info（SMART Web アプリ 及び SMART Web アプリ タブレット版）をIFSとは独立して運用させる
Back officeではこれまで通りSMART Web アプリを使用、現場の整備士は今までAPP1を利用してShared Infoにアクセスする運用がメインであったが、今後はSMART Web アプリ タブレット版を使用して情報にアクセスする必要がある。
SMART Webアプリで今後不要となる機能の廃止、タブレット版を利用しやすい形にするための改修をDXさんへ依頼済み（資料参照）
他システムとの連携（現在Mightyと連携して情報を得ているもの）
FLT情報：SOFIAと連携して取得
User情報：MatriXと連携して取得予定だった。DXさんからはMatriXは情報量が多すぎるため、WebアプリのSettingから設定する方が良いのではという提案を受けている。（Settingは今もあるもの、Userの権限設定に利用している）初回の登録はCSV等で読み込ませ一括登録するなどの方法もあるが、異動があった場合には手動で登録を変更する必要が出てくるので（登録申請を行う必要がある）運用できるか検討する必要がある。
Ship情報：WebアプリのSettingから登録を行う
C/O情報：Ship monitorの情報源がC/O Itemである場合、そのMighty上でのtitleとDiscriptionやAMOSのHead LineやActionをImportできる機能(Import From Deferral Item)がある。IFSとの連動は考えておらず、この機能で連動される項目が少ないこと、使用されるケースが少ないことからこの機能自体を廃止する

担当：DX由波さん、DX佐藤誠さん

やること
User情報どこからもらうか決める
Maint Plan FLT Noteのカテゴリー必要か
現業部門への説明
変更管理後、DXさんへ本格的に業務要件の共有
スケジュール管理(テスト・ドキュメント・教育含め)
維持管理（JNZ/DX）
リソース確保、本当にARISEでやるのか

現業部門に確認して欲しいこと
変更点について共有、問題点はないか
App1/App2なくなる→Ship sideではWebアプリタブレット版利用
Customor機は対象外になる
Reprot機能
自分のアサインされたSHIPには紐づかない、自分でshipを検索してアクセス、情報をとりに行かないといけない
Ship Monitor機能
Import from defferal item機能の廃止
Maintenance Plan機能
FLT Noteへ連携しなくなる
Shipの登録をsetting（System）で行わなければいけない。（→誰がやる？）
人の登録もsetting（System）で行わなければならない。異動等あった際の申請等、どのように行うか現業部門との調整が必要、現在の権限申請と同様の方法を用いる？★SMART Kintone権限ロール操作ガイド_V3.0 .pptx

質問事項
Maint Plan Flight Noteのカテゴリー分けは今後も必要かNEXTMNTPJ-2538


資料
大まかな業務要件/SMART Webアプリ.pptx
JALDX佐藤さんからのfeedback【システム要件】Shred Info_ARISE検討.pptx

関連JIRA
NEXTMNTPJ-2537
NEXTMNTPJ-2538
NEXTMNTPJ-2539

































