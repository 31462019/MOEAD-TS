#encoding=utf-8
#暂认为，每个个体即是一个解
from random import shuffle
from random import randint


class individual():
	def __init__(self,file_name):
		self.read_data(file_name) 								
		
		self.num = self.room - self.a - self.b  		#除中心岛外的其他房间个数
		self.array =range(self.room)
		self.cut=[0,self.a,self.b,self.num]
		self.obj = [0.0,0.0]

	def randomize(self):
		#产生随机解
		shuffle(self.array)				#将顺序打乱，即随机产生初始解
		cut = randint(1,self.num-1)
		self.cut = [cut,self.a,self.b,self.num-cut]
		self.gap = self.limit_wid	#初始化时将其设置为最小值
		self.wid = [0]*3				#计算三行的宽度
		for i in range(self.cut[0]):
			self.wid[0] += self.width[self.array[i]]
		for i in range(self.cut[1]+self.cut[2]):
			self.wid[1] += self.width[self.array[i+cut]]
		self.wid[1] += self.gap[0] + self.gap[1] + self.gap[2]
		for i in range(self.cut[3]):
			self.wid[2] += self.width[self.array[i+cut+self.a+self.b]]
		print self.wid
		print self.limit_row

	#随机初始化
	'''
	def GreedyRepairHeuristic(self):
		while(!self.IsFeasible()):
			CurrentValue = FitnessValue()
	'''
	def isFeasible(self):				#判断解是否满足条件
		for i in self.wid:
			if(i > self.obj.limit_row):
				return False
		return True

	def getObj(self):
		self.distance =[[],[],[],[],[],[],[],[]]
		for i in range(self.room):
			for j in range(self.room):
				if(i == j):
					

	def read_data(self,file_name):
		f = open(file_name,'r')
		line = f.readline()
		if line.strip() == 'Room':
			i = f.readline()
			self.room = int(i.strip())								#房间数：self.room
			line = f.readline()
		if line.strip() =='center_island':
			i = f.readline()
			self.a,self.b = map(int,i.strip().split(','))			#中心岛数：self.a,self.b
			line = f.readline()
		if line.strip() =='width':
			i = f.readline()
			self.width = map(float,i.strip().split(','))			#各个房间宽度	self.width
			line = f.readline()			
		if line.strip() =='flow':
			self.flow = []
			for i in range(self.room):
				line = f.readline()
				self.flow.append(map(float,line.strip().split(',')))	#房间间流量		self.flow
			line = f.readline()
		if line.strip() =='limit_row':
			i = f.readline()
			self.limit_row = map(float,i.strip().split(','))			#行宽限制 	self.limit_row
			line = f.readline()
		if line.strip() == 'limit_wid':
			i = f.readline()
			self.limit_wid = map(float,i.strip().split(','))			#中间行房间宽度限制
			line = f.readline()
		if line.strip() == 'corridor':
			i = f.readline()
			self.corridor = int(i.strip())								#走廊宽度
			line = f.readline()
		f.close()
	
        

if __name__ == '__main__':
	ind = individual(15)
	ind.randomize()

