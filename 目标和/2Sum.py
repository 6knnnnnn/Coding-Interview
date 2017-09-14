# -*- coding: utf-8 -*-

from collections import deque


def two_sum_hash(nums, target):
    # 如果没有排序，用哈希map记录目标target与每个n的差，作为key，value就是对应n的index
    diff_index_map = {}
    result = []
    for i in xrange(len(nums)):
        n = nums[i]
        if n in diff_index_map:
            # 这里找的是可能的pair，但可能不是所有的pair，如果任意一个此时可以return
            result.append((diff_index_map[n], i))
        else:
            diff = target - n
            diff_index_map[diff] = i
    return result


def two_sum_sorted_2_pointers(nums, target):
    # 如果只是找一个index pair即可，那么可以两头scan，缩小搜索区间，时间O(N)
    # 或者可以用二分搜索，但此时最坏情况为O(N*logN)，即每一个元素都要logN一次
    # 如果要找所有的pair？二分搜索可以O(N*logN)，普通扫描需要O(N^2）
    i, j = 0, len(nums) - 1
    while nums[i] + nums[j] != target:
        if i == j:
            return []
        if nums[i] + nums[j] > target:
            j -= 1
        else:
            i += 1
    return [i + 1, j + 1]


def two_sum_sorted_binary_search(numbers, target):
    for i in xrange(len(numbers)):
        # left 从i+1开始，i以及i之前的都已经考虑过了
        l, r = i + 1, len(numbers) - 1
        diff = target - numbers[i]
        while l <= r:  # binary search
            mid = (l + r) / 2
            if numbers[mid] == diff:
                # 如果是所有的pair，此时应该加到结果中
                return [i + 1, mid + 1]
            elif numbers[mid] < diff:
                l = mid + 1
            else:
                r = mid - 1
    return []


class TwoSum(object):
    # Two sum data structure design
    # https://leetcode.com/problems/two-sum-iii-data-structure-design/description/
    # 还是用哈希，因为可能有重复元素，但是目标是重复元素的两倍
    def __init__(self):
        self.num_count = {}

    def add(self, num):
        self.num_count[num] = self.num_count.get(num, 0) + 1

    def find(self, val):
        for k, v in self.num_count.items():
            diff = val - k
            if k == diff:
                if v > 1:  # 重复元素，看个数
                    return True
            elif diff in self.num_count:
                return True
        return False


def three_sum(nums, target=0):
    # https://leetcode.com/problems/3sum/description/
    # 此时求的是target=0的情况，但是推导到其他target也是可以的
    # 暴力解法三个for loop，O(N^3)，优化：先排序，再用两层loop，里面的循环类似于two sum sorted
    # 这道题目的关键点就是需要去重复
    res = []
    nums.sort()
    for i in xrange(len(nums)-2):
        if i == 0 or nums[i] != nums[i-1]:
            # 过滤掉重复的nums[i]
            l, r = i+1, len(nums)-1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s < target:
                    l +=1
                elif s > target:
                    r -= 1
                else:
                    res.append((nums[i], nums[l], nums[r]))
                    l, r = l + 1, r - 1 # 左右移动
                    while l < r and nums[l] == nums[l-1]:
                        l += 1 # 过滤掉重复的nums[l]
                    while l < r and nums[r] == nums[r+1]:
                        r -= 1 # 过滤掉重复的nums[r]
    return res


def test_3sum():
    print three_sum([3,0,-2,-1,1,2]) # [[-2,-1,3],[-2,0,2],[-1,0,1]]
    print three_sum([1,-1,-1,0])
    print three_sum([-1,0,1,2,-1,-4])
    print three_sum([0,0,0,0])


def three_sum_closet(nums, target):
    # 和3Sum一样解法，只是需要更新closet的值
    nums.sort()
    import sys
    closet = sys.maxint
    for i in xrange(len(nums) - 2):
        if i == 0 or nums[i] != nums[i - 1]:
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == target: # 跟target一样
                    return target
                # if sum(i,j,k) is closer to target
                if abs(target-closet) > abs(target-s):
                    closet = s
                if s > target:
                    r -= 1  # sum is bigger, r-1
                else:
                    l += 1  # sum is smaller, l+1
    return closet


