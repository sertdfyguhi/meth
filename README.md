# meth: A mathematical expression parser.

A python package to parse and evaluate mathematical expressions.

# Examples

> _More examples in the [examples/](examples/) directory._

```py
import meth

meth.evaluate("2 + 2") # 4
meth.evaluate("sqrt(9)") # 3

# using variables
evaluator = meth.Evaluator()
evaluator.evaluate("x = 5")
evaluator.evaluate("x") # 5
```

# Todo

- [x] Lexer
- [x] Parser
  - [x] Bracketing
  - [x] Multiplication using brackets
  - [x] Negative Numbers
  - [x] Variables
  - [x] Functions
- [x] Interpreter
  - [x] Binary Operations
  - [x] Unary Operations
  - [x] Variables
  - [x] Functions
- [x] Add mathematical functions
- [ ] Simplify an expression
- [ ] Expand an expression
- [x] AST to Equation String
- [ ] Documentation
- [ ] Publish to PyPI
