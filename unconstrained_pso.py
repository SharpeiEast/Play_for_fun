# 速度
# Vi+1 = w*Vi + c1 * r1 * (pbest_i - Xi) + c2 * r2 * (gbest_i - Xi)
# 位置
# Xi+1 = Xi + Vi+1
# vi, xi 分别表示粒子第i维的速度和位置
# pbest_i, gbest_i 分别表示某个粒子最好位置第i维的值、整个种群最好位置第i维的值

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def fitness_func(X):
    """计算粒子的的适应度值，也就是目标函数值，X 的维度是 size * 2 """
    pi = np.pi
    x = X[:, 0]
    y = X[:, 1]
    return x**2+y**2+x


def velocity_update(V, X, pbest, gbest, c1, c2, w, max_val):
    """
    根据速度更新公式更新每个粒子的速度
    :param V: 粒子当前的速度矩阵，20*2 的矩阵
    :param X: 粒子当前的位置矩阵，20*2 的矩阵
    :param pbest: 每个粒子历史最优位置，20*2 的矩阵
    :param gbest: 种群历史最优位置，1*2 的矩阵
    """
    size = X.shape[0]
    r1 = np.random.random((size, 1))
    r2 = np.random.random((size, 1))
    V = w*V+c1*r1*(pbest-X)+c2*r2*(gbest-X)
    # 防止越界处理
    V[V < -max_val] = -max_val
    V[V > -max_val] = max_val
    return V


def position_update(X, V):
    """
    根据公式更新粒子的位置
    :param X: 粒子当前的位置矩阵，维度是 20*2
    :param V: 粒子当前的速度举着，维度是 20*2
    """
    return X+V


def pos():
    w = 1
    c1 = 2
    c2 = 2
    r1 = None
    r2 = None
    dim = 2
    size = 20
    iter_num = 1000
    max_val = 0.5
    best_fitness = float(9e10)
    fitness_val_list = []
    # 初始化种群各个粒子的位置
    X = np.random.uniform(-5, 5, size=(size, dim))
    # 初始化各个粒子的速度
    V = np.random.uniform(-0.5, 0.5, size=(size, dim))
    # print(X)
    p_fitness = fitness_func(X)
    g_fitness = p_fitness.min()
    fitness_val_list.append(g_fitness)

    # 初始化的个体最优位置和种群最优位置
    pbest = X
    gbest = X[p_fitness.argmin()]
    # 迭代计算
    for i in range(1, iter_num):
        V = velocity_update(V, X, pbest, gbest, c1, c2, w, max_val)
        X = position_update(X, V)
        p_fitness2 = fitness_func(X)
        g_fitness2 = p_fitness2.min()

        # 更新每个粒子的历史最优位置
        for j in range(size):
            if p_fitness[j] > p_fitness2[j]:
                pbest[j] = X[j]
                p_fitness[j] = p_fitness2[j]
            # 更新群体的最优位置
            if g_fitness > g_fitness2:
                gbest = X[p_fitness2.argmin()]
                g_fitness = g_fitness2
            # 记录最优迭代记录
            fitness_val_list.append(g_fitness)
            i += 1

    # 输出迭代结果
    print("最优值是：%.5f" % fitness_val_list[-1])
    print("最优解是：x=%.5f,y=%.5f" % (gbest[0], gbest[1]))

    # 绘图
    plt.plot(fitness_val_list, color='r')
    plt.title('迭代过程')
    plt.show()


pos()
