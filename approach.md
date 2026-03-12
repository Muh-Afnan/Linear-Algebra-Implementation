# Approach

## Starting Point: What Does a Matrix Even Need to Be?

My first instinct was to write a bunch of functions. `add(matrix1, matrix2)`. `multiply(matrix1, matrix2)`. A flat utility file. That felt natural because that's how I'd seen matrix code written in tutorials.

My mentor pushed back on this immediately. The question wasn't "what functions do I need?" — it was "what should a matrix *be* as an object?" That reframe changed everything.

A matrix is not just a 2D list. It has a shape. It can be added to another matrix. It can be multiplied. It can be transposed. It knows whether it's square, symmetric, diagonal. These aren't external operations applied to data — they're *behaviours* that belong to the object. That's what OOP is actually for.

So the design became: build a `Matrix` class that behaves the way Python objects are supposed to behave.

## The File Structure and Why

The library is split into four files. This wasn't the original plan — it emerged from understanding what each piece of code was actually responsible for.

**`validator.py`** holds nothing but validation logic. Static methods that take inputs, check them, and either return silently or raise a `ValueError` with a descriptive message. No arithmetic. No state. Validators don't need to be instantiated — they just need to be called. That's why every method is `@staticmethod`.

**`utils.py`** holds stateless factory functions — `zeros()`, `ones()`, `identity()`, `build_minor()`. These produce raw list data. They don't know about the `Matrix` class. This matters because `build_minor` is used recursively inside the determinant calculation, and making it independent of the class keeps that recursion clean.

**`matrix.py`** is the core object. The `Matrix` class handles construction, validation on construction, all the dunder methods, property checks, row operations, and factory classmethods. Every method either returns a new `Matrix` instance or a scalar — nothing mutates `self`.

**`operations.py`** holds the heavier mathematical procedures: `determinant`, `cofactor_matrix`, `adjoint`, `inverse`, `chain_multiply`. These live outside `matrix.py` because they involve multi-step algorithms and recursion. Keeping them separate means `matrix.py` stays readable and focused on the object model.

## Key Technical Decisions

**All dunders return `Matrix` instances, not raw lists.**

This was a specific decision that enables chaining. If `A + B` returns a raw list, then `(A + B) @ C` crashes because lists don't have `__matmul__`. By returning `Matrix(result)` from every dunder, chaining works naturally: `A + B + C`, `A @ B @ C`, `(A + B).transpose()`. The object model stays consistent.

**`__init__` deep copies the input data.**

If I pass a list to `Matrix()` and then modify that list, I don't want my matrix to silently change. `copy.deepcopy(data)` in the constructor means the Matrix owns its data. Tests verify this explicitly.

**`__eq__` uses floating point tolerance (`abs(v1 - v2) < 1e-9`) instead of `==`.**

This was forced on me by the inverse test. `A @ inverse(A)` should equal the identity matrix, but the floating point results are things like `0.9999999999999998` and `2.7755575615628914e-17`. Direct equality comparison would fail. Tolerance-based equality is the correct approach for any numerical library.

**Validation raises, never returns False.**

An early version of this code had validators that caught errors and returned `False`. The problem: the caller got a `False` back with no information about what went wrong or why. Library code should raise with a clear message and let the caller decide what to do with the error. The distinction between library code (raises) and caller code (handles) was one of the most important things I worked through building this.

**`chain_multiply` catches and re-raises with position context.**

This is the one place in the library where `try/except/raise from` is genuinely justified. The underlying `validate_multipliable` gives a shape mismatch error, but `chain_multiply` can add something the validator can't: which position in the chain failed. `"Chain multiplication failed at position [2] @ [3]"` is more useful than a raw shape error when you're multiplying five matrices together.

## What I Didn't Do (and Why)

I didn't implement Gaussian elimination or LU decomposition. The current determinant uses cofactor expansion, which is O(n!) and impractical for large matrices. A real library would use LU decomposition for O(n³) performance. I left this as a known limitation rather than a half-implemented feature. The README notes it explicitly.

I didn't add support for complex numbers. The type hints say `int | float` throughout, and that's what's tested. Extending to complex would require changes in several places, particularly in `__eq__` where the tolerance comparison doesn't generalise directly to complex values.

## The Role of Tests

I didn't write tests at the end. By the third iteration of this project, with bugs hiding in places I was sure were correct, it became obvious that tests had to be written alongside the code — not after.

The most important test in the entire suite is `test_a_times_inverse_is_identity`. It doesn't test a single method. It tests that the whole pipeline — determinant, cofactor, adjoint, scalar multiplication, matrix multiplication — composes correctly. A bug anywhere in that chain fails this test. That's what integration tests are for.

76 tests. All passing.