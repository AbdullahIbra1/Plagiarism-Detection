import math
import multiprocessing
import re
import string
import time
from sqlite3 import *
from tqdm import tqdm
from rapidfuzz import fuzz
import docx2txt
import nltk
from nltk import ngrams
from nltk.corpus import stopwords
from multiprocessing import Process

nltk.download('punkt')
nltk.download('stopwords')

BigList1 = []
length1 = []
total1 = []
Length1 = []
outlierList1 = []

def get_ngrams(text, n):
    token = nltk.word_tokenize(text)
    return list(ngrams(token, n))


def preprocess(text):
    text = text.lower()
    text = re.sub("[\u064B-\u0652]", "", text)
    text = re.sub("[\u060C-\u061F]", "", text)
    text = re.sub("[\uf025]", "", text)
    text = re.sub("[\uf0b7]", "", text)
    text = re.sub("؛", "", text)
    text = re.sub(rf"({' عبد'})\s+", r"\1", text)
    text = re.sub("عبد ", "عبد", text)
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("[1234567890]", "", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ـ", "", text)
    # text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    # text = re.sub("([{}])".format(string.punctuation), r' \1 ', text)
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    text = re.sub("\s{2,}", " ", text)  # Removes all spaces
    text = re.sub('’', "", text)
    return text


def check_one(text2,text,one,onelength,per):
    text=text.split(' ')
    text2=text2.split(' ')
    lengthOfwords = 0
    for i in tqdm(text):
        time.sleep(0)
        for j in text2:
            print(i+' '+j)
            value = round(fuzz.ratio(i,j))

            if value >= int(per):
               lengthOfwords += 1
               one.append(f'{j},{i},{value}')

    onelength.append(lengthOfwords)

def check_two(text2, text, two, twolength, outlier,per):
    lengthOfwords = 0
    text = get_ngrams(text, 2)
    text2 = get_ngrams(text2,2)
    for i in tqdm(range(len(text))):
        time.sleep(0)
        for j in range(len(text2)):
            txt1=text[i][0]+' '+text[i][1]
            txt2=text2[j][0]+' '+text2[j][1]
            value = round(fuzz.ratio(txt1, txt2))
            if value >= int(per):
               lengthOfwords += 1
               two.append(f'{txt2},{txt1},{value}')    
    twolength.append(lengthOfwords)

def check_three(text2, text, three, tl, outlier,per):
    lengthOfwords = 0
    text = get_ngrams(text, 3)
    text2 = get_ngrams(text2,3)
    for i in tqdm(range(len(text))):
        time.sleep(0)
        for j in range(len(text2)):
            txt1=text[i][0]+' '+text[i][1]+' '+text[i][2]
            txt2=text2[j][0]+' '+text2[j][1]+' '+text2[j][2]
            value = round(fuzz.ratio(txt1, txt2))
            if value >= int(per):
               lengthOfwords += 1
               three.append(f'{txt2},{txt1},{value}')    
    tl.append(lengthOfwords)

def check_four(text2, text, four, fl, outlier,per):
    lengthOfwords = 0
    text = get_ngrams(text, 4)
    text2 = get_ngrams(text2,4)
    for i in tqdm(range(len(text))):
        time.sleep(0)
        for j in range(len(text2)):
            txt1=text[i][0]+' '+text[i][1]+' '+text[i][2]+' '+text[i][3]
            txt2=text2[j][0]+' '+text2[j][1]+' '+text2[j][2]+' '+text2[j][3]
            value = round(fuzz.ratio(txt1, txt2))
            if value >= int(per):
               lengthOfwords += 1
               four.append(f'{txt2},{txt1},{value}')    
    fl.append(lengthOfwords)

def check_five(text2, text, five, fv, outlier,per):
    lengthOfwords = 0
    text = get_ngrams(text, 5)
    text2 = get_ngrams(text2,5)
    for i in tqdm(range(len(text))):
        time.sleep(0)
        for j in range(len(text2)):
            txt1=text[i][0]+' '+text[i][1]+' '+text[i][2]+' '+text[i][3]+' '+text[i][4]
            txt2=text2[j][0]+' '+text2[j][1]+' '+text2[j][2]+' '+text2[j][3]+' '+text2[j][4]
            value = round(fuzz.ratio(txt1, txt2))
            if value >= int(per):
               lengthOfwords += 1
               five.append(f'{txt2},{txt1},{value}')    
    fv.append(lengthOfwords)

def wordFiles(file):
    my_text = docx2txt.process(file)
    my_text = preprocess(my_text)  # Preprocessing
    my_text = remove_stopwords_without_tokenize(my_text)  # Remove stop words
                  # Tokenize
    return  my_text


def pdfFiles(file, num):
    reader = pypdf.PdfReader(file)
    global pdftext
    pdftext = ''
    for i in range(len(reader.pages)):
        r = reader.pages[i]
        data = r.extract_text()
        pdftext += data
        time.sleep(0)
    my_text = preprocess(pdftext)  # Preprocessing
    filtered_text = remove_stopwords_without_tokenize(my_text)  # Remove stop words
    filtered_text = get_ngrams(filtered_text, num)  # Tokenize
    return filtered_text, pdftext


def fetchDB():
    from pathlib import Path
    THIS_FOLDER = Path(__file__).parent.resolve()
    my_file = THIS_FOLDER / "plagiarism_checker.db"
    con = connect('plagiarism_checker.db')
    c = con.cursor()
    x = c.execute("SELECT * FROM text").fetchall()

    dbElements = []
    for i in range(len(x)):
        dbContents = preprocess(x[i][1])  # preprocess  db elements
        dbElements.append(dbContents)
    return dbElements


def remove_stopwords_without_tokenize(text):
    stop_words = set(stopwords.words('arabic'))
    words = text.split()  # Split the text into words based on spaces
    filtered_text = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_text)


