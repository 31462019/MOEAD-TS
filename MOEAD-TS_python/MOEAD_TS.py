
#encoding=utf-8
from sub_problem import SubProblem
from individual import individual
from random import randint
from copy import deepcopy

class MOEAD_TS():

	def __init__(self,fevals,file_name):
		self.MaxFunEvals = fevals
		#最大迭代次数
		self.neighborsize = 50
		#邻居个数，即T
		self.numF = 2
		#目标函数个数
		self.subnum = 200
		#即N，子问题个数
		self.dict_sub= {}
		#存储sub的list
		self.list_pi = [1.0]*self.subnum	
		#存储权益值
		self.reference = [float('inf'),float('inf')]	
		#存储参考点
		self.EP = []
		self.file_name = file_name

		self.FunEvals = 0
		self.read_data()
		#读取文件数据

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


	def init_weight_vector(self):
	#初始化每个子问题的权向量，并将子问题加至self的List表中
		for i in range(self.subnum):
			sub_problem = SubProblem()
			sub_problem.lam[0] = float(i)/(self.subnum - 1)
			sub_problem.lam[1] = 1.0 - sub_problem.lam[0]
			self.dict_sub[i] = sub_problem
		print "init_weight_vector done!"
		

	def init_reference_point(self):
		ind = individual(self.file_name)
		ind.randomize()
		ind.get_obj()
		self.update_reference_point(ind)
		print "init_reference_point done!"

	def init_neighborhood(self):						#是否需要将neibor函数中的值算出来。在随机化后立即产生？如果不用，在哪里计算F的值
		dis ={}
		self.neibor = {}
		for num in range(len(self.dict_sub)):
			dis[num] = [(pow(self.dict_sub[num].lam[0] - self.dict_sub[j].lam[0],2)+pow(self.dict_sub[num].lam[1]-self.dict_sub[j].lam[1],2),j) for j in range(len(self.dict_sub))]
	
			dis[num].sort(key = lambda x:x[0])	
			self.dict_sub[num].list_neibor = [dis[num][j][1] for j in range(self.subnum)][1:self.neighborsize+1]
			#print self.list_sub[num].list_neibor
			#self.neibor存储以序列为键的最近的T个邻居
		print "init_neighborhood done!"

	def init_population(self):
		
		for i in range(self.subnum):
			ind = individual(self.file_name)
			ind.randomize()
			ind.get_obj()
			self.update_reference_point(ind)
			self.dict_sub[i].individual = ind
			self.FunEvals += 1
		print "init_population done!"

	def update_neighbor_solution(self):					
		pass

	def update_reference_point(self,ind):					#此处求个体中的函数值，执行此步骤后才有函数值
		
		#print ind.func
		for i in range(self.numF):
			if ind.func[i] < self.reference[i]:
				self.reference[i] = ind.func[i]
		#print 'reference',self.reference
		

	def updateEP(self,ind):
		ind_c = deepcopy(ind)
		if not self.EP:
			
			self.EP.append(ind_c)
			print 'append'
			return True
		#num_1,num_2 = 0,0
		for i in self.EP:
			if (self.dominate(i.func,ind_c.func)):
				return False
		self.EP.append(ind_c)
		#print 'before',len(self.EP)
		self.EP = [i for i in self.EP if self.dominate(ind_c.func,i.func)==False]
		self.EP = list(set(self.EP))
		#print 'after',len(self.EP)
		
		#print 'append'
		return True

	def dominate(self,x,y):
		#判断x是否支配y
		if(x[0] <= y[0] and x[1] < y[1]):
			return True
		if(x[0] < y[0] and x[1] <= y[1]):
			return True
		return False



	
	def partially_matched_crossover(self,p1,p2):
		#随机选择交叉点

		k1,k2 = randint(0,self.room),randint(0,self.room)
		if(k1 == k2):
			k2 = (k2 + 1) % self.room
		if(k1 > k2):
			k1,k2 = k2,k1

		ind1,ind2 = deepcopy(p1),deepcopy(p2)
		ind1.array[k1:k2],ind2.array[k1:k2] = p2.array[k1:k2],p1.array[k1:k2]
		for i in range(self.room):
			if(i >= k1 and i < k2):continue
			num1,num2 = ind1.array[i],ind2.array[i]
			while(num2 in p1.array[k1:k2]):
				num2 = p2.array[k1:k2][p1.array[k1:k2].index(num2)]
			ind2.array[i] = num2

			while(num1 in p2.array[k1:k2]):
				num1 = p1.array[k1:k2][p2.array[k1:k2].index(num1)]
			ind1.array[i] = num1


		ind1.get_obj()
		ind2.get_obj()
		return ind1,ind2

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
		self.init_population()		#print self.list_sub[1].compute_fitness_value(self.reference)	返回目标子问题函数值

		while(self.FunEvals < self.MaxFunEvals):
			
			for i in self.dict_sub:
				id1,id2 = randint(0,self.neighborsize-1),randint(0,self.neighborsize-1)
				if (id1 == id2):
					id1 = (id1 + 1) % self.neighborsize
				p1,p2 = self.dict_sub[self.dict_sub[i].list_neibor[id1]].individual ,self.dict_sub[self.dict_sub[i].list_neibor[id2]].individual 			#产生两个父代
				
				
				chd1,chd2 = self.partially_matched_crossover(p1,p2)
				if(set(chd1.array)<8):
					print 'chd1 error'
				if(set(chd2.array)<8):
					print 'chd1 error'
				#	print chd1.array,chd2.array
				
				
				#更新邻居解
				for j in self.dict_sub[i].list_neibor:
					if chd1.compute_fitness_value(self.dict_sub[j].lam,self.reference) < self.dict_sub[j].individual.compute_fitness_value(self.dict_sub[j].lam,self.reference):
						self.dict_sub[j].individual = chd1
					if chd2.compute_fitness_value(self.dict_sub[j].lam,self.reference) < self.dict_sub[j].individual.compute_fitness_value(self.dict_sub[j].lam,self.reference):
						self.dict_sub[j].individual = chd2

				#更新参考点
				self.update_reference_point(chd1)
				self.update_reference_point(chd2)
				
				#更新归档集
				self.updateEP(chd1)
				self.updateEP(chd2)

				self.FunEvals += 1
				if(self.FunEvals % 100 == 0):
					print self.FunEvals
		print self.reference
		
		for i in self.EP:
			print i.func
			print i.array
		print len(self.EP)

		
if __name__ =='__main__':
	moead_ts = MOEAD_TS(210,'data/example_1.txt')
	moead_ts.run()
	