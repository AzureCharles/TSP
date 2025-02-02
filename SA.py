import random
import numpy as np
import math



#==========================================
#构造对称矩阵，包括两个城市之间的距离信息
def distance_p2p_mat(location,num_city):
    dis_mat=[]
    for i in range(num_city):
        dis_mat_each=[]
        for j in range(num_city):
            dis=math.sqrt(pow(location[i][0]-location[j][0],2)+pow(location[i][1]-location[j][1],2))
            dis_mat_each.append(round(dis,2))	#四舍五入保留两位小数
        dis_mat.append(dis_mat_each)
   # print(dis_mat)
    return dis_mat

#计算所有路径对应的距离
def cal_newpath(dis_mat,path,num_city):
    dis=0
    for j in range(num_city-1):
        dis=dis_mat[path[j]][path[j+1]]+dis
    dis=dis_mat[path[num_city-1]][path[0]]+dis#回家
    return dis

#==========================================


def simulatedAnneal(M,dis_mat,path,dis,num_city,t_current):
	while (t_current>lowest_t):#外循环，改变温度
	    count_m=0#M的计数
	    count_iter=0#迭代次数计数
	    while (count_m<M and count_iter<iteration):#内循环，连续多次不接受新的状态或者是迭代多次,跳出内循环        
	        i=0
	        j=0
	        while(i==j):#防止随机了同一城市
	            i=random.randint(1,num_city-1)
	            j=random.randint(1,num_city-1)
	        path_new=path.copy()
	        path_new[i],path_new[j]=path_new[j],path_new[i]#任意交换两个城市的位置,产生新解
	        #计算新解的距离
	        dis_new=cal_newpath(dis_mat,path_new,num_city)
	        #求差
	        dis_delta=dis_new-dis
	        #取0-1浮点随机数
	        rand=random.random()
	        #计算指数函数的值
	        exp_d=math.exp(-dis_delta/t_current)
	        #选择
	        if dis_delta<0:
	            path=path_new
	            dis=dis_new
	        elif exp_d>rand:
	            path=path_new
	            dis=dis_new    
	        else:
	            count_m=count_m+1
	        count_iter=count_iter+1
	    t_current=0.99*t_current#改变温度
	#外循环结束
	minDistanceDict = {'最短距离':dis, '最短路径':path}
	print(minDistanceDict)
	return dis,path

def getTestResult(location,num_city):
	initial_t = 100 * num_city    #初始温度
	global lowest_t,iteration
	lowest_t = 0.001  #最低温度
	iteration = 500  #设置迭代次数
	M = 50 * num_city  #当连续多次都不接受新的状态，开始改变温度
	
	
	#点对点距离矩阵
	dis_mat = distance_p2p_mat(location,num_city)
	#初始路径
	path = list(range(num_city))
	#初始距离
	dis = cal_newpath(dis_mat,path,num_city)
	#初始温度
	
	simulatedAnneal(M,dis_mat,path,dis,num_city,initial_t)


if __name__ == '__main__':
	location1 = np.loadtxt('city30_location.txt')	#test1
	#print(location1)
	location2 = np.loadtxt('city31_location.txt')	#test2
	num_city1 = 30	#城市总数
	num_city2 = 31	#城市总数

	getTestResult(location1,num_city1)
	getTestResult(location2,num_city2)