def divide_into_intervals(number, intervals):
    interval_size = number // intervals
    remaining = number % intervals

    result = []
    start = 0
    for i in range(intervals):
        end = start + interval_size + (1 if i < remaining else 0)
        result.append((start, end))
        start = end

    return result


def jaro_distance(s1, s2):
    # If the s are equal

    if s1 == s2:
        return 1.0

    # Length of two s
    len1 = len(s1)
    len2 = len(s2)

    # Maximum distance upto which matching
    # is allowed
    max_dist = math.floor(max(len1, len2) / 2) - 1

    # Count of matches
    match = 0

    # Hash for matches
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)

    # Traverse through the first
    for i in range(len1):

        # Check if there is any matches
        for j in range(max(0, i - max_dist),
                       min(len2, i + max_dist + 1)):

            # If there is a match
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break

    # If there is no match
    if match == 0:
        return 0.0

    # Number of transpositions
    t = 0
    point = 0

    # Count number of occurrences
    # where two characters match but
    # there is a third matched character
    # in between the indices
    for i in range(len1):
        if hash_s1[i]:

            # Find the next matched character
            # in second
            while (hash_s2[point] == 0):
                point += 1

            if s1[i] != s2[point]:
                t += 1
            point += 1
    t = t // 2

    # Return the Jaro Similarity
    return (match / len1 + match / len2 +
            (match - t) / match) / 3.0


#
def wordFiles2(file1,file2):
    my_text = docx2txt.process(file1)
    my_text2= docx2txt.process(file2)
    my_text = preprocess(my_text)  # Preprocessing
    my_text2 = preprocess(my_text2)
    my_text = remove_stopwords_without_tokenize(my_text)  # Remove stop words
    my_text2 = remove_stopwords_without_tokenize(my_text2)              
    return  my_text,my_text2

