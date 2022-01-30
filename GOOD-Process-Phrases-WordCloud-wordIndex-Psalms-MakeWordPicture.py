# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 09:16:36 2021

@author: codew
"""



import os
import re
import collections

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

import json

from OT19PsalmsText import *

titleList = [
#    'Leviticus000',
#    'Psalm001','Psalm002','Psalm003','Psalm004','Psalm005',
#    'Psalm006','Psalm007','Psalm008','Psalm009','Psalm010',
#    'Psalm011','Psalm012','Psalm013','Psalm014','Psalm015',
#    'Psalm016','Psalm017','Psalm018','Psalm019','Psalm020',
#    'Psalm021','Psalm022','Psalm023','Psalm024','Psalm025',
#    'Psalm026','Psalm027','Psalm028','Psalm029','Psalm030',
#    'Psalm031','Psalm032','Psalm033','Psalm034','Psalm035',
#    'Psalm036','Psalm037','Psalm038','Psalm039','Psalm040',
 #   'Psalm041','Psalm042','Psalm043','Psalm044','Psalm045',
#    'Psalm046','Psalm047','Psalm048','Psalm049','Psalm050',
#    'Psalm051','Psalm052','Psalm053','Psalm054','Psalm055',
#    'Psalm056','Psalm057','Psalm058','Psalm059','Psalm060',
#   'Psalm061','Psalm062','Psalm063','Psalm064','Psalm065',
#    'Psalm066','Psalm067','Psalm068','Psalm069','Psalm070',
#    'Psalm071','Psalm072','Psalm073','Psalm074','Psalm075',
#    'Psalm076','Psalm077','Psalm078','Psalm079','Psalm080',
#    'Psalm081','Psalm082','Psalm083','Psalm084','Psalm085',
#    'Psalm086','Psalm087','Psalm088','Psalm089','Psalm090',
#    'Psalm091','Psalm092','Psalm093','Psalm094','Psalm095',
#    'Psalm096','Psalm097','Psalm098','Psalm099','Psalm100',
    'Psalm101','Psalm102','Psalm103','Psalm104','Psalm105',
    'Psalm106','Psalm107','Psalm108','Psalm109','Psalm010',
#    'Psalm111','Psalm112','Psalm113','Psalm114','Psalm115',
#    'Psalm116','Psalm117','Psalm118','Psalm119','Psalm120',
#    'Psalm121', 'Psalm122','Psalm123','Psalm124','Psalm125',
#    'Psalm126','Psalm127','Psalm128','Psalm129','Psalm130',
#    'Psalm131', 'Psalm132','Psalm133','Psalm134','Psalm135',
#    'Psalm136','Psalm137','Psalm138','Psalm139','Psalm140',
#    'Psalm141','Psalm142','Psalm143','Psalm144','Psalm145',
#    'Psalm146','Psalm147','Psalm148','Psalm149','Psalm150',
]


fileType = [
    'Comments','MyOutlines','OutlinesFromOthers','Statistics',
    'TextExtrasWitHighlights','WordIndex', 'RepeatedPhrases', 
    'WordCloud', 'sql', 
    
]

originalverseStatHeader = ["\\subsection{Chapter Word Statistics}",
                  "\n",
                  "%%%%%%%%%%",
                  "%%%%%%%%%%",
                  "\\normalsize",
                  " ",
                  "\\begin{center}",
                  "\\begin{longtable}{l|c|c|c|c}",
                  "Placeholder",
                  "\\hline \multicolumn{1}{|c|}{\\textbf{Verse(s)}} & \multicolumn{1}{|c|}{\\textbf{Count}} & \multicolumn{1}{|c|}{\\textbf{Unique}} & \multicolumn{1}{|c|}{\\textbf{Italics}} & \multicolumn{1}{|c|}{\\textbf{Uniq Italic}}  \\\ \\hline ",
                  "\\endfirsthead",
                  " ",
                  "\multicolumn{5}{c}",
                  "{{\\bfseries \\tablename\ \\thetable{} -- continued from previous page}} \\\  ",
                  "\\hline \multicolumn{1}{|c|}{\\textbf{Verse(s)}} & \multicolumn{1}{|c|}{\\textbf{Count}} & \multicolumn{1}{|c|}{\\textbf{Unique}} & \multicolumn{1}{|c|}{\\textbf{Italics}} & \multicolumn{1}{|c|}{\\textbf{Uniq Italic}}  \\\ \\hline ",
                  "\\endhead",
                  " ",
                  "\\hline \\multicolumn{5}{|r|}{{Continued if needed}} \\\ \\hline",
                  "\\endfoot ",
                  ]

verseStatHeader = ["\\subsection{Chapter Word Statistics}",
                  "\n",
                  "%%%%%%%%%%",
                  "%%%%%%%%%%",
                  "\\normalsize",
                  " ",
                  "\\begin{center}",
                  "\\begin{longtable}{l|c|c|c|c}",
                  "Placeholder",
                  "\\hline \multicolumn{1}{|c|}{\\textbf{Verse(s)}} & \multicolumn{1}{|c|}{\\textbf{Count}} & \multicolumn{1}{|c|}{\\textbf{Unique}} & \multicolumn{1}{|c|}{\\textbf{Italics}} & \multicolumn{1}{|c|}{\\textbf{Uniq Italic}}  \\\ \\hline ",
                  "\\endfirsthead",
                  " ",
                  "\multicolumn{5}{c}",
                  "{{\\bfseries \\tablename\ \\thetable{} -- continued from previous page}} \\\  ",
                  "\\hline \multicolumn{1}{|c|}{\\textbf{Verse(s)}} & \multicolumn{1}{|c|}{\\textbf{Count}} & \multicolumn{1}{|c|}{\\textbf{Unique}} & \multicolumn{1}{|c|}{\\textbf{Italics}} & \multicolumn{1}{|c|}{\\textbf{Uniq Italic}}  \\\ \\hline ",
                  "\\endhead",
                  " ",
                  "\\hline \\multicolumn{5}{|r|}{{Continued if needed}} \\\ \\hline",
                  "\\endfoot ",
                  ]

verseStatTrailer =  ["\\end{longtable}",
                     "\\end{center}",
                     "\n\n",
                     "%%%%%%%%%%",
                     "%%%%%%%%%%"
                     "\n\n",
                     ]


def createBaseFileName(baseName,fileType):

    '''
    baseName = string, e.g. SecondSamuel000
    fileType = string, choices: 'Comments','WordIndex',
   'RepeatedPhrases', 'Statistics', etc

    returns:    filenames 
                label string
    '''

    #print(baseName,fileType)
    
    splitString = re.split('(\d+)',baseName)
    letterPart = splitString[0]
    numberPart = splitString[1]
    
    if letterPart == "FirstSamuel":
        letterPart = "1Samuel"
    if letterPart == "SecondSamuel":
        letterPart = "2Samuel"
    if letterPart == "FirstKings":
        letterPart = "1Kings"
    if letterPart == "SecondKings":
        letterPart = "2Kings"
    if letterPart == "FirstChronicles":
        letterPart = "1Chronicles"
    if letterPart == "SecondChronicles":
        letterPart = "2Chronicles"
    if letterPart == "FirstThessalonians":
        letterPart = "1Thessalonians"
    if letterPart == "SecondThessalonians":
        letterPart = "2Thessalonians"
    if letterPart == "FirstTimothy":
        letterPart = "1Timothy"
    if letterPart == "SecondTimothy":
        letterPart = "2Timothy"
    if letterPart == "FirstPeter":
        letterPart = "1Peter"
    if letterPart == "SecondPeter":
        letterPart = "2Peter"
    if letterPart == "FirstJohn":
        letterPart = "1John"
    if letterPart == "SecondJohn":
        letterPart = "2John"
    if letterPart == "ThirdJohn":
        letterPart = "3John"

    # if numberPart == '000' then we have a list with entire book
    # so use letterPart as basefilename
    
    if numberPart == '000':
        basefilename = letterPart
        labelString = basefilename
        #print("basefilename is:",basefilename)
    # else, must process away leading zeroe, etc
    else:
        numberPart = str(int(numberPart))
        basefilename = letterPart + numberPart 
        labelString = letterPart + ' ' + numberPart 
        #print("basefilename is:",basefilename)
    
    if fileType == 'sql':
        basefilename = labelString + '-' + fileType+'.db'    
    if fileType == 'Comments':
        basefilename = basefilename + '-' + fileType+'.tex'    
    if fileType == 'MyOutlines':
        basefilename = basefilename + '-' + fileType+'.tex'    
    if fileType == 'OutlinesFromOthers':
        basefilename = basefilename + '-' + fileType+'.tex'    
    if fileType == 'Statistics':
        basefilename = basefilename + '-' + fileType+'.tex'    
    if fileType == 'TextExtrasWitHighlights':
        basefilename = basefilename + '-' + fileType+'.tex'    
    if fileType == 'WordIndex':
        basefilename = basefilename + '-' + fileType+'.tex'    
    if fileType == 'RepeatedPhrases':
        basefilename = labelString + '-' + fileType + '.tex'    
    if fileType == 'WordCloud':
        basefilename = labelString + '-' + fileType+'.jpg'    

    return(basefilename,labelString)

def makeWordPicture(outputFileName,source):
    outputFileName = outputFileName.replace(' ','')
    outputFileName = outputFileName.replace('000','')
    comment_words = ''
    stopwords = set(STOPWORDS)
    stopwords = ['The', 'the', 'of', '\emph'] + list(STOPWORDS)

    df = pd.DataFrame(source,columns =['Book', 'BookAbbr', 'ChapNo', 'VerseNoA', 'VerseNoB', 'text'])
    rowcount = len(df['text'])
    count = 0
    # The folowwing 6 lines get rid of \emph{} to build the word cloud
    while count < rowcount:
        sentence = df['text'][count]
        sentence = sentence.replace('\emph{','')
        sentence = sentence.replace('}','')
        df['text'][count] = sentence
        count +=1
    data = df['text'].value_counts().to_dict()
    
                
    facecolor = 'white'
    wordcloud = WordCloud(width = 1200, height = 750, 
            background_color ='white', 
            stopwords = stopwords, 
            min_font_size = 10).generate(str(data))

    plt.figure(figsize=(15,10), facecolor=facecolor)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad=1)

    plt.savefig(outputFileName, facecolor=facecolor)
    new = outputFileName.replace('jpg','png')
    plt.savefig(outputFileName, facecolor=facecolor)
    new = outputFileName.replace('png','svg')
    plt.savefig(outputFileName, facecolor=facecolor)
  
def makeCommentFile(filepath,text):
    filepath = filepath.replace(' ','')
    filepath = filepath.replace('000','')
    if os.path.exists(filepath):
        print("\tFile",filepath,"exists -- will not overwite")
    else:
        dstring = "\\section{"+ text +' '+"Comments}\n\n\n\n"
        outfile = open(filepath,"w")
        outfile.write(dstring)
        outfile.close()
  
def phraseProcessor(filepath,source):
    filepath = filepath.replace(' ','')
    filepath = filepath.replace('000','')
    print('\t***** Inside phraseProcessor\n\t',filepath)
    SHORTESTLENGTH = 2
    LONGESTLENGTH = 25
    MINFREQUENCY = 3
    MAXFREQUENCY = 100
    print("\t******************* finding phrases of length >",SHORTESTLENGTH,"and <=",LONGESTLENGTH)
    print("\t******************* finding phrases\n")

    ####
    phraseDictionary = {}

    toBereplaced = [",",".","?",":",";","!"]
    for item in source:
        ''' remove punctuation marks
        '''
        for target in toBereplaced:
            item[5] = item[5].replace(target,"")

        startingLine = item[5].split()


        ''' generate all sequences
        '''
        allwords = []
        for begin in range(len(startingLine)):
            for length in range(1,len(startingLine) - begin+1):
                allwords.append(startingLine[begin:begin+length])

        for item in allwords:
            phrase = " ".join(item)
            if phrase not in phraseDictionary:
                if (len(phrase.split()) >= SHORTESTLENGTH) and (len(phrase.split()) <= LONGESTLENGTH):
                    phraseDictionary[phrase] = 1
            else:
                 if (len(phrase.split()) >= SHORTESTLENGTH) and (len(phrase.split()) <= LONGESTLENGTH):
                    phraseDictionary[phrase] = phraseDictionary[phrase] + 1

    sortedPhrases = sorted(phraseDictionary.items(),key=lambda x: x[1], reverse = True)

    for item in sortedPhrases:
        if (item[1] >= MINFREQUENCY) and (item[1] <= MAXFREQUENCY):
            print (item)

    filepath = filepath.replace(' ','')
    jsonFilePath = filepath.replace('tex','json')
    print(jsonFilePath)
    
    jsonString = json.dumps(sortedPhrases)
    if os.path.exists(jsonFilePath):
        pass
    else:
        jsonFile= open(jsonFilePath,"w")
        jsonFile.write(jsonString)
        jsonFile.close()
        
    name = filepath.replace('-RepeatedPhrases.tex','')
    print(name)
    verseStats2 = originalverseStatHeader
    verseStats2[0] = "\\subsection{"+name+" Repeated Phrases}"
    verseStats2[7] = "\\begin{longtable}{|c|c|}"
    verseStats2[8] = "\\caption["+name+" Repeated Phrases]{"+name+" Repeated Phrases}\\label{table:Repeated Phrases "+name+"} \\\\"
    verseStats2[9] = "\\hline \\multicolumn{1}{|c|}{\\textbf{Phrase}} & \\multicolumn{1}{c|}{\\textbf{Frequency}} \\\ \\hline "
    verseStats2[12] = "\\multicolumn{2}{c}"
    verseStats2[14] = verseStats2[9]
    verseStats2[17] = "\\hline \\multicolumn{2}{c}{{ }} \\\\ \\hline"
    
    output=open(filepath,"w")
    for item in verseStats2:
        item = item +'\n'
        output.write(item)
    for item in sortedPhrases:
        if (item[1] >= MINFREQUENCY) and (item[1] <= MAXFREQUENCY):
            string2 = str(item[0]) + " & " + str(item[1]) + "\\\ \hline \n"
            output.write(string2)
    for item in verseStatTrailer:
        item = item + '\n'
        output.write(item)
    output.close()
    
def buildStatisticsFile(filename, source):
    pass

def buildWordIndex(filename, source):
    filename = filename.replace(' ','')
    filename = filename.replace('000','')
   
    print('\t***** In buildWordIndex\n\t*******',filename, source,"\n\n")
    abbr = source[0][0][0:3]
    if source[0][0] == "Philemon":
        abbr = 'Phm'
    
    #filename = 'test-' + filename # For testing
    outputFilePtr = open(filename,"w")
    
    for item in source:

        verse = item[5];
        verse=verse.replace(".","");
        verse=verse.replace(",","");
        verse=verse.replace(":","")
        verse=verse.replace(";","")
        numberWordsInVerse = 0
        tlwDict = {}
        wiiDict = {}
        verseDict = {}
        www = 0
        uniqueWords = 0
        italicWords = 0
        wwtl = 0
        for word in verse.split():
            numberWordsInVerse += 1
            if "\emph{" in word:
                if word not in wiiDict:
                    wiiDict[word] = 1
                else:
                    wiiDict[word] = wiiDict[word] + 1
                italicWords += 1
                stripped = word.replace('\emph{','')
                stripped = stripped.replace('}','')
                if len(stripped) == 13:
                    if word not in tlwDict:
                        tlwDict[word] = 1
                    else:
                        tlwDict[word] = tlwDict[word] + 1
                    wwtl += 1
            if len(word) == 13:
                wwtl += 1
            #print(word)
            if word not in verseDict:
                verseDict[word] = 1
            else:
                verseDict[word] = verseDict[word] + 1
        print(abbr,str(int(item[2])),item[4],'has:')
        print('\t',numberWordsInVerse,'words')
        print('\t',italicWords,'word in italics',wwtl,'words w 13 letters')
        print('\tand',len(verseDict),'unique words')
        print('\t',verseDict)
        '''
        start with number of words in verse
        '''
        outputString = "\index[NWIV]{"+str(numberWordsInVerse)+"!"+item[0]+"!"+abbr+' ' + \
            str(int(item[2]))+":"+str(item[4])+'}'
        #outputFilePtr.write(outputString)
        '''
        add all words
        '''
        for wd in verseDict:
            count = 0
            freq = verseDict[wd]
            while count < freq:
                if count == 0:
                    stringToBeAdded = "\\index[AWIP]{"+wd+"!"+item[0]+"!"+abbr+' ' + \
                        str(int(item[2]))+":"+str(item[4])+'}'
                    outputString = outputString + stringToBeAdded
                else:
                    stringToBeAdded = "\\index[AWIP]{"+wd+"!"+item[0]+"!"+abbr+' ' + \
                        str(int(item[2]))+":"+str(item[4])+' ('+str(count+1)+')}'
                    outputString = outputString + stringToBeAdded
                count +=1
        '''
        add 13-letter words (words in tlwDict)
        '''
        for wd in tlwDict:
            count = 0
            freq = tlwDict[wd]
            while count < freq:
                if count == 0:
                    stringToBeAdded = "\\index[AWIP]{"+wd+"!"+item[0]+"!"+abbr+' ' + \
                        str(int(item[2]))+":"+str(item[4])+'}'
                    outputString = outputString + stringToBeAdded
                else:
                    stringToBeAdded = "\\index[AWIP]{"+wd+"!"+item[0]+"!"+abbr+' ' + \
                        str(int(item[2]))+":"+str(item[4])+' ('+str(count+1)+')}'
                    outputString = outputString + stringToBeAdded
                count +=1
        '''
        add words in italics (words in wiiDict)
        '''
        for wd in wiiDict:
            count = 0
            freq = wiiDict[wd]
            while count < freq:
                if count == 0:
                    stringToBeAdded = "\\index[AWIP]{"+wd+"!"+item[0]+"!"+abbr+' ' + \
                        str(int(item[2]))+":"+str(item[4])+'}'
                    outputString = outputString + stringToBeAdded
                else:
                    stringToBeAdded = "\\index[AWIP]{"+wd+"!"+item[0]+"!"+abbr+' ' + \
                        str(int(item[2]))+":"+str(item[4])+' ('+str(count+1)+')}'
                    outputString = outputString + stringToBeAdded
                count +=1

        outputString = outputString + '\n\n'
        outputFilePtr.write(outputString)
    outputFilePtr.close()
    
for item in titleList:
    print('\n')
    for ftype in fileType:
        if item == 'Psalm001':
            literal = Psalm001
        if item == 'Psalm002':
            literal = Psalm002
        if item == 'Psalm003':
            literal = Psalm003
        if item == 'Psalm004':
            literal = Psalm004
        if item == 'Psalm005':
            literal = Psalm005
        if item == 'Psalm006':
            literal = Psalm006
        if item == 'Psalm007':
            literal = Psalm007
        if item == 'Psalm008':
            literal = Psalm008
        if item == 'Psalm009':
            literal = Psalm009
        if item == 'Psalm010':
            literal = Psalm010
        if item == 'Psalm011':
            literal = Psalm011
        if item == 'Psalm012':
            literal = Psalm012
        if item == 'Psalm013':
            literal = Psalm013
        if item == 'Psalm014':
            literal = Psalm014
        if item == 'Psalm015':
            literal = Psalm015
        if item == 'Psalm016':
            literal = Psalm016
        if item == 'Psalm017':
            literal = Psalm017
        if item == 'Psalm018':
            literal = Psalm018
        if item == 'Psalm019':
            literal = Psalm019
        if item == 'Psalm020':
            literal = Psalm020
        if item == 'Psalm021':
            literal = Psalm021
        if item == 'Psalm022':
            literal = Psalm022
        if item == 'Psalm023':
            literal = Psalm023
        if item == 'Psalm024':
            literal = Psalm024
        if item == 'Psalm025':
            literal = Psalm025
        if item == 'Psalm026':
            literal = Psalm026
        if item == 'Psalm027':
            literal = Psalm027
        if item == 'Psalm028':
            literal = Psalm028
        if item == 'Psalm029':
            literal = Psalm029
        if item == 'Psalm030':
            literal = Psalm030
        if item == 'Psalm031':
            literal = Psalm031
        if item == 'Psalm032':
            literal = Psalm032
        if item == 'Psalm033':
            literal = Psalm033
        if item == 'Psalm034':
            literal = Psalm034
        if item == 'Psalm035':
            literal = Psalm035
        if item == 'Psalm036':
            literal = Psalm036
        if item == 'Psalm037':
            literal = Psalm037
        if item == 'Psalm038':
            literal = Psalm038
        if item == 'Psalm039':
            literal = Psalm039
        if item == 'Psalm040':
            literal = Psalm040
        if item == 'Psalm041':
            literal = Psalm041
        if item == 'Psalm042':
            literal = Psalm042
        if item == 'Psalm043':
            literal = Psalm043
        if item == 'Psalm044':
            literal = Psalm044
        if item == 'Psalm045':
            literal = Psalm045
        if item == 'Psalm046':
            literal = Psalm046
        if item == 'Psalm047':
            literal = Psalm047
        if item == 'Psalm048':
            literal = Psalm048
        if item == 'Psalm049':
            literal = Psalm049
        if item == 'Psalm050':
            literal = Psalm050
        if item == 'Psalm051':
            literal = Psalm051
        if item == 'Psalm052':
            literal = Psalm052
        if item == 'Psalm053':
            literal = Psalm053
        if item == 'Psalm054':
            literal = Psalm054
        if item == 'Psalm055':
            literal = Psalm055
        if item == 'Psalm056':
            literal = Psalm056
        if item == 'Psalm057':
            literal = Psalm057
        if item == 'Psalm058':
            literal = Psalm058
        if item == 'Psalm059':
            literal = Psalm059
        if item == 'Psalm060':
            literal = Psalm060
        if item == 'Psalm061':
            literal = Psalm061
        if item == 'Psalm062':
            literal = Psalm062
        if item == 'Psalm063':
            literal = Psalm063
        if item == 'Psalm064':
            literal = Psalm064
        if item == 'Psalm065':
            literal = Psalm065
        if item == 'Psalm066':
            literal = Psalm066
        if item == 'Psalm067':
            literal = Psalm067
        if item == 'Psalm068':
            literal = Psalm068
        if item == 'Psalm069':
            literal = Psalm069
        if item == 'Psalm070':
            literal = Psalm070
        if item == 'Psalm071':
            literal = Psalm071
        if item == 'Psalm072':
            literal = Psalm072
        if item == 'Psalm073':
            literal = Psalm073
        if item == 'Psalm074':
            literal = Psalm074
        if item == 'Psalm075':
            literal = Psalm075
        if item == 'Psalm076':
            literal = Psalm076
        if item == 'Psalm077':
            literal = Psalm077
        if item == 'Psalm078':
            literal = Psalm078
        if item == 'Psalm079':
            literal = Psalm079
        if item == 'Psalm080':
            literal = Psalm080
        if item == 'Psalm081':
            literal = Psalm081
        if item == 'Psalm082':
            literal = Psalm082
        if item == 'Psalm083':
            literal = Psalm083
        if item == 'Psalm084':
            literal = Psalm084
        if item == 'Psalm085':
            literal = Psalm085
        if item == 'Psalm086':
            literal = Psalm086
        if item == 'Psalm087':
            literal = Psalm087
        if item == 'Psalm088':
            literal = Psalm088
        if item == 'Psalm089':
            literal = Psalm089
        if item == 'Psalm090':
            literal = Psalm090
        if item == 'Psalm091':
            literal = Psalm091
        if item == 'Psalm092':
            literal = Psalm092
        if item == 'Psalm093':
            literal = Psalm093
        if item == 'Psalm094':
            literal = Psalm094
        if item == 'Psalm095':
            literal = Psalm095
        if item == 'Psalm096':
            literal = Psalm096
        if item == 'Psalm097':
            literal = Psalm097
        if item == 'Psalm098':
            literal = Psalm098
        if item == 'Psalm099':
            literal = Psalm099
        if item == 'Psalm100':
            literal = Psalm100
        if item == 'Psalm101':
            literal = Psalm101
        if item == 'Psalm102':
            literal = Psalm102
        if item == 'Psalm103':
            literal = Psalm103
        if item == 'Psalm1014':
            literal = Psalm104
        if item == 'Psalm105':
            literal = Psalm105
        if item == 'Psalm106':
            literal = Psalm106
        if item == 'Psalm107':
            literal = Psalm107
        if item == 'Psalm108':
            literal = Psalm108
        if item == 'Psalm109':
            literal = Psalm109
        if item == 'Psalm110':
            literal = Psalm120
            literal = Psalm111
            literal = Psalm110
        if item == 'Psalm111':
           literal = Psalm111
        if item == 'Psalm112':
            literal = Psalm112
        if item == 'Psalm113':
            literal = Psalm113
        if item == 'Psalm114':
            literal = Psalm114
        if item == 'Psalm115':
            literal = Psalm115
        if item == 'Psalm116':
            literal = Psalm116
        if item == 'Psalm117':
            literal = Psalm117
        if item == 'Psalm118':
            literal = Psalm118
        if item == 'Psalm119':
            literal = Psalm119
        if item == 'Psalm120':
            literal = Psalm120
        if item == 'Psalm121':
            literal = Psalm121
        if item == 'Psalm122':
            literal = Psalm122
        if item == 'Psalm123':
            literal = Psalm123
        if item == 'Psalm124':
            literal = Psalm124
        if item == 'Psalm125':
            literal = Psalm125
        if item == 'Psalm126':
            literal = Psalm126
        if item == 'Psalm127':
            literal = Psalm127
        if item == 'Psalm128':
            literal = Psalm128
        if item == 'Psalm129':
            literal = Psalm129
        if item == 'Psalm130':
            literal = Psalm130
        if item == 'Psalm131':
            literal = Psalm131
        if item == 'Psalm132':
            literal = Psalm132
        if item == 'Psalm133':
            literal = Psalm133
        if item == 'Psalm134':
            literal = Psalm134
        if item == 'Psalm135':
            literal = Psalm135
        if item == 'Psalm136':
            literal = Psalm136
        if item == 'Psalm137':
            literal = Psalm137
        if item == 'Psalm138':
            literal = Psalm138
        if item == 'Psalm139':
            literal = Psalm139
        if item == 'Psalm140':
            literal = Psalm140
        if item == 'Psalm0141':
            literal = Psalm0141
        if item == 'Psalm142':
            literal = Psalm142
        if item == 'Psalm143':
            literal = Psalm143
        if item == 'Psalm144':
            literal = Psalm144
        if item == 'Psalm145':
            literal = Psalm145
        if item == 'Psalm146':
            literal = Psalm146
        if item == 'Psalm147':
            literal = Psalm147
        if item == 'Psalm148':
            literal = Psalm148
        if item == 'Psalm149':
            literal = Psalm149
        if item == 'Psalm150':
            literal = Psalm150


       
        args = createBaseFileName(item,ftype)

        BUILDWORDCLOUD = True
        PROCESSPHRASES = True
        BUILDWORDINDEXES= True
        
        if ftype == 'WordCloud' and BUILDWORDCLOUD == True:
            makeWordPicture(args[0],literal)
        if ftype == 'RepeatedPhrases' and PROCESSPHRASES == True:
            phraseProcessor(args[0],literal)
        if ftype == 'WordIndex'and BUILDWORDINDEXES == True:
            buildWordIndex(args[0],literal)
            
