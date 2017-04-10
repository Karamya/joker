# @Author: Karthick <ramya>
# @Date:   2017-03-31T16:13:23+02:00
# @Last modified by:   ramya
# @Last modified time: 2017-03-31T16:55:38+02:00


import glob

with open("all_jokes.txt", 'wb') as outfile:
    for f in glob.glob("*.txt"):
        if f == "abhinav_moudgil.txt":
            continue
        with open(f, 'rb') as infile:
            outfile.write(infile.read())
