#encoding=utf-8
#暂认为，每个个体即是一个解
from random import shuffle
from random import randint

class individual():
	def __init__(self,room):
		self.a,self.b =2,3
		self.num = room-self.a-self.b
		self.array =range(room)
		self.cut=[0,self.a,self.b,self.num]
		self.gap = 
	def randomize(self):
		shuffle(self.array)#将顺序打乱，即随机产生初始解
		cut = randint(1,self.num-1)
		self.cut = [cut,self.a,self.b,self.num-cut]
		print self.cut

	#随机初始化
	def GreedyRepairHeuristic(self):
		pass
if __name__ == '__main__':
	ind = individual(15)
	ind.randomize()

