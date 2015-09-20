#encoding=utf-8
from sub_problem import SubProblem
from individual import individual
import random

class MOEAD_TS():

	def __init__(self,fevals,file_name):
		self.MaxFunEvals = fevals
		#最大迭代次数
		self.neighborhoodsize = 10
		#邻居个数，即T
		self.numF = 2
		#目标函数个数
		self.subnum = 20
		#即N，子问题个数
		self.list_sub= []
		#存储sub的list
		self.list_pi = [1.0]*self.subnum	
		#存储权益值
		self.reference = self.numF*[0.0]	
		#存储参考点
		self.file_name = file_name
		self.read_data()
		#读取文件数据

	def init_weight_vector(self):
	#初始化每个子问题的权向量，并将子问题加至self的List表中
		for i in range(self.subnum):
			sub_problem = SubProblem()
			sub_problem.lam1 = float(i)/(self.subnum - 1)
			sub_problem.lam2 = 1.0 - sub_problem.lam1
			self.list_sub.append(sub_problem)
		print 'hello'
	
	def init_reference_point(self):
		#for i in range(self.numF):
			ind = individual(self.file_name)
			ind.randomize()

	def init_neighborhood(self):
		pass


	def init_population(self):
		pass

	def update_neighbor_solution(self):
		pass

	def update_reference_point(self):
		pass
		
	def read_data(self):
		f = open(self.file_name,'r')
		line = f.readline()
		if line.strip() == 'Room':
			i = f.readline()
			self.room = int(i.strip())
			line = f.readline()
		if line.strip() =='center_island':
			i = f.readline()
			self.cent_a,self.cent_b = map(int,i.strip().split(','))
			line = f.readline()
		if line.strip() =='width':
			i = f.readline()
			self.width = map(float,i.strip().split(','))
			line = f.readline()			
		if line.strip() =='flow':
			self.flow = []
			for i in range(self.room):
				line = f.readline()
				self.flow.append(map(float,line.strip().split(',')))
			line = f.readline()
		if line.strip() =='limit_row':
			i = f.readline()
			self.limit_row = map(float,i.strip().split(','))
			line = f.readline()
		if line.strip() == 'limit_wid':
			i = f.readline()
			self.limit_wid = map(float,i.strip().split(','))
			line = f.readline()
		if line.strip() == 'corridor':
			i = f.readline()
			self.corridor = int(i.strip())
			line = f.readline()
		if line.strip() == 'adj':
			self.adj = []
			for i in range(self.room):
				line = f.readline()
				self.adj.append(map(int,line.strip().split(',')))
			line = f.readline()
		f.close()
	
	def show(self):
		print '1.sub_problem'
		for i in self.list_sub:
			print i.lam1,i.lam2
		print '2.list_pi'
		print self.adj
		print self.flow

	def run(self):
		pass
		
if __name__ =='__main__':
	moead_ts = MOEAD_TS(200,'data/example_1.txt')
	moead_ts.init_reference_point()
	moead_ts.show()