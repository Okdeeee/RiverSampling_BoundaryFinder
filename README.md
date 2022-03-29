# 河流紋溝邊界查詢工具
### 功能：
這個工具主要功能是讓使用者輸入河流中心線的shp以及DEM，找出可能是河流邊界的點，最後輸出為點圖層。
###    使用流程：
工具為ArcGIS Script Tool，在ArcGIS上開啟.tbx檔案即可，RiverSplit.tbx為ArcGIS Pro的版本；RiverSplit_ArcMap.tbx為ArcMap的版本。

1.	River split point and sampling >>
2.	extract value by point (ArcGIS SA Tool)>>
3.	River find boundary point

![](https://i.imgur.com/SR9Di1h.png)
![](https://i.imgur.com/9jxLs0k.png)


###    程式參數輸入：

1. **River Split Point and Sampling**
> ![](https://i.imgur.com/S2ESZce.png)
* River Layer：
    >輸入河流的中心線Shapefile
* Output Layer Path：
    >程式輸出點圖層的路徑
* River Code Field：
    >河流中心線的編碼欄位。使用者需要為河流中心線製作一個編碼欄位(EX: AA、AB、AC)，為每條河流中心線賦予一個不重複的編碼值，後續判斷河流邊界時會用到這個編碼。
* Split Distance(m)：
    > 輸入浮點數x，設定沿著河流中心線每隔x公尺做一排取樣點。
* Extend Distance(m)：
    >輸入浮點數x，設定最遠的取樣點距離中心線x公尺(單邊)
* Sampling Distance(m)：
    >輸入浮點數x，設定一排取樣點上每個相距x公尺。
* Type：
    >供使用者輸入Horizontal或Vertical，讓取樣點以水平或垂直方式延展


**輸出圖層**
> ![](https://i.imgur.com/k3pspR0.png)

2. **Extract Value to Point**
> 詳見 https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/extract-values-to-points.htm
為取樣點寫入對應dem的網格值

3. **River find boundary point**
> ![](https://i.imgur.com/pDwfGge.png)
*    Sample Point Layer : 
> 輸入Extract Value By Point工具生成的點圖層
*    Output Point Layer : 
> 選擇成果點圖層的輸出路徑
*    Thershold(m) : 
   > 設定河流紋溝判斷高度落差的門檻值，單位為公尺
   > 
**輸出成果**
> ![](https://i.imgur.com/AwSjigZ.png)
