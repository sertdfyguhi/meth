import meth

ast = meth.parse("10 + (10 * 10) ^ 2")
print(meth.utils.get_leaf_node_right(ast))
