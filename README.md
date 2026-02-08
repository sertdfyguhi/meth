# meth: A mathematical expression evaluator.

A python package to parse and evaluate mathematical expressions.

# Installation

```sh
pip install meth
```

or install it from source:

```sh
git clone https://github.com/sertdfyguhi/meth/
cd meth
python3 -m build
pip install dist/*.whl
```

# Examples

> _More examples in the [examples/](https://github.com/sertdfyguhi/meth/tree/master/examples) directory._

```py
import meth

# tokenizing equations
tokens = meth.tokenize("5 + 2") # Token(NUMBER, 5), Token(+), Token(NUMBER, 2)

# parsing equations
ast = meth.parse(tokens) # BinaryOp(Number(5), +, Number(2))

# evaluating equations
meth.evaluate("2 + 2") # 4
meth.evaluate("sqrt(9)") # 3

# evaluation with variables
evaluator = meth.Evaluator()
evaluator.evaluate("x = 5")
evaluator.evaluate("x") # 5
```
