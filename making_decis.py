# Стратегии платежной матрицы
N = 3
A1 = [30 + N, 10, 20, 25 + N/2]
A2 = [50, 70 - N, 10 + N/2, 25]
A3 = [25 - N/2, 35, 40, 60 - N/2]
matrix_A = [A1, A2, A3]
# Вероятности наступления исходов со стороны оппонента
q1 = 0.3
q2 = 0.2
q3 = 0.4
q4 = 0.1
q = [q1, q2, q3, q4]
# Функция для поиска оптимальной стратегии
def find_strategy(strategies):
    maximum = strategies[0]
    ind = 0
    for i in range(1, len(strategies)):
        if strategies[i] > maximum:
            maximum = strategies[i]
            ind = i
    return ind + 1, maximum

# Критерий Байеса
def for_Bayes_and_Lapl_cr(A, q=q):
    summ = 0
    i = 0
    for element in A:
        summ += element*q[i]
        i += 1
    return summ

strategies_bayes = [for_Bayes_and_Lapl_cr(A1), for_Bayes_and_Lapl_cr(A2), for_Bayes_and_Lapl_cr(A3)]
print(f'По критерию Байеса выбираем стратегию {find_strategy(strategies_bayes)[0]} со значением', find_strategy(strategies_bayes)[1])
# Критерий Лапласа
P = 4
q2 = [1/P for i in range(P)]
strategies_laplas = [for_Bayes_and_Lapl_cr(A1, q2), for_Bayes_and_Lapl_cr(A2, q2), for_Bayes_and_Lapl_cr(A3, q2)]
print(f'По критерию Лапласа выбираем стратегию {find_strategy(strategies_laplas)[0]} со значением', find_strategy(strategies_laplas)[1])
# Критерий Вальда
def Vald_cr(matrix_A):
    maxi = find_strategy(matrix_A)[0]
    return maxi + 1, min(matrix_A[maxi])

print(f'По критерию Вальда выбираем стратегию {Vald_cr(matrix_A)[0]} со значением', Vald_cr(matrix_A)[1])
# Критерий Сэвиджа
# Рассчитываем матрицу рисков
# Столбцы
def columns(n, matrix_A=matrix_A, A2=A2):
    return [A2[n] - matrix_A[i][n] for i in range(len(matrix_A))]
ri1 = columns(0)
ri2 = columns(1)
ri3 = columns(2, A2=A3)
ri4 = columns(3, A2=A3)
matr = [ri1, ri2, ri3, ri4]
def Sev_cr(n, matr=matr):
    row = []
    for i in range(len(matr)):
        row.append(matr[i][n])
    return max(row)
Sev = [Sev_cr(0), Sev_cr(1), Sev_cr(2)]
minim = min(Sev)
index_min = min(range(len(Sev)), key=Sev.__getitem__)
print(f'По критерию Сэвиджа выбираем стратегию {index_min+1} со значением', minim)
# Критерий Гурвица
# Выбираем y=0.5
def Gurv_cr(A, y=0.5):
    return y*min(A) + (1-y)*max(A)
Gurv = [Gurv_cr(A1), Gurv_cr(A2), Gurv_cr(A3)]
index_max = max(range(len(Gurv)), key=Gurv.__getitem__)
print(f'По критерию Гурвица выбираем стратегию {index_max+1} со значением', max(Gurv))