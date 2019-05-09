from File import File
import os
import pandas as pd
import sys
sys.path.append(os.path.abspath('./'))


class FileConverter:
    def __init__(self):
        pass

    def xlsx_to_csv(src_file_path):
        if not File(src_file_path).check_exists_and_isfile():
            return False

        (src_file_text, _) = os.path.splitext(src_file_path)
        dst_file_path = src_file_text + ".csv"

        data_xls = pd.read_excel(src_file_path, index_col=0)
        data_xls.to_csv(dst_file_path, encoding='utf-8')
        if not File(dst_file_path).check_exists_and_isfile():
            return False
        else:
            return True


if __name__ == "__main__":

    FileConverter.xlsx_to_csv(r"C:\Data\stock_database_test\all_stocks_2019-04-21.xlsx")