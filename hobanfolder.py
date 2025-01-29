import os
import sys
import shutil
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox

def get_script_path():
    return os.getcwd() + os.sep

def get_script_filename():
    if getattr(sys, 'frozen', False):
        return os.path.basename(sys.executable)
    return os.path.basename(__file__)

def zero_pad(num):
    return f"{num:02d}"

def rename_file(file_path):
    base_name, ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base_name}_{counter}{ext}"
        counter += 1
    return file_path

def is_same_file(file1_path, file2_path):
    # 比較檔案的大小和內容是否相同
    if os.path.getsize(file1_path) != os.path.getsize(file2_path):
        return False
    
    # 比較檔案內容
    chunk_size = 1024
    with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
        while True:
            chunk1 = f1.read(chunk_size)
            chunk2 = f2.read(chunk_size)
            if chunk1 != chunk2:
                return False
            if not chunk1:  # 檔案讀取完畢
                break
    return True

class ProgressWindow:
    def __init__(self, total_files):
        self.root = tk.Tk()
        self.root.title("處理進度")
        
        # 設定視窗大小和位置
        window_width = 400
        window_height = 150
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 設定視窗樣式
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # 建立進度條框架
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 進度標籤
        self.label = ttk.Label(frame, text="正在處理檔案...")
        self.label.pack(pady=(0, 10))
        
        # 進度條
        self.progress = ttk.Progressbar(
            frame, 
            orient="horizontal", 
            length=300, 
            mode="determinate"
        )
        self.progress.pack(pady=(0, 10))
        
        # 當前處理檔案名稱
        self.file_label = ttk.Label(frame, text="")
        self.file_label.pack()
        
        self.total_files = total_files
        self.current_file = 0
        
        # 更新進度條最大值
        self.progress["maximum"] = total_files
        
    def update(self, filename):
        self.current_file += 1
        self.progress["value"] = self.current_file
        self.label.config(text=f"進度: {self.current_file}/{self.total_files}")
        self.file_label.config(text=f"正在處理: {filename}")
        self.root.update()
        
    def close(self):
        self.root.destroy()

def create_context_menu():
    try:
        # 獲取程式所在路徑
        exe_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
        exe_dir = os.path.dirname(exe_path)
        
        # 準備註冊表內容（注意：這裡使用 bytes 來處理中文）
        reg_content = f'''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\HobanFolder]
@=hex(2):75,00,73,00,65,00,20,00,E9,BD,81,E6,96,91,E8,B3,87,E6,96,99,E5,A4,BE,E6,95,B4,E7,90,86,00
"Icon"="\"%SystemRoot%\\System32\\shell32.dll\",45"

[HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\HobanFolder\\command]
@="\"{exe_path}\" \\"%V\\""
'''
        
        # 創建臨時的 .reg 檔案，使用 utf-16le 編碼
        reg_path = os.path.join(exe_dir, 'temp_context_menu.reg')
        with open(reg_path, 'w', encoding='utf-16le') as f:
            # 加入 BOM
            f.write('\ufeff')
            f.write(reg_content)
        
        # 執行 .reg 檔案
        os.system(f'regedit /s "{reg_path}"')
        
        # 刪除臨時檔案
        try:
            os.remove(reg_path)
        except:
            pass
            
        return True
    except Exception as e:
        return False

def main():
    # 檢查是否為打包後的執行檔
    if getattr(sys, 'frozen', False):
        # 嘗試建立右鍵選單
        create_context_menu()
    
    # 顯示確認對話框
    if not msgbox.askokcancel("齁斑資料夾", "按確定開始將檔案依照日期分類到資料夾中，如不執行請按取消"):
        return

    start_time = time.time()
    path = get_script_path()
    script_name = get_script_filename()
    
    # 先計算要處理的檔案數量
    total_files = sum(1 for f in os.listdir(path) 
                     if os.path.isfile(os.path.join(path, f)) and f != script_name)
    
    # 創建進度視窗
    progress_window = ProgressWindow(total_files)
    
    count_files = 0
    count_folders = 0
    error_files = []
    print_log = []
    print_log.append(f"開始處理目錄：{path}")
    
    # 處理目錄中的所有檔案
    for filename in os.listdir(path):
        try:
            if filename == script_name:
                continue
                
            file_path = os.path.join(path, filename)
            if not os.path.isfile(file_path):
                continue
            
            # 更新進度條
            progress_window.update(filename)
            print_log.append(f"正在處理檔案：{filename}")
            
            # 取得檔案修改日期
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            folder_name = f"{file_time.year}{zero_pad(file_time.month)}{zero_pad(file_time.day)}"
            folder_path = os.path.join(path, folder_name)
            
            # 建立目標資料夾
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                count_folders += 1
                print_log.append(f"建立資料夾：{folder_name}")
                
            # 移動檔案
            dest_path = os.path.join(folder_path, filename)
            if os.path.exists(dest_path):
                if is_same_file(file_path, dest_path):
                    shutil.move(file_path, dest_path)
                    print_log.append(f"覆蓋相同檔案：{filename}")
                else:
                    new_path = rename_file(dest_path)
                    shutil.move(file_path, new_path)
                    print_log.append(f"重新命名並移動：{filename} -> {os.path.basename(new_path)}")
            else:
                shutil.move(file_path, dest_path)
                print_log.append(f"移動檔案：{filename} -> {folder_name}")
                
            count_files += 1
            
        except Exception as e:
            error_msg = f"處理檔案 {filename} 時發生錯誤：{str(e)}"
            print_log.append(error_msg)
            error_files.append(filename)
    
    # 關閉進度視窗
    progress_window.close()
    
    elapsed_time = time.time() - start_time
    
    if error_files:
        # 有錯誤時顯示詳細記錄
        result_message = [
            f"已建立{count_folders}個新資料夾，並處理了{count_files}個檔案",
            f"共花了{elapsed_time:.2f}秒",
            "",
            "處理過程中發生錯誤，詳細記錄：",
            "-------------------"
        ]
        result_message.extend(print_log)
        result_message.extend([
            "",
            "發生錯誤的檔案：",
            "-------------------"
        ])
        result_message.extend(error_files)
        
        # 顯示錯誤訊息
        msgbox.showerror("齁斑資料夾 - 處理完成但發生錯誤", "\n".join(result_message))
    else:
        # 成功時只顯示簡短訊息
        result_message = f"已成功建立{count_folders}個新資料夾，並處理了{count_files}個檔案\n共花了{elapsed_time:.2f}秒"
        msgbox.showinfo("齁斑資料夾 - 完成", result_message)
    
    # 無論是否有錯誤都將完整記錄寫入檔案
    # log_file = os.path.join(path, "hobanfolder_log.txt")
    
    full_log = [
        f"齁斑資料夾執行記錄",
        f"執行時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"已建立{count_folders}個新資料夾，並處理了{count_files}個檔案",
        f"共花了{elapsed_time:.2f}秒",
        "",
        "詳細處理記錄：",
        "-------------------"
    ]
    full_log.extend(print_log)
    
    # with open(log_file, "w", encoding="utf-8") as f:
    #     f.write("\n".join(full_log))

if __name__ == "__main__":
    main() 