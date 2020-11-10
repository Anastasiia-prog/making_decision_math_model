'''
# Целевая функция
def W():
    Ограничения:
    2*x1 + 5*x2 + 2*x3 <= 12
    7*x1 + x2 + 2*x3 <= 18
    x1, x2, x3 >= 0
    return 3*x1 + 4*x2 + 6*x3 -> max

'''

'''
1) Приводим к каноническому виду: Вводим добавочные неотрицательные переменные, 
 если <= то со знаком +, если >=, то со знаком -
 2*x1 + 5*x2 + 2*x3 + x4 = 12
 7*x1 + x2 + 2*x3 + x5 = 18
 Добавили x4, x5
 x1, x2, x3, x4, x5 >= 0
2) Составляем симплекс-таблицу
   x1 x2 x3 x4 x5  свободные члены
x4 2  5  2  1  0         12
x5 7  1  2  0  1         18
  -3 -4 -6  0  0          0    <--- коэффициенты при целевой ф-ции со знаком "-" так как задача на max

3) Выбираем столбец с наименьшей оценкой (у нас это -6 x3)
4) Исходя из пункта 3 выбираем разрешающий элемент:
min(12/2; 18/2) = 6 (строка x4)
5) Далее действуем по правилу прямоугольника: отнимаем из второй строке первую, умноженную на 2/2=1.
Из третьей строки отнимаем элемент из первой строки того же столбца, умноженный на наим. оценку деленную на 2 (-6/2).
Делим первую строку на 2.
Получаем новую таблицу, вводя в базис x3 и выводя из базиса x4.
   x1 x2  x3 x4 x5  свободные члены
x3 1  2.5 1  1  0         6
x5 5  -4  0 -1  1         6
r  3  11  0  3  0            
элементы для r: 1) -3-2*(-6)/2=3; 2) -4-5*(-6)/2=11; 
                3) -6-2*(-6)/2=0; 4) 0-1*(-6)/2=3; 5) 0-0*(-6)/2=0.

6) В последней строке нет отрицательных элементов, значит задача решена.
Ответ: 0, 0, 6
'''

# 1)
# Ограничения
cond1 = [2, 5, 2]
cond2 = [7, 1, 2]
cond = [cond1, cond2]
eq_cond1 = 12
eq_cond2 = 18
eq_cond = [eq_cond1, eq_cond2]
sign = '<='
# Целевая функция
func = [3, 4, 6]
minmax = 'MAX'

# Для приведения к каноническому виду
def kan_form(cond):
    n = []
    for i in range(len(cond)):
        if sign == '<=':
            n.append(1)
        elif sign == '>=':
            n.append(-1)
    return n

# 2) Составляем симплекс-таблицу
n = 4
# Создаем таблицу нужного размера и заполняем нулями
def get_zero_table(cond, n):
    table_zero = [[0] * (len(cond) + n) for i in range(len(cond) + 1)]
    return table_zero

print('table_zero:', get_zero_table(cond, n))
table = get_zero_table(cond, n)

def simplex_table(cond, eq_cond, minmax, table):
    c = 0
    # Добавляем ограничения в таблицу
    for i in range(len(table)):
        for j in range(len(table[i])):
            if i < len(cond) and j < len(cond[i]):
                table[i][j] = cond[i][j]
            else: # Добавляем коэффициенты при добавочных переменных
                if c < len(kan_form(cond)):
                    table[i][j] = kan_form(cond)[c]
                    i += 1
                    c += 1
    # Добавляем свободные члены
    for i in range(len(eq_cond)):
        table[i][-1] = eq_cond[i]
    # Добавляем коэффициенты при целевой функции
    if minmax == 'MAX':
        for i in range(len(func)):
            table[-1][i] = -func[i]
    elif minmax == 'MIN':
        for i in range(len(func)):
            table[-1][i] = func[i]
    return table

print('simplex table:', simplex_table(cond, eq_cond, minmax, table))

# 3) Выбираем столбец с наименьшей оценкой
def find_min_column():
    global min_est, index_min
    if minmax == 'MAX':
        min_est = min(simplex_table(cond, eq_cond, minmax, table)[-1])
        index_min = min(range(len(simplex_table(cond, eq_cond, minmax, table)[-1])), key=simplex_table(cond, eq_cond, minmax, table)[-1].__getitem__)

    return min_est, index_min

print('Наименьшая оценка:', find_min_column()[0], 'Индекс столбца с наименьшей оценкой:', find_min_column()[1])

# 4) Исходя из пункта 3 выбираем разрешающий элемент:
def perm_element():
    lst_for_find_perm_el = []
    current_table = simplex_table(cond, eq_cond, minmax, table)
    for i in range(len(current_table) - 1):
        lst_for_find_perm_el.append(current_table[i][-1]/current_table[i][find_min_column()[1]])
    for_perm_el = min(lst_for_find_perm_el)
    for i in range(len(lst_for_find_perm_el)):
        if lst_for_find_perm_el[i] == for_perm_el:
            ind_perm_el = i
    perm_el = simplex_table(cond, eq_cond, minmax, table)[ind_perm_el][find_min_column()[1]]
    # найдем индекс столбца разрешающего элемента
    row_perm_el = min(range(len(lst_for_find_perm_el)),
                    key=lst_for_find_perm_el.__getitem__)
    return perm_el, row_perm_el

print('Разрешающий элемент:', perm_element()[0], 'Индекс строки разрешающего элемента:', perm_element()[1])

# 5) Перерасчитываем значения симплекс-таблицы и разрешающего элемента,
# пока в последней строке есть отрицательные элементы
from math import fabs

def recalculation_simplex_table_for_max():
    current_table = simplex_table(cond, eq_cond, minmax, table)
    perm_el = perm_element()[0]
    row_ind_perm = perm_element()[1]
    column_ind_perm = find_min_column()[1]
    ###
    fabs_values_from_table = [fabs(i) for i in current_table[-1]]
    ###
    while max(current_table[-1]) < max(fabs_values_from_table):
        for j in range(len(current_table[row_ind_perm])):
            current_table[row_ind_perm][j] = current_table[row_ind_perm][j] / perm_el
        for i in range(len(current_table)):
            for j in range(len(current_table[i])):
                current_table[i][j] = current_table[i][j] - (current_table[row_ind_perm][j] * current_table[i][column_ind_perm]) / perm_el

    return current_table
print('')
print('Перерасчет симплекс-таблицы:')
print(recalculation_simplex_table_for_max())
###############

def old_simplex_table(cond, eq_cond, minmax):
    find_n = kan_form(cond)
    table = [cond[i] + [0] * i + [find_n[i]] + [eq_cond[i]] for i in range(len(find_n))]
    if minmax == 'MAX':
        from_func = []
        for i in func:
            from_func.append(-i)
        table.append(from_func)
    elif minmax == 'MIN':
        table.append(func)
    table[-1].append(0)

    count = 0
    while count != len(find_n):
        table[-1].append(0)
        count += 1
    ###
    table[0][4] = 0
    table[0].append(12)
    ###
    return table

