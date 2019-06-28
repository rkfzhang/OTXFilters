import subprocess
import os
import shutil
import cv2
#import numpy as np

#print (dir_loc)


##subprocess.call('dir', shell=True, cwd = dir_loc)

testArr = []

##Doesnt do anything
def getSize(dir_loc):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_loc):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


##not used
def createFolders(builds_dir, output_dir): ##path must end with /
	inputFoldersNames = os.walk(builds_dir).next()[1]
	outputFoldersNames = os.walk(output_dir).next()[1]
	for x in outputFoldersNames:
		shutil.rmtree(output_dir + x)
	for x in inputFoldersNames:
		os.mkdir(output_dir + x +"-output")


##single images only
def compareImage(im_path1, im_path2):
	print (im_path1)
	im1 = cv2.imread(im_path1)
	im2 = cv2.imread(im_path2)
	if im1.shape == im2.shape:
		#print ("same size and channels")
		dif = cv2.subtract(im1,im2);
		b, g, r = cv2.split(dif)
		total = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
		if not total:

			print("the images are equal")
		else:
			cv2.namedWindow('difference',cv2.WINDOW_NORMAL)
			cv2.imshow("difference", dif)
			##cv2.namedWindow('im1',cv2.WINDOW_NORMAL)
			##cv2.namedWindow('im2',cv2.WINDOW_NORMAL)
			##cv2.imshow("im1", dif)
			##cv2.imshow("im2", dif)

			cv2.waitKey(0)
			cv2.destroyAllWindows()
			print("Images are different")
			testArr.append([im_path1,im_path2])
	else:
		testArr.append(im_path1)
		##print("Not matching files")	

##folders
def compareFolders(f_path1, f_path2): ##path must end with /
	inputFileNames = os.walk(f_path1).next()[2]
	##print os.walk(f_path1).next()[2]
	for x in inputFileNames:
		compareImage(f_path1 + x, f_path2 + x)
		##print("done")







##compareImage("Test/image_Test/v1.png","Test/image_Test/v2.png" )
##compareImage("Test/image_Test/v1.png","Test/image_Test/v3.png" )
##compareImage("Test/image_Test/v1.png","Test/image_Test/v4.png" )
##compareImage("Test/image_Test/v1.png","Test/image_Test/v5.png" )
##compareImage("Test/image_Test/v1.png","Test/image_Test/v6.png" )
##compareImage("Test/image_Test/v1.png","Test/image_Test/v7.png" )
##compareImage("Test/image_Test/v6.png","Test/image_Test/v7.png" )

compareFolders("Test/image_Test/before64/", "Test/image_Test/after64/")
print(testArr)

##print(getSize("Test/"))
##createFolders("Test/builds/", "Test/output/");

#def imscoreTest(image_dir, file_path):
	
