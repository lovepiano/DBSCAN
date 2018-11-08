#__author__:波爷
#__date__:2018/11/1

from scipy.io import loadmat          #导入加载mat文件的函数
from pylab import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

matplotlib.rcParams['axes.unicode_minus']=False
mpl.rcParams['font.sans-serif'] = ['SimHei']    #设置字体编码
'导入数据'
# data=loadmat('./data/2d4c.mat')    #data是一个字典类型数据
# data=loadmat('./data/long.mat')    #data是一个字典类型数据
# data=loadmat('./data/moon.mat')    #data是一个字典类型数据
# data=loadmat('./data/sizes5.mat')    #data是一个字典类型数据
# data=loadmat('./data/smile.mat')    #data是一个字典类型数据
# data=loadmat('./data/spiral.mat')    #data是一个字典类型数据
# data=loadmat('./data/square1.mat')    #data是一个字典类型数据
data=loadmat('./data/square4.mat')    #data是一个字典类型数据

print(data.keys())

'smile'
# data_D=data['smile'][:,[0,1]]   #样本集
'moon'
# data_D=data['moon'][:,[0,1]]   #样本集
# data_D=data['a'][:,[0,1]]   #样本集     moom.mat数据集中是这个字段
'long1'
# data_D=data['long1'][:,[0,1]]   #样本集
# print(data['long1'].shape)
'sizes5'
# data_D=data['sizes5'][:,[0,1]]   #样本集
'spiral'
# data_D=data['spiral'][:,[0,1]]   #样本集
'square1'
# data_D=data['square1'][:,[0,1]]   #样本集
'square4'
data_D=data['b'][:,[0,1]]   #样本集
'2d4c'
# data_D=data['a'][:,[0,1]]   #样本集

# print(data_D)
print(pd.DataFrame(data_D).describe())

'参数,调的时候优先调节epis，再调MinPts'
epis =1.28    #增大会使聚类数减少
MinPts = 28    #增大会使聚类数增大

'欧氏距离定义'
def distance(x,y):
    #np.square() 求各个元素的平方
    return np.sqrt(np.sum(np.square((x - y))))       #返回欧氏距离

'DBSCANs算法实现'
def MY_DBSCAN(data_D,epis,MinPts):
    '寻找核心对象集合'
    core_obj = []
    for i in range((data_D.shape)[0]):
        total = 0
        for j in range((data_D.shape)[0]):
            dis=distance(data_D[i],data_D[j])               #计算邻域数（包括自身）
            if dis <= epis:
                total += 1
        if total >= MinPts:
            core_obj.append(list(data_D[i]))

    # print(len(core_obj))

    '簇'
    C={}
    '初始化聚类簇'
    k=0
    '未访问样本集'
    not_visited_data_D=[]
    for i in range((data_D.shape)[0]):
        not_visited_data_D.append(list(data_D[i]))

    old_not_visited_data_D=0
    while len(core_obj) > 0:
        #记录当前未访问样本集合
        old_not_visited_data_D = not_visited_data_D
        #堆积选取核心对象
        rand_index=np.random.choice(len(core_obj),1,replace=False)
        rand_core_obj = core_obj[rand_index[0]]
        #初始化队列
        queue = []
        queue.append(rand_core_obj)
        # !=号是对数组中的每个元素进行比较，得出bool值，所以判断时要用any()或者all()，而列表不会这样逐个元素进行判断
        not_visited_data_D=[m for m in not_visited_data_D if (m != rand_core_obj)]
        # np.delete(not_visited_data_D,core_index,0)          #删除行或列，第三个参数指定删除列1还是行0，第二个参数指定删除第几列或行
        #lsit.remove()   删除列表中指定的对象
        while len(queue)>0:
            #取出首个元素
            first_ele = queue[0]
            queue.remove(queue[0])
            total = 0
            idx = []
            for j in range((data_D.shape)[0]):
                dis=distance(first_ele,data_D[j])               #计算邻域数（包括自身）
                if dis <= epis:
                    total += 1
                    idx.append(j)
            if total >= MinPts:
                derta=[]
                for i in idx:
                    if list(data_D[i]) in not_visited_data_D:
                        derta.append(list(data_D[i]))
                queue.extend(derta)    #将列表derta中的元素逐个加入queue列表中
                # not_visited_data_D.remove(derta)
                not_visited_data_D=[m for m in not_visited_data_D if m not in derta]   #列表生成器

        k=k+1
        C[k]=[x for x in old_not_visited_data_D if x not in not_visited_data_D]
        core_obj=[c_obj for c_obj in core_obj if c_obj not in C[k]]

    return C

C=MY_DBSCAN(data_D,epis,MinPts)
print(len(C))
#绘制结果
def draw(C):
    color = ['r', 'y', 'g', 'b', 'c', 'k', 'm']
    maker = ['+', 'x', '*', 'd', '>', '<']
    for i in C.keys():
        X = []
        Y = []
        datas = C[i]
        for j in range(len(datas)):
            X.append(datas[j][0])
            Y.append(datas[j][1])
        if i<=6:
            plt.scatter(X, Y, marker='o', color=color[i])
        else:
            plt.scatter(X, Y, marker=maker[i-7], color=color[0])
    plt.title('square4聚类结果')
    # plt.legend()
    plt.grid()
    plt.show()
draw(C)



