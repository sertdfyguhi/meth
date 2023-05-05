# meth: A mathematical expression parser.

Hopefully this would become a python package to parse mathematical expressions.

# Example

```py
import meth

meth.evaluate("2 + 2") # 2
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
- [ ] Nodes to Equation String
- [ ] Documentation
- [ ] Publish to PyPI
