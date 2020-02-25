# Changelog

## [0.11.2] - 2019-2-19
## Added
* preprocessing: chi2 feature independence test.
### Fixed
* Feature(i_slot_between_dash) default value has been changed to 100.
* A glitch caused by urllib.parse.quote.

## [0.11.1] - 2019-2-18
### Fixed
* A glitch for not setting the QWebEngineView initial url.

## [0.11.0] - 2019-2-12
### Added
* 3 Layer model Grid Search: batch_size, epochs, optimizer, init_mode, neurons.
* Training model saved.
## Fixed
* ALL categorical columns now use OrdinalEncoder except Label.

## [0.10.0] - 2019-2-6
### Added
* Baseline four_layer train/validation accuracy, loss plot.
* Accuracy improved (91.40%) with feature standardization, normalization.

## [0.9.1] - 2019-2-3
### Fixed
* 重抓artist, artist_info, title_info資料。Accurary大約是86%

## [0.9.0] - 2019-1-30
### Added
* 完成Baseline four_layer training，使用label/one hot encoding辨識率都是90.80% (3.62%)

## [0.8.1] - 2019-1-30
### Added
* 完成Baseline four_layer training，使用label/one hot encoding辨識率都是90.80% (3.62%)
### Fixed
* word_segmentation: stopword出現在FeactureVectors裡面
* 清理title_infos.pkl, TitleInfo.title 型態資料為str


## [0.7.0] - 2019-1-28
### Added
* YouTube Search爬蟲可同時準確搜尋("")Artist, track title
* MBService
    * 查詢歌手所有歌曲（每張專輯以第一次發行為主）
    * 隨機選擇10首歌曲
* 完成歌手、歌曲、標題labeled data收集
### Fixed
* 處理MBService取得所有歌曲時日期剖析ValueError
* Segmentizer: that's正確分段， ' 前後空白不再吃掉
* Segmentizer: ('Lstr', "thinkin' about") 正常連接


## [0.6.0] - 2019-1-27
### Added
* x , & 等連接詞現在可正確連接左右詞彙成segment，例如：
(Shawn Mendes & Camila Cabello), (鍾一憲 x 麥貝夷)
* 資料傳遞現在使用TitleInfo
* feat.不跟其他segment組合，成為('Po', 'feat.')
### Fixed
* 移除feature: valueless，無意義的詞彙直接刪除。
* 使用OOP重構斷句、特徵擷取程式碼


## [0.5.0] - 2019-1-26
### Added
* Dataset Labeler實作完成
### Fixed
* feature: i_slot_between_dash，用index表示token在多個dash間的位置
* 調整Dataset Labeler外觀
* 沒括號的title會缺少in_quote, quote_type兩個feature
* 修正Data Labeler artist, title按F1仍然會儲存feature錯誤
* ) - 前後空白沒正確去除


## [0.4.0] - 2019-1-25
### Added
* 實作華語歌手姓名爬蟲
### Fixed
* feature: 分隔或括弧字元周圍空白去除
* feature: 括弧中token分別用in_quote, quote_type兩個feature代表


## [0.3.0] - 2019-1-24
### Added
* 實作title feature擷取
### Fixed
* before_dash, after_dash邏輯錯誤
* left/right_lo_token_cnt造成feature vector長度不一錯誤
* 為求統一，調整left count為reclusive, right count為inclusive
* 修正stopword大小寫辨識問題


## [0.2.0] - 2019-1-24
### Added
* 實作classes.eng_artist_titles.py
* 抓取、清理英文歌曲標題清單


## [0.1.0] - 2019-1-23
### Added
* 完成MusicBrainz資料庫查詢實作，如果比對到完整歌手名稱，會自動抓取唱片、歌曲等資料。
* 取得YouTube搜尋前10首歌曲標題