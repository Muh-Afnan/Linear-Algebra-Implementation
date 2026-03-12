# Comparison with Standard Libraries

> How does this library compare to NumPy, SciPy, and SymPy?
> This document goes operation by operation — same algorithm, different mechanism, or fundamentally different approach.
> Inverse is excluded intentionally. Both this library and NumPy agree on the math. The difference (LU decomposition) deserves its own dedicated study.

---

## The Big Picture First

Before diving into individual operations, it helps to understand the three categories of difference that explain almost every gap between this library and NumPy.

**Memory Layout.** This library stores matrices as nested Python lists — a list of lists of Python floats. Each element is a full Python object with reference counting, type information, and heap allocation. NumPy stores matrices as flat C arrays in a single contiguous block of memory. Accessing `matrix[i][j]` in this library requires two pointer dereferences. In NumPy it requires one addition and one memory read. This difference alone accounts for a large portion of the performance gap.

**Views vs Copies.** When this library transposes a matrix, it creates a new matrix with all elements copied. When NumPy transposes, it returns a *view* — a new array object pointing at the same memory block, with swapped stride values. No data moves. Transposing a 1000×1000 NumPy matrix takes nanoseconds. Transposing the same matrix in this library takes time proportional to the number of elements.

**Algorithm Choice.** Some operations use fundamentally different algorithms. The determinant here uses cofactor expansion — correct, recursive, O(n!). NumPy uses LU decomposition — O(n³). For a 10×10 matrix, that's the difference between ~3.6 million recursive calls and ~1000 arithmetic operations.

Everything else in this comparison is a variation on these three themes.

---

## Construction & Validation

**This library:**
```python
A = Matrix([[1, 2], [3, 4]])
# validates shape, deep copies data, stores rows and cols
```

**NumPy:**
```python
A = np.array([[1, 2], [3, 4]])
# validates shape, copies data, stores dtype + shape + strides
```

The validation logic is conceptually identical — check that the input is non-empty, non-jagged, and well-formed. The difference is what gets stored afterward.

NumPy stores a `strides` tuple alongside `shape`. Strides describe how many bytes to skip in memory to move one step along each dimension. For a 2×2 float64 array, strides might be `(16, 8)` — move 16 bytes to go to the next row, 8 bytes to go to the next column. This is what enables views, broadcasting, and cache-friendly access patterns.

This library stores `rows`, `cols`, and a nested list. Simpler, slower, correct.

One thing this library does that NumPy also does: defensive copy on construction. If you modify the list you passed in, the Matrix doesn't change. NumPy does this by default (`copy=True`). Both make the same safety decision.

---

## Matrix Multiplication (`@`)

**This library:**
```python
def __matmul__(self, other):
    other_T = list(zip(*other.data))
    result = [
        [sum(a * b for a, b in zip(row, col)) for col in other_T]
        for row in self.data
    ]
    return Matrix(result)
```
Transpose B, then dot each row of A with each column of B. O(n³).

**NumPy:**
```python
C = A @ B  # or np.matmul(A, B)
```
Also O(n³) at the algorithmic level. But NumPy calls BLAS (Basic Linear Algebra Subprograms) — specifically the `dgemm` routine for double precision matrix multiplication.

BLAS does four things this library cannot in pure Python:

- Operates on contiguous memory rather than Python object lists
- Uses SIMD CPU instructions to multiply multiple numbers in a single clock cycle
- Tiles the computation into blocks sized to fit the L1/L2 CPU cache
- Parallelises across multiple CPU cores automatically

The algorithm is identical. The execution environment is completely different.

**PyTorch / TensorFlow** go further — if a GPU is available, `@` dispatches to cuBLAS, the GPU-accelerated equivalent of BLAS, capable of thousands of parallel multiply-accumulate operations per clock cycle.

**Verdict:** Same algorithm. Incomparable execution. The O(n³) complexity is shared — everything else is the gap between Python lists and hardware-optimised linear algebra kernels.

---

## Transpose

**This library:**
```python
def transpose(self):
    return Matrix([list(row) for row in zip(*self.data)])
```
Creates a new matrix. Copies every element. O(n²) time and space.

