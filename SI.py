import random
import numpy as np
import math
import time
import matplotlib.pyplot as plt



ANT_NUM=200 #蚂蚁个数

alpha=1 #信息素影响因子
beta=1  #期望影响因子
info=0.1 #信息素的挥发率
Q=1 #常数

ITER_MAX = 500 #迭代上限

#==========================================
#对称矩阵，两个城市之间的距离
def distance_p2p_mat():
    dis_mat=[]
    for i in range(num_city):
        dis_mat_each=[]
        for j in range(num_city):
            dis=math.sqrt(pow(location[i][0]-location[j][0],2)+pow(location[i][1]-location[j][1],2))
            dis_mat_each.append(dis)
        dis_mat.append(dis_mat_each)
   # print(dis_mat)
    return dis_mat

#计算所有路径对应的距离
def cal_newpath(dis_mat,path_new):
    dis_list=[]
    for each in path_new:
        dis=0
        for j in range(num_city-1):
            dis=dis_mat[each[j]][each[j+1]]+dis
        dis=dis_mat[each[num_city-1]][each[0]]+dis#回家
        dis_list.append(round(dis,2))
    return dis_list

#==========================================
def antSwarmIntelligence(dis_mat,num_city,):
    #期望矩阵
    e_mat_init=1.0/(dis_mat+np.diag([10000]*num_city))#加对角阵是因为除数不能是0
    diag=np.diag([1.0/10000]*num_city)
    e_mat=e_mat_init-diag#还是把对角元素变成0
    #初始化每条边的信息素浓度，全1矩阵
    pheromone_mat=np.ones((num_city,num_city))
    #初始化每只蚂蚁路径，都从0城市出发
    path_mat=np.zeros((ANT_NUM,num_city)).astype(int)

    iter_num_list = []  #记录当前迭代次数
    dis_record_list = []    #记录局部较优值

    count_iter = 0
    #while dis_new>400:
    while count_iter < ITER_MAX :
        for ant in range(ANT_NUM):
            visit=0 #都从0城市出发
            unvisit_list=list(range(1,30)) #未访问的城市
            for j in range(1,num_city):
                #轮盘法选择下一个城市
                trans_list=[]
                tran_sum=0
                trans=0
                for k in range(len(unvisit_list)):
                    trans +=np.power(pheromone_mat[visit][unvisit_list[k]],alpha)*np.power(e_mat[visit][unvisit_list[k]],beta)
                    trans_list.append(trans)
                    tran_sum =trans

                rand=random.uniform(0,tran_sum) #产生随机数

                for t in range(len(trans_list)):
                    if(rand <= trans_list[t]):
                        visit_next=unvisit_list[t]

                        break
                    else:
                        continue
                path_mat[ant,j]=visit_next #填路径矩阵

                unvisit_list.remove(visit_next)#更新
                visit=visit_next#更新

        #所有蚂蚁的路径表填满之后，算每只蚂蚁的总距离
        dis_allant_list=cal_newpath(dis_mat,path_mat)

        #每次迭代更新最短距离和最短路径
        if count_iter == 0:
            dis_new=min(dis_allant_list)
            path_new=path_mat[dis_allant_list.index(dis_new)].copy()
        else:
            if min(dis_allant_list) < dis_new:
                dis_new=min(dis_allant_list)
                path_new=path_mat[dis_allant_list.index(dis_new)].copy()

        # 更新信息素矩阵
        pheromone_change=np.zeros((num_city,num_city))
        for i in range(ANT_NUM):
            for j in range(num_city-1):
                pheromone_change[path_mat[i,j]][path_mat[i,j+1]] += Q/dis_mat[path_mat[i,j]][path_mat[i,j+1]]
            pheromone_change[path_mat[i,num_city-1]][path_mat[i,0]] += Q/dis_mat[path_mat[i,num_city-1]][path_mat[i,0]]
        pheromone_mat=(1-info)*pheromone_mat+pheromone_change

        iter_num_list.append(count_iter)
        dis_record_list.append(dis_new)
        count_iter += 1 #迭代计数+1，进入下一次
    asiResult = {'最短距离':dis_new,'最短路径':path_new}

    return iter_num_list,dis_record_list,asiResult


if __name__ == '__main__':
    start1 = time.perf_counter()
    location = np.loadtxt('city30_location.txt')	#test1
    num_city = 30  # 城市个数
    #exp_value = 427
    # 点对点距离矩阵
    dis_list = distance_p2p_mat()
    dis_mat = np.array(dis_list)  # 转为矩阵
    #print(dis_mat)

    x,f,result = antSwarmIntelligence(dis_mat, num_city)
    print(result)
    plt.figure(figsize=(40, 30), dpi=100)
    plt.plot(x,f)
    plt.show()
    end1 = time.perf_counter()
    print("finished in : %s Seconds " % (end1 - start1))

