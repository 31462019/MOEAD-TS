from sub_problem import SubProblem
class MOEAD_TS():

	def __init__(self):
		self.neighborhoodsize = 10
		self.subnum = 20
		self.list_sub=[]

	def init_weight_vector(self):
		for i in range(self.subnum):
			sub_problem = SubProblem()
			sub_problem.lam = float(i)/(self.subnum-1)
			self.list_sub.append(sub_problem)
		

	def init_population(self):
		pass

	def update_neighbor_solution(self):
		pass

	def update_reference_point(self):
		pass

	def init_neighborhood(self):
		pass

	def init_reference_point(self):
		pass
		
if __name__ =='__main__':
	moead_ts = MOEAD_TS()
	moead_ts.init_weight_vector()