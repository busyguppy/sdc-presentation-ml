# MP3 Tagger
僅供簡報DEMO，未實作mp3 tagging相關功能，model準確率約93%。

## 安裝
1. 安裝Python 3.7（Tensorflow只支援到這版本） 
2. git clone https://github.com/busyguppy/SDC-presentation-ML.git
3. cd SDC-presentation-ML
4. python -m pip install --upgrade pip
5. pip install pipenv --upgrade
6. pipenv --python 3.7
7. pipenv shell
8. pip install -r requirements.txt
9. Have fun :)

## 執行
``` bash
├─data
├─mp3tagger
│  ├─bootstrap
│  ├─classes            # 特徵擷取       
│  ├─labeler            # 使用者界面：檢查文字分段正確性、建立直覺
│  ├─musicbrainz        # 音樂資料庫查詢
│  │  └─entities
│  ├─pagescraper        # 網頁爬蟲
│  │  ├─billboard
│  │  ├─mojim
│  │  └─youtube
│  ├─preprocessing      # 資料前置處理（特徵選擇工具）
│  └─training
│      ├─grid_search    # Hyperparameter Grid Search
│      └─models         # 模組訓練程式碼
│          └─obsolete
├─notebooks             # jupyter notebook，基本沒在用...
├─scripts               # 準備dataset的腳本
│  └─obsolete
└─tests                 # 特徵擷取測試用
```
