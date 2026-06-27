import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

import meth

if __name__ == "__main__":
    print("Calculator made using meth.")

    evaluator = meth.Evaluator()

    while True:
        try:
            expr = input("> ")
        except KeyboardInterrupt:
            # dont print keyboard interrupt error
            break

        try:
            result = evaluator.evaluate(expr)
            if result is not None:
                print(result)
        except meth.MethError as err:
            print(err)