def three_sum_smaller(nums, target):
    # https://leetcode.com/problems/3sum-smaller/description/
    # 找到所有的比target小的3 sum的个数，也就是没有必要输出所有可能结果（否则必定为O(N^3)）
    # O(N^2)的做法是，如果对于排序后，i<j<k，且i+j+k<target，那么对于以i,j为pilot pointer
    # 所有属于[j+1, k]的元素x，都满足i+j+x<target，即nums[i]+nums[j]+nums[j+1..k]<target，此后j向右移
    # 这道题目不需要考虑重复元素，即重复也算结果，否则还需要不断地去掉重复元素，最坏情况也有可能O(N^3)
    count = 0
    nums.sort()
    for i in xrange(len(nums) - 2):
        j, k = i + 1, len(nums) - 1
        while j < k:
            s = nums[i] + nums[j] + nums[k]
            if s < target:
                count += k - j # k-(j+1)+1即是新的以i,j为pilot pointer的个数
                j += 1 # 满足，j右移变大一点
            else: # 如果不满足，k左移动变小一点
                k -= 1
    return count


def four_sum_recur(nums, target):
    # 把所有N sum的题目都变成2 sum的变体，时间复杂度为O(N^(N-1))
    def find_N_sum(nums, target, N, temp, results):
        # temp 是一个临时list，每次都要从之前的新建，results是最终结果
        if len(nums) >= N >= 2 and nums[0]*N <= target<=nums[-1]*N:
            if N == 2: # two pointers solve sorted 2-sum problem
                l,r = 0,len(nums)-1
                while l < r:
                    s = nums[l]+nums[r]
                    if s == target:
                        results.append(temp + [nums[l], nums[r]])
                        l += 1
                        while l < r and nums[l] == nums[l-1]:
                            l += 1 # 去重复
                    elif s < target:
                        l += 1
                    else:
                        r -= 1
            else: # recursively reduce N
                for i in range(len(nums)-N+1):
                    if i == 0 or (i > 0 and nums[i-1] != nums[i]):
                        find_N_sum(nums[i+1:], target-nums[i], N-1, temp+[nums[i]], results)

    results = []
    find_N_sum(sorted(nums), target, 4, [], results)
    return results


def four_sum_four_list(A, B, C, D):
    # 4个list A、B、C、D，找到所有可能的满足A[i] + B[j] + C[k] + D[l]=0的情况的个数
    # https://leetcode.com/problems/4sum-ii/description/
    # 其实就是两个2Sum的子问题，AB所有可能2Sum，CD所有可能2Sum但key是和的相反数
    # 然后看两个2Sum共有的key里面的value相加就是满足条件的总数。（如果是找到所有的index的组合，就是另一回事了）
    smap = {} # smap: 2sum value->count
    count = 0
    for x in A:
        for y in B:
            s = x + y
            smap[s] = smap.get(s, 0) + 1
    for i in C:
        for j in D:  # if not in map, 0
            count += smap.get(-i - j, 0)
    return count


def two_sum_binary_search_tree(root, target):
    """
    https://leetcode.com/problems/two-sum-iv-input-is-a-bst/description/
    Input:
        5
       / \
      3   6
     / \   \
    2   4   7
    Target = 9 -> True Target = 28 -> False Target = 11 -> True 也就是可能是任意两个节点
    解法1：遍历所有node，把所有的value放到一个array里面，然后用2sum的方法做，时间空间O(N)
    解法2：对于每一个node，求出target-node.val=diff，然后对这个diff做二分搜索，时间O(NlogN)，空间O(N)
    """
    def convert_to_array(root, target):
        nums = list([])
        if root:
            stack = list([root])
            while stack:
                node = stack.pop()
                nums.append(node.val)
                if node.left:
                    stack.append(node.left)
                if node.right:
                    stack.append(node.right)
        return two_sum_hash(nums, target)

    def binary_search(root, target):
        def bst(node, root, k):
            while root:
                if k == root.val:
                    if root != node:
                        # 如果root和node不是同一个，找到了目标node
                        return True
                    # 是同一个node，那么要继续向node的左边和右边找
                    return bst(None, node.left, k) or bst(None, node.right, k)
                elif k > root.val:
                    root = root.right
                else:
                    root = root.left
            return False
        if root:
            queue = deque([root])
            while queue:
                size = len(queue)
                while size:
                    size -= 1
                    node = queue.popleft()
                    diff = target - node.val
                    # do binary search on left and right
                    if bst(node, root, diff):
                        return True
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
        return False
