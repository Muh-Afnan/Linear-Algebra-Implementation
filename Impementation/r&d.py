# a = [[3,2],[1,2],[1,1]]
# transpose = list(zip(*a))
# for item in transpose:
#     for single in item:
#         print(single)
# print(transpose)
a = [[1,2,3],[3,4,6]]
b = [[1,2],[2,3],[3,4]]
# print(list(zip(*a)))
# array = []
# for idx , list in enumerate(range(len(a))):
#     f"list{idx}" = []
b = list(zip(*b))
print(b)
result = []
for row11 in a:
    row = []
    for row12 in b:
        # print(f"row11: {row11}, row12: {row12}")
        sum = 0
        for item1,item2 in zip(row11,row12):
            sum += item1*item2
        row.append(sum)
    result.append(row)

print(result)



def calculate_minor(self, number, matrix):
    if self.is_square(matrix):
        order = self.find_order(matrix)

        # Base case: 2x2 determinant
        if order[0] == 2 and order[1] == 2:
            val_1 = matrix[0][0] * matrix[1][1]
            val_2 = matrix[0][1] * matrix[1][0]
            det = val_1 - val_2
            return number * det

        # Recursive case
        else:
            det = 0
            for j in range(order[1]):
                val = matrix[0][j]
                matrix_det = self.build_determinate(0, j, matrix)
                minor = self.calculate_minor(val, matrix_det)
                sign = (-1) ** (0 + j)
                det += sign * minor
            return number * det


def build_determinate(self, i, j, matrix):
    # remove row i
    matrix_without_row = matrix[:i] + matrix[i+1:]

    # remove column j
    matrix_without_col = []
    for row in matrix_without_row:
        matrix_without_col.append(row[:j] + row[j+1:])

    return matrix_without_col


def cal_cofactor(self, matrix):
    if self.is_square(matrix):
        order = self.find_order(matrix)
        det = []

        for i in range(order[0]):
            row = []
            for j in range(order[1]):
                val = matrix[i][j]

                matrix_det = self.build_determinate(i, j, matrix)

                deter = self.calculate_minor(1, matrix_det)

                sign = (-1) ** (i + j)

                cofactor = sign * deter

                row.append(cofactor)

            det.append(row)

        return det