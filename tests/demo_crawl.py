import math
t1 = 1500


def sigmoid(d, t):
    """
    :param d: 目标距离
    :param t: 运动时间
    :return: 目前位移距离
    """

    def g(t):
        return abs(1 / (1 + math.exp(-3.5 * t / t1)))

    return d * (g(t) / g(t1))


from ReSpider.utils.tools import get_files


if __name__ == '__main__':
    print(get_files('H:/维普期刊'))
    # print(get_files('H:/ERS客户'))

