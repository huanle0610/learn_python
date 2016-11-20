""" Windows class """
import win32api
import win32file
import win32profile
import win32netcon
import win32net
import traceback
import sys
import string

import math


def convert_size(size):
    if (size == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return '%s %s' % (s, size_name[i])


class Windows:
    """A class to  represent a windows machine"""
    compute_name = ''
    user_name = ''
    drivers = []
    disks = []

    def __init__(self):
        self.compute_name = win32api.GetComputerName()
        self.user_name = win32api.GetUserName()
        self.drivers = self.get_drivers()

    def get_drivers(self):
        """ 获取所有的驱动器 """
        drives = []
        bitmask = win32api.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                letter += ':/'
                drives.append(letter)
                self.get_disk(letter)
            bitmask >>= 1

        return drives

    def get_disk(self, root_path):
        """ 判断盘符是否为硬盘，若是加入disks """
        if win32file.GetDriveType(root_path) == win32file.DRIVE_FIXED:
            self.disks.append(root_path)

    def get_disk_size(self, path):
        return win32file.GetDiskFreeSpaceEx(path)

    def print_disk_size(self):
        for disk in self.disks:
            free_bytes, total_bytes, total_free_bytes = win32file.GetDiskFreeSpaceEx(disk)
            # print("%s %s %s" % tuple(map(convert_size, self.get_disk_size(disk))))
            print("%s %s %s %.2f%%" %
                  (disk, convert_size(free_bytes), convert_size(total_bytes), (total_bytes-free_bytes)*100/total_bytes))

    def print_info(self):
        print('Compute Name: ' + self.compute_name)
        print('User: ' + self.user_name)
        print('Drives: %s' % self.drivers)
        print('Disks: %s' % self.disks)
        self.print_disk_size()
        self.print_env()

    def print_env(self):
        print(win32profile.GetEnvironmentStrings())

    def getusers(self, server):
        res = 1  # initially set it to true
        pref = win32netcon.MAX_PREFERRED_LENGTH
        level = 0  # setting it to 1 will provide more detailed info
        total_list = []
        try:
            while res:  # loop until res2
                (user_list, total, res2) = win32net.NetWkstaUserEnum(server, level, res, pref)
                print(user_list, total, res2)
                for i in user_list:
                    total_list.append(i['username'])
                res = res2
                return total_list
        except win32net.error:
            print(traceback.format_tb(sys.exc_info()[2]), '\n', sys.exc_info(), '\n')

    def getall_boxes(self, domain='', server=''):
        res = 1
        wrk_lst = []
        try:
            while res:  # loop until res2
                (wrk_list2, total, res2) = win32net.NetServerEnum('', 100, win32netcon.SV_TYPE_ALL, server, res,
                                                                  win32netcon.MAX_PREFERRED_LENGTH)
                wrk_lst.extend(wrk_list2)
                res = res2
        except win32net.error:
            print('Error: %s' % traceback.format_tb(sys.exc_info()[2]), '\n')

        final_lst = []
        for i in wrk_lst:
            final_lst.append(str(i['name']))
        return final_lst


if __name__ == '__main__':
    w = Windows()
    w.print_info()
    server = r'\\' + w.compute_name
    print(w.getusers(server))
    print(w.getall_boxes(server=server))

