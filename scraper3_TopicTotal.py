# -*- coding: utf8 -*-
import requests
import bs4
import sys
import csv
import codecs

#map non unicode values 
non_bmp_map = dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
errors = 0

#download webpage - input = webpage link
#output requests.models.response object
def download(link):
    res = requests.get(link)
    print(type(res))
    try:
        res.raise_for_status()
    except Exception as e:
        print('issue: %s' %(e))
    return res

#Take parameters as input, print as row in csv
def outputToCSV(nick,time,text,bagOfWords,label):
    if outputWriter.writerow([nick,time,text,bagOfWords,label])==0:
        return False
    return True
    
    
def turnToBagOfWords(text):
    #TODO: take as input post text
    #return bag of words vector
    return text

def spellCheck(text):
    #TODO: spell check
    return text

def labelling(text):
    if 'depressed' in text:
        return True
    return False


#parse the goodies and get posts from page - this is for post page
#eg 'https://www.mumsnet.com/Talk/substance_addiction_/2850457-Professor-White-and-the-line-dancing-surfers-eat-cold-turkey'
#take as input a link to a page of posts, output: nick, time, text

def getPage(aPage):
    global posts
    
    post = aPage.select('.post')
    for i in range(len(post)):
        posts = posts + 1
        #Parse & break apart object
        nick = post[i].select('.nick')[0].getText()
        time = post[i].select('.post_time')[0].getText()
        text = post[i].select('p')[0].getText()
        
        #encode and decode to completely ascii text
        textMapped = text.translate(non_bmp_map) #map emojis
        textMapped = textMapped.encode('ascii',errors='ignore')
        textMapped = textMapped.decode('ascii')
        
        #spellcheck, vectorize and label
        checkedText = spellCheck(textMapped)
        bagOfWords = turnToBagOfWords(textMapped)
        label = labelling(textMapped)
        
        #print all dem depressed peeeps
        print('nickname: '+nick)
        print('time: '+time)
        print('text: '+textMapped)
        print('\n')

    ######################comment out for testing this function
        #Send row to csv
        if not outputToCSV(nick,time,textMapped,bagOfWords, label):
           print('Error!')
            #errors += 1

#######getPage test
#pglink = 'https://www.mumsnet.com/Talk/substance_addiction_/2850457-Professor-White-and-the-line-dancing-surfers-eat-cold-turkey'
#res = download(pglink)
#aPage = bs4.BeautifulSoup(res.text,'html.parser')
#getPage(aPage)


#retrieve link of next page if exist, otherwise return -1
#take link of posts page and returns link of next page
def getNextPage(aPage,topicLink):
    
    #get message_pages class object
    msgPages = aPage.select('.message_pages')

    #error check for when no more pages
    if not msgPages:
        print(aPage)
        print(topicLink)
        return -1
    
    #retrieve current and total pages
    pgInfo = msgPages[0].select('p') #error here
    infoSplit = pgInfo[0].getText().split(' ')
    currentPage = int(infoSplit[3])
    totalPages = int(infoSplit[5].split('(')[0])
    print(currentPage)
    print(infoSplit)

    #get link of next page if not at last page
    if currentPage < totalPages:
        nextPage = msgPages[0].select('a[title="Next page"]')[0]
        link = topicLink+'/'+nextPage.get('href')
        return link
    elif currentPage == totalPages:
        #if at last page
        return -1
    else:
        outputWriter.writerow([-1,'Error',aPage,topicLink])

#test function
#aPage =
#topicLink =
#getNextPage

#take as input first page
#output all posts in the thread
#eg https://www.mumsnet.com/Talk/
#substance_addiction_/2850457-Professor-
#White-and-the-line-dancing-surfers-eat-cold-turkey
def getAllPostsInThread(pglink, topicLink):
    res = download(pglink)
    aPage = bs4.BeautifulSoup(res.text,'html.parser')
    #aPage = aPage.encode("utf-8")
    getPage(aPage)

    #get all other pages if around
    pglink = getNextPage(aPage,topicLink) #error here
    while not (-1 == pglink) :
        res = download(pglink)
        aPage = bs4.BeautifulSoup(res.text,'html.parser')
        getPage(aPage)
        pglink = getNextPage(aPage, topicLink)
        
#principle component  | MNIST
#input: a page in topic
#output: list of all links to posts on that page (postfix links)
def getAPageTopicLinks(topicPage):
    result = []
    thread_list = topicPage.select('tr > td > span[class="title"] > a')

    del thread_list[0] #discard start thread description
    for i in range(len(thread_list)):
        result.append('https://www.mumsnet.com/Talk/'+thread_list[i].get('href'))
    return result

#take as input:
#output link to next page, -1 if already last page
def getTopicNextPage(topicPage):
    
    talkBarClass = 'div[class="talk_bar_bottom thread_pages"]'
    pgNumInfo = topicPage.select(talkBarClass+' > p')

    #get current and total pages
    pgNumInfoText = pgNumInfo[0].getText().split(" ")
    currentPage = pgNumInfoText[3]
    totalPages = pgNumInfoText[5]

    print(currentPage)
    print(totalPages)

    if currentPage < totalPages:
        nextPgLink = topicPage.select(talkBarClass+' > ul > li > a[title="Next"]')
        return 'https://www.mumsnet.com/Talk/'+nextPgLink[0].get('href')
    else:
        return -1

#input: link of topic page
#eg https://www.mumsnet.com/Talk/substance_addiction_
#output: wheee  everything
def scrapeWholeTopic(topicLink):
    res = download(topicLink)
    topicPage = bs4.BeautifulSoup(res.text, 'html.parser')

    #print all links on first page
    listOfThreadLinks = getAPageTopicLinks(topicPage)
    for i in range(len(listOfThreadLinks)):
        getAllPostsInThread(listOfThreadLinks[i],topicLink)

    #print all links on the rest of pages
    nextPgLink = getTopicNextPage(topicPage)
    while not (-1 == nextPgLink):
        res = download(nextPgLink)
        topicPage = bs4.BeautifulSoup(res.text, 'html.parser')
        listOfThreadLinks = getAPageTopicLinks(topicPage)
        for i in range(len(listOfThreadLinks)):
            getAllPostsInThread(listOfThreadLinks[i],topicLink)
        
        nextPgLink = getTopicNextPage(topicPage)

#reads from csv file eg 'inputLinks.csv'
#output list of lists - one list per row
def readFromCSV(fileName):
    file = open()
    reader = csv.reader(file)
    listOfLinks = list(reader)
    return listOfLinks

#################################MAIN########################
outputFile = open('output.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)
outputToCSV('nickname','time','Post','Bag Of Words', 'Label')
posts = 0
#getPage('https://www.mumsnet.com/Talk/substance_addiction_/2850457-Professor-White-and-the-line-dancing-surfers-eat-cold-turkey')
#TODO: all other functions run here
#link = 'https://www.mumsnet.com/Talk/substance_addiction_/2850457-Professor-White-and-the-line-dancing-surfers-eat-cold-turkey'
topicLink = 'https://www.mumsnet.com/Talk/substance_addiction_'
#getAllPostsInThread(link, topicLink)
scrapeWholeTopic(topicLink)

print('Posts'+str(posts))
print('Done scraping '+topicLink)
outputFile.close()
#print('Errors '+str(errors))
#############################CLOSE###########################
