# https://leetcode.com/problems/missing-number/description/
# https://leetcode.com/problems/first-missing-positive/description/

# Interview Question

# Given an array of sorted integers without duplicates, and two indices, i and j.
# Can you write code to calculate the numbers of missing integers between these two #indices.

# For example nums = [2,4,7,8,9,15],
# of missing integer between 0,1 is 1, nums[0] = 2,nums[1] = 4, 2, 3, 4, -> 3, as 1 numbers
# of missing integer between 1,2 is 2, nums[1] = 4, nums[2]= 7, [4, 7] -> 5,6  so 2 numbers
# of missing integer between 0,2 is 3, 2, 4, 7 in nums, but no 3, 5,6 so 3 numbers missing
# of missing integer between index i and index j ?


def find_missing_numbers(nums, i, j):
    # return total # of missing numbers in nums between i and j
    # 1st idea: get nums[i]=x and nums[j]=y, then get a range between then [x, y]
    # iterate all numbers z in [x, y], if z is not in nums[i...j], z is a missing numbers, then we increase the total count
    # return the result total count; to find if z is in nums[i...j], we do binary search O(logN)
    # if not BS: use hash set to record all numbers in nums[i...j] not missing in the nums, search time = O(1), but space O(N)
    # 0,2 we have 2,4,7, we need iterate [3, 6], then check if a numbers is in set(4), 3,4,5,6, O(N) time in total
    # 3rd idea: get all numbers between nums[i...j], then for each pair of them, [2, 4, 7], 1 + 2 = 3, O(M) M = element between i...j
    # improve O(M) -> 7-2-1=4, 4-1 = 3, as long as we have nums[i] and nums[j], get the total = nums[j]-nums[i]-1 - (j-i-1)
    return nums[j] - nums[i] - 1 - (j - i - 1) # get the range between them


nums = [2, 4, 7, 8, 9, 15]


def test():
    for i in xrange(len(nums) - 1):
        for j in xrange(i + 1, len(nums)):
            print i, j, nums[i], nums[j], "total=", find_missing_numbers(nums, i, j)


# Q2
# Given the same array, can you write code to tell me what is the Nth missing integer.

# For example [2,4,7,8,9,15],
# the 1st missing integer is 3,
# the 2nd missing integer is 5,
# the 3rd missing integer is 6
# Nth?


def find_nth_missing_number(nums, n):
    # return the nth missing numbers
    # idea: iterate from begning, when have a pair, i and j, find the total missing numbers M inbetween
    # check if n < M, the target is between i and j, return nums[i] + n
    # else: the target is after j, 1) update n = n - M  2) continue to the next pair of j and j+1
    # space O(1), time O(N), N = the numbers of elements in nums, N-1, each time call lib, O(1), in total = O(N)
    # binary search, pre-process the nums to get another array, with the total numbers of misssing in nums
    # [1, 3, 3, 3, 8], do binary search say n = 7, then between [3,8] go to the nums[i] then nums[i] + (n - 3)
    # cost O(N)
    # do binary search: narrow down the range of i..j for search by:
    # two ranges, [i...k] [k...j], then call the lib to get missing numbers of each range, left and right,
    # if n is in left, then we go to left, next time, narrow down to [i...m] [m...k]
    # until n is in a range [x...y] where x = y - 1. in this case, the nth is after nums[x], the result = nums[x] + n

    # how to improve?
    # SQL, ETL, pipeline, redshift, hive,
    if n == 0:
        raise Exception("Error message...")
    i = 0
    while i < len(nums) - 1:
        j = i + 1
        M = find_missing_numbers(nums, i, j)
        if n <= M:
            return nums[i] + n
        else:
            n -= M
            i += 1
    # we don't find, return None
    return None


nums = [2, 4, 7, 8, 9, 15]


def test2():
    for i in xrange(1, 11):
        print i, find_nth_missing_number(nums, i)


test2()


