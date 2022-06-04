import unittest
from utils import dfs


class Tree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.search_results = []

    def has_children(self):
        return self.left or self.right

    def get_children(self):
        res = []
        if self.left:
            res.append(self.left)
        if self.right:
            res.append(self.right)
        return res

    def get_value(self):
        return self.value

    def add_to_search_results(self, node):
        self.search_results.append(node.value)


example_tree = Tree('node')
example_tree.left = Tree('left')
example_tree.right = Tree('right')

example_tree1 = Tree('node')
example_tree1.left = Tree('left')
example_tree1.right = Tree('right')

example_tree2 = Tree(1)
example_tree2.left = Tree(2)
example_tree2.right = Tree(3)
example_tree2.left.left = Tree(4)
example_tree2.left.right = Tree(5)
"""
example_tree2:
    1
   / \
  2   3
 / \
4  5
"""


class TestVector(unittest.TestCase):

    def test_dfs_pre_order(self):
        dfs.dfs_pre_order(example_tree, example_tree.add_to_search_results)
        res = ['node', 'left', 'right']
        self.assertEqual(example_tree.search_results, res)

    def test_dfs_post_order(self):
        dfs.dfs_post_order(example_tree1, example_tree1.add_to_search_results)
        res = ['left', 'right', 'node']
        self.assertEqual(example_tree1.search_results, res)
        dfs.dfs_post_order(example_tree2, example_tree2.add_to_search_results)
        res = [4, 5, 2, 3, 1]
        self.assertEqual(example_tree2.search_results, res)


if __name__ == '__main__':
    unittest.main()
