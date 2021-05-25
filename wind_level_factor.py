import numpy as np

wind_scale_min_const = {0: 0.0, 1: 0.3, 2: 1.6, 3: 3.4, 5: 8.0,
                        6: 10.8, 7: 13.9, 8: 17.2, 9: 20.8, 10: 24.5,
                        -1: np.NAN}

wind_scale_max_const = {0: 0.2, 1: 1.5, 2: 3.3, 3: 7.9, 5: 10.7,
                        6: 13.8, 7: 17.1, 8: 20.7, 9: 24.4, 10: 28.4,
                        -1: np.NAN}


def drag_coefficient(p, v, w_real):
    """
    风阻系数
    :param p: 压强
    :param v: 速度
    :param w_real: 油耗
    :return:
    """
    w_saloulate = 0.5 * p * np.power(v, 2)
    ms = w_real / w_saloulate
    return ms


def get_maxSpeed(f, c, rho, s):
    """
    获取最大速度
    :param f: 力
    :param c:
    :param rho: 密度
    :param s:
    :return:
    """
    param_temp = c * rho * s
    v_power = 2 * f / param_temp
    v_max = np.power(v_power, 0.5)
    return v_max
