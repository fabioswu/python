def find_the_peak(nums):
    # 判断是否为空
    if not nums:
        return []

    # 判断是否只有一位数
    if len(nums) == 1:
        return [0]

    # 主体
    ans = []
    if nums[0] > nums[1]:    # 判断开头
        ans.append(0)
    for i in range(1, len(nums)-1):    # 依次遍历（只遍历中间的，两头另外判断）
        if nums[i] > nums[i-1] and nums[i] > nums[i+1]:  # 判断是否大于左右两边
            ans.append(i)
    if nums[-1] > nums[-2]:  # 判断结尾
        ans.append(len(nums)-1)

    return ans

print(find_the_peak([1, 2, 3, 1, 4, 5]))
