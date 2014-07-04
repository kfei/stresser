#!/usr/bin/env python
import json
import sys
from subprocess import call


class Task(object):
    task_type = None
    task_url = None

    def __init__(self, j):
        """
        Deserialize and get informations from the json-format RPC request.
        """
        self.task_name = json.loads(j)[0]['task_name']
        self.task_type = json.loads(j)[0]['task_type']
        self.task_url = json.loads(j)[0]['task_url']
        self.task_executable = None

    def get_executable(self):
        """
        Download the task's executable file to local.
        """
        import tempfile
        import urllib
        import urlparse
        from os.path import join

        try:
            temp_dir = tempfile.mkdtemp()
            split = urlparse.urlsplit(self.task_url)
            file_name = join(temp_dir, split.path.split("/")[-1])
            urllib.urlretrieve(self.task_url, file_name)
        except:
            sys.exit(1)

        self.task_executable = file_name

    def clean_executable(self):
        """
        Remove the temporary directory for storing task's executable.
        """
        from shutil import rmtree
        from os.path import dirname
        dir = dirname(self.task_executable)
        try:
            rmtree(dir)
        except:
            print("[INFO] Failed to clean temporary files.")

    def run_sikuli(self, java_bin, sikuli_ide):
        cmd = [java_bin, '-jar', sikuli_ide, '-r', self.task_executable]

        return call(cmd, shell=True)

    def run_script(self, shell):
        import platform

        if platform.system() == 'Windows':
            cmd = [self.task_executable]
        else:
            cmd = [shell] + [self.task_executable]

        return call(cmd, shell=True)

    def run_bin(self):
        cmd = [self.task_executable]

        return call(cmd, shell=True)

    def start(self, config):
        ret = 1

        if self.task_type == 'sikuli':
            ret = self.run_sikuli(config.java_bin, config.sikuli_ide)
        elif self.task_type == 'script':
            ret = self.run_script(config.shell)
        elif self.task_type == 'bin':
            ret = self.run_bin()
        else:
            print("[ERROR] Task type is not supported")

        self.clean_executable()

        return ret
