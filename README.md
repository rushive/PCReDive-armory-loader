《超異域公主連結☆Re:Dive》裝備數量匯出程式
---
從螢幕錄影中辨識裝備數量，並以 json 格式匯出

## 使用方式

在此目錄中執行：( 需要 python ⩾ 3.6, opencv-python, numpy )
```
$ python3 main.py --input <your_video_path>
```

或使用預編譯的 [可執行檔]()，在 `result.json` 檔案中生成裝備數量

<br>

首次使用時會從 [蘭德索爾圖書館](https://pcredivewiki.tw/) 下載用於比對的裝備縮圖至 `images/` 中

若想要查看辨識的過程，取消 `Loader.py` 行 112, 182 中的註解即可

### 可用參數

```
$ python3 main.py --help

usage: main.py [-h] -i PATH [-s NUM]

optional arguments:
  -h, --help            show this help message and exit
  -i PATH, --input PATH
                        path to the video
  -s NUM, --scale NUM   proportion of scaling (default = 1)
```

`-i/--input` : 欲載入的影片路徑

`-s/--scale` : 影片的縮放比 ( 預設為 1.0 ) ，建議數值為 **影片高度 ( 短邊 ) * 縮放比 ≈ 540** 。e.g. 1080p 的影片使用 0.5 ，720p 使用 0.75

## 匯出檔案格式

```
[
    [similarity, quantity],
    ...
]
```

`similarity` : 與 `images/` 中的縮圖的相似度

`quantity` : 該裝備的數量
