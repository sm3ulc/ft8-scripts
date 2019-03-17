#
# Script to split stream from stdin into files with x seconds of data 
# 

import datetime
import getopt
import sys
import time

verbose = False
nametag = ''

print("ARGV:", sys.argv[1:])
options, remainder = getopt.getopt(sys.argv[1:], 't:v', ['output=', 'verbose',])

for opt, arg in options:
    if opt in ('-t', '--tag'):
        nametag = arg
    elif opt in ('-v', '--verbose'):
        verbose = True

blocktime = 15
blocktimeoffset = datetime.timedelta(milliseconds=200)
samplerate = 12000
chunksize = 32768


block = bytearray(0)
time1 = int(int(datetime.datetime.now().strftime('%s')) / blocktime) * blocktime
starttime = datetime.datetime.fromtimestamp(time1)
endtime = datetime.datetime.fromtimestamp(time1+15)
print(starttime, endtime)

first=True

while True:
    data = sys.stdin.buffer.read(chunksize)
    block.extend(data)

    if datetime.datetime.now() > endtime:
        print("Buffersize", len(block))
        fname = "/ramdrive/file-"+nametag+"-"+starttime.strftime("%H%M%S")+".iq"

        if not first:
            print("Writing: ",fname)
            iq = open(fname, "wb")
            iq.write(block)
            iq.close()
        else:
            print("Unfilled block. Ditching data")
            first=False
            
        time1 = int(int(datetime.datetime.now().strftime('%s')) / blocktime) * blocktime
        starttime = datetime.datetime.fromtimestamp(time1)
        endtime = datetime.datetime.fromtimestamp(time1+15)
        block = bytearray(0)        
