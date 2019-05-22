# -*- coding: utf-8 -*-

'''
Структуры данных

Линейные структуры данных (или списки) – это упорядоченные структуры, в которых адрес данного однозначно определяется его номером (индексом). Примером может быть список учебной группы.

Табличные структуры данных – это упорядоченные структуры, в которых адрес данных однозначно определяется двумя числами – номером строки и номером столбца, на пересечении которых находится ячейка с искомым элементом. Структуры данных могут быть и трехмерными, тогда три числа характеризуют положение элемента и требуются три типа разделителей.

Иерархические структуры данных – это такие структуры, в которых адрес каждого элемента определяется путем (маршрутом доступа), идущим от вершины структуры к данному элементу. Нерегулярные данные, которые трудно представляются в виде списка или таблицы, могут быть представлены в иерархической структуре. Например, иерархическую структуру образуют почтовые адреса.

Единожды добавленный, элемент остаётся на одном и том же месте по отношению к остальным, пришедшим раньше и позже него. Коллекции такого рода часто называют линейными структурами данных. О линейных структурах можно думать, как об имеющих два конца. Иногда эти концы называют левым и правым, иногда - головой и хвостом.

Стек (иногда говорят "магазин" - по аналогии с магазином огнестрельного оружия) - это упорядоченная коллекция элементов, где добавление нового или удаление существующего всегда происходит только на одном из концов. Стопка книг, подносы в столовой, перемещение по вкладкам браузера кнопкой назад.
'''

# Проверка открывающихся и закрывающихся скобок

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




print(parChecker('func({{([][])}()})'))
print(parChecker('func([{()])'))