# import urllib2

from urllib.request import urlopen
from urllib.request import urljoin
from bs4 import BeautifulSoup
import sqlite3

# import nn
# mynet=nn.searchnet('nn.db')

# Создать список игнорируемых слов
ignorewords={'the':1,'of':1,'to':1,'and':1,'a':1,'in':1,'is':1,'it':1}

wikiList = [
    'https://en.wikipedia.org/wiki/Perl',
    'https://en.wikipedia.org/wiki/Modular_programming',
    'https://en.wikipedia.org/wiki/Free_software',
    'https://en.wikipedia.org/wiki/American_National_Standards_Institute',
    'https://en.wikipedia.org/wiki/V6_(Perl)',
    'https://en.wikipedia.org/wiki/Perl_Foundation',
    'https://en.wikipedia.org/wiki/Subroutine',
    'https://en.wikipedia.org/wiki/PhP',
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
        return None

    # Индексирование одной страницы
    def addtoindex(self, url, soup):
        print('Индексируется %s' % url)

    # Извлечение текста из HTML-страницы (без тегов)
    def gettextonly(self, soup):
        return None

    # Разбиение текста на слова
    def separatewords(self, text):
        return None

    # Возвращает true, если данный URL уже проиндексирован
    def isindexed(self,url):
        return False

    # Добавление ссылки с одной страницы на другую
    def addlinkref(self, urlFrom, urlTo, linkText):
        print('addlinkref', urlFrom, urlTo, linkText)
        pass

    '''
    Начиная с заданного списка страниц, выполняет поиск в ширину до заданной глубины, индексируя все встречающиеся по пути страницы
    '''
    def crawl(self, pages, depth = 2):
        for i in range(depth):
            newpages = {}
            for page in pages:
                try:
                    c = urlopen(page)
                except:
                    print("Could not open %s" % page)
                    continue
                try:
                    soup = BeautifulSoup(c.read())
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
                except:
                    print("Could not parse page %s" % page)

        pages = newpages
      
    '''
    В каждой таблице SQLite по умолчанию имеется поле rowid , поэтому явно задавать ключевые поля необязательно.
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



# pagelist = ['https://en.wikipedia.org/wiki/Perl']
# crawler = crawler('')
# crawler.crawl(pagelist)



crawler = crawler('searchindex.db')
crawler.createindextables()