import src.binary_tree as bt

root = bt.build()
result = bt.bf(6, root)
if result:
    print('Found {}'.format(result.val))
