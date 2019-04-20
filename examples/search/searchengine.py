# import urllib2

from urllib.request import urlopen
from urllib.request import urljoin
from bs4 import BeautifulSoup
import sqlite3
from pathlib import Path
import re

# import nn
# mynet=nn.searchnet('nn.db')

# Создать список игнорируемых слов
ignorewords={'the':1,'of':1,'to':1,'and':1,'a':1,'in':1,'is':1,'it':1}

wikiList = [
    'https://en.wikipedia.org/wiki/PHP',
    'https://en.wikipedia.org/wiki/Perl',
    'https://en.wikipedia.org/wiki/Modular_programming',
    'https://en.wikipedia.org/wiki/Free_software',
    'https://en.wikipedia.org/wiki/American_National_Standards_Institute',
    'https://en.wikipedia.org/wiki/V6_(Perl)',
    'https://en.wikipedia.org/wiki/Perl_Foundation',
    'https://en.wikipedia.org/wiki/Subroutine',
    'https://en.wikipedia.org/wiki/Python_(programming_language)',
    'https://en.wikipedia.org/wiki/JavaScript',
    'https://en.wikipedia.org/wiki/Android_(operating_system)',
    'https://en.wikipedia.org/wiki/Java_(programming_language)',
    'https://en.wikipedia.org/wiki/Ubuntu',
    'https://en.wikipedia.org/wiki/Web_development',
    'https://en.wikipedia.org/wiki/Node.js',
    'https://en.wikipedia.org/wiki/React_(JavaScript_library)',
    'https://en.wikipedia.org/wiki/Flask_(web_framework)'
]

'''

Первый шаг при создании поисковой машины – разработать методику сбора документов. Иногда для этого применяется ползание (начинаем с небольшого набора документов и переходим по имеющимся в них ссылкам).

Ну и последний шаг – это, конечно, возврат ранжированного списка документов в ответ на запрос. Имея индекс, найти документы, содержащие заданные слова, сравнительно несложно; хитрость заключается в том, как отсортировать результаты.

Для проработки примеров из этой главы нам понадобится создать на языке Python модуль searchengine , в котором будет два класса: один – для ползания по сети и создания базы данных, а второй – для выполнения полнотекстового поиска в этой базе в ответ на запрос.

Библиотека urllib2, входящая в дистрибутив Python, предназначена для скачивания страниц. От вас требуется только указать URL. В этом разделе мы воспользуемся ею, чтобы скачать страницы для последующего индексирования.

С помощью библиотек urllib2 и Beautiful Soup можно построить паука, который принимает на входе список подлежащих индексированию URL и, переползая по ссылкам, находит другие страницы.

'''
class crawler:
    # Инициализировать паука, передав ему имя базы данных
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()


    # Вспомогательная функция для получения идентификатора и
    # добавления записи, если такой еще нет
    def getentryid(self, table, field, value, createnew = True):
        cur=self.con.execute("select rowid from %s where %s='%s'" % (table, field, value))
        res=cur.fetchone()

        if res == None:
            cur = self.con.execute("insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]


    '''
    Индексирование одной страницы - вызывает две функции, чтобы получить список слов на странице. Затем эта страница и все найденные на ней слова добавляются в индекс и создаются ссылки между словами и их вхождениями в документ. В нашем примере адресом вхождения будет считаться номер слова в списке слов.
    '''
    def addtoindex(self, url, soup):
        if self.isindexed(url): return
        print('Indexing ' + url)

        # Get the individual words
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # Get the URL id
        urlid = self.getentryid('urllist', 'url', url)

        # Link each word to this url
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid, wordid, location) values (%d, %d, %d)" % (urlid, wordid, i))

    '''
    Эта функция возвращает длинную строку, содержащую весь имеющийся на странице текст. Для этого она рекурсивно обходит объектную модель HTML-документа, отыскивая текстовые узлы. Текст, находящийся в различных разделах, помещается в отдельные абзацы.
    '''
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    '''
    функция которая разбивает строку на отдельные слова, чтобы их можно было добавить в индекс. Сделать это правильно не так просто, как может показаться, и существует немало работ о том, как улучшить эту методику.
    '''
    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    '''
    определяет, есть ли указанная страница в базе данных и, если да, ассоциированы ли с ней какие-нибудь слова:
    '''
    def isindexed(self, url):
        u = self.con.execute("select rowid from urllist where url='%s'" % url).fetchone( )
        if u != None:
            # Проверяем, что страница посещалась
            v = self.con.execute('select * from wordlocation where urlid=%d' % u[0]).fetchone( )
            if v != None: return True
        return False

    # Добавление ссылки с одной страницы на другую
    def addlinkref(self, urlFrom, urlTo, linkText):
        if linkText is None or linkText == '':
            return

        words = self.separatewords(linkText)
        fromid = self.getentryid('urllist', 'url', urlFrom)
        toid = self.getentryid('urllist', 'url', urlTo)
        if fromid == toid: return
        cur = self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into linkwords(linkid, wordid) values (%d, %d)" % (linkid, wordid))


    '''
    Эта функция в цикле обходит список страниц, вызывая для каждой функцию addtoindex. Далее с помощью библиотеки Beautiful Soup она получает все ссылки на данной странице и добавляет их URL в список newpages . В конце цикла newpages присваивается pages , и процесс повторяется.
    '''
    def crawl(self, pages, depth = 2):
        for i in range(depth):
            newpages = {}
            for i in range(len(pages)):
                page = pages[i]
                html = None
                fPath = './pages/' + str(i) + '.txt'

                if Path(fPath).is_file():
                    f = open(fPath, 'r')
                    html = f.read()

                if html is None:
                    try:
                        c = urlopen(page)
                        html = c.read().decode('utf-8')

                        f = open(fPath, 'w')
                        f.write(html)
                        f.close()
                    except Exception as e:
                        print("Could not open %s" % page, str(e))
                        continue

                try:
                    soup = BeautifulSoup(html, 'html.parser')
                    self.addtoindex(page, soup)

                    links = soup('a')
                    for link in links:
                        if ('href' in dict(link.attrs)):
                            url = urljoin(page, link['href'])
                            if url.find("'") != -1: continue
                            url = url.split('#')[0]  # remove location portion
                            if url[0:4] == 'http' and not self.isindexed(url):
                                newpages[url] = 1
                            linkText = self.gettextonly(link)
                            self.addlinkref(page, url, linkText)

                    self.dbcommit()
                except Exception as e:
                    print(e)
                    print("Could not parse page %s" % page, str(e))

        pages = newpages




    '''
    В каждой таблице SQLite по умолчанию имеется поле rowid , поэтому явно задавать ключевые поля необязательно. Эта функция создает все нужные нам таблицы, а также ряд индексов, ускоряющих поиск.
    '''
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()


