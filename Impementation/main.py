import array

from streamlit import empty


class MatrixValidation:
    def validate_addition(self,array):
        try:
            orders = [self.find_order(matrix) for matrix in array]
            if len(set(orders))==1:
                return True
        except ValueError as e:
            return False
    
    def find_order(self,matrix):
        try:
            rows = len(matrix)
            if rows<1:
                raise ValueError ("Matrix is Empty")
            cols = [len(item) for item in matrix]
            if len(set(cols))!=1:
                raise ValueError ("Non Equal number of Columns found in rows")
            return (rows , cols[0])
        except ValueError as e:
            print (f"Caught an exception: {e}")
    
    def scalar_addition(self, number, matrix:list[list[int|float]]):
        self.validate_addition([matrix])
        transformation = [[item+number for item in row] for row in matrix]
        return transformation
    
    def scalar_multiplication(self, number, matrix:list[list[int|float]]):
        self.validate_addition([matrix])
        transformation = [[item*number for item in row] for row in matrix]
        return transformation
    
    def matrix_add(self,matrix1,matrix2):
        result = [[item1+item2 for item1,item2 in zip(row1,row2)] for row1,row2 in zip(matrix1,matrix2)]
        # result = [[item1 + item2 for item1 in row1 for item2 in row2] for row1 in matrix1 for row2 in matrix2]
        return result

    def matrix_addition(self,matrix:list[list[int|float]], matrix2:list[list[int|float]], *othermartix):
        array = [matrix,matrix2,*othermartix]
        self.validate_addition(array)
        while len(array) >1:
            matrix1 = array.pop()
            matrix2 = array.pop()
            result = self.matrix_add(matrix1,matrix2)
            array.append(result)
        return array[0]
    
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
        self.validate_addition(array)
        result = array[0]
        print(f"array: {array}")
        print(f"len: {len(array)}")
        for matrix in array[1:]:
            result = self.matrix_multiply(result, matrix)
        return result

    def matrix_transpose(self,matrix):
        return list(zip(*matrix))


# matrix = [[1,2],[112,8],[2,3]]
# matrix2 = [[1,2,3],[112,56,8],[1,2,3]]
# matrix3 = [[1,2,3],[112,56,8],[1,2,3]]
# matrix4 = [[1,2],[2,2]]

# m1 = [[1,2,3],[4,5,6]]
# m2 = [[1,2],[3,4],[5,6]]
# m3 = [[1,2],[3,4]]
# mat_op = MatrixValidation()
# # print(mat_op.validate_addition(matrix,matrix2,matrix3))
# # print(mat_op.scalar_multiplication(matrix=matrix,number=6))
# # print(mat_op.scalar_addition(matrix=matrix,number=6))
# # print(mat_op.matrix_addition(matrix,matrix2))
# print(mat_op.matrix_chain_multiply(m1,m2,m3))





