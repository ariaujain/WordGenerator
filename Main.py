import schedule
import time
from pickWord import job, getWordOfDay
import emailSend
import userDatabase

def runDaily():
    try:
        #Select a test word of the day
        word = getWordOfDay()
        print(f"Testing email with Word of the Day: {word}")

        #Get the list of users from the database
        users = userDatabase.getUsers()
        print(f"Retrieved users: {users}")

        if not users:
            print("No users available to send the test email.")
        else:
            #Send the selected word to all users
            emailSend.sendEmail(users, word)
            print("Test email sent successfully.")
    except Exception as e:
        print("Error during test email send:", e)

userDatabase.setupDatabase()
print("Emails in the database at startup:", userDatabase.getUsers())

def test():
    #Test for running job
    print("Running Word of the Day job manually for testing:")
    job()  #Run the job directly for testing

    #Test for email
    print("Running test for sending email with a sample word:")
    runDaily()

#Schedule the job
print("Scheduling email for daily run at 20:00...")
schedule.every().day.at("20:00").do(runDaily)

#Scheduler loop
while True:
    try:
        schedule.run_pending()
        print("Checking schedule...")
        time.sleep(60)
    except Exception as e:
        print("Error in scheduler loop:", e)
