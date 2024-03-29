import pathlib
import os
import subprocess
import sys

# this is a help program to convert all files under "to_convert" to convert.
# if the directory has the subdirectories those will be converte
# use it at your own risk i did very minimal change
 
# assign directory
# ffmpeg -i source.avi -c copy -bsf:v mpeg4_unpack_bframes -vtag FMP4 source_fixed.avi

directory = 'to_convert'
tempfile = 'processed.avi'
 
# iterate over files in
# that directory
# if i get the offset errors add following flags  '-fflags' '+getnpts'
def doFile(filename):
    p = subprocess.Popen(['ffprobe', filename],stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    out, err = p.communicate()
    if b'XVID' in err or b'DX50' in err:
        print("TO PROCESS [%s]", filename)
        p = subprocess.Popen( ['ffmpeg', '-i', filename, '-c', 'copy', '-bsf:v', 'mpeg4_unpack_bframes', '-vtag', 'FMP4', tempfile])
        p.wait() 
        os.remove(filename) # some files you have to remove first before replacing them
        os.rename(tempfile, filename)

def doFolder(folder):
    files = pathlib.Path(folder).glob('*')
    for f in files:
        if (os.path.isdir(f)): # and f.name[0] != '.'):
            doFolder(os.path.join(folder, f.name))
        else :
            if (f.name.endswith(".avi")) :
                filename = "%s"%(os.path.join(folder,f.name)) 
                doFile(filename)
                #os.system( "ffmpeg -i %s -c copy -bsf:v mpeg4_unpack_bframes -vtag FMP4 %s"%(filename,tempfile))
                #os.system( "mv %s %s"%(tempfile,filename))

if len(sys.argv) != 2 :
    print("Usage: python3 process.py <foldername>")
else:
    doFolder(sys.argv[1])

print("done")

