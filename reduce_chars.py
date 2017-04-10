# @Author: Karthick <ramya>
# @Date:   2017-04-03T11:38:02+02:00
# @Last modified by:   ramya
# @Last modified time: 2017-04-10T22:35:01+02:00



import glob
import unicodedata
import string
import re
import argparse


parser = argparse.ArgumentParser(description="Remove unwanted characters, and words")

parser.add_argument('--data', type=str, default="data/all_jokes_shortened.txt",
                    help="location of the data corpus")

args = parser.parse_args()



###############################################################################

# Permitted characters

###############################################################################

permitted_letters = string.ascii_letters + string.digits +" \"@&€%.,:'-()?/\n"


###############################################################################

# Convert certain characters and remove unwanted characters

###############################################################################

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.strip())
    s = re.sub(r"(['.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z[0-9]'.!?]+", r" ", s)
    return s

def preclean(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = normalizeString(line)
            line = line.replace("$", '€')
            line = line.replace("$", '€')
            line = line.replace("£", '€')
            line = line.replace("£", '€')
            line = line.replace("¢", '€')
            line = line.replace("“", '"')
            line = line.replace('”', '"')
            line = line.replace('”', '"')
            line = line.replace('’', "'")
            line = line.replace('´', "'")
            line = line.replace('`', "'")
            line = line.replace('_', "-")
            line = line.replace('[', "(")
            line = line.replace(']', ")")
            line = line.replace('{', "(")
            line = line.replace('}', ")")
            line = line.replace('<', "(")
            line = line.replace('>', ")")
            line = line.replace(';', ":")
            line = ''.join([i for i in line if i in permitted_letters])
            with open("reduced_char_jokes.txt", 'a') as outfile:
                outfile.write(str(line) + "\n")

preclean(args.data)
