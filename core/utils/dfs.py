from collections import deque


def dfs_pre_order(root, func):
    """
    For node (N) with children left (L) and right (R) order is: NLR
    :param root: Tree with functions "has_children" and "get_children"
    :param func: Function to perform on individual node
    """
    if root is None:
        return
    nodes_to_visit = deque([root])
    while len(nodes_to_visit) > 0:
        current_node = nodes_to_visit.popleft()
        if current_node.has_children():
            for child in reversed(current_node.get_children()):
                nodes_to_visit.appendleft(child)
        func(current_node)


def dfs_post_order(root, func):
    """
    For node (N) with children left (L) and right (R) order is: LRN
    :param root: Tree with functions "has_children" and "get_children"
    :param func: Function to perform on individual node
    """
    if root is None:
        return
    stack = [root]
    children_added = set()
    while len(stack) > 0:
        current_node = stack.pop()
        if current_node.has_children():
            if current_node not in children_added:
                stack.append(current_node)
                children_added.add(current_node)
                for child in reversed(current_node.get_children()):
                    stack.append(child)
                continue
        func(current_node)


if __name__ == '__main__':
    pass
