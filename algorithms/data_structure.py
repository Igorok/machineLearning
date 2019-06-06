# -*- coding: utf-8 -*-

'''
O(n) — линейная сложность
Такой сложностью обладает, например, алгоритм поиска наибольшего элемента в не отсортированном массиве. Нам придётся пройтись по всем n элементам массива, чтобы понять, какой из них максимальный.

O(log n) — логарифмическая сложность
Простейший пример — бинарный поиск. Если массив отсортирован, мы можем проверить, есть ли в нём какое-то конкретное значение, методом деления пополам. Проверим средний элемент, если он больше искомого, то отбросим вторую половину массива — там его точно нет. Если же меньше, то наоборот — отбросим начальную половину. И так будем продолжать делить пополам, в итоге проверим log n элементов.

O(n2) — квадратичная сложность
Такую сложность имеет, например, алгоритм сортировки вставками. В канонической реализации он представляет из себя два вложенных цикла: один, чтобы проходить по всему массиву, а второй, чтобы находить место очередному элементу в уже отсортированной части. Таким образом, количество операций будет зависеть от размера массива как n * n, т. е. n2.


Структуры данных

Линейные структуры данных (или списки) – это упорядоченные структуры, в которых адрес данного однозначно определяется его номером (индексом). Примером может быть список учебной группы.

Табличные структуры данных – это упорядоченные структуры, в которых адрес данных однозначно определяется двумя числами – номером строки и номером столбца, на пересечении которых находится ячейка с искомым элементом. Структуры данных могут быть и трехмерными, тогда три числа характеризуют положение элемента и требуются три типа разделителей.

Иерархические структуры данных – это такие структуры, в которых адрес каждого элемента определяется путем (маршрутом доступа), идущим от вершины структуры к данному элементу. Нерегулярные данные, которые трудно представляются в виде списка или таблицы, могут быть представлены в иерархической структуре. Например, иерархическую структуру образуют почтовые адреса.

Единожды добавленный, элемент остаётся на одном и том же месте по отношению к остальным, пришедшим раньше и позже него. Коллекции такого рода часто называют линейными структурами данных. О линейных структурах можно думать, как об имеющих два конца. Иногда эти концы называют левым и правым, иногда - головой и хвостом.

Стек (иногда говорят "магазин" - по аналогии с магазином огнестрельного оружия) - это упорядоченная коллекция элементов, где добавление нового или удаление существующего всегда происходит только на одном из концов. Стопка книг, подносы в столовой, перемещение по вкладкам браузера кнопкой назад.
'''

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


'''
Проверка открывающихся и закрывающихся скобок
Открывающиеся скобки добавляются в стек, а закрывающаяся сравнивается с последней открывшейся, при этом она удаляется из стека, не соответсвие открывшейся и закрывшейся скобки означает нарушение форматирования
'''
def parChecker(symbolString):
    s = Stack()
    balanced = True
    index = 0
    opens = "([{"
    closers = ")]}"

    def matches(open, close):
        return opens.index(open) == closers.index(close)

    while index < len(symbolString) and balanced:
        symbol = symbolString[index]
        # if this is opened bracket, add symbol to stack
        if symbol in opens:
            s.push(symbol)
        # if this is closed bracket
        elif symbol in closers:
            # if stack is empty- balance is broken
            if s.isEmpty():
                balanced = False
            else:
                # get last opened bracket
                top = s.pop()
                # if closed bracket is not fit to last opened bracket - balance is broken
                if opens.index(top) != closers.index(symbol):
                    balanced = False
        index = index + 1

    if balanced and s.isEmpty():
        return True
    else:
        return False

# print(parChecker('func({{([][])}()})'))
# print(parChecker('func([{()])'))

'''
Конвертирование десятичных чисел в двоичные
При это десятичное число разделяется на 2, затем остаток от деления добавляется в стек, а результат продолжает делиться. По завершению деления необходимо получить символы из стека, остатки от деления в обратном порядке составляют двоичное значение десятичного числа
'''

def divideBy2(decNumber):
    remstack = Stack()

    while decNumber > 0:
        rem = decNumber % 2
        remstack.push(rem)
        decNumber = decNumber // 2

    binString = ""
    while not remstack.isEmpty():
        binString = binString + str(remstack.pop())

    return binString

