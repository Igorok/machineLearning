'''
Есть много разновидностей нейронных сетей, но все они состоят из множества узлов (нейронов) и связей между ними (синапсов). Сеть, которую мы собираемся построить, называется многоуровневым перцептроном (multilayer perceptron – MLP). Такая сеть состоит из нескольких уровней нейронов, первый из которых принимает входные данные – в данном случае поисковые слова, введенные пользователем. Последний уровень возвращает результаты – в нашем примере это список весов найденных URL.

Промежуточных уровней может быть много, но мы ограничимся только одним. Он называется скрытым уровнем, так как не взаимодействует напрямую с внешним миром, а реагирует на комбинации входных данных. В данном случае комбинация входных данных – это набор слов, поэтому скрытый уровень можно назвать уровнем запроса.

Чтобы получить от нейронной сети наилучшие результаты для некоторого запроса, значения входных узлов для указанных в запросе слов устанавливают равными 1. Включаются выходы этих узлов, и они пытаются активировать скрытый слой. В свою очередь, узлы скрытого слоя, получающие достаточно сильный входной сигнал, включают свои выходы и пытаются активировать узлы выходного уровня. Узлы выходного уровня оказываются активны в разной степени, и по уровню их активности можно судить, как сильно данный URL ассоциирован со словами исходного запроса.
'''

from math import tanh
import sqlite3