# crawler = crawler('searchindex.db')
# crawler.createindextables()

# crawler = crawler('searchindex.db')
# crawler.crawl(wikiList)



class searcher:
    def __init__(self,dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    '''
    Таблица wordlocation обеспечивает простой способ связать слова с документами, так что мы можем легко найти, какие страницы содержат данное слово. Однако поисковая машина была бы довольно слабой, если бы не позволяла задавать запросы с несколькими словами. Чтобы исправить это упущение, нам понадобится функция, которая принимает строку запроса, разбивает ее на слова и строит SQL-запрос для поиска URL тех документов, в которые входят все указанные слова.

    На первый взгляд функция довольно сложна, но, по существу, она просто создает по одной ссылке на таблицу wordlocation для каждого слова и выполняет соединение таблиц по идентификаторам URL

    select w0.urlid, w0.location, w1.location
    from wordlocation w0, wordlocation w1
    where w0.urlid = w1.urlid
    and w0.wordid = 10
    and w1.wordid = 17
    '''
    def getmatchrows(self, q):
        # Strings to build the query
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # Split the words by spaces
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            # Get the word ID
            wordrow = self.con.execute("select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)

                # we try to find words in the table wordlocation and join these by urlid
                if tablenumber > 0:
                    # wordlocation w0,
                    tablelist += ','
                    # w0.wordid=123 and w0.urlid=w1.urlid and
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1, tablenumber)
                
                # w0.urlid, w0.location
                fieldlist += ',w%d.location' % tablenumber
                # wordlocation w0
                tablelist += 'wordlocation w%d' % tablenumber
                # w0.wordid=123
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1
        

        # fieldlist += ',url'
        # tablelist += ' left join urllist on w0.urlid = urllist.rowid'

        # Create the query from the separate parts
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        print(fullquery)

        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        return rows, wordids


searcher = searcher('searchindex.db')
rows, wordids = searcher.getmatchrows('php js')

print('rows', rows, len(rows))


# for row in rows:
#     print('row', row)
