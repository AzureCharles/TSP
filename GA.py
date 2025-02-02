import random
import numpy as np
import math

num_city = 30   #城市总数,编号为0-29
num_total = 100 #随机生成的初始解的总数
copy_num = 70   #保留的解的个数
cross_num = 20  #交叉解的个数
var_num = 10    #变异解的个数
GEN = 3000   #终止进化代数

#print(location)

#随机生成初始解，以列表存储： [[],[],[]...]
def generate_initial():
    initial=[]
    city=list(range(num_city))
    for i in range(num_total):
        random.shuffle(city)
        p=city.copy()
        while (p in initial):
            #print('2333')#随机了一个重复的解
            random.shuffle(city)
            p=city.copy()
        initial.append(p)
    return initial


#计算两个城市之间的距离
def distance_p2p_mat():
    dis_mat=[]
    for i in range(30):
        dis_mat_each=[]
        for j in range(30):
            dis=math.sqrt(pow(location[i][0]-location[j][0],2)+pow(location[i][1]-location[j][1],2))
            dis_mat_each.append(round(dis,2))   #四舍五入保留两位小数
        dis_mat.append(dis_mat_each)
   # print(dis_mat)
    return dis_mat


#目标函数计算,适应度计算&中间计算。适应度为1/总距离*10000,将原问题求最小转化为求适应度函数最大，与适应度概念一致
def dis_adp_total(dis_mat,initial):
    dis_adp=[]
#    dis_test=[]   
    for i in range(num_total):
        dis=0
        for j in range(num_city-1):
            dis=dis_mat[initial[i][j]][initial[i][j+1]]+dis
        dis=dis_mat[initial[i][num_city-1]][initial[i][0]]+dis#回家
#        dis_test.append(dis)        
        dis_adp_each= 10000.0/dis
        dis_adp.append(dis_adp_each)
#    print(dis_test)
    return dis_adp




def choose_fromlast(dis_adp,answer_source):
    mid_adp=[]
    mid_adp_each=0
    for i in range(num_total):
        mid_adp_each=dis_adp[i]+mid_adp_each
        mid_adp.append(mid_adp_each)
    # print(mid_adp)
    # 产生0-mid_adp[num_total-1]之间的随机数
    # 选择n-1<随机数<n的那个n的解,保留
    copy_ans=[]
    for p in range(copy_num):
        rand=random.uniform(0,mid_adp[num_total-1])#产生随机数
       # print(rand)
       # print(p)
        for j in range(num_total):
            if (rand<mid_adp[j]):#查找位置
                copy_ans.append(answer_source[j])
                break
            else:
                continue
    return copy_ans
                
    


#随机选择保留下来的70中的20个进行交叉
def cross_pronew(copy_ans):
    for i in range(cross_num):
        which=random.randint(0,copy_num-1)#选择对那个解交叉
        cross_list=copy_ans[which].copy()
        while (cross_list in copy_ans):
            p=random.randint(0,num_city-1)
            q=random.randint(0,num_city-1)
            cross_list[p],cross_list[q]=cross_list[q],cross_list[p]#第一次交换位置
            m=random.randint(0,num_city-1)
            n=random.randint(0,num_city-1)
            cross_list[m],cross_list[n]=cross_list[n],cross_list[m]#第二次交换位置            
        copy_ans.append(cross_list)
    cross_ans=copy_ans.copy()
    return cross_ans
        
    

#随机选择那90中的10个进行变异
def var_pronew(cross_ans):
    for i in range(var_num):
        which = random.randint(0,copy_num+cross_num-1)#选择对那个解交叉
        var_list = cross_ans[which].copy()
        while (var_list in cross_ans):
            p = random.randint(0,num_city-1)
            q = random.randint(0,num_city-1)
            var_list[p],var_list[q] = var_list[q],var_list[p]#交换位置
        cross_ans.append(var_list)
    var_ans = cross_ans.copy()
    return var_ans



    
'''

answer_source=generate_initial()#原initial
#print(initial)
dis_mat=distance_p2p_mat()
#print(dis_mat)
dis_adp=dis_adp_total(dis_mat,answer_source)
#print(dis_adp)
copy_answer=choose_fromlast(dis_adp,answer_source)
#print(copy_answer)
cross_answer=cross_pronew(copy_answer)
#print(cross_answer)
var_answer=var_pronew(cross_answer)
print(var_answer)



'''


def geneticAlgorithm(dis_mat,exp=600):
    '''
    简单遗传算法主体
    设置终止代数与期望值exp双条件，若存在距离<期望值的结果，则直接停止算法。
    '''
    answer_source = generate_initial()
    dis_adp = dis_adp_total(dis_mat,answer_source)
    
    if (max(dis_adp)>10000/exp):
        print('已经找到期望距离：',10000/max(dis_adp))

    else:
        print('未找到期望距离，尝试遗传算法')    
        answer_new = answer_source
        dis_adp_new = dis_adp
        adp_max_new = max(dis_adp)
        while(adp_max_new <= 10000/exp && generation < GEN):
            generation = 1
            copy_answer = choose_fromlast(dis_adp_new,answer_new)
            cross_answer = cross_pronew(copy_answer)
            var_answer = var_pronew(cross_answer)
            answer_new = var_answer.copy()
            dis_adp_new = dis_adp_total(dis_mat,answer_new)
            adp_max_new = max(dis_adp_new)
    #        dis_min=10000/adp_max_new
    #        print('这次是：',dis_min)
            generation += 1
        dis_min=10000/adp_max_new
        print('遗传算法得出最短距离是：',dis_min)

if __name__ == '__main__':
    location = np.loadtxt('city30_location.txt')	#test1
    exp = 430
    dis_mat = distance_p2p_mat()
    #print(dis_mat)
    geneticAlgorithm(dis_mat, exp)
    

