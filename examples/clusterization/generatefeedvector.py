'''
feedlist.txt - this is file with list of links to blogs
getwords - function to remove html tags
getwordcounts - function to calculate count of words in blog
after calculation, we save words that found in blogs from 10% till 50% 
blogdata.txt - file to save calculated data
'''

import feedparser
import re

def getwords(html):
    # Удалить все HTML-теги
    txt = re.compile(r'<[^>]+>').sub('', html)
    # Выделить слова, ограниченные небуквенными символами
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # Преобразовать в нижний регистр
    return [word.lower( ) for word in words if word!='']

# Возвращает заголовок и словарь слов со счетчиками для RSS-канала
def getwordcounts(url):
    # Проанализировать канал
    d = feedparser.parse(url)
    wc = {}
    # Цикл по всем записям
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description

        # Сформировать список слов
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    title = None
    if 'title' in d.feed: 
        title = d.feed.title

    return title, wc


apcount={}
wordcounts={}
for feedurl in open('feedlist.txt'):
    title, wc = getwordcounts(feedurl)
    if title is None: continue

    # if not title in wordcounts: continue
    wordcounts[title] = wc

    for word, count in wc.items( ):
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1



wordlist=[]
for w, bc in apcount.items( ):
    frac = float(bc) / len(wordcounts)
    if frac  > 0.1 and frac < 0.5: wordlist.append(w)

out = open('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcounts.items( ):
    out.write(blog)
    for word in wordlist:
        if word in wc: out.write('\t%d' % wc[word])
        else: out.write('\t0')
    out.write('\n')






