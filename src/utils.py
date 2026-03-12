"""
utils.py

Stateless utility and factory functions.
These do not depend on the Matrix class — they produce raw list data
that Matrix.__init__ can consume.

Kept separate so they can be used independently or in tests
without importing the full Matrix object.
"""

from src.validator import MatrixValidator


def zeros(rows: int, cols: int) -> list[list[float]]:
    """Return a rows x cols matrix of zeros."""
    if rows < 1 or cols < 1:
        raise ValueError(f"Dimensions must be positive. Got ({rows}, {cols}).")
    return [[0.0] * cols for _ in range(rows)]


def ones(rows: int, cols: int) -> list[list[float]]:
    """Return a rows x cols matrix of ones."""
    if rows < 1 or cols < 1:
        raise ValueError(f"Dimensions must be positive. Got ({rows}, {cols}).")
    return [[1.0] * cols for _ in range(rows)]


def identity(n: int) -> list[list[int]]:
    """Return an n x n identity matrix."""
    if n < 1:
        raise ValueError(f"Identity matrix size must be positive. Got {n}.")
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def build_minor(data: list[list], i: int, j: int) -> list[list]:
    """
    Return the minor of matrix data with row i and column j removed.
    Used internally by determinant and cofactor calculations.
    """
    return [
        row[:j] + row[j+1:]
        for row in (data[:i] + data[i+1:])
    ]