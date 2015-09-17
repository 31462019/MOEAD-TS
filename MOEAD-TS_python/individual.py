#encoding=utf-8
#暂认为，每个个体即是一个解
from random import shuffle
from random import randint


class individual():
	def __init__(self,obj):
		self.a,self.b = obj.cent_a,obj.cent_b
		room =obj.room
		self.num = room-self.a-self.b
		self.obj = obj
		self.array =range(room)
		self.cut=[0,self.a,self.b,self.num]

	def randomize(self):
		shuffle(self.array)				#将顺序打乱，即随机产生初始解
		cut = randint(1,self.num-1)
		self.cut = [cut,self.a,self.b,self.num-cut]
		self.gap = self.obj.limit_wid	#初始化时将其设置为最小值
		self.wid = [0]*3
		for i in range(self.cut[0]):
			self.wid[0] += self.obj.width[self.array[i]]
		for i in range(self.cut[1]+self.cut[2]):
			self.wid[1] += self.obj.width[self.array[i+cut]]
		for i in range(self.cut[3]):
			self.wid[2] += self.obj.width[self.array[i+cut+self.a+self.b]]
		print self.wid

	#随机初始化
	def GreedyRepairHeuristic(self):
		pass

if __name__ == '__main__':
	ind = individual(15)
	ind.randomize()

