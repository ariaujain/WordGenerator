import wordForms
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

numWordsPerFile = []


def containsUpper(word):
    return any(w.isupper() for w in word)


def containsThree(word):
    return any(word[i] == word[i + 1] == word[i + 2] for i in range(len(word) - 2))


def isCommonWord(check):
    fileNames = ['commonWords', 'interjections', 'instrument', 'animalsReptiles']
    for fileName in fileNames:
        with open(f'{fileName}.txt', 'r') as file:
            if any(check in line for line in file):
                return True
    return False


# Open one file for all words
with open('allWords.txt', 'w') as text_file:
    for l in letters:
        pageNumber = 1
        totalWords = 0  #Track the number of words found per letter

        while True:
            url = f'https://www.merriam-webster.com/browse/dictionary/{l}/{pageNumber}'
            session = HTMLSession()
            response = session.get(url)
            print(f'Parsing "{l}" on page {pageNumber}: {response.html.url}')

            soup = BeautifulSoup(response.html.html, 'html.parser')
            words = soup.select('div.mw-grid-table-list span')

            sameWords = []
            listWords = []

            for w in words:
                check = w.contents[0]

                if (len(check) > 4 and not any(c in check for c in ' -\'/') and
                        not isCommonWord(check) and check not in sameWords and
                        not containsThree(check) and not containsUpper(check)):
                    listWords.append(check)
                    allForms, sameWord = wordForms.getAllForms(check)
                    sameWords.append(sameWord)

            #Write words to the file and update word count
            for word in listWords:
                text_file.write(word + "\n")
            totalWords += len(listWords)

            #Check if there's a next page
            next_disabled = soup.select('.next.disabled')
            if next_disabled:
                print(f'Finished parsing letter "{l}" after {pageNumber} pages. Total words added: {totalWords}')
                numWordsPerFile.append(totalWords)
                break

            pageNumber += 1
