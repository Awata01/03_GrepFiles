import sys
from sys import path, argv
import os
from dataclasses import dataclass   
import tempfile
import csv
import platform
from PySide6.QtWidgets import *

path.append(r"C:\Users\awata\Awata01\Programming\00_Common\src")
import common_functions as co
from custom_logging import CustomLogging
path.append(r"C:\Users\awata\Awata01\Programming\01_FolderManager\src")
from select_file_manager import SelectFileManager
from grep_files import GrepFiles

def Main():
    """複数のファイルから正規表現でマッチした部分を抽出し、一時CSVファイルに出力する
    """
    logger = CustomLogging("grep_files_main")
    logger.process_start()

    app = QApplication(argv)

    file_filter = "All Files (*.*))"
    dialog_manager = SelectFileManager(file_filter)
    match dialog_manager.exec():
        case SelectFileManager.Accepted:
            file_path_list = dialog_manager.file_path_list
            logger.info(f"選択されたファイルリスト：{file_path_list}")
        case SelectFileManager.Rejected:
            logger.info("SelectFileManagerが強制的に終了")
            logger.process_end()
            sys.exit()

    dialog_grep = GrepFiles(file_path_list)
    match dialog_grep.exec():
        case GrepFiles.Accepted:
            regex_pattern = dialog_grep.regex
            logger.info(f"正規表現：{regex_pattern}")
        case GrepFiles.Backed:
            logger.info("GrepFilesが戻るボタンで終了")
        case GrepFiles.Rejected:
            logger.info("GrepFilesが強制的に終了")
            logger.process_end()
            sys.exit()

    @dataclass
    class dataDef:
        file_name: str
        match_str: str
        file_path: str
        
    
    
    # ヘッダー
    fieldnames = ["file_name", f"match_str", "file_path"]

    # # ファイルリストの各ファイルに対して、正規表現でマッチした部分を取得
    # matches = [
    #     {
    #         "file_name": os.path.basename(file_path)
    #         , "match_str": match_str
    #         , "file_path": file_path
    #     }
    #     for file_path in file_path_list
    #     for match_str in co.regex_matches(file_path, regex_pattern)
    # ]

    # # 一時ファイルに出力する例
    # with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', newline='', suffix='.csv') as temp_file:
    #     writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

    #     writer.writeheader()  # ヘッダーを書き込み
    #     writer.writerows(matches)  # matchesの内容を一時ファイルに書き込み

    #     temp_file_path = temp_file.name

    # # ファイルをデフォルトのテキストエディタで開く (クロスプラットフォーム対応)
    # match platform.system():
    #     case 'Windows':
    #         os.startfile(temp_file_path)
    #     case 'Darwin':  # macOS
    #         os.system(f"open {temp_file_path}")
    #     case 'Linux':
    #         os.system(f"xdg-open {temp_file_path}")

if __name__ == "__main__":
    Main()