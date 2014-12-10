#!/usr/bin/env python

import os
import sys
import cmd
import plist
from imobiledevice import *

debug_printf = lambda msg: sys.stdout.write(msg)

def lockdown_get_service_client(service_class):
	ld = LockdownClient(iDevice())
	return ld.get_service_client(service_class)

class CommandShell(cmd.Cmd):
	afc = None
	_path = None
	_dirs = []

	def __init__(self, root=True):
		cmd.Cmd.__init__(self)
		if root:
			self.afc = lockdown_get_service_client(Afc2Client)
		else:
			self.afc = lockdown_get_service_client(AfcClient)

		self._set_path("/")
		self._dirs = self.afc.read_directory("/")

	def _set_path(self, path):
		if (path[-1] == '/'):
			self._path = path[:-1]
		else:
			self._path = path

		if self._path:
			self.prompt = "afc:%s # " % self._path
		else:
			self.prompt = "afc:/ # "

	def _relative_path(self, line):
		if line.strip() == '':
			new_path = self._path
		elif line == "..":
			new_path = os.path.dirname(self._path)
		elif line[0] == '/':
			new_path = line
		else:
			new_path = "%s/%s" % (self._path, line)
		return new_path

	def _complete_dir(self, text, line, start_index, end_index):
		if text:
			return [tmp_dir for tmp_dir in self._dirs if tmp_dir.startswith(text)]
		else:
			return tmp_dir

	def do_pwd(self, line):
		"""pwd: return working directory name\n"""
		debug_printf("%s\n" % self._path)

	def do_cd(self, line):
		new_path = self._relative_path(line)
		try:
			self.afc.get_file_info(new_path)
			self._set_path(new_path)
			self._dirs = self.afc.read_directory(new_path)
		except AfcError, e:
			debug_printf("cd %s: %s\n" % (new_path, e))
	complete_cd = _complete_dir

	def do_ls(self, line):
		new_path = self._relative_path(line)
		try:
			self._dirs = self.afc.read_directory(new_path)
			for tmp_dir in self._dirs:
				if (tmp_dir == ".") or (tmp_dir == ".."):
					continue
				debug_printf("%s\n" % tmp_dir)
		except AfcError, e:
			debug_printf("ls %s: %s\n" % (new_path, e))
	complete_ls = _complete_dir

	def do_mkdir(self, line):
		"""mkdir <path>: make directories\n"""
		new_path = self._relative_path(line)
		try:
			self.afc.make_directory(new_path)
		except AfcError, e:
			debug_printf("%s\n" % e)

	def do_rm(self, line):
		"""rm <path>: remove files or directories\n"""
		new_path = self._relative_path(line)
		try:
			self.afc.remove_path(new_path)
		except AfcError, e:
			debug_printf("%s\n" % e)

	def do_rename(self, line):
		"""rename <from> <to>: change the name of a file\n"""
		f_from, f_to = line.split(" ")[:2]
		new_from = self._relative_path(f_from)
		new_to = self._relative_path(f_to)
		try:
			self.afc.rename_path(new_from, new_to)
		except AfcError, e:
			debug_printf("%s\n" % e)
	do_rn = do_rename

	def do_sz(self, line):
		"""sz <remote> <local>\n"""
		f_remote, f_local = line.split(" ")[:2]
		new_remote = self._relative_path(f_remote)
		try:
			with self.afc.open(new_remote, mode="r") as rfile:
				rfile.seek(0, 2)	# SEEK_END(2)
				rfile_size = rfile.tell()

				rfile.seek(0, 0)	# SEEK_SET(0)

				local_file = open(f_local, "w+")
				local_file.write(rfile.read(rfile_size))
				local_file.close()

				debug_printf("Write %d bytes to %s.\n" % (rfile_size, f_local))

		except AfcError, e:
			debug_printf("%s\n" % e)
	complete_sz = _complete_dir

	def do_rz(self, line):
		"""rz <local> <remote>\n"""
		f_local, f_remote = line.split(" ")[:2]
		new_remote = self._relative_path(f_remote)
		try:
			with self.afc.open(new_remote, mode="w+") as rfile:
				local_file = open(f_local, "r")
				rfile.write(local_file.read())
				local_file.close()

			debug_printf("Upload to %s success.\n" % (new_remote))

		except AfcError, e:
			debug_printf("%s\n" % e)
	complete_rz = _complete_dir

	def do_cat(self, line):
		"""cat: concatenate and print files"""
		new_path = self._relative_path(line)
		try:
			with self.afc.open(new_path, mode="r") as rfile:
				rfile.seek(0, 2)	# SEEK_END(2)
				rfile_size = rfile.tell()

				rfile.seek(0, 0)	# SEEK_SET(0)
				debug_printf("%s\n" % rfile.read(rfile_size))

		except AfcError, e:
			debug_printf("%s\n" % e)
	complete_cat = _complete_dir

	def do_exit(self, line):
		return True
	do_quit = do_exit
	do_q = do_quit

def main():
	shell = CommandShell()
	shell.cmdloop()

if __name__ == '__main__':
	main()
