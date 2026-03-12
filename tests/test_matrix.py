"""
test_matrix.py

Tests for the Matrix class — construction, dunders, properties, row operations.
"""

import unittest
from src import Matrix


class TestMatrixConstruction(unittest.TestCase):

    def test_valid_construction(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A.shape(), (2, 2))

    def test_shape_rectangular(self):
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(A.shape(), (2, 3))

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            Matrix([])

    def test_jagged_raises(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2], [3]])

    def test_constructor_deep_copies(self):
        data = [[1, 2], [3, 4]]
        A = Matrix(data)
        data[0][0] = 99         # mutate original
        self.assertEqual(A.data[0][0], 1)  # Matrix should be unaffected


class TestMatrixRepr(unittest.TestCase):

    def test_repr_returns_string(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertIsInstance(repr(A), str)

    def test_repr_contains_values(self):
        A = Matrix([[1, 2], [3, 4]])
        r = repr(A)
        self.assertIn("1", r)
        self.assertIn("4", r)


class TestMatrixEquality(unittest.TestCase):

    def test_equal_matrices(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A, B)

    def test_unequal_matrices(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        self.assertNotEqual(A, B)

    def test_different_shapes_not_equal(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertNotEqual(A, B)

    def test_float_equality_tolerance(self):
        A = Matrix([[1.0000000001]])
        B = Matrix([[1.0]])
        self.assertEqual(A, B)


class TestMatrixAddition(unittest.TestCase):

    def test_add_2x2(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        self.assertEqual(A + B, Matrix([[6, 8], [10, 12]]))

    def test_add_returns_matrix_instance(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 0], [0, 1]])
        self.assertIsInstance(A + B, Matrix)

    def test_add_shape_mismatch_raises(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            A + B

    def test_add_chaining(self):
        A = Matrix([[1, 0], [0, 1]])
        B = Matrix([[2, 0], [0, 2]])
        C = Matrix([[3, 0], [0, 3]])
        self.assertEqual(A + B + C, Matrix([[6, 0], [0, 6]]))


class TestMatrixSubtraction(unittest.TestCase):

    def test_sub_2x2(self):
        A = Matrix([[5, 6], [7, 8]])
        B = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A - B, Matrix([[4, 4], [4, 4]]))

    def test_sub_shape_mismatch_raises(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3]])
        with self.assertRaises(ValueError):
            A - B


