class MatrixOperations:
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

    def element_matrix_multiply(self,matrix1, matrix2):
        result = [[item1*item2 for item1,item2 in zip(row1,row2)] for row1,row2 in zip(matrix1,matrix2)]
        return result

    def element_wise_multiplication(self, matrix1,matrix2,*other):
        array = [matrix1, matrix2,*other]
        if self.validate_addition(array):
            result = array[0]
            for matrix in array[1:]:
                result = self.element_matrix_multiply(result,matrix)
            return result       
    
    def matrix_multiply(self, matrix1,matrix2):
        item2_trans = [list(row) for row in zip(*matrix2)]
        result = []
        for m1_row in matrix1:
            row = []
            for m2_row in item2_trans:
                sum_matrix = 0
                for item1,item2 in zip(m1_row,m2_row):
                    sum_matrix += item1*item2
                row.append(sum_matrix)
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
        return [list(row) for row in zip(*matrix)]
    
    def row_operation(self,matrix,r1,r2):
        matrix_new = matrix.copy()
        matrix_new[r1-1] = matrix[r2-1]
        matrix_new[r2-1] = matrix[r1-1]
        return matrix_new, matrix

    def sum_matrix_of_diagonal(self,matrix):
        sum_matrix = 0
        number = 0
        for row in matrix:
            sum_matrix +=row[number]
            number +=1
        return sum_matrix
    
    def row_addition(self, matrix,row1,row2):
        sum_matrix = [item1+item2 for item1,item2 in zip(matrix[row1-1],matrix[row2-1])]
        matrix[row1-1] = sum_matrix
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
    
    def is_square(self,matrix):
        order = self.find_order(matrix)
        if order[0] == order[1]:
            return True
        return False
    
    def is_symmetric(self,matrix):
        if self.is_square(matrix):
            matrix_trans = self.matrix_transpose(matrix)
            for row1,row2 in zip(matrix,matrix_trans):
                if row1 != row2:
                    return False
            return True
        else:
            raise ValueError("Matrix is not Square, hence cannot be symmetric")
        

    def is_skew_symmetric(self,matrix):
        if self.is_square(matrix):
            matrix_trans = self.matrix_transpose(matrix)
            for row1,row2 in zip(matrix,matrix_trans):
                for item1,item2 in zip(row1,row2):
                    if item1 != -item2:
                        return False
            return True
        else:
            raise ValueError("Matrix is not Square, hence cannot be skew-symmetric")
        
    def is_diagonal(self,matrix):
        if self.is_square(matrix):
            order = self.find_order(matrix)
            for i in range(order[0]):
                for j in range(order[1]):
                    if i==j and matrix[i][j] ==0:
                        return False
            return True
        else:
            raise ValueError("Matrix is not Square, hence cannot be Diagonal")
        
    def is_identity(self,matrix):
        if self.is_square(matrix):
            order = self.find_order(matrix)
            for i in range(order[0]):
                for j in range(order[1]):
                    if i==j and matrix[i][j] !=1:
                        return False
                    elif i!=j and matrix[i][j] !=0:
                        return False
            return True
        else:
            raise ValueError("Matrix is not Square, hence cannot be Identity")
        
    def build_identity(self,number):
        order = number
        identity = []
        for i in range(order):
            row = []
            for j in range(order):
                if i==j:
                    row.append(1)
                else:
                    row.append(0)
            identity.append(row)
        return identity
    
    def calculate_minor(self, number, matrix):
        if self.is_square(matrix):
            order = self.find_order(matrix)
            if order[0]==2 and order[1]==2:
                val_1 = matrix[0][0]*matrix[1][1]
                val_2 = matrix[0][1]*matrix[1][0]
                det = val_1 - val_2
                return number*det
            else:
                self.cal_cofactor(matrix)
    
    def build_determinate(self, i,j,matrix):
        matrix_end = matrix[i:]
        matrix_start = matrix[:i]
        row_elimented = [matrix_start,matrix_end]
        matrix_trans = [list(row) for row in zip(*row_elimented)]
        matrix_col_end = matrix_trans[j:]
        matrix_col_start = matrix_trans[:j]
        return [matrix_col_start,matrix_col_end]


    def cal_cofactor(self,matrix):
        if self.is_square(matrix):
            order = self.find_order(matrix)
            det = []
            for i in range(order[0]):
                row = []
                for j in range(order[1]):
                    val = matrix[i][j]
                    matrix_det = self.build_determinate(i,j,matrix)
                    deter = self.calculate_minor(val,matrix_det)
                    sign = (-1)**(i+j)
                    cofactor = sign*deter
                    row.append(cofactor)
                det.append(row)
            return det


    