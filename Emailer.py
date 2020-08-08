import smtplib
from sqlalchemy import create_engine
import random
from email.mime.text import MIMEText
from datetime import datetime

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

def createEmail(quotes):
    quoteHTMLSkeleton = """
        <h3>{}</h3>
       <font size="+1">{}</font> <br><br>
    """
    quoteHTMLSkeletons = []
    for quote in quotes:
        title = quote[1]
        author = quote[2]
        quoteContent = htmlifyQuote(quote[3])
        quoteHTMLSkeletons.append(quoteHTMLSkeleton.format("<u>" + title + "&mdash;" + author + "</u>", quoteContent))
    return MIMEText("""
    <html>
      <head></head>
      <body>
        {}
      </body>
    </html>
    """.format(" ".join(quoteHTMLSkeletons)), 'html')

def htmlifyQuote(quote):
    quote = quote.replace('\n', '<br />')
    quote = quote.replace('{', "<br /><i>")
    quote = quote.replace('}', "</i><br />")
    return quote

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
    try:
        emailContent = getQuotesFromDB()
        sendMail(emailContent)
    except Exception as e:
        log = open(str(datetime.date(datetime.now())), "w")
        log.write("Failed to send email with exception {0}\n".format(str(e)))
        log.close()