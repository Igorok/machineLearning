# -*- coding: utf-8 -*-
'''
Кластерный анализ - многомерная статистическая процедура, выполняющая сбор данных, содержащих информацию о выборке объектов, и затем упорядочивающая объекты в сравнительно однородные группы.
Цели кластеризации:
    Понимание данных путём выявления кластерной структуры. Разбиение выборки на группы схожих объектов позволяет упростить дальнейшую обработку данных и принятия решений, применяя к каждому кластеру свой метод анализа (стратегия «разделяй и властвуй»).
    Сжатие данных. Если исходная выборка избыточно большая, то можно сократить её, оставив по одному наиболее типичному представителю от каждого кластера.
    Обнаружение новизны. Выделяются нетипичные объекты, которые не удаётся присоединить ни к одному из кластеров.
'''


from PIL import Image,ImageDraw

def readfile(filename):
    lines=[line for line in open(filename)]

    # First line is the column titles
    colnames=lines[0].strip().split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames,colnames,data

from math import sqrt

def pearson(v1,v2):
    # Simple sums
    sum1=sum(v1)
    sum2=sum(v2)

    # Sums of the squares
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])

    # Sum of the products
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 0

    return 1.0-num/den

'''
Алгоритм иерархической кластеризации строит иерархию групп, объединяя на каждом шаге две самые похожие группы. В начале каждая
группа состоит из одного элемента, в данном случае – одного блога. На каждой итерации вычисляются попарные расстояния между группами, и группы, оказавшиеся самыми близкими, объединяются в новую группу. Так повторяется до тех пор, пока не останется всего одна группа.
'''
class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance

