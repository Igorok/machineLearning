# import urllib2

from urllib.request import urlopen
from urllib.request import urljoin
from bs4 import BeautifulSoup
import sqlite3
from pathlib import Path
import re

import nn
mynet=nn.searchnet('nn.db')

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
    'https://en.wikipedia.org/wiki/Flask_(web_framework)',
    'https://en.wikipedia.org/wiki/Zend_Framework',
    'https://en.wikipedia.org/wiki/Angular_(web_framework)'
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


    '''
    Алгоритм PageRank был придуман основателями компании Google, и вариации этой идеи теперь применяются во всех крупных поисковых машинах. Этот алгоритм приписывает каждой странице ранг, оценивающий ее значимость. Значимость страницы вычисляется исходя из значимостей ссылающихся на нее страниц и общего количества ссылок, имеющихся на каждой из них.

    Теоретически алгоритм PageRank (названный по фамилии одного из его изобретателей Лари Пейджа (Larry Page)) рассчитывает вероятность того, что человек, случайно переходящий по ссылкам, доберется до некоторой страницы. Чем больше ссылок ведет на данную страницу с других популярных страниц, тем выше вероятность, что экспериментатор чисто случайно наткнется на нее. Разумеется, если пользователь будет щелкать по ссылкам бесконечно долго, то в конце концов он посетит каждую страницу, но большинство людей в какой-то момент останавливаются. Чтобы учесть это, в алгоритм Page-Rank введен коэффициент затухания 0,85, означающий, что пользователь продолжит переходить по ссылкам, имеющимся на текущей странице, с вероятностью 0,85.
    PR(A) = 0,15 + 0,85 × (PR(B)/ссылки(B) + PR(C)/ссылки(C) + PR(D)/ссылки(D))
    Невозможно вычислить ранг страницы, пока неизвестны ранги ссылающихся на нее страниц, а эти ранги можно вычислить, только зная ранги страницы, которые ссылаются на них. Решение состоит в том, чтобы присвоить всем страницам произвольный начальный ранг (в программе ниже взято значение 1,0, но на самом деле точная величина несущественна) и провести несколько итераций. После каждой итерации ранг каждой страницы будет все ближе к истинному значению PageRank. Количество необходимых итераций зависит от числа страниц, но для того небольшого набора, с которым мы работаем, 20 должно быть достаточно.
    '''
    def calculatepagerank(self, iterations = 20):
        # clear out the current page rank tables
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')

        # initialize every url with a page rank of 1
        for (urlid,) in self.con.execute('select rowid from urllist'):
            self.con.execute('insert into pagerank(urlid,score) values (%d,1.0)' % urlid)
        self.dbcommit()

        for i in range(iterations):
            print("Iteration %d" % (i))
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr = 0.15
                # Loop through all the pages that link to this one
                for (linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    # Get the page rank of the linker
                    linkingpr = self.con.execute('select score from pagerank where urlid=%d' % linker).fetchone()[0]
                    # Get the total number of links from the linker
                    linkingcount = self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr += 0.85 * (linkingpr / linkingcount)
                self.con.execute('update pagerank set score=%f where urlid=%d' % (pr, urlid))

            self.dbcommit()



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

        # Create the query from the separate parts
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        print(fullquery)

        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        return rows, wordids



    '''
    Нам понадобится новый метод, который принимает на входе запрос, получает строки, помещает их в словарь и отображает в виде отформатированного списка.
    '''
    def getscoredlist(self, rows, wordids):
        totalscores = dict([(row[0], 0) for row in rows])
        # This is where we'll put our scoring functions
        weights = [
            (1.0, self.frequencyscore(rows)),
            (1.0, self.locationscore(rows)),
            # (1.0, self.distancescore(rows)),
            # (1.0, self.inboundlinkscore(rows)),
            (1.0, self.pagerankscore(rows)),
            (1.0, self.linktextscore(rows, wordids)),
            (5.0, self.nnscore(rows, wordids))
        ]

        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight * scores[url]

        return totalscores

    def geturlname(self, id):
        return self.con.execute("select url from urllist where rowid=%d" % id).fetchone()[0]

    def query(self, q):
        #  w0.urlid, w0.location, w1.location, w2.location, w2.location ...
        rows, wordids = self.getmatchrows(q)
        # sum of weights for every url
        scores = self.getscoredlist(rows, wordids)
        rankedscores = [(score, url) for (url, score) in scores.items()]
        rankedscores.sort()
        rankedscores.reverse()
        for (score, urlid) in rankedscores[0:10]:
            print('%f\t%s' % (score, self.geturlname(urlid)))

        return wordids, [r[1] for r in rankedscores[0:10]]

    '''
    Все рассматриваемые ниже функции ранжирования возвращают словарь, в котором ключом является идентификатор URL, а значением – числовой ранг. Иногда лучшим считается больший ранг, иногда – меньший. Чтобы сравнивать результаты, получаемые разными методами, необходимо как-то нормализовать их, то есть привести к одному и тому же диапазону и направлению.
    Функция нормализации принимает на входе словарь идентификаторов и рангов и возвращает новый словарь, в котором идентификаторы те же самые, а ранг находится в диапазоне от 0 до 1.
    '''
    def normalizescores(self, scores, smallIsBetter = 0):
        vsmall = 0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0: maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])

    '''
    Метрика, основанная на частоте слов, ранжирует страницу исходя из того, сколько раз в ней встречаются слова, упомянутые в запросе. wordlocation (urlid, wordid, location) - содержит id ссылки, id слова и номер слова в тексте. Сумма результатов для каждой ссылки будет являться суммой обнаруженных слов на странице
    '''
    def frequencyscore(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows: counts[row[0]] += 1
        return self.normalizescores(counts)

    '''
    Еще одна простая метрика для определения релевантности страницы запросу – расположение поисковых слов на странице. Обычно, если страница релевантна поисковому слову, то это слово расположено близко к началу страницы, быть может, даже находится в заголовке.
    Первый элемент в каждой строке row – это идентификатор URL, а за ним следуют адреса вхождений всех поисковых слов. Каждый идентификатор может встречаться несколько раз, по одному для каждой комбинации вхождений. Для каждой строки этот метод суммирует адреса вхождений всех слов и сравнивает результат с наилучшим, вычисленным для данного URL к текущему моменту. Затем окончательные результаты передаются функции normalize . Заметьте, параметр smallIsBetter означает, что ранг 1,0 будет присвоен URL с наименьшей суммой адресов вхождений.
    '''
    def locationscore(self, rows):
        locations = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]: locations[row[0]] = loc

        return self.normalizescores(locations, smallIsBetter = 1)

    '''
    Если запрос содержит несколько слов, то часто бывает полезно ранжировать результаты в зависимости от того, насколько близко друг к другу встречаются поисковые слова. Как правило, вводя запрос из нескольких слов, человек хочет найти документы, в которых эти слова концептуально связаны. Это более слабое условие, чем фраза, заключенная в кавычки, когда слова должны встречаться точно в указанном порядке без промежуточных слов. Рассматриваемая метрика допускает изменение порядка и наличие дополнительных слов между поисковыми.
    '''
    def distancescore(self, rows):
        # If there's only one word in a query, everyone wins!
        if len(rows[0]) <= 2: return dict([(row[0], 1.0) for row in rows])

        # Initialize the dictionary with large values
        mindistance = dict([(row[0], 1000000) for row in rows])

        for row in rows:
            # check distance with previous word
            dist = sum([abs(row[i] - row[i - 1]) for i in range(2, len(row))])
            if dist < mindistance[row[0]]: mindistance[row[0]] = dist

        return self.normalizescores(mindistance,smallIsBetter = 1)

    '''
    Простейший способ работы с внешними ссылками заключается в том, чтобы подсчитать, сколько их ведет на каждую страницу, и использовать результат в качестве метрики. Так обычно оцениваются научные работы; считается, что их значимость тем выше, чем чаще их цитируют. Представленная ниже функция ранжирования создает словарь счетчиков, делая запрос к таблице ссылок для каждого уникального идентификатора URL в списке rows , а затем возвращает нормализованный результат
    '''
    def inboundlinkscore(self, rows):
        uniqueurls = dict([(row[0], 1) for row in rows])
        inboundcount = dict(
            [
                (u, self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0])
                for u in uniqueurls
            ]
        )
        return self.normalizescores(inboundcount)

    '''
    Теперь, когда у нас есть таблица рангов, для ее использования достаточно написать функцию, которая будет извлекать ранг и выполнять нормализацию.
    '''
    def pagerankscore(self, rows):
        pageranks = dict(
            [
                (row[0], self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0])
                for row in rows
            ]
        )
        maxrank = max(pageranks.values())
        normalizedscores = dict(
            [
                (u, float(l) / maxrank) for (u, l) in pageranks.items()
            ]
        )
        return normalizedscores

    '''
    Еще один полезный способ ранжирования результатов – использование текста ссылок на страницу при определении степени ее релевантности запросу. Часто удается получить более качественную информацию из того, что сказано в ссылках, ведущих на страницу, чем из самой страницы, поскольку авторы сайтов обычно включают краткое описание того, на что ссылаются.

    Этот код в цикле обходит все слова из списка wordids и ищет ссылки, содержащие эти слова. Если страница, на которую ведет ссылка, совпадает с каким-нибудь результатом поиска, то ранг источника ссылки прибавляется к окончательному рангу этой страницы. Страница, на которую ведет много ссылок со значимых страниц, содержащих поисковые слова, получит очень высокий ранг. Для многих найденных страниц вообще не будет ссылок с подходящим текстом, поэтому их ранг окажется равен 0.
    '''
    def linktextscore(self, rows, wordids):
        linkscores = dict([(row[0], 0) for row in rows])
        for wordid in wordids:
            cur = self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
            for (fromid, toid) in cur:
                if toid in linkscores:
                    pr = self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid] += pr
        maxscore = max(linkscores.values())
        normalizedscores = dict([(u, float(l) / maxscore) for (u, l) in linkscores.items()])
        return normalizedscores


    def nnscore(self, rows, wordids):
        # Get unique URL IDs as an ordered list
        urlids = [urlid for urlid in dict([(row[0], 1) for row in rows])]
        nnres = mynet.getresult(wordids, urlids)
        print('nnres', nnres)
        scores = dict([(urlids[i], nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)






# crawler = crawler('searchindex.db')
# crawler.crawl(wikiList)
# crawler.calculatepagerank()

e = searcher('searchindex.db')
# e.query('java script react')
# e.query('php web')
e.query('java script angular')