# 齁斑資料夾 (HobanFolder)

這是由齁斑科技社會企業開發的智慧檔案整理工具，能夠自動將檔案依據修改日期分類到對應的資料夾中。

This is an intelligent file organization tool developed by Hoban Technology Social Enterprise that automatically categorizes files into corresponding folders based on their modification dates.

## 功能特點 | Features

- 自動依據檔案的修改日期建立資料夾（格式：YYYYMMDD）
- 自動處理重複檔案
- 提供進度條顯示處理進度
- 完整的錯誤處理機制
- 使用者友善的圖形介面

- Automatically creates folders based on file modification dates (format: YYYYMMDD)
- Automatic handling of duplicate files
- Progress bar to show processing status
- Comprehensive error handling
- User-friendly graphical interface

## 使用方法 | Usage

1. 將 `hobanfolder.py` 放在要整理的資料夾中
2. 執行程式：
   - 直接點擊 `hobanfolder.py`
   - 或在命令列中執行 `python hobanfolder.py`
3. 在確認對話框中點選「確定」開始處理
4. 等待處理完成

1. Place `hobanfolder.py` in the folder you want to organize
2. Run the program:
   - Double-click `hobanfolder.py`
   - Or execute `python hobanfolder.py` in command line
3. Click "OK" in the confirmation dialog to start
4. Wait for completion

## 檔案處理規則 | File Processing Rules

- 檔案會被移動到以其修改日期命名的資料夾中（例如：20240315）
- 如果遇到相同檔名：
  - 若檔案內容相同，則直接覆蓋
  - 若檔案內容不同，則自動重新命名（加上數字後綴）

- Files are moved to folders named by their modification date (e.g., 20240315)
- For duplicate filenames:
  - If content is identical, the file will be overwritten
  - If content differs, file will be automatically renamed (with numeric suffix)

## 系統需求 | System Requirements

- Python 3.6 或更高版本
- tkinter（Python 標準庫，通常已預裝）

- Python 3.6 or higher
- tkinter (Python standard library, usually pre-installed)

## 安裝方法 | Installation

### 方法一：直接使用執行檔 | Method 1: Using Executable
1. 下載 `hobanfolder.exe`
2. 將程式放在您想要的位置
3. 第一次執行時會自動加入右鍵選單

1. Download `hobanfolder.exe`
2. Place the program where you want
3. Right-click menu entry will be added automatically on first run

### 方法二：使用原始碼 | Method 2: Using Source Code
1. 下載 `hobanfolder.py`
2. 確保系統已安裝 Python 3.6+
3. 無需額外安裝其他套件

1. Download `hobanfolder.py`
2. Ensure Python 3.6+ is installed
3. No additional packages required

### 開發者：打包執行檔 | For Developers: Building Executable
1. 安裝 PyInstaller：
   ```bash
   pip install pyinstaller
   ```
2. 執行打包指令：
   ```bash
   pyinstaller --onefile --noconsole hobanfolder.py
   ```
3. 執行檔將會在 `dist` 資料夾中產生

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run packaging command:
   ```bash
   pyinstaller --onefile --noconsole hobanfolder.py
   ```
3. Executable will be generated in the `dist` folder

## 注意事項 | Notes

- 建議在執行前先備份重要檔案
- 程式執行時會顯示進度視窗，請等待處理完成
- 處理完成後會顯示處理結果統計

- Backing up important files before running is recommended
- Progress window will be shown during execution, please wait for completion
- Processing statistics will be displayed upon completion

## 授權條款 | License

MIT License