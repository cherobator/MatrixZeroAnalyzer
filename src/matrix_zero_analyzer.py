def count_zeros(matrix):
    n = len(matrix)
    up_main = 0
    down_main = 0
    up_side = 0
    down_side = 0

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                if j > i:
                    up_main += 1
                elif i > j:
                    down_main += 1

                if i + j < n - 1:
                    up_side += 1
                elif i + j > n - 1:
                    down_side += 1

    return up_main, down_main, up_side, down_side


def read_matrix():
    n = int(input("Введите размерность матрицы n: "))
    print(f"Введите элементы матрицы {n}x{n} построчно через пробел:")
    matrix = []
    for _ in range(n):
        row = input().split()
        matrix.append([float(num) for num in row])
    return matrix


def main():
    matrix = read_matrix()
    up_main, down_main, up_side, down_side = count_zeros(matrix)

    print("\nИсходная матрица:")
    for row in matrix:
        print(" ".join(map(str, row)))

    print("\nРезультаты анализа:")
    print("Количество нулей выше главной диагонали:", up_main)
    print("Количество нулей ниже главной диагонали:", down_main)
    print("Количество нулей выше побочной диагонали:", up_side)
    print("Количество нулей ниже побочной диагонали:", down_side)


if __name__ == "__main__":
    main()