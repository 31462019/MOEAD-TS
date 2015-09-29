#encoding=utf-8

#from individual import individual


class SubProblem():
	def __init__(self):
		self.lam = [0,0]
		self.individual = None
		self.list_neibor = []

	def randomize(self):
		pass

	def compute_fitness_value(self,reference):	#计算当前适应度函数值
		return self.individual.compute_fitness_value(self.lam,reference)