**NumPy:**
```python
A.T  # or np.transpose(A)
```
Returns a *view*. Zero data is copied. Only the strides are swapped.

```
Original:  shape=(3,4), strides=(32, 8)
Transposed: shape=(4,3), strides=(8, 32)
```

Same memory block. Different interpretation. The transpose of a 10,000×10,000 matrix in NumPy takes roughly the same time as transposing a 2×2 matrix — because nothing moves.

This is one of the starkest differences in the entire comparison. The output is mathematically identical. The mechanism is completely different.

Understanding the distinction between views and copies is one of the most important concepts in NumPy for ML engineering. When you do `B = A.T` in NumPy and then modify `B`, you're modifying `A` too. This surprises people. Now you know why.

**Verdict:** Correct output, fundamentally different mechanism. The view concept is impossible to replicate in pure Python with nested lists.

---

## Determinant

**This library:**
```python
# Cofactor expansion along row 0
det = sum(
    (-1)**j * matrix[0][j] * determinant(minor(matrix, 0, j))
    for j in range(n)
)
```
Recursive cofactor expansion. O(n!).

**NumPy (`np.linalg.det`):**
LU decomposition. Factor A = PLU where P is a permutation matrix, L is lower triangular, U is upper triangular. The determinant is then:

```
det(A) = det(P) * det(L) * det(U)
       = sign * 1 * product(diagonal of U)
```

`det(L) = 1` always (triangular matrix with 1s on diagonal). `det(P) = ±1` depending on row swap parity. So the whole determinant reduces to multiplying the diagonal of U together. O(n³).

**The scale of the difference:**

| Matrix Size | Cofactor Expansion (ops) | LU Decomposition (ops) |
|---|---|---|
| 4×4 | 24 | ~21 |
| 6×6 | 720 | ~72 |
| 8×8 | 40,320 | ~170 |
| 10×10 | 3,628,800 | ~333 |
| 12×12 | 479,001,600 | ~576 |

At 12×12, cofactor expansion makes nearly half a billion recursive calls. LU decomposition makes ~576.

**Why cofactor expansion is still the right place to start:**

Cofactor expansion reveals *why* the determinant exists as a concept. The recursive structure shows that the determinant measures signed volume — each cofactor is a lower-dimensional volume, scaled and summed. LU decomposition computes the same number through a completely different geometric lens. Understanding both is the goal. Starting with cofactor expansion is correct.

**SymPy (symbolic math):** Uses cofactor expansion for symbolic matrices where LU decomposition would produce irrational intermediate values. In this narrow sense, this library's approach matches what SymPy actually does.

**Verdict:** Correct for small matrices (up to ~8×8 before noticeable slowdown). Pedagogically the right algorithm to implement first. Not suitable for production use.

---

## Cofactor Matrix & Adjoint

**This library:**
```python
def cofactor_matrix(matrix):
    # compute (-1)^(i+j) * det(minor(i,j)) for every entry
    ...

def adjoint(matrix):
    return cofactor_matrix(matrix).transpose()
```

**NumPy / SciPy:** Do not expose cofactor or adjoint directly. They are intermediate steps toward inverse, and since inverse is computed via LU, cofactor and adjoint are never needed. There is no `np.cofactor()` or `np.adjoint()`.

**SymPy:** Exposes `Matrix.cofactor_matrix()` and `Matrix.adjugate()`. Its implementation is conceptually identical to this library — compute each cofactor by expanding the corresponding minor, assemble into a matrix, transpose for adjugate. For symbolic matrices this is the correct approach because LU decomposition would introduce square roots and fractions that obscure symbolic results.

This is one area where this library's implementation genuinely mirrors what a real library does for its intended use case (symbolic / exact arithmetic). The approach is not a simplification — it is the right tool for exact computation.

**Verdict:** Direct match with SymPy's implementation for the symbolic case. No NumPy equivalent exists because NumPy operates numerically and uses LU instead.

---

## Trace

**This library:**
```python
def trace(self):
    return sum(self.data[i][i] for i in range(self.rows))
```

**NumPy:**
```python
np.trace(A)  # or A.trace()
```

This is a direct algorithmic match. NumPy's default `np.trace()` sums `A[i, i]` for `i` in range of the smaller dimension. The only additional feature NumPy provides is an `offset` parameter for summing super- or sub-diagonals (`np.trace(A, offset=1)` sums the diagonal one above the main).

