#!/usr/bin/env python

from os import popen
from subprocess import call
from optparse import OptionParser
import time
from glob import glob

parser = OptionParser()
parser.add_option('--data', '-d', action='store_true',
                  default=False, dest='isData',
                  help='run on data or MC'
                  )
parser.add_option('--exe', '-e', action='store',
                  default='analyzer', dest='exe',
                  help='name of executable'
                  )
parser.add_option('--local', '-l', action='store_true',
                  default=False, dest='local',
                  help='running locally or not'
                  )
(options, args) = parser.parse_args()

if options.isData:
    path = "/store/user/tmitchel/smhet_22feb_SV/"
else:
    path = "/store/user/tmitchel/smhet_20march/"

start = time.time()
if options.local:
    if options.isData:
    	fileList = [ifile for ifile in glob('root_files/smhet_22feb_SV/*') if '.root' in ifile and 'Data' in ifile]
    else:
	    fileList = [ifile for ifile in glob('root_files/smhet_20march/*') if '.root' in ifile and not 'Data' in ifile]
    suffix = ' -l'
else:
    fileList = [ifile for ifile in filter(None, popen('xrdfs root://cmseos.fnal.gov/ ls '+path).read().split('\n'))]
    suffix = ''
print options.local, options.isData
for ifile in fileList:
    if not 'root' in ifile:
        continue
    if 'DY' in ifile:
        call('./'+options.exe+' '+ifile.split('/')[-1].split('.root')[0]+' ZTT'+suffix, shell=True)
        call('./'+options.exe+' '+ifile.split('/')[-1].split('.root')[0]+' ZL'+suffix, shell=True)
        call('./'+options.exe+' '+ifile.split('/')[-1].split('.root')[0]+' ZJ'+suffix, shell=True)
    elif 'TT' in ifile:
        call('./'+options.exe+' '+ifile.split('/')[-1].split('.root')[0]+' TT'+suffix, shell=True)
    elif 'W.root' in ifile or 'W1' in ifile or 'W2' in ifile or 'W3' in ifile or 'W4' in ifile:
        call('./'+options.exe+' '+ifile.split('/')[-1].split('.root')[0]+' W'+suffix, shell=True)
    else:
        call('./'+options.exe+' '+ifile.split('/')[-1].split('.root')[0]+' '+ifile.split('/')[-1].split('.root')[0]+suffix, shell=True)
end = time.time()
print 'Processing completed in', end-start, 'seconds.'
