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

def createTarg(s,targ):
	os.mkdir(s + targ +"-targ\\")
	return s + targ +"-targ\\"

def removeTree(s):
	shutil.rmtree(s)

def imscoreTest(image_dir, im_path, output_dir):
	command = "imscore_test.exe -s " + im_path + " -t " + output_dir + " -f10001"
	subprocess.call(command, shell=True, cwd = image_dir)

def createFolder(path, name):
	os.mkdir(path + name + "\\")
	return path + name + "\\"

def getFolderPaths(s):
	path = os.walk(s).next()
	currDir = path[0]
	folderNames = path[1]
	folderPaths = []
	for i in folderNames:
		folderPaths.append(currDir + i + "\\")

	return folderNames, folderPaths

def imscoreAll(input_file, output_dir, builds_path):
	builds = getFolderPaths(pathFormat(builds_path))
	buildNames = builds[0]
	buildPaths = builds[1]
	#print(buildNames)
	#print(buildPaths)

	l = len(buildNames)
	for i in range(l):
		bPath = buildPaths[i]
		bName = buildNames[i]

		outputPath = createFolder(pathFormat(output_dir),bName)

		imscoreTest(pathFormat(bPath),pathFormat(input_file),pathFormat(outputPath))

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
			cv2.imwrite(save_path + getFileName(im_path1), dif)

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

def getFileName(s):
	if (s[-1] == "/" or s[-1] == "\\"):
		s = s[:-1]
	i = 0
	while i < len(s):
		if s[i] == "/" or s[i] == "\\":
			s = s[i+1:]
			i = 0
		else:
			i+=1
	return s

def folderEmpty(path):
	if not len(os.listdir(path)):
		return True
	else:
		return False

def emptyFolderContents(path):
	for root, dirs, files in os.walk(pathFormat(path)):
	    for f in files:
	        os.unlink(os.path.join(root, f))
	    for d in dirs:
	        shutil.rmtree(os.path.join(root, d))

def regressionTest(input_file,output_dir,builds_path,target_build):
	emptyFolderContents(output_dir)
	targ = createTarg(pathFormat(output_dir),getFileName(target_build));
	imscoreTest(pathFormat(target_build),pathFormat(input_file),pathFormat(targ))
	imscoreAll(pathFormat(input_file), pathFormat(output_dir), pathFormat(builds_path))
	builds = getFolderPaths(pathFormat(builds_path))[0]
	for b in builds:
		if (compareFolders(pathFormat(targ), pathFormat(output_dir)+b+"\\")):
			removeTree(pathFormat(output_dir)+b+"\\")

def start(s):
	l = len(s)
	input_file = ""
	output_dir = ""
	builds_path = ""
	target_build = ""
	for i in range(l-1):
		if (s[i] == "-s"):
			input_file = s[i+1]
		elif (s[i] == "-t"):
			output_dir = s[i+1]
		elif (s[i] == "-b"):
			builds_path = s[i+1]
		elif (s[i] == "-c"):
			target_build = s[i+1]
	if (input_file == "" or output_dir == "" or builds_path == "" or target_build == ""):
		print("-s: source file")
		print("-t: output location")
		print("-b: builds location")
		print("-c: target build")
		print(input_file,output_dir,builds_path,target_build)
	else:
		regressionTest(input_file,output_dir,builds_path,target_build)





##TESTING
#print (pathFormatpath('C:/Users/zhangr/Desktop/OTXFilters/Test'))
#print (createTemp(pathFormat('C:/Users/zhangr/Desktop/OTXFilters/Test')))
#removeTemp(pathFormat('C:/Users/zhangr/Desktop/OTXFilters/Test/temp'))
#imscoreTest(pathFormat("C:/dv_builds/16.2.10.5620-64"), pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/input/I-AF-CU-009.docx"), pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/output"))
#print(createFolder(pathFormat("C://Users/zhangr/Desktop/OTXFilters/Test"),"asdf"))
#print(getFolderPaths(pathFormat("C:/dv_builds"))[0])
#print(getFolderPaths(pathFormat("C:/dv_builds"))[1])
#imscoreAll(pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/input/I-AF-CU-009.docx"),pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/output"),pathFormat("C:/dv_builds"))
#deleteFolders(pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/output"))
#compareareImage(pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/compare/a.png/"),pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/compare/b.png/"),pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/compare/d/"))
#print(compareFolders(pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/compare/a"),pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/compare/b")))
#print(getFileName("C:/Users/zhangr/Desktop/OTXFilters/Test/compare/a/"))
#print(folderEmpty(pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/compare/empty/")))
#regressionTest(pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/total/input"),pathFormat("C:/Users/zhangr/Desktop/OTXFilters/Test/total/output"),pathFormat("C:/dv_builds"),pathFormat("C:/dv_builds/16.2.10.5620-64"))


start(sys.argv)

