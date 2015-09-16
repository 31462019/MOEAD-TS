#encoding=utf-8
from sub_problem import SubProblem
from individual import individual
import random

class MOEAD_TS():

	def __init__(self,fevals):
		self.MaxFunEvals = fevals
		#最大迭代次数
		self.neighborhoodsize = 10
		#邻居个数，即T
		self.numF = 2
		#目标函数个数
		self.subnum = 20
		#即N，子问题个数
		self.room_num = 15
		#房间数
		self.mid_a,self.mid_b =2,3
		#左中心岛，右中心岛
		self.list_sub= []
		#存储sub的list
		self.list_pi = [1.0]*self.subnum	
		#存储权益值
		self.reference = self.numF*[0.0]	
		#存储参考点

	def init_weight_vector(self):
		for i in range(self.subnum):
			sub_problem = SubProblem()
			sub_problem.lam1 = float(i)/(self.subnum - 1)
			sub_problem.lam2 = 1.0 - sub_problem.lam1
			self.list_sub.append(sub_problem)
	
	def init_reference_point(self):
		for i in range(self.numF):
			ind = individual(self.room_num)
			ind.
 
	def init_neighborhood(self):
		pass



	def init_population(self):
		pass

	def update_neighbor_solution(self):
		pass

	def update_reference_point(self):
		pass

	def show(self):
		print '1.sub_problem'
		for i in self.list_sub:
			print i.lam1,i.lam2
		print '2.list_pi'
		print self.list_pi

		
if __name__ =='__main__':
	moead_ts = MOEAD_TS(200)
	moead_ts.init_weight_vector()
	moead_ts.show()