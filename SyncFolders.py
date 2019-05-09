import os
import sys
import hashlib
import shutil
sys.path.append(".")
from File import *


def build_dict(folder_path, paths):
    n = len(folder_path)
    path_dict = {}
    for path in paths:
        file_path_id = path[n:]
        path_dict[file_path_id] = path
    return path_dict


# 首先删除待同步目标目录下是否存在多余的文件夹，有则删除；
def remove_dst_redundant_folders(src_File, dst_File):
    src_folders = src_File.get_folderpath_in_dir(aim_depth=100)
    dst_folders = dst_File.get_folderpath_in_dir(aim_depth=100)
    src_path_len = len(src_File.path)
    dst_path_len = len(dst_File.path)

    src_folders_chop_list = []
    for src_folder in src_folders:
        src_folders_chop_list.append(src_folder[src_path_len:])

    dst_folders_chop_list = []
    for dst_folder in dst_folders:
        dst_folders_chop_list.append(dst_folder[dst_path_len:])

    for dst_folders_chop_id in dst_folders_chop_list:
        if dst_folders_chop_id not in src_folders_chop_list:
            restore_target_dir_path = dst_File.path + dst_folders_chop_id
            if File(restore_target_dir_path).exists():
                shutil.rmtree(restore_target_dir_path)


def sync_two_folders_by_md5(src_folder_path, dst_folder_path):
    src = File(os.path.abspath(src_folder_path))
    dst = File(os.path.abspath(dst_folder_path))

    if not src.check_exists_and_isdir():
        return False
    if not dst.check_exists_and_isdir():
        return False

    src_folder_name = src.get_foldername_by_path()
    dst_folder_name = dst.get_foldername_by_path()

    if src_folder_name != dst_folder_name:
        print("SRC DST FolderName not the same：%s and %s ." % (src_folder_name, dst_folder_name))
        return False

    remove_dst_redundant_folders(src, dst)

    src_file_paths = src.get_filepath_in_dir()
    dst_file_paths = dst.get_filepath_in_dir()

    src_file_dict = build_dict(os.path.abspath(src_folder_path), src_file_paths)
    dst_file_dict = build_dict(os.path.abspath(dst_folder_path), dst_file_paths)

    # 对于文件
    # src这边有，dst没有，则复制过去
    # src这边没有，dst有，则删除dst的
    # src这边有，dst有，比较MD5值，一样，跳过；不一样就复制过去

    src_keys = list(src_file_dict.keys())
    dst_keys = list(dst_file_dict.keys())

    common_keys = []
    for src_key in src_keys:
        if src_key in dst_keys:
            common_keys.append(src_key)

    for common_key in common_keys:
        src_keys.remove(common_key)
        dst_keys.remove(common_key)

    independent_keys = []
    independent_keys.extend(src_keys)
    independent_keys.extend(dst_keys)

    for common_key in common_keys:
        src_target_path = src_file_dict.get(common_key)
        dst_target_path = dst_file_dict.get(common_key)
        src_target_md5 = hashlib.md5()
        src_target_md5.update(open(src_target_path, "rb").read())
        dst_target_md5 = hashlib.md5()
        dst_target_md5.update(open(dst_target_path, "rb").read())

        # 比较两个文件的MD5值是否相同，相同则跳过，不同则复制替换
        if src_target_md5.hexdigest() == dst_target_md5.hexdigest():
            continue
        else:
            shutil.copyfile(src_target_path, dst_target_path)

    for independent_key in independent_keys:
        # 对于src中刚出现的文件，拷贝到dst
        if independent_key in src_keys:
            src_target_path = src_file_dict.get(independent_key)
            dst_target_path = dst_folder_path + independent_key
            file_dir, _ = os.path.split(dst_target_path)
            File(file_dir).mkdirs()
            shutil.copyfile(src_target_path, dst_target_path)
        # 对于src中没有文件，dst做相应删除
        else:
            dst_target_path = dst_folder_path + independent_key
            os.remove(dst_target_path)

    print("Sync %s to %s is Done." % (src_folder_path, dst_folder_path))


if __name__ == "__main__":
    sync_two_folders_by_md5(input("Sync src dir: "), input("Sync dst dir: "))




