# import urllib2

from urllib.request import urlopen
from urllib.request import urljoin
from bs4 import BeautifulSoup

# Создать список игнорируемых слов
ignorewords=set(['the','of','to','and','a','in','is','it'])

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

class crawler:
    # Инициализировать паука, передав ему имя базы данных
    def __init__(self,dbname):
        pass

    def __del__(self):
        pass

    def dbcommit(self):
        pass

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

    # Начиная с заданного списка страниц, выполняет поиск в ширину
    # до заданной глубины, индексируя все встречающиеся по пути
    # страницы
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
      
    # Создание таблиц в базе данных
    def createindextables(self):
        pass



pagelist = ['https://en.wikipedia.org/wiki/Perl']
crawler = crawler('')
crawler.crawl(pagelist)