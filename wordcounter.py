#!/usr/bin/python

# current release builds databases from which to compare and explore many documents
# future release will provide methods for doing this analysis  

import numpy as np
import sqlite3
from sys import argv

def wordCount(file_name,docid):
    try:
        lst = []
        # open file in read mode
        with open(file_name,'r') as f:
            # set up dictionary for word counts to be stored
            words = {}
            for line in f:
                # split words on the line for reading and counting
                linewords = line.split()
                # make all words lowercase to ensure duplicates are not created
                lowerwords = [x.lower() for x in linewords]
                for word in lowerwords:
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1

            # sort words in descending order
            final_words = sorted(words.items(), key=lambda x: x[1], reverse = True)
        # build word list to quickly add to database structure
        for point in final_words:
            lst.append((docid,point[0],point[1]))
        return lst
    
    # return error if user does not enter an available filename               
    except IOError as e:
        print "Error: Invalid filename entered"

def databaseCreate(dbname):
    conn = sqlite3.connect(str(dbname))
    c = conn.cursor()
    c.execute('''CREATE TABLE words (id INT, word TEXT, count INT)''')
    c.execute('''CREATE TABLE docs (id INT PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

def dbUpdate(dbname,lst,documentname,docid):
    conn = sqlite3.connect(str(dbname))
    c = conn.cursor()
    zz = (docid,str(documentname))
    c.execute("INSERT INTO docs VALUES (?,?)",zz)
    c.executemany("INSERT INTO words VALUES (?,?,?)", lst)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # determine if database has been constructed
    check = raw_input('Are you creating a new database? [0] no, [1] yes: ')
    if check == '1':
        dbname = raw_input('Enter name for new database (add .db extension): ')
        # build database for new document
        databaseCreate(dbname)
    else:
        dbname = raw_input('Enter database to update (add .db extension): ')

    # request data files
    val = 1
    while (val == 1):
        # obtain filename for the text document
        datafile = raw_input('Enter file name (with .txt ending): ')
        # obtain document identification number
        docid = raw_input('Enter document id: ')
        # run word counter
        lst = wordCount(datafile,docid)
        # fill database with document data
        dbUpdate(dbname,lst,datafile,docid)
        # ask for additional file
        val = raw_input('New file? [1] for yes, [0] for no: ')
