## ❇ 從零開始的 Line 聊天機器人

![python](https://img.shields.io/badge/python-3.6.0-blue.svg)
![keras](https://img.shields.io/badge/keras-2.3.1-green.svg)
![linebot](https://img.shields.io/badge/line-SDK%201.16.0-brightgreen.svg)
![flask](https://img.shields.io/badge/flask-1.1.2-yellow.svg)

匯出聊天記錄，接著訓練、部署，最後上架自己的對話機器人。

![Imgur](https://i.imgur.com/ouHct9T.png)


### 🗳 0. 前置作業與需求

|條目|內容|
|:-:|:-|
|#1|Line 帳號|
|#2|萬筆以上的對話紀錄|
|#3|擁有實體 IP 位址或是家用數據機的管理員身分|


### 🖨 1. 匯出對話記錄

|平台|步驟|
|:-:|:-:|
|iOS|進入對話－設定－傳送聊天記錄－上傳至雲端－再下載|
|Android|進入對話－設定－備份聊天記錄－以文字檔備份－上傳至雲端－再下載|

應為一純文字檔，可透過編輯器開啟檢查。


### 🖱 2. 安裝 WSL 作為開發和部署環境
至[微軟商店](https://www.microsoft.com/store/productId/9NBLGGH4MSV6)下載「Ubuntu」，安裝完成後可能需要重啟電腦，之後可於開始功能表中搜尋「Ubuntu」啟動該應用。透過 WSL 的好處在於能夠完全將開發環境獨立出來，並可在專案捨棄或完成後，透過移除「Ubuntu」來完全刪除相關的資料。啟動並完成使用者建置後，於命令提示介面依序完成下列指令：

|指令|簡介|
|:-|:-|
|sudo add-apt-repository ppa:deadsnakes/ppa|增加依賴套件庫|
|sudo apt-get update|同步索引文件|
|sudo apt-get install python3.6|安裝 Python 3.6|
|sudo apt-get install python3.6-dev|安裝 Python 3.6 相關工具|
|sudo apt-get install python3.6-venv|安裝 Python 3.6 虛擬環境|

接著，下載專案並建置 Python 虛擬環境。虛擬環境能夠使各個專案（雖然這裡只有一個）的依賴庫、Python 版本彼此獨立。

|指令|簡介|
|:-|:-|
|git clone https://github.com/der3318/linebot-converter.git|下載專案資源|
|cd linebot-converter|進入資料夾|
|python3.6 -m venv env|建立一個 Python 版本為 3.6 的虛擬環境|
|. evn/bin/activate|啟用虛擬環境|
|pip install -r requirements.txt|安裝依賴套件|

最後，複製一份對話記錄到專案中，作為下一步的模型訓練資料。假設從手機匯出的文字檔的路徑是「C:\Users\admin\Downloads\chat.txt」，那麼可以透過指令「cp -f /mnt/c/Users/admin/Downloads/chat.txt history.txt」來進行檔案複製。


### 📖 訓練模型
透過「python train.py」來進行模型的訓練。每學習一輪，即會「預覽」當前模型的表現。若認為回答得很不滿意，可以透過任何按鍵再接續下一輪的訓練，或是以「CTRL-C」來終止。中止後，會將目前的模型參數存入檔案「model.h5」中。

![Imgur](https://i.imgur.com/iojpHJF.png)

這裡使用的模型是常見的「Sequence To Sequence」序列，搭配「Attention Mechanism」來優化，並啟用「Beam Search」來建構較佳的句子。通常會需要訓練約二十至三十輪才會有相當的結果，而每輪所需的時間從數十秒至數分鐘都有可能，取決於電腦處理器的效能。此外，目前 WSL 尚未支援 GPU 加速，因此顯卡有無並不影響。


### 🌐 伺服器設定
絕大部分的電腦都不會擁有實體 IP，而是位於分享器或數據機的內網內。先關閉防火牆，並以指令「ip route | grep default」來查詢分享器的 IP，接著透過瀏覽器連接該 IP（http://查詢到的分享器位址）、輸入帳號密碼登入主控。若沒有設登入調整的印象，估計可能還是原廠的設定，可上網查詢廠牌的預設帳號密碼。

![Imgur](https://i.imgur.com/covoffG.png)

主控介面中應能查到所有連接的設備，以及分配給電腦的位址，接著尋找「Port Forwarding」或稱「通訊埠轉發」的功能，新增規則，將公開位址的 443 和 80 分別轉發至內部位址的同樣通訊埠，完成後儲存並套用。

![Imgur](https://i.imgur.com/oM6hFLH.png)

接下來，要為自己的電腦設定一個網域名稱，因為安全協定的簽發憑證時需要用到。到 https://www.whatismyip.com/ 查詢並記下分享器的公開位址，並到 https://nctu.me/ 以台灣人身分（TWID）免費註冊自己專屬的網域。完成後，到網域管理新增一個網域，再到「DNS 管理」增加一筆類型為「A」的資料，最後如下圖，名稱就是新註冊的網域，內容則是分享器的公開位址。

![Imgur](https://i.imgur.com/NnQjJ2N.png)

可透過指令「sudo env/bin/python validation.py」來啟動路由，並在瀏覽器中以「http://剛剛註冊的網域」來測試使否能成功連線。理論上能夠看到「The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.」等訊息出現。


### 🔐 金鑰與 SSL 憑證

因為 Line 機器人的後端需要加密的連線，因此需要將 HTTP 伺服器調整為 HTTPS。至 https://www.sslforfree.com/ 輸入剛剛拿到的網域，並選擇免費的方案之後，會進入到「認證伺服器域名」的步驟。選擇「HTTP File Upload」的方式進行認證，下載檔案並透過指令「cp -f /mnt/c/該檔案的路徑/亂碼.txt sslforfree.txt」來複製（與複製對話記錄的邏輯相同）。

![Imgur](https://i.imgur.com/Xdy4Pyx.png)

完成後，以「sudo env/bin/python validation.py」啟用路由，並回到網頁中點下一步完成。認證成功後，點擊下載金鑰與憑證，並解壓縮，應有三個檔案：

![Imgur](https://i.imgur.com/GpI8jw8.png)

先以「CTRL-C」關閉路由後分，別以「cp -f /mnt/c/金鑰憑證的路徑/ca_bundle.crt ca_bundle.crt」、「cp -f /mnt/c/金鑰憑證的路徑/certificate.crt certificate.crt」與「cp -f /mnt/c/金鑰憑證的路徑/private.key private.key」來複製。最後，再依序指令「cat certificate.crt > chain.pem」、「echo "" >> chain.pem」與「cat ca_bundle.crt >> chain.pem」來合成完整的憑證。


### 🛠 註冊 Line 官方帳號並連結網域
這是最後一個步驟。到開發者平台 https://developers.line.biz/zh-hant/ 登入後，選擇「Messaging API」依照指示創立一個官方 Line 帳號。相關資訊填寫完成之後，到「Basic Settings」記下「Channel Secret」，並到「Messaging API」最下方點選「Issue」來發行並記下「Channel Access Token」，而「Messaging API」上半部則有該官方帳號的 Line ID 和二維碼，可用來將它加入好友進行測試。以指令「sudo env/bin/python chatbot.py SECRET TOKEN」啟動加密後的路由並驅動聊天機器人，其中「SECRET」和「TOKEN」分別是剛剛記下的雜湊亂碼。

![Imgur](https://i.imgur.com/5pKN2WF.png)

啟動路由後，如上圖所示，將「Webhook URL」設定為「https://註冊並認證後的網域/webhook」並啟用，且到「Auto Reply Messages」點選「Edit」，依照上圖勾選相關設定。

上架的步驟至此全數完成，將機器人加為好友後即可開啟對話，它應能根據學習的結果給出對應的回覆！

