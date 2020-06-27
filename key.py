import matplotlib.pyplot as plt
import numpy as np


class ChaoticLogisticMap:
    # Chaotic 1D Logistic Map

    def __init__(self):
        self.i = 0
        # self.lambda_lst = np.arange(0, 4, 4 / (10000 - 1))
        self._lambda = 3.144
        self.w_p = 0.003  # w(0) is initial condition

    def next_key(self):
        self.i += 1
        # self.w_p = self.lambda_lst[self.i] * (self.w_p - self.w_p ** 2)
        self.w_p = self._lambda * (self.w_p - self.w_p ** 2)

        rounded_key = int(np.floor(self.w_p / 0.1))
        return rounded_key


# testing area:
# key = ChaoticLogisticMap()
#
# m = []
# for i in range(1000):
#     m.append(key.next_key())
# print(m)
# plt.plot(m)
# plt.show()
