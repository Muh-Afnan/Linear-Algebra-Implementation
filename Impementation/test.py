from main import MatrixValidation

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
# (print(mat_op.sum_of_diagonal(m2)))
(print(mat_op.matrix_transpose(m1)))


