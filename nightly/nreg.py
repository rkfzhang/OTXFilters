import os
import shutil
import subprocess
import cv2
import sys

def pathFormat(s):
	s = list(s)
	if (s[-1] != "/" and s[-1] != "\\"):
		s.append("/")

	length = len(s)
	for i in range(length):
		if s[i] == '/':
			s[i] = '\\'

	return "".join(s)

def getInput():
	file = open("config.txt", "r")
	with file as f:
		flist = f.read().splitlines()
	file_paths = []
	build_paths = []
	build = True
	for i in flist:
		if (i =="[Builds]"):
			continue
		if (i =='[Files]'):
			build = False
		elif build:
			build_paths.append(i.split('\t'))
		else:
			file_paths.append(i)

	return build_paths,file_paths



def getFilePaths(s):
	path = os.walk(s).next()
	currDir = path[0]
	folderNames = path[2]
	folderPaths = []
	for i in folderNames:
		folderPaths.append(currDir + i + "\\")

	return folderNames, folderPaths


def createFiles(build_paths):
	output_files = []
	for i in build_paths:
		name = "Output\\" + getName(i[0]) + "-" + getName(i[1]) + ".txt"
		f = open(name,"w+")
		f.close()
		output_files.append(name)
	return output_files

def write(file,text):
	f = open(file, "a+")
	f.write("[" + text[0] + "]\n")
	for i in range(1,len(text)):
		f.write(text[i] + "\n")
	f.write("\n")
	f.close()

def getName(build_path):
	names = pathFormat(build_path).split("\\")
	return names[-2]




def imscoreTest(image_dir, im_path, output_dir):
	command = "imscore_test.exe -s " + im_path + " -t " + output_dir + " -f10001"
	subprocess.call(command, shell=True, cwd = image_dir)


def createFolder(path, name):
	os.mkdir(path + name + "\\")
	return path + name + "\\"

def removeTree(s):
	shutil.rmtree(s)

def compareImage(im_path1, im_path2, save_path):
	if (im_path1[-1] == "/" or im_path1[-1] == "\\"):
		im_path1 = im_path1[:-1]
	if (im_path2[-1] == "/" or im_path2[-1] == "\\"):
		im_path2 = im_path2[:-1]

	im1 = cv2.imread(im_path1)
	im2 = cv2.imread(im_path2)

	if im1.shape == im2.shape:
		dif = cv2.subtract(im1,im2);
		b, g, r = cv2.split(dif)
		total = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)

		if total:
			cv2.imwrite(save_path + getName(im_path1), dif)

def folderEmpty(path):
	if not len(os.listdir(path)):
		return True
	else:
		return False

def compareFolders(f_path1, f_path2): 
	fileNames1 = os.walk(f_path1).next()[2]
	fileNames2 = os.walk(f_path2).next()[2]
	save_path = createFolder(pathFormat(f_path2), "diff")
	if len(fileNames1) != len(fileNames2):
		return False
	for x in fileNames1:
		compareImage(f_path1 + x, f_path2 + x, save_path)
	if folderEmpty(save_path):
		return True
	else:
		return False

def checkFolder(build_path1,build_path2,folder,current):
	fileNames, filePaths = getFilePaths(pathFormat(folder))
	l = len(fileNames)
	files = [getName(folder)]
	temp = createFolder(current + "Output\\","temp")
	for i in range(l):
		t1 = createFolder(current + "Output\\","t1")
		t2 = createFolder(current + "Output\\","t2")
		os.rename(pathFormat(filePaths[i])[:-1], pathFormat(temp + fileNames[i]))
		imscoreTest(pathFormat(build_path1),pathFormat(temp),pathFormat(t1))
		imscoreTest(pathFormat(build_path2),pathFormat(temp),pathFormat(t2))
		os.rename(pathFormat(temp + fileNames[i])[:-1], pathFormat(filePaths[i]))
		if not compareFolders(t1,t2):
			files.append(fileNames[i])
		removeTree(t1)
		removeTree(t2)
	removeTree(temp)
	return files

def emptyFolderContents(path):
	for root, dirs, files in os.walk(pathFormat(path)):
	    for f in files:
	        os.unlink(os.path.join(root, f))
	    for d in dirs:
	        shutil.rmtree(os.path.join(root, d))


def nreg():
	current = os.getcwd()
	emptyFolderContents(pathFormat(current) + "Output")
	build_paths,file_paths = getInput()
	output_files = createFiles(build_paths)
	current = os.getcwd()
	l = len(build_paths)
	for i in range(l):
		for p in file_paths:
			print(p)
			files = checkFolder(pathFormat(build_paths[i][0]),pathFormat(build_paths[i][1]),pathFormat(p),pathFormat(current))
			write(output_files[i],files)
			#print(build_paths[i])
			#



nreg()
#print(getInput())
#print(getFilePaths(pathFormat("C:/imscore_testing/folders/Word2016")[-1]))