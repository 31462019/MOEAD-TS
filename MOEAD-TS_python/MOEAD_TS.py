
#encoding=utf-8
from sub_problem import SubProblem
from individual import individual
import random

class MOEAD_TS():

	def __init__(self,fevals,file_name):
		self.MaxFunEvals = fevals
		#最大迭代次数
		self.neighborsize = 10
		#邻居个数，即T
		self.numF = 2
		#目标函数个数
		self.subnum = 20
		#即N，子问题个数
		self.list_sub= []
		#存储sub的list
		self.list_pi = [1.0]*self.subnum	
		#存储权益值
		self.reference = [float('inf'),float('inf')]	
		#存储参考点
		self.file_name = file_name

		self.FunEvals = 0
		self.read_data()
		#读取文件数据

	def init_weight_vector(self):
	#初始化每个子问题的权向量，并将子问题加至self的List表中
		for i in range(self.subnum):
			sub_problem = SubProblem()
			sub_problem.lam1 = float(i)/(self.subnum - 1)
			sub_problem.lam2 = 1.0 - sub_problem.lam1
			self.list_sub.append(sub_problem)
		

	def init_reference_point(self):
		ind = individual(self.file_name)
		ind.randomize()
		self.update_reference_point(ind)

	def init_neighborhood(self):
		dis ={}
		self.neibor = {}
		for num in range(len(self.list_sub)):
			dis[num] = [(pow(self.list_sub[num].lam1-self.list_sub[j].lam1,2)+pow(self.list_sub[num].lam2-self.list_sub[j].lam2,2),j) for j in range(len(self.list_sub))]
		for i in dis.keys():
			dis[i].sort(key = lambda x:x[0])	
			self.neibor[i] = [dis[i][j][1] for j in range(self.subnum)][1:self.neighborsize+1]
		#self.neibor存储以序列为键的最近的T个邻居


	def init_population(self):
		for i in range(self.subnum):
			ind = individual(self.file_name)
			ind.randomize()
			self.update_reference_point(ind)
			self.list_sub[i].list_ind.append(ind)
			self.FunEvals += 1
		

	def update_neighbor_solution(self):
		pass

	def update_reference_point(self,ind):									
		ind.get_obj()
		#print ind.func
		for i in range(self.numF):
			if ind.func[i] < self.reference[i]:
				self.reference[i] = ind.func[i]
		#print 'reference',self.reference
		
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
		self.init_weight_vector()
		self.init_neighborhood()
		self.init_reference_point()
		self.init_population()

		
if __name__ =='__main__':
	moead_ts = MOEAD_TS(200,'data/example_1.txt')
	moead_ts.run()
	