# print(divideBy2(42))

'''
Очередь - это упорядоченная коллекция элементов, в которой добавление новых происходит с одного конца, называемого “хвост очереди”, а удаление существующих - с другого, “головы очереди”. 
'''
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

'''
Задача Иосифа Флавия или считалка Джозефуса — математическая задача с историческим подтекстом.
Воины, в составе сорока человек, стали по кругу и договорились, что каждые два воина будут убивать третьего, пока не погибнут все. Иосиф Флавий, командовавший этим отрядом, якобы быстро рассчитал, где нужно встать ему и его товарищу, чтобы остаться последними и сдать крепость римлянам.
'''

soldiers = ['soldier ' + str(i + 1) for i in range(10)]
num = 2

def iosifFlavius (s, n):
    q = Queue()
    l = len(s)

    # заполняем очередь, каждый новый элемент добавляется в начало, а предыдущий продвигается вперед
    for i in range(len(s)):
        q.enqueue(s[i])

    # так исчисление идет с 1 а не 0
    i = 1
    # пока размер очереди больше чем 1
    while q.size() > 1:
        # удаляется первый из очереди (последний элемент списка)
        sold = q.dequeue()
        if i % n != 0:
            # если не кратно нужному числу, помещается в конец очереди (в начало списка)
            q.enqueue(sold)
            i = i + 1
        else:
            # кратно нужно числу, возобновляю отсчет
            i = 1

    # последний оставшийся
    return q.dequeue()


# print('iosifFlavius', iosifFlavius(soldiers, num))

