import scipy.constants as cn
import numpy as np


class curveMaxSpeed:
    def __init__(self, f, m, r, theta, g=cn.g, accuracy=2):
        """
        初始化方法
        :param f: 所受的力
        :param m: 物体的质量
        :param r: 坡道长度
        :param theta: 倾斜角度
        :param g: 重力加速度，默认由scipy.constants科学常量库提供
        :param accuracy: 精确度，即精确到几位小数，默认为2
        """
        self.f = f
        self.m = m
        self.theta = theta
        self.g = g
        self.accuracy_regex = f'0.{accuracy}f'
        self.r = r

    def centripetal_force(self, m, g, theta):
        """
        计算向心力
        :return:
        """
        f = m * g * np.tan(theta)
        return format(f, self.accuracy_regex)

    def friction_coefficient(self, f, m, g):
        """
        计算摩擦因数
        :param f: 力
        :param m: 质量
        :param g: 重力加速度，默认由scipy.constants科学库提供
        :return:
        """
        mu = f / m * g
        return format(mu, self.accuracy_regex)

    def get_maxSpeed(self):
        f_centripetal = self.centripetal_force(self.m, self.g, self.theta)
        param_temp = f_centripetal * self.r / self.m
        v_max = np.power(param_temp, 0.5)
        return format(v_max, self.accuracy_regex)