def hcluster(rows,distance=pearson):
    distances={}
    currentclustid=-1

    # Clusters are initially just the rows
    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]

    while len(clust)>1:
        lowestpair=(0,1)
        closest=distance(clust[0].vec,clust[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d<closest:
                    closest=d
                    lowestpair=(i, j)

        # calculate the average of the two clusters
        mergevec=[
        (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
        for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster=bicluster(mergevec,left=clust[lowestpair[0]],
                                right=clust[lowestpair[1]],
                                distance=closest,id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printclust(clust,labels=None,n=0):
    # indent to make a hierarchy layout
    for i in range(n): print(' '),
    if clust.id<0:
        # negative id means that this is branch
        print('-')
    else:
        # positive id means that this is an endpoint
        if labels==None: print(clust.id)
        else: print(labels[clust.id])

    # now print the right and left branches
    if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)


# blognames, words, data = readfile('blogdata.txt')
# clust = hcluster(data)
# printclust(clust, labels = blognames)


'''
Интерпретацию кластеров можно облегчить, если изобразить их в виде дендрограммы. Результаты иерархической кластеризации обычно так и представляются.
'''

def getheight(clust):
    # Is this an endpoint? Then the height is just 1
    if clust.left==None and clust.right==None: return 1

    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left==None and clust.right==None: return 0

    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    # height and width
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)

    # width is fixed, so scale distances accordingly
    scaling=float(w-150)/depth

    # Create a new image with a white background
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    # Draw the first node
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')

def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id < 0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        # Line length
        ll=clust.distance*scaling
        # Vertical line from this cluster to children
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        # Horizontal line to left item
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

        # Horizontal line to right item
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        # Call the function to draw the left and right nodes
        drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
        drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x+5,y-7),labels[clust.id],(0,0,0))



'''
Часто бывает необходимо выполнить кластеризацию одновременно по строкам и столбцам. В маркетинговых исследованиях интересно сгруппировать людей с целью выявления общих демографических признаков или предпочитаемых товаров, а быть может, для того чтобы выяснить, на каких полках размещены товары, которые обычно покупают вместе. В наборе данных о блогах столбцы представляют слова, и можно поинтересоваться, какие слова часто употребляют вместе.
Простейший способ решить эту задачу с помощью уже написанных функций – повернуть весь набор данных, так чтобы столбцы (слова) стали строками. Тогда списки чисел в каждой строке покажут, сколько раз данное слово встречалось в каждом блоге.
'''
def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])):
        newrow=[data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata

# blognames, words, data = readfile('blogdata.txt')
# data = rotatematrix(data)
# wordclust = hcluster(data)
# drawdendrogram(wordclust, labels=words, jpeg='wordclust.jpg')


'''
Кластеризация методом K-средних начинается с выбора k случайно расположенных центроидов (точек, представляющих центр кластера). Каждому элементу назначается ближайший центроид. После того как назначение выполнено, каждый центроид перемещается в точку, рассчитываемую как среднее по всем приписанным к нему элементам. Затем назначение выполняется снова. Эта процедура повторяется до тех пор, пока назначения не прекратят изменяться. На рис. 3.5 показано, как развивается процесс для пяти элементов и двух кластеров.
'''
import random
def kcluster(rows, distance = pearson, k = 4):
    # Determine the minimum and maximum values for each point
    # max and min values for every word, from all blogs
    ranges=[
        (min([row[i] for row in rows]), max([row[i] for row in rows]))
        for i in range(len(rows[0]))
    ]

    # Create k randomly placed centroids
    clusters= [
        [
            random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
            for i in range(len(rows[0]))
        ] for j in range(k)
    ]

    lastmatches = None
    for t in range(100):
        print('Iteration %d' % t)
        bestmatches=[[] for i in range(k)]

        # Find which centroid is the closest for each row
        # every blog
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            # for every cluster
            for i in range(k):
                # distance between current cluster and current blog
                d = distance(clusters[i], row)
                # if distance is less that best distance, set this distance as best
                if d < distance(clusters[bestmatch], row): bestmatch = i
            # push the blog to most similar cluster
            bestmatches[bestmatch].append(j)

        # If the results are the same as last time, this is complete
        if bestmatches == lastmatches: break
        lastmatches = bestmatches

        # Move the centroids to the average of their members
        # every cluster
        for i in range(k):
            # list of zeros for every word in cluster
            avgs = [0.0] * len(rows[0])
            # most similar blogs for cluster
            if len(bestmatches[i]) > 0:
                # every blog from similars
                for rowid in bestmatches[i]:
                    # every word from blog
                    for m in range(len(rows[rowid])):
                        # sum of words
                        avgs[m] += rows[rowid][m]
                # every word in cluster
                for j in range(len(avgs)):
                    # every word in cluster will equal average value from all best blogs
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches

blognames, words, data = readfile('blogdata.txt')
kclust = kcluster(data)

for k in kclust:
    print('cluster', k)
    for r in k:
        print(blognames[r])

'''
Для набора данных о блогах, где значениями являются счетчики слов, коэффициент корреляции Пирсона работает неплохо. Но в данном случае у нас есть лишь единицы и нули, представляющие соответственно наличие и отсутствие, и было бы полезнее определить некую меру перекрытия между людьми, желающими иметь два предмета. Такая мера существует и называется коэффициентом Танимото; это отношение мощности пересечения множеств (элементов, принадлежащих обоим множествам) к мощности их объединения (элементов, принадлежащих хотя бы одному множеству).
'''
def tanamoto(v1, v2):
    c1, c2, shr = 0, 0, 0

    for i in range(len(v1)):
        if v1[i] != 0: c1+=1 # in v1
        if v2[i] != 0: c2+=1 # in v2
        if v1[i] != 0 and v2[i] != 0: shr += 1 # in both

    return 1.0 - (float(shr) / (c1 + c2 - shr))


'''
Чтобы понять, как соотносятся различные предметы, было бы полезно видеть их на странице и оценивать степень
схожести по близости. В этом разделе мы ознакомимся с методом многомерного шкалирования, позволяющим найти двумерное представление набора данных. Этот алгоритм принимает на входе различие между каждой парой предметов и пытается нарисовать диаграмму так, чтобы расстояния между точками, соответствующими предметам, отражали степень их различия. Для этого сначала вычисляются желаемые расстояния между всеми предметами. В случае набора данных
о блогах для сравнения предметов применялся коэффициент корреляции Пирсона.

Затем все предметы (в данном случае блоги) случайным образом размещаются на двумерной диаграмме. Вычисляются попарные евклидовы расстояния между всеми текущими положениями предметов.

Для каждой пары предметов желаемое расстояние сравнивается с текущим и вычисляется расхождение. Каждый предмет приближается или отодвигается от своего соседа пропорционально расхождению между ними. 

Каждый узел перемещается под воздействием всех остальных узлов, которые притягивают или отталкивают его. После каждого такого перемещения разница между текущими и желаемыми расстояниями немного уменьшается. Эта процедура повторяется многократно и прекращается, когда общее расхождение не удается уменьшить за счет перемещения предметов. Реализующая ее функция принимает вектор данных и возвращает массив с двумя столбцами, содержащими координаты X и Y предметов на двумерной диаграмме.

'''
def scaledown(data, distance = pearson, rate = 0.01):
    n = len(data)

    # The real distances between every pair of items
    realdist = [
        [distance(data[i], data[j]) for j in range(n)]
        for i in range(0, n)
    ]

    # Randomly initialize the starting points of the locations in 2D
    loc=[[random.random(),random.random()] for i in range(n)]
    fakedist=[[0.0 for j in range(n)] for i in range(n)]

    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2)
                                        for x in range(len(loc[i]))]))

        # Move points
        grad=[[0.0, 0.0] for i in range(n)]

        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                # The error is percent difference between the distances
                errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]

                # Each point needs to be moved away from or towards the other
                # point in proportion to how much error it has
                grad[k][0] += ((loc[k][0] - loc[j][0]) / fakedist[j][k]) * errorterm
                grad[k][1] += ((loc[k][1] - loc[j][1]) / fakedist[j][k]) * errorterm

                # Keep track of the total error
                totalerror += abs(errorterm)

        print('totalerror', totalerror)

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]

    return loc

def draw2d(data, labels, jpeg = 'mds2d.jpg'):
    img = Image.new('RGB',(2000,2000),(255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x=(data[i][0] + 0.5) * 1000
        y=(data[i][1] + 0.5) * 1000
        draw.text((x, y), labels[i], (0, 0, 0))
    img.save(jpeg, 'JPEG')



blognames, words, data = readfile('blogdata.txt')
coords = scaledown(data)
draw2d(coords, blognames, jpeg = 'blogs2d.jpg')


# blognames, words, data = readfile('blogdata.txt')
# clust = hcluster(data)
# drawdendrogram(clust, blognames, jpeg='blogclust.jpg')