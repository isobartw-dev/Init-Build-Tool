import sublime, sublime_plugin
import os
import shutil

setting = sublime.load_settings("InitBuildTool.sublime-settings")
workflow_path = setting.get('workflow_package_path')
workflow_files = setting.get('use_files')

class InitBuildToolCommand(sublime_plugin.WindowCommand):
	def run(self):
		# print(folder)
		if self.window.folders():
			folder = self.window.folders()
		else:
			folder = "請先建立project"

		def on_done(index):
			if index == -1: return
			select = folder[index]
			# print(select)
			copy_files(select)
			 
		self.window.show_quick_panel(folder, on_done)

		# def build():
		# 	print('build')

		def copy_files(dest_folder):
			for file in workflow_files:
				src_path = os.path.abspath(os.path.join(workflow_path, file))
				dest_path = os.path.abspath(os.path.join(dest_folder, file))
				# print (src_path, dest_path)
				if os.path.isdir(src_path):
					shutil.copytree(src_path, dest_path)
				else:
					shutil.copy(src_path, dest_path)
			# return build()

		
				
				