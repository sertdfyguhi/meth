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
