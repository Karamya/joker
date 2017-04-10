# @Author: Karthick <ramya>
# @Date:   2017-03-31T15:09:28+02:00
# @Last modified by:   ramya
# @Last modified time: 2017-04-03T15:20:03+02:00


import pandas as pd
import argparse
import csv


parser = argparse.ArgumentParser(description="Precleaning of the data file. Remove unwanted words")

parser.add_argument('--data', type=str, default="data/all_jokes.txt",
                    help="location of the data corpus")

parser.add_argument('--length', type=int, default=200,
                    help="length of the jokes, that you want to keep")

args = parser.parse_args()


###############################################################################

# Load data

###############################################################################


df = pd.read_csv(args.data, header= None, delimiter="\r\n")


###############################################################################

#  Drop duplicate jokes (assuming, it is an exact match)

###############################################################################

df.drop_duplicates(inplace=True)

###############################################################################

#  Drop bad words from the joke. Have to update the list, if something new shows up

###############################################################################
bad_words = ["fuck", "cunt", "pussy", "shit", "shitty"
			 "dick", "bitch", "bastard",
			 "fucker", "dickhead", "asshole",
			"fag", "slut", "whore"]

for word in bad_words:
    df = df[df[0].str.contains(word) == False]

### remove jokes containing links to somewhere else

df = df[df[0].str.contains("http") == False]

###############################################################################

# Extract only short jokes

###############################################################################

df_shortened = df[(df[0].str.len() <= args.length) & (df[0].str.len()>=30)] ### take jokes which are less than 200 chars long

df_shortened.to_csv(args.data[:-4] +"_shortened.txt", index = False, header = None,
                    quoting=csv.QUOTE_NONE, escapechar='§')
