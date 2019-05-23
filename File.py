import os


class File:
    def __init__(self, path, verbose=True):
        self.path = path
        self.verbose = verbose

    def check_exists_and_isfile(self):
        if not os.path.exists(self.path):
            if self.verbose:
                print("%s does not exist!" % self.path)
            return False
        else:
            if not os.path.isfile(self.path):
                if self.verbose:
                    print("%s exists and is not a file!" % self.path)
                return False
            else:
                if self.verbose:
                    print("%s exists and is a file." % self.path)
                    return True

    def check_exists_and_isdir(self):
        if not os.path.exists(self.path):
            if self.verbose:
                print("%s does not exist!" % self.path)
            return False
        else:
            if not os.path.isdir(self.path):
                if self.verbose:
                    print("%s exists and is not a dir!" % self.path)
                return False
            else:
                if self.verbose:
                    print("%s exists and is a dir." % self.path)
                    return True

    def mkdirs(self):
        if not os.path.exists(self.path):
            if self.verbose:
                print("Folder: %s does not exist, creating..." % self.path)
            os.makedirs(self.path)

    def exists(self):
        if not os.path.exists(self.path):
            if self.verbose:
                print("%s does not exist!" % self.path)
            return False
        else:
            if self.verbose:
                print("%s exists!" % self.path)
            return True

    def get_folderpath_in_dir(self, aim_depth=1, current_dept=1, include_hidden=False):
        folderpath_list = []
        if not os.path.exists(self.path):
            print("Dir: %s is not exist, quit...", self.path)
            return folderpath_list
        else:
            thislayer_filenames = os.listdir(self.path)
            for thislayer_filename in thislayer_filenames:
                thislayer_filepath = os.path.join(self.path, thislayer_filename)
                if os.path.isdir(thislayer_filepath):  # handle dir
                    if not include_hidden:
                        if "." in thislayer_filename:
                            continue
                    folderpath_list.append(thislayer_filepath)
                    if aim_depth != current_dept:
                        folderpath_list.extend(File(thislayer_filepath).get_folderpath_in_dir(aim_depth, current_dept + 1))
        return folderpath_list

    def get_foldername_by_path(self):
        if os.path.isdir(self.path):
            if '\\' in self.path:
                foldername = self.path.split('\\')[-1]
                if foldername == '':
                    return self.path.split('\\')[-2]
                return foldername
            elif '/' in self.path:
                foldername = self.path.split('/')[-1]
                if foldername == '':
                    return self.path.split('/')[-2]
                return foldername
            else:
                return self.path
        elif os.path.isfile(self.path):
            print("wait to be coded!")
        else:
            return []


    def get_filepath_in_dir(self, include_hidden=False):
        filepath_list = []
        if not os.path.exists(self.path):
            print("Dir: %s is not exist, quit...", dir)
            return filepath_list
        else:
            if not os.path.isdir(self.path):
                return filepath_list
            else:
                thislayer_filenames = os.listdir(self.path)
                for thislayer_filename in thislayer_filenames:
                    thislayer_filepath = os.path.join(self.path, thislayer_filename)
                    if os.path.isdir(thislayer_filepath):  # handle dir
                        if not include_hidden:
                            if "." in thislayer_filename:
                                continue
                        filepath_list.extend(File(thislayer_filepath).get_filepath_in_dir(include_hidden))
                    else:  # handle file
                        filepath_list.append(thislayer_filepath)

        return filepath_list

