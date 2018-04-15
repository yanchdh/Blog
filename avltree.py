# -*- coding=utf-8 -*-

class avlnode(object):
    def __init__(self, val):
        self.left = None
        self.right = None
        self.height = 0
        self.val = val

class avltree(object):
    def __init__(self):
        self.root = None    
    
    def insert(self, val):
        self.root = self._insert(self.root, val)
        
    def remove(self, val):
        self.root = self._remove(self.root, val)
        
    def has(self, val):
        return False if not self.root else self._has(self.root, val)
        
    def travel(self):
        print self._travel(self.root)
            
    def _insert(self, root, val):
        if not root:
            return avlnode(val)
        ret = cmp(val, root.val)
        if ret < 0:
            root.left = self._insert(root.left, val)
        elif ret > 0:
            root.right = self._insert(root.right, val)
        else:
            root.val = val
        return self._balance(root)
    
    def _remove(self, root, val):
        if not root:
            return root
        ret = cmp(val, root.val)
        if ret < 0:
            root.left = self._remove(root.left, val)
        elif ret > 0:
            root.right = self._remove(root.right, val)
        elif root.left and root.right:
            root.val = self._minval(root.right)
            root.right = self._remove(root.right, root.val)
        else:
            root = root.left if root.left else root.right
        return self._balance(root)
        
    def _has(self, root, val):
        if not root:
            return False
        ret = cmp(val, root.val)
        if ret < 0:
            return root.left and self._remove(root.left, val)
        elif ret > 0:
            return root.right and self._remove(root.right, val)
        else:
            return True
        
    def _travel(self, root):
        if not root:
            return [None]
        ret = [root.val]
        ret.extend(self._travel(root.left))
        ret.extend(self._travel(root.right))
        return ret
        
    def _balance(self, root):
        if not root:
            return root
        bf = self._height(root.left) - self._height(root.right)
        if bf > 1:
            left_bf = self._height(root.left.left) - self._height(root.left.right)
            if left_bf >= 0:
                root = self._rotate_ll(root)
            else:
                root = self._rotate_lr(root)
        elif bf < -1:
            right_bf = self._height(root.right.right) - self._height(root.right.left)
            if right_bf >= 0:
                root = self._rotate_rr(root)
            else:
                root = self._rotate_rl(root)        
        root.height = max(self._height(root.left), self._height(root.right)) + 1
        return root
        
    def _height(self, root):
        return -1 if not root else root.height
        
    def _minval(self, root):
        if not root:
            return None
        return root.val if not root.left else self._minval(root.left)
    
    def _rotate_ll(self, root):
        left = root.left
        root.left = left.right
        left.right = root
        root.height = max(self._height(root.left), self._height(root.right)) + 1
        left.height = max(self._height(left.left), self._height(left.right)) + 1
        return left
        
    def _rotate_rr(self, root):
        right = root.right
        root.right = right.left
        right.left = root
        root.height = max(self._height(root.left), self._height(root.right)) + 1
        right.height = max(self._height(right.left), self._height(right.right)) + 1
        return right
            
    def _rotate_lr(self, root):
        root.left = self._rotate_rr(root.left)
        return self._rotate_ll(root)
        
    def _rotate_rl(self, root):
        root.right = self._rotate_ll(root.right)
        return self._rotate_rr(root)

import random
        
tree = avltree()

nums = range(10)
random.shuffle(nums)

for num in nums:
    tree.insert(num) 

tree.remove(5)    
    
tree.travel()
