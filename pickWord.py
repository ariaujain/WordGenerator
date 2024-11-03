import random
import dictionary #comment it out to test individually
import emailSend
from bs4 import BeautifulSoup
import requests


def getGoogleDef(word):
    url = f"https://www.google.com/search?q=define+{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    definitionDiv = soup.find("div", {"data-dobid": "dfn"})
    posSpan = soup.find("span", {"class": "YrbPuc"})

    definition = definitionDiv.text if definitionDiv else "No definition found"
    partOfSpeech = posSpan.text if posSpan else "No part of speech found"

    return definition, partOfSpeech


#picks a word of the day from the AllWords file
def getWordOfDay():
    try:
        #Read all lines from allWords.txt
        with open('allWords.txt', 'r') as file:
            lines = file.readlines()

        if not lines:
            raise Exception("No more words in file.")  #Handle empty file case

        #Pick a random word
        word = random.choice(lines).strip()

        #Rewrite the file without the selected word
        with open('allWords.txt', 'w') as file:
            for line in lines:
                if line.strip() != word:
                    file.write(line)

        return word

    except FileNotFoundError:
        raise Exception("allWords.txt file not found.")

def job():
    try:
        #Retrieve the word of the day
        word = getWordOfDay()
        print(f"Word of the Day selected: {word}")

        #Get the list of users from the database
        from userDatabase import getUsers
        users = getUsers()

        if not users:
            print("No users to send the Word of the Day email.")
        else:
            emailSend.sendEmail(users, word) #sends email
            print("Email sent successfully.")

    except Exception as e:
        print("Error in job function:", e)
