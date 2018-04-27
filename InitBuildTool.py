import sublime, sublime_plugin
import os
import shutil
import time

class InitBuildToolCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.setting = sublime.load_settings("InitBuildTool.sublime-settings")
		workflowFiles = self.setting.get('useFiles')
		folders = [];
		if self.window.folders():
			folder = self.window.folders();
			for path in self.window.folders():
				folders.append(path.split('\\')[-1])
		else:
			sublime.message_dialog("請先建立project並且加入folder")
		# print(folder)

		def on_done(index):
			if index == -1: return
			select = folder[index]
			# print(select)
			exist = []
			overwrite = 'none' # none all file system
			for file in workflowFiles:
				result = os.path.exists(os.path.abspath(os.path.join(select, file)))
				exist.append(result)

			if os.path.exists(self.window.project_file_name()):
				with open (self.window.project_file_name(), 'r+', encoding='utf8') as project:
					projectData = project.readlines()
					exist.append('\t"build_systems":\n' in projectData)
			else:
				sublime.message_dialog("請先建立project\nProject -> Save Project As...")
			
			if True in exist:
				while exist.count(True) == len(exist):
					if sublime.yes_no_cancel_dialog('build tool 已建立\n是否要更新為最新版本', '全部更新', '指定更新') == sublime.DIALOG_NO:
						if sublime.yes_no_cancel_dialog('請選擇要更新的項目', '更新 task 及 package.json', '更新 build system') == sublime.DIALOG_YES:
							overwrite = 'file'
						elif sublime.DIALOG_NO:
							overwrite = 'system'
						elif sublime.DIALOG_CANCEL:
							return None
					elif sublime.DIALOG_YES:
						overwrite = 'all'
					elif sublime.DIALOG_CANCEL:
						 return None
					break
				while overwrite == 'none' and exist.index(True) < len(exist) - 1:
					print("bb");
					if not sublime.ok_cancel_dialog('task 和 package 已建立\n是否需要更新為最新版本', '更新'):
						print("aa");
						overwrite = 'system'
					break
				while overwrite == 'none' and exist.index(True) == len(exist) - 1:
					if not sublime.ok_cancel_dialog('build system 已建立\n是否需要更新為最新版本', '更新'):
						overwrite = 'file'
					break	

			print('overwrite '+ overwrite)
			copyFiles(select, copied, overwrite)
		self.window.show_quick_panel(folders, on_done)

		def copied(overwrite):
			workflowPath = self.setting.get('workflowPackagePath')
			buildSystem = self.setting.get('buildSystem')
			if overwrite == 'file':
				print('成功複製檔案')
				sublime.message_dialog('成功複製檔案')
				return
			print('成功複製檔案，偵測是否有 build system')
			file = os.path.abspath(os.path.join(workflowPath, buildSystem))
			with open (self.window.project_file_name(), 'r+', encoding='utf8') as project:
				projectData = project.readlines()
				if (overwrite == 'system' or 'all') and '\t"build_systems":\n' in projectData:
					newProjectData = ['{\n']
					breakLine = projectData.index('\t],\n') + 1
					dataLine = len(projectData)
					for line in range(breakLine, dataLine):
						newProjectData.append(projectData[line])
					projectData = newProjectData
					# print(projectData)
				with open (file, 'r') as txt:
					# print(projectData)
					txtData = txt.readlines()
					dataLine = len(txtData)
					for line in range(0, dataLine):
						projectData.insert(line + 1,txtData[line])
					# print(projectData)
					project.seek(0, 0)
					project.truncate(0)
					project.writelines(projectData)				
					self.window.open_file(self.window.project_file_name())
					sublime.message_dialog('成功建立環境')

		def getSize(path):
			folderSize = 0
			if os.path.isdir(path):
				for (path, dirs, files) in os.walk(path):
					for file in files:
						filename = os.path.abspath(os.path.join(path, file))
						folderSize += os.path.getsize(filename)
					size = folderSize
					# print(forder_size)
			else:
				fileSize = os.path.getsize(path)
				size = fileSize
				# print(fileSize)
			return size

		def copyFiles(destFolder, copied, overwrite):
			workflowPath = self.setting.get('workflowPackagePath')
			workflowFiles = self.setting.get('useFiles')
			if overwrite == "system":
				copied(overwrite)
				return
			for file in workflowFiles:
				srcPath = os.path.abspath(os.path.join(workflowPath, file))
				destPath = os.path.abspath(os.path.join(destFolder, file))
				srcSize = getSize(srcPath)
				# print(srcSize, file)
				if overwrite == 'file' or 'all':
					if os.path.isdir(destPath):
						shutil.rmtree(destPath)
				if os.path.isdir(srcPath):
					shutil.copytree(srcPath, destPath)
				else:
					if file == 'package.json' and os.path.isfile(destPath):
						packageItems = self.setting.get('packageData');
						with open (destPath, 'r+', encoding='utf8') as itPackage:
							itPackageData = itPackage.readlines()
							itPackageLine = len(itPackageData)
							itPackageBreakLine = {}
							
							if "Isobar" in itPackage:
								for i, val in enumerate(itPackageData):
									rangeLine = []
									if (val.endswith(': {\n') or val.endswith(':{\n')) and val.split('"')[1] in packageItems:
										if val.count(packageItems[0]):
											itPackageBreakLine[val.split('"')[1]] = i
										else:
											itPackageBreakLine[val.split('"')[1]] = i+1
								itPackageBreakLine['none'] = itPackageBreakLine[list(itPackageBreakLine)[0]] - 2;

								with open (srcPath, 'r') as f2ePackage:
									f2ePackageData = f2ePackage.readlines()
									insertData = {}
									f2ePackageBreakLine = []

									for i, val in enumerate(f2ePackageData):
										if (val.endswith(': {\n') or val.endswith(':{\n')) and val.split('"')[1] in packageItems:
											rangeLine = []
											dataDict = {}
											dataDict['title'] = val.split('"')[1]
											if val.count(packageItems[0]):
												rangeLine.append(i)
											else:
												rangeLine.append(i+1)
										elif val.count('},') > 0 and len(rangeLine) < 2:
											rangeLine.append(i)
											dataDict['range'] = rangeLine
											f2ePackageBreakLine.append(dataDict)

									for i, val in enumerate(f2ePackageBreakLine):
										value = []
										for line in range(val['range'][0], val['range'][1]):
											value.append(f2ePackageData[line])
											# if line+1 == val['range'][1] and f2ePackageData[line].count('},') == 0:
											# 	value.append(f2ePackageData[line][:-1] + ',\n')
											# else:
										insertData[val['title']] = value
								# print(insertData)
								# print(itPackageBreakLine)	
								lineDefault = 0;		
								for val in packageItems:
									for txt in list(itPackageBreakLine):
										if val == txt:
											insertData[val][-1] = insertData[val][-1][:-1] + ',\n'
											line = itPackageBreakLine[val]
											if line > lineDefault:
												line = line + lineDefault
											lineDefault = lineDefault + len(insertData[val]);
											# print(itPackageBreakLine, val, line, lineDefault);
											for insertLine in range(0, len(insertData[val])):
												itPackageData.insert(line, insertData[val][insertLine])
												line = line+1
										elif val != txt and insertData[val][0].count('{') > 0:
											if  insertData[val][-1].count('}') == 0:
												insertData[val].append('\t},\n')
												line = itPackageBreakLine['none'] + lineDefault + 1
												lineDefault = lineDefault + len(insertData[val]);
												for insertLine in range(0, len(insertData[val])):
													itPackageData.insert(line, insertData[val][insertLine])
													line = line+1
								# print(itPackageData)
								itPackage.seek(0, 0)
								itPackage.truncate(0)
								itPackage.writelines(itPackageData)
								self.window.open_file(destPath)
							else:
								shutil.copy(srcPath, destPath)
					else:
						shutil.copy(srcPath, destPath)
				destSize = getSize(destPath)
				# print(srcSize, destSize)
				if srcSize == destSize:
					# print(workflowFiles.index(file), file, len(workflowFiles))
					if workflowFiles.index(file) + 1 ==  len(workflowFiles):
						copied(overwrite)
					else:
						continue
				else:
					time.sleep(3)