class TestScalarMultiplication(unittest.TestCase):

    def test_mul_scalar_right(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A * 2, Matrix([[2, 4], [6, 8]]))

    def test_mul_scalar_left(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(3 * A, Matrix([[3, 6], [9, 12]]))

    def test_mul_returns_matrix(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertIsInstance(A * 2, Matrix)


class TestElementWiseMultiplication(unittest.TestCase):

    def test_elementwise_2x2(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        self.assertEqual(A * B, Matrix([[5, 12], [21, 32]]))

    def test_elementwise_shape_mismatch_raises(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            A * B


class TestMatmul(unittest.TestCase):

    def test_matmul_2x2(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        self.assertEqual(A @ B, Matrix([[19, 22], [43, 50]]))

    def test_matmul_rectangular(self):
        F = Matrix([[1, 2, 3], [4, 5, 6]])
        G = Matrix([[7, 8], [9, 10], [11, 12]])
        self.assertEqual(F @ G, Matrix([[58, 64], [139, 154]]))

    def test_matmul_returns_matrix(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 0], [0, 1]])
        self.assertIsInstance(A @ B, Matrix)

    def test_matmul_chaining(self):
        """(A @ B) @ C should work because __matmul__ returns a Matrix."""
        F = Matrix([[1, 2, 3], [4, 5, 6]])
        G = Matrix([[7, 8], [9, 10], [11, 12]])
        C = Matrix([[1, 2], [3, 4]])
        result = F @ G @ C
        self.assertEqual(result, Matrix([[250, 372], [601, 894]]))

    def test_matmul_incompatible_raises(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with self.assertRaises(ValueError):
            A @ B


class TestTranspose(unittest.TestCase):

    def test_transpose_square(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A.transpose(), Matrix([[1, 3], [2, 4]]))

    def test_transpose_rectangular(self):
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(A.transpose(), Matrix([[1, 4], [2, 5], [3, 6]]))

    def test_double_transpose_is_original(self):
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(A.transpose().transpose(), A)


class TestTrace(unittest.TestCase):

    def test_trace_2x2(self):
        A = Matrix([[1, 0], [0, 5]])
        self.assertEqual(A.trace(), 6)

    def test_trace_3x3(self):
        A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(A.trace(), 15)

    def test_trace_non_square_raises(self):
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            A.trace()


class TestRowOperations(unittest.TestCase):

    def test_swap_rows(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A.swap_rows(1, 2), Matrix([[3, 4], [1, 2]]))

    def test_swap_rows_does_not_mutate(self):
        A = Matrix([[1, 2], [3, 4]])
        _ = A.swap_rows(1, 2)
        self.assertEqual(A.data, [[1, 2], [3, 4]])

    def test_swap_rows_invalid_index_raises(self):
        A = Matrix([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            A.swap_rows(1, 5)

    def test_add_rows(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A.add_rows(1, 2), Matrix([[4, 6], [3, 4]]))

    def test_add_rows_does_not_mutate(self):
        A = Matrix([[1, 2], [3, 4]])
        _ = A.add_rows(1, 2)
        self.assertEqual(A.data, [[1, 2], [3, 4]])

    def test_scale_row(self):
        A = Matrix([[1, 2], [3, 4]])
        self.assertEqual(A.scale_row(1, 3), Matrix([[3, 6], [3, 4]]))

    def test_scale_row_does_not_mutate(self):
        A = Matrix([[1, 2], [3, 4]])
        _ = A.scale_row(1, 3)
        self.assertEqual(A.data, [[1, 2], [3, 4]])

    def test_scale_row_invalid_index_raises(self):
        A = Matrix([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            A.scale_row(5, 2)


class TestMatrixProperties(unittest.TestCase):

    def test_is_square_true(self):
        self.assertTrue(Matrix([[1, 2], [3, 4]]).is_square())

    def test_is_square_false(self):
        self.assertFalse(Matrix([[1, 2, 3], [4, 5, 6]]).is_square())

    def test_is_zero_true(self):
        self.assertTrue(Matrix([[0, 0], [0, 0]]).is_zero())

    def test_is_zero_false(self):
        self.assertFalse(Matrix([[0, 1], [0, 0]]).is_zero())

    def test_is_identity_true(self):
        self.assertTrue(Matrix.identity(3).is_identity())

    def test_is_identity_false(self):
        self.assertFalse(Matrix([[2, 0], [0, 1]]).is_identity())

    def test_is_diagonal_true(self):
        self.assertTrue(Matrix([[5, 0], [0, 3]]).is_diagonal())

    def test_is_diagonal_false(self):
        self.assertFalse(Matrix([[1, 2], [0, 3]]).is_diagonal())

    def test_is_symmetric_true(self):
        self.assertTrue(Matrix([[1, 2], [2, 1]]).is_symmetric())

    def test_is_symmetric_false(self):
        self.assertFalse(Matrix([[1, 2], [3, 4]]).is_symmetric())

    def test_is_skew_symmetric_true(self):
        A = Matrix([[0, 2, -1], [-2, 0, -4], [1, 4, 0]])
        self.assertTrue(A.is_skew_symmetric())

    def test_is_skew_symmetric_false(self):
        self.assertFalse(Matrix([[1, 2], [3, 4]]).is_skew_symmetric())

    def test_non_square_symmetric_raises(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2, 3], [4, 5, 6]]).is_symmetric()


class TestFactories(unittest.TestCase):

    def test_zeros(self):
        self.assertTrue(Matrix.zeros(3, 3).is_zero())

    def test_ones(self):
        A = Matrix.ones(2, 2)
        self.assertEqual(A, Matrix([[1, 1], [1, 1]]))

    def test_identity(self):
        self.assertTrue(Matrix.identity(4).is_identity())


if __name__ == "__main__":
    unittest.main()