The core algorithm is identical. NumPy executes it in C on contiguous memory — faster by constant factor, not by a different complexity class.

**Verdict:** This is a direct match. One of the few operations where this library and NumPy do the same thing in essentially the same way.

---

## Property Checks

**This library:**
```python
def is_symmetric(self):
    return self == self.transpose()  # uses __eq__ with 1e-9 tolerance
```

**NumPy:**
```python
np.allclose(A, A.T, rtol=1e-05, atol=1e-08)
```

The approach is identical — compare matrix to its transpose. The difference is tolerance handling. `np.allclose` uses both relative and absolute tolerance, which is more robust for matrices with values at very different scales. This library uses a fixed absolute tolerance of `1e-9` in `__eq__`.

For integer matrices: no difference. For floating point matrices produced by computation: NumPy's relative tolerance is more correct. A matrix where `A[0][0]` is `1e15` and `A[1][0]` is `1e15 + 1` might be "symmetric enough" in relative terms but fail an absolute tolerance check.

This is a real limitation. A matrix produced by floating point operations — say, the result of several multiplications — might be mathematically symmetric but fail this library's `is_symmetric` due to accumulation of floating point error.

**Verdict:** Same algorithm, same intent. NumPy's tolerance model is more robust for numerical work. Worth noting as a known limitation.

---

## Row Operations

**This library:**
```python
def swap_rows(self, r1, r2):
    new_data = copy.deepcopy(self.data)
    new_data[r1-1], new_data[r2-1] = new_data[r2-1], new_data[r1-1]
    return Matrix(new_data)  # returns new Matrix, never mutates self
```

**NumPy:**
```python
A[[0, 1]] = A[[1, 0]]  # in-place, modifies A directly
```

Opposite philosophies. This library is non-mutating — every row operation returns a new Matrix. NumPy is mutating by default — row operations modify the array in place.

NumPy's approach is faster (no copy) and is appropriate when working with large arrays where copying is expensive. This library's approach is safer — the caller's data is never modified by passing it to a function. For a library where correctness and predictability matter more than raw performance, non-mutating operations are the better default.

Both approaches are legitimate design decisions. They reflect different priorities.

**Verdict:** Different philosophy. This library is safer. NumPy is faster. For the scale of problems this library is designed for, safety is the right priority.

---

## Summary

| Operation | This Library | NumPy/SciPy | Algorithm Match |
|---|---|---|---|
| Construction | O(n²) nested lists | O(n²) flat C array | Same logic, different memory |
| Matrix multiply | O(n³) Python loops | O(n³) BLAS/CUDA | Same algorithm, different execution |
| Transpose | O(n²) copy | O(1) view | Different mechanism entirely |
| Determinant | O(n!) cofactor | O(n³) LU | Different algorithm |
| Cofactor/Adjoint | O(n!) exact | Not in NumPy | Matches SymPy exactly |
| Trace | O(n) diagonal sum | O(n) diagonal sum | Direct match |
| Property checks | O(n²) compare | O(n²) allclose | Same, NumPy has better tolerance |
| Row operations | O(n²) non-mutating | O(n²) mutating | Different philosophy |

---

## What Building This Taught Me About NumPy

Before this project, NumPy felt like a faster version of the same thing. After building this library, I understand that NumPy is not a faster version — it is a fundamentally different thing operating under the same mathematical abstraction.

The determinant comparison makes this concrete. Cofactor expansion and LU decomposition produce the same number from the same input. But one is O(n!) and the other is O(n³). They are not the same algorithm wearing different clothes. They approach the same mathematical object from completely different directions.

The transpose comparison makes the view/copy distinction real in a way that reading documentation never did. When you see that transposing a matrix involves *zero data movement*, the whole concept of memory layout stops being abstract.

The multiplication comparison reframes what `import numpy` actually means. You're not importing a Python library. You're importing a Python interface to decades of hardware-optimised numerical computing — BLAS routines that have been hand-tuned to specific CPU architectures, cache sizes, and instruction sets.

This library is not a competitor to NumPy. It is an explanation of NumPy.