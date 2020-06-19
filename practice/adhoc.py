

def binary_search(nums, x):
    l , r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) / 2
        if nums[mid] == x:
            return True
        elif nums[mid] < x:
            l = mid + 1
        else:
            r = mid - 1

    return False


nums = [0,1,2,3,4,5,6,7,8,10,14,16,20]
for i in range(-4, 23):
    if not binary_search(nums, i):
        print i