'''
Чтобы определить, насколько следует изменить суммарный входной сигнал, алгоритм обучения должен знать наклон функции tanh для текущего уровня выходного сигнала. В средней точке графика, когда выходной сигнал равен 0,0, функция изменяется очень круто, поэтому небольшое изменение входного сигнала приводит к большому изменению выходного. По мере того как уровень выходного сигнала приближается к –1 или к 1, изменение входного сигнала меньше сказывается на выходном.
'''
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

    '''
    Прежде чем вызывать алгоритм feedforward , наш класс должен прочитать из базы информацию об узлах и связях и построить в памяти часть сети, релевантную конкретному запросу. Первым делом мы напишем функцию, которая ищет все узлы из скрытого слоя, релевантные запросу; в нашем случае это узлы, связанные с любым из слов запроса или с каким-нибудь URL, принадлежащим множеству результатов поиска. Так как никакие другие узлы не участвуют в определении выхода или в обучении сети, то и включать их необязательно.
    '''
    def getallhiddenids(self, wordids, urlids):
        l1 = {}
        for wordid in wordids:
            cur = self.con.execute('select toid from wordhidden where fromid=%d' % wordid)
            for row in cur: l1[row[0]] = 1
        for urlid in urlids:
            cur = self.con.execute('select fromid from hiddenurl where toid=%d' % urlid)
            for row in cur: l1[row[0]] = 1
        return l1.keys()

    '''
    Нам также понадобится метод для конструирования релевантной сети с текущими весами из базы данных. Эта функция инициализирует различные переменные экземпляра класса: список слов, относящиеся к запросу узлы и URL, уровень выходного сигнала для каждого узла и веса всех связей между узлами. Веса считываются из базы данных с помощью ранее разработанных функций.
    '''
    def setupnetwork(self, wordids, urlids):
        # value lists
        self.wordids = wordids
        self.hiddenids = self.getallhiddenids(wordids, urlids)
        self.urlids = urlids
 
        # node outputs
        self.ai = [1.0] * len(self.wordids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.urlids)
        
        # create weights matrix
        self.wi = [
                [
                    self.getstrength(wordid,hiddenid,0) 
                    for hiddenid in self.hiddenids
                ] 
                for wordid in self.wordids
            ]
        self.wo = [
                [
                    self.getstrength(hiddenid, urlid, 1) 
                    for urlid in self.urlids
                ] 
                for hiddenid in self.hiddenids
            ]

    '''
    Вот теперь все готово для реализации алгоритма feedforward . Он принимает список входных сигналов, пропускает их через сеть и возвращает выходные сигналы от всех узлов на выходном уровне. Поскольку в данном случае мы сконструировали сеть только для слов, входящих в запрос, то выходной сигнал от всех входных узлов равен 1

    Алгоритм feedforward в цикле обходит все узлы скрытого слоя и для каждого из них вычисляет сумму величин выходных сигналов от узлов входного слоя, помноженных на вес соответствующей связи. Выходной сигнал каждого скрытого узла – это результат применения функции tanh к взвешенной сумме входных сигналов. Этот сигнал передается на выходной уровень. Выходной уровень делает то же самое – умножает полученные от предыдущего уровня сигналы на веса связей и применяет функцию tanh для получения окончательного результата. Сеть можно легко обобщить, введя дополнительные уровни, которые будут преобразовывать выходные сигналы от предыдущего уровня во входные сигналы следующему.
    '''
    def feedforward(self):
        # the only inputs are the query words
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        # hidden activations
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        # output activations
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)

        return self.ao[:]

    def getresult(self, wordids, urlids):
        self.setupnetwork(wordids, urlids)
        return self.feedforward()


    '''
    Сеть принимает входные сигналы и генерирует выходные, но, поскольку ее не научили, какой результат считать хорошим, выдаваемые ею ответы практически бесполезны. Сейчас мы обучим сеть, предъявив ей реальные примеры запросов, найденных результатов и действий пользователей. Чтобы это сделать, нам необходим алгоритм, который будет изменять веса связей между узлами, так чтобы сеть поняла, как выглядит правильный ответ. Веса следует подстраивать постепенно, поскольку нельзя предполагать, что ответ, выбранный одним пользователем, устроит и всех остальных. Описанный ниже алгоритм называется обратным распространением, поскольку в процессе подстройки весов он продвигается по сети в обратном направлении.

    Для каждого узла из выходного слоя необходимо:
    1. Вычислить разность между текущим и желательным уровнем выходного сигнала.
    2. С помощью функции dtanh определить, насколько должен измениться суммарный входной сигнал для этого узла.
    3. Изменить вес каждой входящей связи пропорционально ее текущему весу и скорости обучения.
    Для каждого узла в скрытом слое необходимо:
    1. Изменить выходной сигнал узла на сумму весов каждой выходной связи, умноженных на величину требуемого изменения выходного сигнала конечного узла этой связи.
    2. С помощью функции dtanh вычислить, насколько должен измениться суммарный входной сигнал для этого узла.
    3. Изменить вес каждой входящей связи пропорционально ее текущему весу и скорости обучения.
    '''
    def backPropagate(self, targets, N = 0.5):
        # calculate errors for output
        output_deltas = [0.0] * len(self.urlids)
        for k in range(len(self.urlids)):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dtanh(self.ao[k]) * error

        # calculate errors for hidden layer
        hidden_deltas = [0.0] * len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.urlids)):
                error = error + output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j]) * error

        # update output weights
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N * change

        # update input weights
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N * change

    '''
    Осталось только написать простой метод, который подготовит сеть, вызовет алгоритм feedforward и запустит обратное распространение.
    '''
    def trainquery(self, wordids, urlids, selectedurl): 
        # generate a hidden node if necessary
        self.generatehiddennode(wordids, urlids)

        self.setupnetwork(wordids, urlids)
        self.feedforward()
        targets = [0.0] * len(urlids)
        targets[urlids.index(selectedurl)] = 1.0
        error = self.backPropagate(targets)
        self.updatedatabase()

    '''
    Для сохранения результатов понадобится метод записи в базу данных новых весов, которые хранятся в переменных экземпляра wi и wo
    '''
    def updatedatabase(self):
        # set them to database values
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.wordids[i], self. hiddenids[j], 0, self.wi[i][j])

        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setstrength(self.hiddenids[j], self.urlids[k], 1, self.wo[j][k])

        self.con.commit()
















'''

mynet = searchnet('nn.db')
mynet.maketables( )
wWorld, wRiver, wBank = 101, 102, 103
uWorldBank, uRiver, uEarth = 201, 202, 203
mynet.generatehiddennode([wWorld, wBank], [uWorldBank, uRiver, uEarth])

for c in mynet.con.execute('select * from wordhidden'): print c
for c in mynet.con.execute('select * from hiddenurl'): print c

'''
 

