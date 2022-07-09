《超異域公主連結☆Re:Dive》裝備數量匯出程式
---
從螢幕錄影中辨識裝備數量以 json 格式匯出，並將數量匯入至 [蘭德索爾圖書館 - 裝備庫](https://pcredivewiki.tw/Armory) 中

## 使用方式

在此目錄中執行：( 需要 python ⩾ 3.6, opencv-python = 4.5.3.56, numpy, requests )
```
$ python3 main.py -i <your_video_path> -q
```

或使用預編譯的 [可執行檔](https://github.com/rushive/PCReDive-armory-loader/releases)
```
# Windows
$ main.exe -i <your_video_path>

# Linux
$ main -i <your_video_path>
```

並在 `result.json` 檔案中生成裝備數量

<br>

首次使用時會從 [蘭德索爾圖書館](https://pcredivewiki.tw/) 下載用於比對的裝備縮圖至 `images/` 中

若要查看辨識的過程，移除命令的 `-q` 選項即可， **請勿按 `X` 關閉預覽視窗**，若要關閉可以在彈出視窗中按下 <kbd>q</kbd> 提早中止

### 可用參數

```
$ python3 main.py --help

usage: main.py [-h] -i PATH [-s NUM]

optional arguments:
  -h, --help            show this help message and exit
  -i PATH, --input PATH
                        path to the video
  -s NUM, --scale NUM   proportion of scaling (default = 1)
  -q, --quiet           hide window when processing
```

`-i/--input` : 欲載入的影片路徑

`-s/--scale` : 影片的縮放比 ( 預設為 1.0 ) ，建議數值為 **影片高度 ( 短邊 ) * 縮放比 ≈ 540** 。e.g. 1080p 的影片使用 0.5 ，720p 使用 0.75

`-q/--quiet` : 安靜模式，隱藏辨識時的彈出預覽視窗

## 匯出檔案格式

```
[
    [equipment_id, similarity, quantity],
    ...
]
```

`equipment_id` : 該裝備的 id

`similarity` : 與 `images/` 中的縮圖的相似度

`quantity` : 該裝備的數量

## 匯出至蘭德索爾圖書館裝備庫

**(首次使用時建議使用無痕模式測試避免在發生錯誤時覆寫先前輸入的數據)**

進入 [蘭德索爾圖書館 - 裝備庫](https://pcredivewiki.tw/Armory) ，加入角色後點選道具欄，按下 <kbd>F12</kbd> 開啟 devTools ，將檔案 `template.js` 中的內容全選貼上至 `console` 分頁中並執行，然後重新整理即可 ( 若有其他操作 ( 例如加入角色、改 rank 等 ) ，需要再按一次儲存隊伍，前面的程式碼只有修改裝備數量而已 )

## 更新本機端的裝備縮圖 ( 開新地圖時使用 )

刪除目錄 images ，同上進入 **裝備庫 - 道具欄** 中，並 **向下捲動至網頁底部** ，開啟瀏覽器 console ，將檔案 `fetchURLs.js` 內容貼上並執行，點選右下角的 `copy` 複製 ( 以 google chrome 為例 ) ，將結果貼上至 `armory.json` 中 ( 直接全選貼上覆寫，不用保留原本的內容 ) ，並重新執行 main.py / 可執行檔下載新的裝備縮圖

## FAQ

**貼上 `template.js` 程式碼匯出到裝備庫中時出現 `Uncaught TypeError: Cannot read properties of null (reading 'map')` 錯誤**

目前瀏覽器中還未儲存隊伍資料，先按儲存隊伍後再試一次
