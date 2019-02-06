# collaborative filtering
'''
Обычно алгоритм коллаборативной фильтрации работает следующим образом: просматривает большую группу людей и отыскивает в ней меньшую группу с такими же вкусами, как у вас. Он смотрит, какие еще вещи им нравятся, объединяет предпочтения и создает ранжированный список предложений. Есть несколько способов решить, какие
люди похожи, и объединить их предпочтения в список.
'''

# dictionary of user's ratings
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    }
}

'''
Один из самых простых способов вычисления оценки подобия – это евклидово расстояние. Составляется система координат из двух фильмов, рейтинг пользователей размещается как точки, расстояние между точками рассчитывается по теореме пифагора: сумма квадратов катетов равна квадрату гипотенузы. Следовательно расстояние между точками равно корню квадратному из суммы квадратов разницы координат.

Расстояние, вычисленное по этой формуле, будет тем меньше, чем больше сходства между людьми. Однако нам нужна функция, значение которой тем больше, чем люди более похожи друг на друга. Этого можно добиться, добавив к вычисленному расстоянию 1 (чтобы никогда не делить на 0) и взяв обратную величину
'''


from math import sqrt

# Возвращает оценку подобия person1 и person2 на основе расстояния
def sim_distance(person1, person2):
    # Получить список предметов, оцененных обоими
    si={}
    for item in critics[person1]:
        if item in critics[person2]:
            si[item]=1

    # Если нет ни одной общей оценки, вернуть 0
    if len(si) == 0: return 0

    # Сложить квадраты разностей
    sum_of_squares = 0
    for item in critics[person1]:
        if item in critics[person2]:
            sum_of_squares = sum_of_squares + pow(critics[person1][item] - critics[person2][item], 2)

    return 1 / (1 + sum_of_squares)


# compare all users by euclidean distance
def euclidean_distance():
    critics_names = list(critics.keys())
    critics_compare = {}

    # get every user from names
    i = 0
    while i < len(critics_names):
        name1 = critics_names[i]
        j = i + 1

        # get all users after previous
        while j < len(critics_names):
            name2 = critics_names[j]
            comp = ', '.join(sorted([name1, name2]))
            critics_compare[comp] = sim_distance(name1, name2)
            j = j + 1

        i = i + 1

    critics_list = []
    for key in critics_compare.keys():
        critics_list.append({
            'users': key,
            'rating': critics_compare[key]
        })

    critics_list = sorted(critics_list, key=lambda value: -1 * value['rating'])

    print('critics_list', critics_list)

euclidean_distance()

"""
[{
    'users': 'Gene Seymour, Jack Matthews',
    'rating': 0.8
}, {
    'users': 'Claudia Puig, Michael Phillips',
    'rating': 0.5714285714285714
}, {
    'users': 'Lisa Rose, Michael Phillips',
    'rating': 0.4444444444444444
}, {
    'users': 'Lisa Rose, Mick LaSalle',
    'rating': 0.3333333333333333
}, {
    'users': 'Mick LaSalle, Toby',
    'rating': 0.3076923076923077
}, {
    'users': 'Claudia Puig, Lisa Rose',
    'rating': 0.2857142857142857
}, {
    'users': 'Michael Phillips, Mick LaSalle',
    'rating': 0.2857142857142857
}, {
    'users': 'Michael Phillips, Toby',
    'rating': 0.2857142857142857
}, {
    'users': 'Claudia Puig, Toby',
    'rating': 0.23529411764705882
}, {
    'users': 'Lisa Rose, Toby',
    'rating': 0.2222222222222222
}, {
    'users': 'Jack Matthews, Lisa Rose',
    'rating': 0.21052631578947367
}, {
    'users': 'Gene Seymour, Michael Phillips',
    'rating': 0.21052631578947367
}, {
    'users': 'Jack Matthews, Michael Phillips',
    'rating': 0.18181818181818182
}, {
    'users': 'Claudia Puig, Jack Matthews',
    'rating': 0.18181818181818182
}, {
    'users': 'Claudia Puig, Mick LaSalle',
    'rating': 0.17391304347826086
}, {
    'users': 'Gene Seymour, Lisa Rose',
    'rating': 0.14814814814814814
}, {
    'users': 'Jack Matthews, Mick LaSalle',
    'rating': 0.13793103448275862
}, {
    'users': 'Claudia Puig, Gene Seymour',
    'rating': 0.13333333333333333
}, {
    'users': 'Gene Seymour, Mick LaSalle',
    'rating': 0.12903225806451613
}, {
    'users': 'Jack Matthews, Toby',
    'rating': 0.11764705882352941
}, {
    'users': 'Gene Seymour, Toby',
    'rating': 0.10810810810810811
}]
"""