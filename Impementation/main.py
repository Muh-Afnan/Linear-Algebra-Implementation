class MatrixValidation:
    def validate_addition(self,array):
        try:
            orders = [self.find_order(matrix) for matrix in array]
            if len(set(orders))!=1:
                raise ValueError("Matrix dimensions not compatible for addition")
            return True
        except ValueError as e:
            return False
    
    def validate_dot_product(self, array):
        try:
            orders = [self.find_order(matrix) for matrix in array]
            for idx in range(len(orders)-1):
                if orders[idx][1] != orders[idx+1][0]:
                    raise ValueError("Matrix dimensions not compatible for multiplication")
            return True
        except ValueError as e:
            print(e)
            return False
        
    def find_order(self,matrix):
        try:
            rows = len(matrix)
            if rows<1:
                raise ValueError ("Matrix is Empty")
            cols = [len(row) for row in matrix]
            if len(set(cols))!=1:
                raise ValueError ("Non Equal number of Columns found in rows")
            return (rows,cols[0])
        except ValueError as e:
            print (f"Caught an exception: {e}")
    
    def scalar_addition(self, number, matrix:list[list[int|float]]):
        if self.validate_addition([matrix]):
            transformation = [[item+number for item in row] for row in matrix]
            return transformation
    
    def scalar_multiplication(self, number, matrix:list[list[int|float]]):
        if self.validate_addition([matrix]):
            transformation = [[item*number for item in row] for row in matrix]
            return transformation
    
    def matrix_add(self,matrix1,matrix2):
        result = [[item1+item2 for item1,item2 in zip(row1,row2)] for row1,row2 in zip(matrix1,matrix2)]
        return result

    def matrix_addition(self,matrix:list[list[int|float]], matrix2:list[list[int|float]], *othermartix):
        array = [matrix,matrix2,*othermartix]
        if self.validate_addition(array):
            result = array[0]
            for matrix in array[1:]:
                result = self.matrix_add(result,matrix)
            return result

    def matrix_multiply(self,matrix1, matrix2):
        result = [[item1*item2 for item1,item2 in zip(row1,row2)] for row1,row2 in zip(matrix1,matrix2)]
        return result

    def element_wise_multiplication(self, matrix1,matrix2,*other):
        array = [matrix1, matrix2,*other]
        if self.validate_addition(array):
            result = array[0]
            for matrix in array[1:]:
                result = self.matrix_multiply(result,matrix)
            return result       
    
    def matrix_multiply(self, matrix1,matrix2):
        item2_trans = list(zip(*matrix2))
        result = []
        for m1_row in matrix1:
            row = []
            for m2_row in item2_trans:
                sum = 0
                for item1,item2 in zip(m1_row,m2_row):
                    sum += item1*item2
                row.append(sum)
            result.append(row)
        return result
      
    def matrix_chain_multiply(self,matrix1:list[list[int|float]], matrix2:list[list[int|float]],*othermatrix):
        array = [matrix1,matrix2,*othermatrix]
        try: 
            if self.validate_dot_product(array):
                result = array[0]
                print(f"array: {array}")
                print(f"len: {len(array)}")
                for matrix in array[1:]:
                    result = self.matrix_multiply(result, matrix)
                return result
        except ValueError as e:
            print(f"Matrix Not in order for Dot product")

    def matrix_transpose(self,matrix):
        return list(zip(*matrix))
    
    def row_operation(self,matrix,r1,r2):
        matrix_new = matrix[r1]
        matrix[r1] = matrix[r2]
        matrix[r2] = matrix_new
        return matrix

    def sum_of_diagonal(self,matrix):
        sum = 0
        for row in matrix:
            number = 0
            sum +=row[number]
            number +=1
        return sum
    
    def row_addition(self, matrix,row1,row2):
        sum = [item1+item2 for item1,item2 in zip(matrix[row1-1],matrix[row2-1])]
        matrix[row1-1] = sum
        return matrix
    
    def row_scaling(self,matrix,row,factor):
        scaled_row = [item * factor for item in matrix[row-1]]
        matrix[row-1] = scaled_row
        return matrix
    
    def zero_matrix_check(self,matrix):
        for row in matrix:
            for item in row:
                if item !=0:
                    return False
        return True

# matrix = [[1,2],[112,8],[2,3]]
# matrix2 = [[1,2,3],[112,56,8],[1,2,3]]
# matrix3 = [[1,2,3],[112,56,8],[1,2,3]]
# matrix4 = [[1,2],[2,2]]

m1 = [[1,2,3],[4,5,6]]
m3 = [[1,2],[3,4],[5,6]]
m2 = [[1,2],[3,4],[3,4],[3,4],[3,4]]
m_zero = [[0,0,0],[0,0,0]]

mat_op = MatrixValidation()
# # print(mat_op.validate_addition(matrix,matrix2,matrix3))
# # print(mat_op.scalar_multiplication(matrix=matrix,number=6))
# # print(mat_op.scalar_addition(matrix=matrix,number=6))
# # print(mat_op.matrix_addition(matrix,matrix2))
# print(mat_op.matrix_chain_multiply(m1,m2,m3))
# print(mat_op.sum_of_diagonal(m1))
# print(mat_op.zero_matrix_check(m_zero))
# print(mat_op.zero_matrix_check(m1))

# print(mat_op.row_addition(m1,1,2))
(print(mat_op.sum_of_diagonal(m2)))






