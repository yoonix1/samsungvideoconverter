import pathlib
import os

# this is a help program to convert all files under "to_convert" to convert.
# if the directory has the subdirectories those will be converte
# use it at your own risk i did very minimal change
 
# assign directory
# ffmpeg -i source.avi -c copy -bsf:v mpeg4_unpack_bframes -vtag FMP4 source_fixed.avi

directory = 'to_convert'
tempfile = 'processed.avi'
 
# iterate over files in
# that directory

def doFolder(folder):
    files = pathlib.Path(folder).glob('*')
    for f in files:
        if (os.path.isdir(f)): # and f.name[0] != '.'):
            doFolder(os.path.join(folder, f.name))
        else :
            if (f.name.endswith(".avi")) :
                filename = "%s"%(os.path.join(folder,f.name)) 
                print("processing %s"%filename)
                os.system( "ffmpeg -i %s -c copy -bsf:v mpeg4_unpack_bframes -vtag FMP4 %s"%(filename,tempfile))
                os.system( "mv %s %s"%(tempfile,filename))

doFolder(directory)

print("done")

