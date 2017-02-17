# -*- coding: utf8 -*-
import requests
import bs4
import sys
import csv
import codecs



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
def scrapeWholeTopic(link):
    res = download(link)
    topicPage = bs4.BeautifulSoup(res.text, 'html.parser')

    #print all links on first page
    listOfThreadLinks = getAPageTopicLinks(topicPage)
    for i in range(len(listOfThreadLinks)):
        print(listOfThreadLinks[i])

    #print all links on the rest of pages
    nextPgLink = getTopicNextPage(topicPage)
    while not (nextPgLink == -1):
        res = download(nextPgLink)
        topicPage = bs4.BeautifulSoup(res.text, 'html.parser')
        listOfThreadLinks = getAPageTopicLinks(topicPage)
        for i in range(len(listOfThreadLinks)):
            print(listOfThreadLinks[i])
        
        nextPgLink = getTopicNextPage(topicPage)

#link = 'https://www.mumsnet.com/Talk/alcohol_support?order=&pg=3'
#res = download(link)
#topicPage = bs4.BeautifulSoup(res.text, 'html.parser')
#print(getTopicNextPage(topicPage))

scrapeWholeTopic('https://www.mumsnet.com/Talk/alcohol_support')
#print(topicNextPage('https://www.mumsnet.com/Talk/substance_addiction_'))
#print(topicNextPage('https://www.mumsnet.com/Talk/adoptions'))
#scrapeTopic('https://www.mumsnet.com/Talk/substance_addiction_')
