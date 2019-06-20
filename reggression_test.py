import subprocess
import os
import shutil

#print (dir_loc)


##subprocess.call('dir', shell=True, cwd = dir_loc)

def getSize(dir_loc):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_loc):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

#def createFolder(dir_loc, name):




def createFolders(builds_dir, output_dir):
	inputFoldersNames = os.walk(builds_dir).next()[1]
	outputFoldersNames = os.walk(output_dir).next()[1]
	for x in outputFoldersNames:
		shutil.rmtree(output_dir + x)
	for x in inputFoldersNames:
		os.mkdir(output_dir + x +"-output")



print(getSize("Test/"))
createFolders("Test/builds/", "Test/output/");
