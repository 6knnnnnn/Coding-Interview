# -*- coding: utf-8 -*-


class Flatten2DVector(object):
    """
    为一个2D数组设计一个iterator
    Follow up: 如何实现remove方法？需要一个flag，来标志当前next node是否已经被删除了
    """
    def __init__(self, vec2d):
        self.row = self.col = 0
        self.vec = vec2d
        self.can_remove_current = False

    def next(self):
        self.col += 1
        self.can_remove_current = True
        return self.vec[self.row][self.col-1]

    def has_next(self):
        while self.row < len(self.vec):
            if self.col < len(self.vec[self.row]):
                return True
            # 如果有一个元素为空array，col=0 < 0 为False，继续下一行
            self.col = 0
            self.row += 1
        return False

    def remove(self):
        """
        remove the last element returned by the iterator.
        That is, remove the element that the previous next() returned
        This method can be called only once per call to next(), otherwise an exception will be thrown.
        """
        if self.can_remove_current:
            self.can_remove_current = False
            del self.vec[self.row][self.col-1]
            # 这里是关键点，因为下次调用next方法的时候
            # 其实对应的元素是删除后的当前元素
            self.col -= 1
        else:
            raise Exception("Already deleted the current element, please get next element before delete.")


matrix = [
  [1,2],
  [3], [],
  [4,5,6]
]

iterator = Flatten2DVector(matrix)
while iterator.has_next():
    num = iterator.next()
    print num
    if num % 2 == 0:
        iterator.remove()

print iterator.vec