'''
Дек имеет структуру упорядоченной коллекции элементов, которые могут добавляться и удаляться с любого конца - и с головы, и с хвоста.
'''
class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)

    def addRear(self, item):
        self.items.insert(0, item)

    def removeFront(self):
        return self.items.pop()

    def removeRear(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

'''
Палиндромом называют строку, которая одинаково читается справа налево и слева направо. Например, radar, toot или madam. Мы хотим создать алгоритм, принимающий на вход строку символов и проверяющий, является ли она палиндромом.
'''

def palchecker(aString):
    chardeque = Deque()
    
    # превращаем строку в заполненый дек
    for ch in aString:
        chardeque.addRear(ch)

    # проверка соответствия
    stillEqual = True

    # если дек опустел или остался последний символ то условия для палиндрома соблюдены
    while chardeque.size() > 1 and stillEqual:
        # первый символ
        first = chardeque.removeFront()
        # последний символ
        last = chardeque.removeRear()
        # если символы не равны, условие нарушилось
        if first != last:
            stillEqual = False

    return stillEqual

# print(palchecker("lsdkjfskf"))
# print(palchecker("radar"))

'''
Граф — абстрактный математический объект, представляющий собой множество вершин графа и набор рёбер, то есть соединений между парами вершин. Например, за множество вершин можно взять множество аэропортов, обслуживаемых некоторой авиакомпанией, а за множество рёбер взять регулярные рейсы этой авиакомпании между городами.

Вершина (иногда её называют узел) - основная часть графа. Может иметь имя, которое называется ключ. Также вершина может обладать дополнительной информацией, которую мы будем называть полезной нагрузкой.

Ребро (или дуга) - другая фундаментальная часть графа. Ребро, соединяющее две вершины, показывает наличие между ними определённых отношений. Рёбра могут быть одно- и двунаправленными. Если все рёбра графа однонаправленные, то мы называем его направленным графом. 

Вес - рёбра могут иметь вес, показывающий стоимость перемещения от одной вершины к другой. Например, в графе дорог, связывающих города, вес ребра может отображать расстояние между двумя населёнными пунктами.

Путь в графе - это последовательность вершин, соединённых рёбрами.

Цикл в направленном графе начинается и заканчивается в одной и той же вершине.

Есть две широко известные реализации графа: матрица смежности и список смежности. 

Одним из простейших способов реализовать граф является использование двумерной матрицы. Таблица осями которой являются вершины графа, если они связаны то значением являются ребра.

Более пространственно-экономичным способом реализации разреженного графа является использование списка смежности. Список, внутри которого списки содержащие связаные вершины.

'''
# вершина
class Vertex:
    def __init__(self, num):
        self.id = num
        self.connectedTo = {}
        self.color = 'white'
        self.dist = 1000
        self.pred = None
        self.disc = 0
        self.fin = 0

    # def __lt__(self,o):
    #     return self.id < o.id
    
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight
        
    def setColor(self,color):
        self.color = color
        
    def setDistance(self,d):
        self.dist = d

    def setPred(self,p):
        self.pred = p

    def setDiscovery(self,dtime):
        self.disc = dtime
        
    def setFinish(self,ftime):
        self.fin = ftime
        
    def getFinish(self):
        return self.fin
        
    def getDiscovery(self):
        return self.disc
        
    def getPred(self):
        return self.pred
        
    def getDistance(self):
        return self.dist
        
    def getColor(self):
        return self.color
    
    def getConnections(self):
        return self.connectedTo.keys()
        
    def getWeight(self,nbr):
        return self.connectedTo[nbr]
                
    def __str__(self):
        return str(self.id) + ":color " + self.color + ":disc " + str(self.disc) + ":fin " + str(self.fin) + ":dist " + str(self.dist) + ":pred \n\t[" + str(self.pred)+ "]\n"
    
    def getId(self):
        return self.id

# граф
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    # вершины
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    # ребра
    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

"""
g = Graph()
for i in range(6):
    g.addVertex(i)

print('g', g)

g.addEdge(0,1,5)
g.addEdge(0,5,2)
g.addEdge(1,2,4)
g.addEdge(2,3,9)
g.addEdge(3,4,7)
g.addEdge(3,5,3)
g.addEdge(4,0,1)
g.addEdge(5,4,8)
g.addEdge(5,2,1)

for v in g:
    for w in v.getConnections():
        print("( %s , %s )" % (v.getId(), w.getId()))
"""


'''
Задача о словесной лестнице
В начале изучения алгоритмов для графов, давайте рассмотрим следующую головоломку, которая называется словесная лестница. Требуется преобразовать слово FOOL в слово SAGE. Изменения должны происходить постепенно, по букве за раз. На каждом шаге вы должны трансформировать слово в другое слово, а не в бессмыслицу. Словесная лестница была изобретена в 1878 году Льюисом Кэрролом - автором Алисы в Стране Чудес.
FOOL
POOL
POLL
POLE
PALE
SALE
SAGE
1) первый вариант создать список слов, потом сравнить их все друг с другом
2) сгруппировать слова используя _ вместо одной буквы
_ope
pope
rope
nope
...

p_pe
pope
pipe
pape
...

po_e
pope
pole
pore
...

При обработке каждого слова в списке мы сравниваем его с корзинами, используя _ для произвольной подстановки. 
'''

def buildGraph(wordFile):
    d = {}
    g = Graph()
    wfile = open(wordFile, 'r')
    # группировка слов, с заменой букв от 1 до последней на _
    for line in wfile:
        word = line[:-1]
        word = word.lower()

        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i+1:]
            if bucket in d:
                d[bucket].append(word)
            else:
                d[bucket] = [word]

    # перебор групп
    for bucket in d.keys():
        # перебор всех слов в группе
        for word1 in d[bucket]:
            # сравнение текущего слова со всеми в группе и добавление ребра в граф
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1, word2)
    return g

'''
Поиск в ширину - breadth first search
Чтобы отслеживать своё продвижение, BFS окрашивает каждую вершину в белый, серый или чёрный цвета. Все вершины при создании инициализируются белым. Когда вершина обнаруживается в первый раз, то ей задаётся серый цвет. Когда же BFS её полностью исследует, вершина окрашивается в чёрный. Это означает, что не существует смежных с ней белых вершин. С другой стороны, серый узел может иметь несколько связанных с ним белых вершин, показывая, что у нас ещё есть пространство для исследования.
'''


