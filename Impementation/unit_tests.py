import unittest
from main import MatrixOperations


class TestMatrixOperations(unittest.TestCase):

    def setUp(self):
        self.mat = MatrixOperations()

        # 1x1
        self.A = [[5]]
        self.B = [[3]]

        # 2x2
        self.C = [[1,2],
                  [3,4]]

        self.D = [[5,6],
                  [7,8]]

        # 3x3
        self.E = [[1,2,3],
                  [4,5,6],
                  [7,8,9]]

        # rectangular
        self.F = [[1,2,3],
                  [4,5,6]]

        self.G = [[7,8],
                  [9,10],
                  [11,12]]

        # zero
        self.zero = [[0,0],[0,0]]

        # 4x4
        self.M4 = [
            [1,2,3,4],
            [5,6,7,8],
            [9,10,11,12],
            [13,14,15,16]
        ]

        self.N4 = [
            [16,15,14,13],
            [12,11,10,9],
            [8,7,6,5],
            [4,3,2,1]
        ]

        # 5x5 identity
        self.I5 = self.mat.build_identity(5)

        # 5x5 diagonal
        self.D5 = [
            [1,0,0,0,0],
            [0,2,0,0,0],
            [0,0,3,0,0],
            [0,0,0,4,0],
            [0,0,0,0,5]
        ]


# ------------------------------------------------
# ORDER TESTS
# ------------------------------------------------

    def test_find_order_small(self):
        self.assertEqual(self.mat.find_order(self.A), (1,1))

    def test_find_order_rectangular(self):
        self.assertEqual(self.mat.find_order(self.F), (2,3))

    def test_find_order_invalid_matrix(self):
        invalid = [[1,2],[3]]
        with self.assertRaises(Exception):
            self.mat.find_order(invalid)


# ------------------------------------------------
# SCALAR OPERATIONS
# ------------------------------------------------

    def test_scalar_addition(self):
        result = self.mat.scalar_addition(2, self.C)
        self.assertEqual(result, [[3,4],[5,6]])

    def test_scalar_multiplication(self):
        result = self.mat.scalar_multiplication(3, self.C)
        self.assertEqual(result, [[3,6],[9,12]])

    def test_scalar_addition_1x1(self):
        result = self.mat.scalar_addition(5, self.A)
        self.assertEqual(result, [[10]])


# ------------------------------------------------
# MATRIX ADDITION
# ------------------------------------------------

    def test_matrix_addition_2x2(self):
        result = self.mat.matrix_addition(self.C, self.D)
        self.assertEqual(result, [[6,8],[10,12]])

    def test_matrix_addition_4x4(self):
        result = self.mat.matrix_addition(self.M4, self.N4)

        expected = [
            [17,17,17,17],
            [17,17,17,17],
            [17,17,17,17],
            [17,17,17,17]
        ]

        self.assertEqual(result, expected)

    def test_matrix_addition_invalid(self):
        with self.assertRaises(Exception):
            self.mat.matrix_addition(self.C, self.F)


# ------------------------------------------------
# ELEMENTWISE MULTIPLICATION
# ------------------------------------------------

    def test_elementwise(self):
        result = self.mat.element_wise_multiplication(self.C, self.D)
        self.assertEqual(result, [[5,12],[21,32]])

    def test_elementwise_4x4(self):
        result = self.mat.element_wise_multiplication(self.M4, self.N4)

        expected = [
            [16,30,42,52],
            [60,66,70,72],
            [72,70,66,60],
            [52,42,30,16]
        ]

        self.assertEqual(result, expected)


# ------------------------------------------------
# MATRIX MULTIPLICATION
# ------------------------------------------------

    def test_matrix_multiply_2x2(self):
        result = self.mat.matrix_multiply(self.C, self.D)
        self.assertEqual(result, [[19,22],[43,50]])

    def test_matrix_multiply_rectangular(self):
        result = self.mat.matrix_multiply(self.F, self.G)

        expected = [
            [58,64],
            [139,154]
        ]

        self.assertEqual(result, expected)


