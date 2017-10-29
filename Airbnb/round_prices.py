# -- coding: utf-8 --
"""
  公司list价格分成好几个部分，但是都是整数，如果在美金是整数，
  到了欧洲的网页显示汇率转换之后就变成了floating point，然后要round成整数，
  但是全部加起来round，和单独round再加起来，结果会不一样
                  USD     其他货币     其他货币取整
  # base price    100 =>  131.13   => 131
  # cleaning fee   20 =>   26.23   => 26
  # service fee    10 =>   13.54   => 14
  # tax             5 =>    6.5    => 7
  #                   =>  177.4    => 178
  # sum           135 =>  178.93   => 179

  Abstraction:
  Given an array of numbers A = [x1, x2, ..., xn] and T = Round(x1+x2+... +xn).
  We want to find a way to round each element in A such that
  after rounding we get a new array B = [y1, y2, ...., yn]
  such that y1+y2+...+yn = T where  yi = Floor(xi) or Ceil(xi), ceiling or floor of xi.
  We also want to minimize sum |x_i-y_i|

  Input: A = [x1, x2, ..., xn], Sum T = Round(x1+x2+... +xn)
  Output: B = [y1, y2, ...., yn]

  Constraint #1: y1+y2+...+yn = T
  Constraint #2: minimize sum(abs(diff(xi - yi)))

  Examples:
  A = [1.2, 2.3, 3.4]
  Round(1.2 + 2.3 + 3.4) = 6.9 => 7
  1 + 2 + 3 => 6

  1 + 3 + 3 => 7
  0.2 + 0.7 + 0.4 = 1.3

  2 + 2 + 3 => 7
  0.8 + 0.3 + 0.4 = 1.5

  1 + 2 + 4 => 7
  0.2 + 0.3 + 0.6 = 1.1
  所以[1,2,4]比[1,3,3]要好

  Solution:
  - 计算 raw_price_sum_round 与 round_price_sum
  - 检查其差值
     1. raw_price_sum_round > round_price_sum
       - 说明我们round_price_sum小了，应该把有些原本取floor(小数部分<0.5)的取ceil，差X就要改X个
       - 按照小数部分从大到小排序，取小于0.5的X个用ceil，其他正常round
     2. raw_price_sum_round < round_price_sum
       - 说明我们round_price_sum大了，应该把有些原本取ceil(小数部分>=0.5)的取floor，差X就要改X个
       - 按照小数部分从小到大排序，取大于等于0.5的X个用floor，其他正常round
     3. raw_price_sum_round = round_price_sum
       - 不用任何操作
"""
import math


class Number(object):
    def __init__(self, val, index):
        self.val = val
        # 最开始的index需要保留，因为之后可能需要排序
        self.index = index
        self.fraction = val - math.floor(val)

    def __repr__(self):
        return "%s, %s, %s" % (self.index, self.fraction, self.val)


def calculate_round_prices(prices):
    def ceil_or_floor():
        return math.ceil if raw_price_sum_round > round_price_sum else math.floor

    def check_fraction():
        return lambda x: x.fraction < 0.5 if raw_price_sum_round > round_price_sum else \
            lambda x: x.fraction >= 0.5

    if not prices or len(prices) == 0:
        return [0]
    raw_sum, round_price_sum = 0.0, 0
    round_prices, numbers = [], []
    # 计算出raw price sum，还有round price sum，以及生成一个 Number array
    for i, raw_price in enumerate(prices):
        numbers.append(Number(raw_price, i))
        raw_sum += raw_price
        round_price = int(round(raw_price))
        round_price_sum += round_price
        round_prices.append(round_price)
    # 把raw price sum round 成一个int
    raw_price_sum_round = int(round(raw_sum))
    if raw_price_sum_round == round_price_sum:
        # 刚好相等，res里面的round price就是我们想要的
        return round_prices
    # 不相等，找到需要改变的数量，并按照小数位来排序
    # 如果raw_price_sum_round > round_price_sum， 按照小数部分从大到小排序
    # 即从最大的小数位的number开始，这样子绝对值之差才会变min
    count = abs(raw_price_sum_round - round_price_sum)
    change = ceil_or_floor()
    check_half = check_fraction()
    # 按照小数部分排序，默认为升序
    numbers.sort(reverse=raw_price_sum_round > round_price_sum, key=lambda n: n.fraction)
    for i, num in enumerate(numbers):
        if check_half(num) and count > 0:
            count -= 1
            round_prices[num.index] = int(change(num.val))
        else:
            round_prices[num.index] = int(round(num.val))

    return round_prices


test = [ 2.3, 1.2, 3.4]
print calculate_round_prices(test)
