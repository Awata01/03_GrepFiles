from sys import exit, argv, path
import os
import tempfile
import csv
import platform
from PySide6.QtWidgets import *

path.append(r"C:\Users\awata\Awata01\Programming\00_Common\src")
import common_functions as co
import grep_files as pyw

def Main():
    """複数のファイルから正規表現でマッチした部分を抽出し、一時CSVファイルに出力する
    """
    QApplication(argv)
    file_list_path = test()

    dialog = pyw.GrepFiles(file_list_path)
    dialog.show()
    if dialog.exec() == QDialog.Accepted:
        regex_pattern = dialog.regex
    else:
        exit()

    # ヘッダー
    fieldnames = ["file_name", f"match_str", "file_path"]

    # ファイルリストの各ファイルに対して、正規表現でマッチした部分を取得
    matches = [
        {
            "file_name": os.path.basename(file_path)
            , "match_str": match_str
            , "file_path": file_path
        }
        for file_path in file_list_path
        for match_str in co.regex_matches(file_path, regex_pattern)
    ]

    # 一時ファイルに出力する例
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', newline='', suffix='.csv') as temp_file:
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

        writer.writeheader()  # ヘッダーを書き込み
        writer.writerows(matches)  # matchesの内容を一時ファイルに書き込み

        temp_file_path = temp_file.name

    # ファイルをデフォルトのテキストエディタで開く (クロスプラットフォーム対応)
    match platform.system():
        case 'Windows':
            os.startfile(temp_file_path)
        case 'Darwin':  # macOS
            os.system(f"open {temp_file_path}")
        case 'Linux':
            os.system(f"xdg-open {temp_file_path}")

if __name__ == "__main__":
    Main()