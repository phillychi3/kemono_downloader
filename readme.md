# Kemono Downloader



### 使用 Poetry 安裝

```bash
poetry install
```

### 手動安裝

```bash
pip install requests fake-useragent progress
```

## 使用方法

### 基本語法

```bash
python downloader.py <kemono_url> [選項]
```

### 選項

- `-z, --zip`: 將檔案保存為 ZIP 格式
- `-f, --folder <路徑>`: 指定下載資料夾路徑 預設為 `downloads`
- `-d, --delay <秒數>`: 設定請求間隔時間（預設為 1 秒）

### 使用範例

#### 下載用戶的所有貼文

```bash
# 下載到預設資料夾
python downloader.py https://kemono.su/patreon/user/12345

# 下載並保存為 ZIP 檔案
python downloader.py https://kemono.su/patreon/user/12345 -z

# 指定下載資料夾
python downloader.py https://kemono.su/patreon/user/12345 -f ./my_downloads

# 設定 2 秒延遲
python downloader.py https://kemono.su/patreon/user/12345 -d 2
```

#### 下載單個貼文

```bash
# 下載特定貼文
python downloader.py https://kemono.su/patreon/user/12345/post/67890

# 下載特定貼文並保存為 ZIP
python downloader.py https://kemono.su/patreon/user/12345/post/67890 -z
```

## 支援的 URL 格式

### 用戶頁面 URL
```
https://kemono.su/{service}/user/{user_id}
```

### 貼文 URL
```
https://kemono.su/{service}/user/{user_id}/post/{post_id}
```