def run2(filename,filename2,per,min,max):
    st = time.time()

    x = str(filename)
    y = str(filename2)
    x = x.split('.')
    y = y.split('.')

    if x[-1] in ['pdf', 'PDF']:
        text, my_text = pdfFiles(filename, 4)  # remove the comments in order to use PDF file
    else:
        text,text2 = wordFiles2(filename,filename2)  # remove the comments in order to use Word file\

    
    

    with multiprocessing.Manager() as manager:
        
        oneLength = manager.list()
        twoLength = manager.list()
        threeLength = manager.list()
        fourLength = manager.list()
        fifteenLength = manager.list()
        
        one = manager.list()
        two = manager.list()
        three = manager.list()
        four = manager.list()
        five = manager.list()
        outlier = manager.list()

        min=int(min)
        max=int(max)
        total1.clear()
        txt = text.split(' ')
        txt2 = text2.split(' ')
        if len(txt) > len(txt2):
            for i in range(len(txt)):
                total1.append(txt[i])
        else:
            for i in range(len(txt2)):
                total1.append(txt2[i])
        
        
        if min==1 and max==1:
            p=Process(target=check_one, args=(text2, text, one, oneLength, per))
            p.start()
            p.join()
        elif min==1 and max==2:
            p=Process(target=check_one, args=(text2, text, one, oneLength, per))
            p0=Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
            p.start()
            p0.start()
            p.join()
            p0.join()
        elif min==1 and max==3:
            p=Process(target=check_one, args=(text2, text, one, oneLength, per))
            p0=Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
            p1 = Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p.start()
            p0.start()
            p1.start()
            p.join()
            p0.join()
            p1.join()
        elif min==1 and max==4:
            p=Process(target=check_one, args=(text2, text, one, oneLength, per))
            p0=Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
            p1=Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p.start()
            p0.start()
            p1.start()
            p2.start()
            p.join()
            p0.join()
            p1.join()
            p2.join()
        elif min==1 and max==5:
            p=Process(target=check_one, args=(text2, text, one, oneLength, per))
            p0=Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
            p1=Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p3 = Process(target=check_five, args=(text2, text, five, fifteenLength, outlier,per))
            p.start()
            p0.start()
            p1.start()
            p2.start()
            p3.start()
            p.join()
            p0.join()
            p1.join()
            p2.join()
            p3.join()
            
        if min==2 and max ==2:
            p0 = Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
            p0.start()    
            p0.join()
        elif min==3 and max==3:
            p1 = Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p1.start()    
            p1.join()
        elif min==4 and max==4:
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p2.start()
            p2.join()
        elif min==5 and max==5:
            p3 = Process(target=check_five, args=(text2, text, five, fifteenLength, outlier,per))
            p3.start()
            p3.join()

        elif min==2 and max==3:
             p0 = Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
             p1 = Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
             p0.start()
             p1.start()
             p0.join()
             p1.join()

        elif min==2 and max==4:
            p0 = Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
            p1 = Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p0.start()
            p1.start()
            p2.start()
            p0.join()
            p1.join()
            p2.join()
        elif min==2 and max==5:
            p0 = Process(target=check_two, args=(text2, text, two, twoLength, outlier,per))
            p1 = Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p3 = Process(target=check_five, args=(text2, text, five, fifteenLength, outlier,per))
            p0.start()
            p1.start()
            p2.start()
            p3.start()
            p0.join()
            p1.join()
            p2.join()
            p3.join()
        elif min==3 and max==4:
            p1 = Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p1.start()
            p2.start()
            p1.join()
            p2.join()

        elif min==3 and max==5:
            p1 = Process(target=check_three, args=(text2, text, three, threeLength, outlier,per))
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p3 = Process(target=check_five, args=(text2, text, five, fifteenLength, outlier,per))
            p1.start()
            p2.start()
            p3.start()
            p1.join()
            p2.join()
            p3.join()
        elif min==4 and max==5:
            p2 = Process(target=check_four, args=(text2, text, four, fourLength, outlier,per))
            p3 = Process(target=check_five, args=(text2, text, five, fifteenLength, outlier,per))
            p2.start()
            p3.start()
            p2.join()
            p3.join()


    
        BigList1.clear()
        outlierList1.clear()
        for i in one:
            if i not in BigList1:
                BigList1.append(i)
        
        for i in two:
            # file.write(i)
            if i not in BigList1:
                BigList1.append(i)
        #print(BigList1)
        for i in three:
            # file.write(i)
            if i not in BigList1:
                BigList1.append(i)

        for i in four:
            # file.write(i)
            if i not in BigList1:
                BigList1.append(i)

        for i in five:
            # file.write(i)
            if i not in BigList1:
                BigList1.append(i)

        for i in outlier:
            if i not in outlierList1:
              outlierList1.append(i)

        #####################################
        length1.clear()
        for i in oneLength:
            Length1.append(i)
        for i in twoLength:
            length1.append(i)
        for i in threeLength:
            length1.append(i)
        for i in fourLength:
            length1.append(i)
        for i in fifteenLength:
            length1.append(i)
       
        Length1.clear()
        j=0
        for i in length1:
            j+=i
        Length1.append(j)

        en = time.time()
        print(round(en - st))
        # print(total)
        # print(Length)
