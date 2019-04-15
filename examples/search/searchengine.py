import urllib2
from BeautifulSoup import *
from urlparse import urljoin
# Создать список игнорируемых слов
ignorewords=set(['the','of','to','and','a','in','is','it'])


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
        print 'Индексируется %s' % url

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
        pass

    # Начиная с заданного списка страниц, выполняет поиск в ширину
    # до заданной глубины, индексируя все встречающиеся по пути
    # страницы
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = {}
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
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
                    print "Could not parse page %s" % page

        pages = newpages
      
    # Создание таблиц в базе данных
    def createindextables(self):
        pass