'''
Принимает начальную вершину графа, потом проходит по всем связанным вершинам - дочерним, и добавляет их в очередь. После этого из очереди берется первая дочерняя вершина, потом вторая и далее, а их связи попадают в конец очереди.

sage
sale
pale
pall
poll
pool
fool
'''
def bfs(g, start):
    # расстояние 0
    start.setDistance(0)
    # предок None
    start.setPred(None)

    # инициализация очереди
    vertQueue = Queue()
    vertQueue.enqueue(start)

    # пока очередь не закончилась
    while (vertQueue.size() > 0):
        # текущая вершина
        currentVert = vertQueue.dequeue()

        # все связанные вершины, они станут дочерними
        for nbr in currentVert.getConnections():
            # связанная вершина, если она еще не оказывалась в очереди и имеет белый цвет:
            # устанавливаем ей цвет, дистанцию, родителя и добавляем в очередь для анализа ее связей
            if (nbr.getColor() == 'white'):
                # устанавливаем серый цвет
                nbr.setColor('gray')
                # дистанция на единицу больше текущей вершины
                nbr.setDistance(currentVert.getDistance() + 1)
                # текущую вершину устанавливаем как родителя
                nbr.setPred(currentVert)
                # добавляем в очередь
                vertQueue.enqueue(nbr)

        # все связи текущей вершины обработаны, окращиваем в черный
        currentVert.setColor('black')

'''
проходит от заданной вершины, по всем родителям, до начала
'''
def traverse(y):
    x = y
    while (x.getPred()):
        print(x.getId())
        x = x.getPred()
    print(x.getId())


'''
g = buildGraph('word_tree.txt')
bfs(g, g.getVertex('fool'))
traverse(g.getVertex('sage'))
'''


'''
Поиск в глубину - depth first search
Стратегия поиска в глубину, как и следует из названия, состоит в том, чтобы идти «вглубь» графа, насколько это возможно. Алгоритм поиска описывается рекурсивно: перебираем все исходящие из рассматриваемой вершины рёбра. Если ребро ведёт в вершину, которая не была рассмотрена ранее, то запускаем алгоритм от этой нерассмотренной вершины, а после возвращаемся и продолжаем перебирать рёбра. Возврат происходит в том случае, если в рассматриваемой вершине не осталось рёбер, которые ведут в нерассмотренную вершину. Если после завершения алгоритма не все вершины были рассмотрены, то необходимо запустить алгоритм от одной из нерассмотренных вершин
'''

'''
Рекурсивный метод функция получает вершину, и рекурсивно запускает себя для всех потомков помечая их как пройденные, пока они не закончатся.

sage
page
pape
pipe
pope
pole
pale
pall
poll
pool
fool

'''
def dfs_recursion (start):
    for nbr in start.getConnections():
        if (nbr.getColor() == 'white'):
            # устанавливаем серый цвет
            nbr.setColor('gray')
            # дистанция на единицу больше текущей вершины
            nbr.setDistance(start.getDistance() + 1)
            # текущую вершину устанавливаем как родителя
            nbr.setPred(start)
            
            dfs_recursion(nbr)

'''
g = buildGraph('word_tree.txt')
start = g.getVertex('fool')
start.setDistance(0)
start.setPred(None)
start.setColor('gray')

dfs_recursion(start)

traverse(g.getVertex('sage'))
'''



'''
Не рекурсивный обход, принимает старт, помещает его в стек, далее помечает как пройденный, все дочерние элементы попадают в стек, из стека берется последний попавший в него элемент, который будет дочерним элементом а не соседним, как в случает с обходом в ширину.

sage
page
pale
pall
fall
fail
foil
fool
'''
def dfs_not_recursion (g, start):
    start.setDistance(0)
    start.setPred(None)

    stack = [start]

    while (len(stack) > 0):
        currentVert = stack.pop()
        currentVert.setColor('gray')

        for nbr in currentVert.getConnections():
            if (nbr.getColor() == 'white'):
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                stack.append(nbr)

'''
g = buildGraph('word_tree.txt')
dfs_not_recursion(g, g.getVertex('fool'))
traverse(g.getVertex('sage'))
'''

