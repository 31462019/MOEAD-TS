#encoding=utf-8
#暂认为，每个个体即是一个解
from random import shuffle,randint,uniform
#from random import randint

import numpy as np


class individual():
	def __init__(self,file_name):
		self.read_data(file_name) 								
		
		self.num = self.room - self.a - self.b  		#除中心岛外的其他房间个数
		self.array =range(self.room)
		self.cut=[0,self.a,self.b,self.num]

		self.func = [0.0,0.0]


	def randomize(self):
		#产生随机解
		shuffle(self.array)				#将顺序打乱，即随机产生初始解
		cut = randint(1,self.num-1)
		#self.cut = [cut,self.a,self.b,self.num-cut]
		self.cut = [3,2,2,3]
		#self.gap = self.limit_wid	#初始化时将其设置为最小值
		self.gap = [2.15,2,2]
		'''
		self.wid = [0]*3				#计算三行的宽度
		for i in range(self.cut[0]):
			self.wid[0] += self.width[self.array[i]]
		for i in range(self.cut[1]+self.cut[2]):
			self.wid[1] += self.width[self.array[i+cut]]
		self.wid[1] += self.gap[0] + self.gap[1] + self.gap[2]
		for i in range(self.cut[3]):
			self.wid[2] += self.width[self.array[i+cut+self.a+self.b]]
		'''
		'''
		#随机生成间隙
		gap_add = []
		gap_add.append(uniform(0,self.limit_row[1] - self.wid[1]))
		gap_add.append(uniform(0,self.limit_row[1] - self.wid[1] - gap_add[-1]))
		gap_add.append(uniform(0,self.limit_row[1] - self.wid[1] - gap_add[-1] - gap_add[-2]))
		for i in range(3):
			self.gap[i] += gap_add[i]
			self.wid[1] += gap_add[i] 		
		'''
		#print self.wid
		#print self.limit_row

	def isFeasible(self):				#判断解是否满足条件
		for i in self.wid:
			if(i > self.obj.limit_row):
				return False
		return True

	def get_obj(self):
		
		self.get_dis()		#获取房间之间的距离，存入self.list_dis中

		#获取目标函数值
		self.func = [0.0,0.0]
		#print self.list_dis
		for i in range(self.room-1):
			for j in range(i+1,self.room):
				self.func[0] += self.list_dis[i][j]*self.flow[i][j]
				self.func[1] += self.list_dis[i][j]*self.adj[i][j]
		#print self.func

	def get_dis(self):
	#获取相互之间的距离
		try:
			self.cutsum = [sum(self.cut[0:x+1]) for x in range(len(self.cut))]
			locate = []
			self.dict_locate = {}

			#第一行
			ans = self.width[self.array[0]]/2
			locate.append([ans])
			self.dict_locate[self.array[0]] = (ans,0)

			for i in range(self.cut[0]):
				if(i == 0):
					continue
				ans = locate[0][-1] + (self.width[self.array[i-1]]+self.width[self.array[i]])/2
				locate[0].append(ans)
				self.dict_locate[self.array[i]] = (ans,0)

			#第二行
			ans = self.width[self.array[self.cutsum[0]]]/2 + self.gap[0]
			locate.append([ans])
			self.dict_locate[self.array[self.cutsum[0]]] = (ans,1)

			for i in range(self.cutsum[0] + 1,self.cutsum[2]):
				ans = locate[1][-1] + (self.width[self.array[i-1]] + self.width[self.array[i]])/2
				locate[1].append(ans)
				if(i < self.cutsum[1]):
					self.dict_locate[self.array[i]] = (ans,1)
				else:
					self.dict_locate[self.array[i]] = (ans+self.gap[1],1)

			#第三行
			ans = self.width[self.array[self.cutsum[2]]]/2
			locate.append([ans])
			self.dict_locate[self.array[self.cutsum[2]]] = (ans,2)

			for i in range(self.cutsum[2]+1,self.cutsum[3]):
				ans = locate[2][-1] + (self.width[self.array[i-1]]+self.width[self.array[i]])/2
				locate[2].append(ans)
				self.dict_locate[self.array[i]] = (ans,2)

			#print self.dict_locate
			self.list_dis = []
			for i in range(self.room):
				self.list_dis.append([abs(self.dict_locate[i][0] - self.dict_locate[j][0]) +abs(self.dict_locate[i][1] - self.dict_locate[j][1])*self.corridor for j in range(self.room)])
			#print self.list_dis
		except Exception,e:
			print e
			print self.dict_locate
			print self.list_dis
			print self.cut
			print self.array
			

	def compute_fitness_value(self,lam,reference):								#计算适应度函数，切比雪夫方法
		
		a = [lam[j]*abs(self.func[j] - reference[j]) for j in range(len(lam))]
		#a[1] = a[1]*500
		#print self.func
		return max(a) 



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
		if line.strip() == 'adj':
			self.adj = []												#紧密度
			for i in range(self.room):
				line = f.readline()
				self.adj.append(map(int,line.strip().split(',')))
			line = f.readline()
		f.close()
	
	def show(self):
		print 'self.array',self.array
		print 'self.cut',self.cut
		print 'self.cutsum',self.cutsum
		print 'self.locate',self.dict_locate

        

if __name__ == '__main__':
	ind = individual('data/example_1_8.txt')
	ind.randomize()
	ind.array = [6,5,3,1,2,0,4,7]
	ind.cut = [2,2,2,2]
	ind.get_obj()
	print ind.func
