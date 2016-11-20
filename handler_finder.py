"""
Wrapper to call Handle
https://download.sysinternals.com/files/Handle.zip
"""
import os
import os.path
import sys
import re
import subprocess


def run_handle(opt, opt_val, handle_cmd_path):
    p = subprocess.Popen([handle_cmd_path, opt, opt_val], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None,
                         universal_newlines=True)
    stdout_text, stderr_text = p.communicate(input="1\n\n")

    # print("stdout: %r\nstderr: %r" % (stdout_text, stderr_text))
    # print("stdout: %s\n" % (stdout_text,))
    if p.returncode != 0:
        raise RuntimeError("%r failed, status code %d" % (handle_cmd_path, p.returncode))

    return stdout_text


class HandlerFinder:
    """ find handler """

    def __init__(self, handle_path):
        if not os.path.isfile(handle_path):
            raise RuntimeError("handle can't find in %s" % handle_path)
        self.handle_path = handle_path

    def find_pid_in_str(self, text):
        # print("Got It:" + text)
        pid_str = ' pid: '
        pos = text.rfind(pid_str)
        if pos != -1:
            pos += len(pid_str)
            return text[pos:pos+10].split(' ')[0]

    def find_by_application(self, app_name, file_path, lower_find=True):
        output_text = run_handle('-p', app_name, self.handle_path)

        if lower_find:
            output_text_lower = output_text.lower()
            file_path_lower = file_path.lower()
            pos = output_text_lower.find(file_path_lower)
        else:
            pos = output_text.find(file_path)

        if pos == -1:
            return False

        pos += len(file_path)
        pid = self.find_pid_in_str(output_text[0:pos])
        return pid

    def find_by_file_path(self, file_path):
        pass


if __name__ == '__main__':
    handler_path = r"H:\csharp\Handle\handle64.exe"
    hf = HandlerFinder(handler_path)
    # run_handler()
    app = 'vlc'
    file = '.MP3'
    pid = hf.find_by_application(app, file)
    if pid:
        print('find process %s is opening file %s' % (pid, file))
    else:
        print('no process opened file')
