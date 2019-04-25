'''
Есть много разновидностей нейронных сетей, но все они состоят из множества узлов (нейронов) и связей между ними (синапсов). Сеть, которую мы собираемся построить, называется многоуровневым перцептроном (multilayer perceptron – MLP). Такая сеть состоит из нескольких уровней нейронов, первый из которых принимает входные данные – в данном случае поисковые слова, введенные пользователем. Последний уровень возвращает результаты – в нашем примере это список весов найденных URL.

Промежуточных уровней может быть много, но мы ограничимся только одним. Он называется скрытым уровнем, так как не взаимодействует напрямую с внешним миром, а реагирует на комбинации входных данных. В данном случае комбинация входных данных – это набор слов, поэтому скрытый уровень можно назвать уровнем запроса.

Чтобы получить от нейронной сети наилучшие результаты для некоторого запроса, значения входных узлов для указанных в запросе слов устанавливают равными 1. Включаются выходы этих узлов, и они пытаются активировать скрытый слой. В свою очередь, узлы скрытого слоя, получающие достаточно сильный входной сигнал, включают свои выходы и пытаются активировать узлы выходного уровня. Узлы выходного уровня оказываются активны в разной степени, и по уровню их активности можно судить, как сильно данный URL ассоциирован со словами исходного запроса.
'''

from math import tanh
import sqlite3

def dtanh(y):
    return 1.0 - y * y

class searchnet:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    '''
    Поскольку нейронную сеть необходимо обучать на запросах пользователей, потребуется сохранить представление сети в базе данных. В нашей базе уже есть таблицы слов и URL, поэтому нужна лишь еще одна таблица для хранения скрытого слоя (которую мы назовем hiddennode) и две таблицы для хранения связей (одна – для связей между слоем слов и скрытым слоем, другая – для связей между скрытым и выходным слоем).
    '''
    def maketables(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table wordhidden(fromid, toid, strength)')
        self.con.execute('create table hiddenurl(fromid, toid, strength)')
        self.con.commit()

    '''
    getstrength - определяет текущую силу связи. Поскольку новые связи создаются только по мере необходимости, этот метод должен возвращать некое специальное значение, если связей еще нет. Для связей между словами и скрытым слоем мы выберем в качестве такого значения –0,2, так что по умолчанию дополнительные слова будут несколько снижать уровень активации скрытого узла. Для связей между скрытым слоем и URL метод по умолчанию будет возвращать значение 0.
    '''
    def getstrength(self, fromid, toid, layer):
        if layer == 0: table = 'wordhidden'
        else: table = 'hiddenurl'

        res = self.con.execute('select strength from %s where fromid=%d and toid=%d' % (table, fromid, toid)).fetchone()

        if res == None:
            if layer == 0: return -0.2
            if layer == 1: return 0
        return res[0]

    '''
    Еще необходим метод setstrength , который выясняет, существует ли уже связь, и создает либо обновляет связь, приписывая ей заданную силу. Он будет использоваться в коде для обучения сети:
    '''
    def setstrength(self, fromid, toid, layer, strength):
        if layer == 0: table = 'wordhidden'
        else: table = 'hiddenurl'

        res = self.con.execute('select rowid from %s where fromid=%d and toid=%d' % (table, fromid, toid)).fetchone()

        if res == None:
            self.con.execute('insert into %s (fromid,toid,strength) values (%d,%d,%f)' % (table, fromid, toid, strength))
        else:
            rowid = res[0]
            self.con.execute('update %s set strength=%f where rowid=%d' % (table, strength, rowid))

    '''
    Обычно при построении нейронной сети все узлы создаются заранее. Можно было бы предварительно создать гигантскую сеть с тысячами узлов в скрытом слое и уже готовыми связями, но в данном случае проще и быстрее создавать скрытые узлы, когда в них возникает надобность. Следующая функция создает новый скрытый узел всякий раз, как ей передается не встречавшаяся ранее комбинация слов. Затем она создает связи с весами по умолчанию между этими словами и скрытым узлом и между узлом запроса и URL, который этот запрос возвращает.
    '''
    def generatehiddennode(self, wordids, urls):
        if len(wordids) > 3: return None
        # Check if we already created a node for this set of words
        sorted_words = [str(id) for id in wordids]
        sorted_words.sort()
        createkey = '_'.join(sorted_words)
        res = self.con.execute("select rowid from hiddennode where create_key='%s'" % createkey).fetchone()

        # If not, create it
        if res == None:
            cur = self.con.execute("insert into hiddennode (create_key) values ('%s')" % createkey)
            hiddenid = cur.lastrowid
            # Put in some default weights
            for wordid in wordids:
                self.setstrength(wordid, hiddenid, 0, 1.0 / len(wordids))
            for urlid in urls:
                self.setstrength(hiddenid, urlid, 1, 0.1)
            self.con.commit()









 
