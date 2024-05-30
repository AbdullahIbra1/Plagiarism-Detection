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
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')

BigList3 = []
length3 = []
total3 = []
Length3 = []
linkList1 = []

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

def foo1(text2, text, two, twolength, link,per):
    lengthOfwords = 0
    for i in tqdm(range(len(text))):
        time.sleep(0)
        for j in range(len(text2)):
            txt1=text[i]
            txt2=text2[j]
            value = round(fuzz.ratio(txt1, txt2))
            if value >= int(per):
                lengthOfwords += 2
                two.append(f'{txt2},{txt1},{value},{link}')
    twolength.append(lengthOfwords)
    
def foo2(text2, text, two, twolength, link,per):
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
                lengthOfwords += 2
                two.append(f'{txt2},{txt1},{value},{link}')
    twolength.append(lengthOfwords)

def foo3(text2, text, three, tl, link,per):
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
                lengthOfwords += 3
                three.append(f'{txt2},{txt1},{value},{link}')
    tl.append(lengthOfwords)

def foo4(text2, text, four, fl, link,per):
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
                lengthOfwords += 3
                four.append(f'{txt2},{txt1},{value},{link}')
    fl.append(lengthOfwords)

def foo5(text2, text, five, fv, link,per):
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
                lengthOfwords += 5
                five.append(f'{txt2},{txt1},{value},{link}')
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
def url_splitter(text):
    url_pattern = re.compile(r'https?://\S+')
    urls = url_pattern.findall(text)
    return urls


def urlTextExtraction(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract text from the parsed HTML, specifying 'html' as the parser to handle Arabic content
    text = soup.get_text(separator='\n', strip=True)
    # cleaned_text = re.sub(r'[^\u0621-\u064A\s]', '', text)
    text = text.replace('\n', ' ')
    return text


def run(filename,urls,per,min,max):
    st = time.time()
    urlText = ''
    x = str(filename)
    x = x.split('.')
    BigList3.clear()
    total3.clear()
    Length3.clear()
    length3.clear()
    link = ''
    if x[-1] in ['pdf', 'PDF']:
        text, my_text = pdfFiles(filename, 4)  # remove the comments in order to use PDF file
    else:
        text = wordFiles(filename)  # remove the comments in order to use Word file

    urls_splitted = url_splitter(urls)
    for i in urls_splitted:
        urlText = urlTextExtraction(i)
        urlText = preprocess(urlText)
        link = i

        with multiprocessing.Manager() as manager:

            oneLength = manager.list()
            twoLength = manager.list()
            threeLength = manager.list()
            fourLength = manager.list()
            fifteenLength = manager.list()

            one=manager.list()
            two = manager.list()
            three = manager.list()
            four = manager.list()
            five = manager.list()

    
            min=int(min)
            max=int(max)
    
            if min==1 and max==1:
                p=Process(target=foo1, args=(urlText, text, one, oneLength,link, per))
                p.start()
                p.join()
            elif min==1 and max==2:
                p=Process(target=foo1, args=(urlText, text, one, oneLength,link, per))
                p0=Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p.start()
                p0.start()
                p.join()
                p0.join()
            elif min==1 and max==3:
                p=Process(target=foo1, args=(urlText, text, one, oneLength,link, per))
                p0=Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p1 = Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p.start()
                p0.start()
                p1.start()
                p.join()
                p0.join()
                p1.join()
            elif min==1 and max==4:
                p=Process(target=foo1, args=(urlText, text, one, oneLength,link, per))
                p0=Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p1=Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p.start()
                p0.start()
                p1.start()
                p2.start()
                p.join()
                p0.join()
                p1.join()
                p2.join()
            elif min==1 and max==5:
                p=Process(target=foo1, args=(urlText, text, one, oneLength,link, per))
                p0=Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p1=Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p3 = Process(target=foo5, args=(urlText, text, five, fifteenLength, link,per))
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
                p0 = Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p0.start()
                p0.join()
            elif min==3 and max==3:
                p1 = Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p1.start()
                p1.join()
            elif min==4 and max==4:
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p2.start()
                p2.join()
            elif min==5 and max==5:
                p3 = Process(target=foo5, args=(urlText, text, five, fifteenLength, link,per))
                p3.start()
                p3.join()
    
            elif min==2 and max==3:
                p0 = Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p1 = Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p0.start()
                p1.start()
                p0.join()
                p1.join()
    
            elif min==2 and max==4:
                p0 = Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p1 = Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p0.start()
                p1.start()
                p2.start()
                p0.join()
                p1.join()
                p2.join()
            elif min==2 and max==5:
                p0 = Process(target=foo2, args=(urlText, text, two, twoLength, link,per))
                p1 = Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p3 = Process(target=foo5, args=(urlText, text, five, fifteenLength, link,per))
                p0.start()
                p1.start()
                p2.start()
                p3.start()
                p0.join()
                p1.join()
                p2.join()
                p3.join()
            elif min==3 and max==4:
                p1 = Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p1.start()
                p2.start()
                p1.join()
                p2.join()
    
            elif min==3 and max==5:
                p1 = Process(target=foo3, args=(urlText, text, three, threeLength, link,per))
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p3 = Process(target=foo5, args=(urlText, text, five, fifteenLength, link,per))
                p1.start()
                p2.start()
                p3.start()
                p1.join()
                p2.join()
                p3.join()
            elif min==4 and max==5:
                p2 = Process(target=foo4, args=(urlText, text, four, fourLength, link,per))
                p3 = Process(target=foo5, args=(urlText, text, five, fifteenLength, link,per))
                p2.start()
                p3.start()
                p2.join()
                p3.join()
    
            
            for i in two:
                # file.write(i)
                if i not in BigList3:
                    BigList3.append(i)
    
            for i in three:
                # file.write(i)
                if i not in BigList3:
                    BigList3.append(i)
    
            for i in four:
                # file.write(i)
                if i not in BigList3:
                    BigList3.append(i)
    
            for i in five:
                # file.write(i)
                if i not in BigList3:
                    BigList3.append(i)
    
            # for i in link:
            #     if i not in linkList1:
            #         linkList1.append(i)
            print(BigList3)
            #####################################
            for i in oneLength:
                length3.append(i)
            for i in twoLength:
                length3.append(i)
            for i in threeLength:
                length3.append(i)
            for i in fourLength:
                length3.append(i)
            for i in fifteenLength:
                length3.append(i)    
            
            txt = text.split(' ')
            for i in range(len(txt)):
                total3.append(txt[i])
            
            j=0
            for i in length3:
                j+=i
            Length3.append(j)
    
            en = time.time()
            print(round(en - st))
            # print(total)
            # print(Length)
