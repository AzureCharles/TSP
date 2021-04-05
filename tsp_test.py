import TSP_DP as TSP 	#Dynamic programming
import SA	#Simulated annealing

TEST1 = [[0,12,1,8],[12,0,2,3],[1,2,0,10],[8,3,10,0]]
TEST1_VERTICES = [1,2,3,4]
TEST2 = SA.distance_p2p_mat()
TEST2_VERTICES = [city for city in range(1,SA.num_city+1)]

def dynamicProgramTest(matrix,vertex_data):
	 
    TSP.main(matrix,vertex_data)

def simulatedAnnealTest():
	pass


if __name__ == '__main__':    
    dynamicProgramTest(TEST1,TEST1_VERTICES)	#能够正常工作
    dynamicProgramTest(TEST2,TEST2_VERTICES)	#list index out of range报错
    print(TEST2,TEST2_VERTICES)