'''
Дерево
Является связным графом, не содержащим циклы.
Узел - это основная часть дерева. 
Ветвь - соединяет два узла вместе, показывая наличие между ними определённых отношений. Каждый узел (кроме корня) имеет ровно одну входящую ветвь. При этом он может иметь несколько исходящих ветвей.
Корень дерева - единственный узел, не имеющий входящих ветвей. 
Путь - это упорядоченный список узлов, соединённых ветвями. 
Дети (потомки) -набор узлов c, имеющих входящие ветви от одного узла, называются его детьми. 
Родитель (предок) - Узел является родителем всех узлов, с которыми связан исходящими ветвями. 
Братья - Узлы дерева, являющиеся детьми одного родителя, называют братьями.
Поддерево - это набор узлов и ветвей, состоящий родителя и всех его потомков.
Лист - это узел, у которого нет детей.
Уровень узла n - это число ветвей в пути от корня до n. 
Высота дерева равна максимальному уровню любого его узла. 


Бинарное дерево поиска - структура данных для работы с упорядоченными множествами, обладает следующим свойством: если x — узел бинарного дерева с ключом k, то все узлы в левом поддереве должны иметь ключи, меньшие k, а в правом поддереве большие k.
Есть три операции обхода узлов дерева, отличающиеся порядком обхода узлов:
inorderTraversal — обход узлов в отсортированном порядке,
preorderTraversal — обход узлов в порядке: вершина, левое поддерево, правое поддерево,
postorderTraversal — обход узлов в порядке: левое поддерево, правое поддерево, вершина.

'''

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    # insert data to tree
    def insert(self, data):
        newNode = Node(data)
        if self.root is None:
            self.root = newNode
        else:
            self.insertNode(self.root, newNode)

    # insert new vertex
    def insertNode(self, node, newNode):
        # insert to left less value
        if newNode.data < node.data:
            if node.left is None:
                node.left = newNode
            else:
                self.insertNode(node.left, newNode)
        # insert to right bigger value
        else:
            if node.right is None:
                node.right = newNode
            else:
                self.insertNode(node.right, newNode)

    # remove value
    def remove(self, data):
        self.root = self.removeNode(self.root, data)

    # remove vertex by data
    def removeNode(self, node, data):
        # if vertext empty
        if node is None:
            return None
        # if less remove left
        elif node.data < data:
            self.removeNode(node.left, data)
            return node
        # if bigger remove right
        elif node.data > data:
            self.removeNode(node.right, data)
            return node
        else:
            # remove vertext without children
            if node.left is None and node.right is None:
                node = None
                return node
            # remove vertext with one children, change value to children
            elif node.left is None:
                node = node.right
                return node
            elif node.right is None:
                node = node.left
                return node

            # remove vertex with child
            # find less value from right
            # make this new vertext
            # and remove from right
            aux = self.findMinNode(node.right)
            node.data = aux.data
    
            node.right = this.removeNode(node.right, aux.data)
            return node

    def findMinNode(self, node):
        if node.left is None:
            return node
        else:
            return self.findMinNode(node.left)

    # Algorithm for inorder:
    # Traverse the left subtree i.e perform inorder on left subtree
    # Visit the root
    # Traverse the right subtree i.e perform inorder on right subtree
    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.data)
            self.inorder(node.right)

    # Algorithm for preoder:
    # Visit the root
    # Traverse the left subtree i.e perform inorder on left subtree
    # Traverse the right subtree i.e perform inorder on right subtree
    def preorder(self, node):
        if node is not None:
            print(node.data)
            self.preorder(node.left)
            self.preorder(node.right)

    # Algorithm for postorder:
    # Traverse the left subtree i.e perform inorder on left subtree
    # Traverse the right subtree i.e perform inorder on right subtree
    # Visit the root
    def postorder(self, node):
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.data)

    # returns root of the tree 
    def getRootNode(self):
        return self.root

    # search for a node with given data 
    def search(self, node, data):
        # not found
        if node is None:
            return None
        # if less search left
        elif node.data < data:
            return self.search(node.left, data)
        # if bigger search right
        elif node.data > data:
            return self.search(node.right, data)
        # found
        else:
            return node

'''
bst = BinarySearchTree()
values = (15, 25, 10, 7, 22, 17, 13, 5, 9, 27)
for v in values:
    bst.insert(v)

print('inorder')
bst.inorder(bst.getRootNode())
print('preorder')
bst.preorder(bst.getRootNode())
print('postorder')
bst.postorder(bst.getRootNode())
'''