# ------------------------------------------------
# MATRIX CHAIN MULTIPLICATION
# ------------------------------------------------

    def test_chain_multiplication(self):
        result = self.mat.matrix_chain_multiply(self.F, self.G, self.C)
        expected = [
            [250,372],
            [601,894]
        ]
        self.assertEqual(result,expected)


# ------------------------------------------------
# TRANSPOSE
# ------------------------------------------------

    def test_transpose_square(self):
        result = self.mat.matrix_transpose(self.C)
        self.assertEqual(result, [[1,3],[2,4]])

    def test_transpose_rectangular(self):
        result = self.mat.matrix_transpose(self.F)
        self.assertEqual(result, [[1,4],[2,5],[3,6]])

    def test_transpose_4x4(self):
        result = self.mat.matrix_transpose(self.M4)

        expected = [
            [1,5,9,13],
            [2,6,10,14],
            [3,7,11,15],
            [4,8,12,16]
        ]

        self.assertEqual(result, expected)


# ------------------------------------------------
# ZERO MATRIX
# ------------------------------------------------

    def test_zero_matrix(self):
        self.assertTrue(self.mat.zero_matrix_check(self.zero))

    def test_non_zero_matrix(self):
        self.assertFalse(self.mat.zero_matrix_check(self.C))


# ------------------------------------------------
# MATRIX TYPES
# ------------------------------------------------

    def test_square_matrix(self):
        self.assertTrue(self.mat.is_square(self.C))

    def test_identity_matrix(self):
        self.assertTrue(self.mat.is_identity(self.I5))

    def test_diagonal_matrix(self):
        self.assertTrue(self.mat.is_diagonal(self.D5))

    def test_symmetric_matrix(self):
        matrix = [
            [1,2,3],
            [2,5,6],
            [3,6,9]
        ]
        self.assertTrue(self.mat.is_symmetric(matrix))

    def test_skew_symmetric_matrix(self):
        matrix = [
            [0,2,-1],
            [-2,0,-4],
            [1,4,0]
        ]
        self.assertTrue(self.mat.is_skew_symmetric(matrix))


# ------------------------------------------------
# DETERMINANT
# ------------------------------------------------

    def test_determinant_1x1(self):
        self.assertEqual(self.mat.calculate_determinant([[7]]), 7)

    def test_determinant_2x2(self):
        matrix = [[1,2],[3,4]]
        self.assertEqual(self.mat.calculate_determinant(matrix), -2)

    def test_determinant_3x3(self):
        matrix = [
            [6,1,1],
            [4,-2,5],
            [2,8,7]
        ]
        self.assertEqual(self.mat.calculate_determinant(matrix), -306)

    def test_determinant_identity_5x5(self):
        self.assertEqual(self.mat.calculate_determinant(self.I5), 1)


# ------------------------------------------------
# INVERSE
# ------------------------------------------------

    def test_inverse_2x2(self):
        matrix = [
            [4,7],
            [2,6]
        ]

        result = self.mat.cal_inverse(matrix)

        expected = [
            [0.6, -0.7],
            [-0.2, 0.4]
        ]

        for r1, r2 in zip(result, expected):
            for v1, v2 in zip(r1, r2):
                self.assertAlmostEqual(v1, v2, places=5)

    def test_inverse_singular_matrix(self):
        singular = [
            [1,2],
            [2,4]
        ]

        with self.assertRaises(ValueError):
            self.mat.cal_inverse(singular)


# ------------------------------------------------
# EDGE CASES
# ------------------------------------------------

    def test_empty_matrix(self):
        with self.assertRaises(Exception):
            self.mat.find_order([])

    def test_identity_generation(self):
        I = self.mat.build_identity(4)

        expected = [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]

        self.assertEqual(I, expected)


if __name__ == "__main__":
    unittest.main()