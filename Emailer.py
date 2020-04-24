import smtplib
from sqlalchemy import create_engine
import random
from email.mime.text import MIMEText

def getQuotesFromDB():
    #DB connect and fetch 5 random quotes
    databaseURI = "mysql://root:****@localhost:3306/bookdb"
    engine = create_engine(databaseURI)
    dbConnection = engine.connect()
    recordCount = dbConnection.execute("SELECT COUNT(*) FROM bookdb.quotes;").fetchone()[0]
    randomQuoteIDs = random.sample(range(14, recordCount + 14), 5) #TODO generate 5 random numbers from previous seed (last 5 numbers)/increase randomness if possible
    quotes = []
    for quoteID in randomQuoteIDs:
        quotes.append(dbConnection.execute("SELECT * FROM bookdb.quotes WHERE QuoteID={};".format(quoteID)).fetchone())
    return createEmail(quotes)
    #return MIMEText("\n\n----------\n\n".join(quotes), "plain")

def createEmail(quotes):
    quoteHTMLSkeleton = """
        <h3>{}</h3>
       <font size="+1">{}</font> <br><br>
    """
    quoteHTMLSkeletons = []
    for quote in quotes:
        title = quote[1]
        author = quote[2]
        quoteContent = quote[3]
        quoteHTMLSkeletons.append(quoteHTMLSkeleton.format(title + "&mdash;" + author, quoteContent))
    return MIMEText("""
    <html>
      <head></head>
      <body>
        {}
      </body>
    </html>
    """.format(" ".join(quoteHTMLSkeletons)), 'html')

def sendMail(emailContent):
    emailContent['Subject'] = "Daily Quotes"

    email = 'achinvitha@gmail.com'
    file = open("gmailAppPW", "r")
    appPassword = file.read()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, appPassword)
    server.sendmail(email, email, emailContent.as_string())
    server.quit()

if __name__ == "__main__":
    emailContent = getQuotesFromDB()
    sendMail(emailContent)