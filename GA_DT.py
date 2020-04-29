import random
import csv

def rule():
	rule = []
	rule.append(random.randint(0,3))  #suhu
	rule.append(random.randint(0,4))  #waktu
	rule.append(random.randint(0,4))  #kondisi langit
	rule.append(random.randint(0,3))  #kelembapan
	rule.append(random.randint(0,1))  #terbang/tidak
	return rule

def chromosome():  #bikin chromosome dari rule dengan jumlah rule random dari 2 sampai 3
	chr = []
	for i in range(random.randint(2,3)):
		chr.append(rule())
	return chr

def combinechromosome(chr):  #menggabungkan array
	combine = []
	for i in range(len(chr)):
		combine += chr[i]
	return combine

def splitchromosome(combinechr,n):	#memisahkan array setiap n
	for i in range(0,len(combinechr),n):
		yield combinechr[i:i + n]

def splitrule(rule):  #split rule biner
	new=[]
	new.append(rule[:3])
	new.append(rule[4:7])
	new.append(rule[8:11])
	new.append(rule[11:13])
	new.append(rule[14])
	return new

def deletechromosome(chr):  #menghapus array yang tidak kelipatan 5
	mod = len(chr) % 5
	if mod == 0:
		new = chr
	else:
		for i in range(mod):
			del chr[-1]
		new = chr
	return chr

def population():
	pop = []
	for i in range(random.randint(5,20)):
		pop.append(chromosome())
	return pop

def loadData(file):
	data = []
	with open(file) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count=0
		for row in csv_reader:
			data.append(row)
	return data

def compare(rule,data):  #membandingkan populasi dengan datatrain
	suhu, waktu, langit, lembab, terbang = False, False, False, False, False
	if (rule[0]==int(data[0]) or rule[0]==3):
		suhu = True
	if (rule[1]==int(data[1]) or rule[1]==4):
		waktu = True
	if (rule[2]==int(data[2]) or rule[2]==4):
		langit = True
	if (rule[3]==int(data[3]) or rule[3]==3):
		lembab = True
	if (rule[4]==int(data[4])):
		terbang = True
	if suhu and waktu and langit and lembab and terbang:
		com = True
	else:
		com = False
	return com

def fitness(chr):
	fit = 0
	for rule in chr:
		for data in loadData('data_latih_opsi_2.csv'):
			# print('rule',rule)
			# print('data',data)
			if compare(rule,data):
				fit += 1
	return fit/80
		
def RouletteWheelSelection(pop,fit,total):
	r = random.random()
	i = 0
	# print("random",r)   
	while (r>0):
		r -= fit[i]/total
		i += 1
		if (i == (len(pop)-1)): #berhentiin loop kalo udah sampe batas populasi
			break
	parent = pop[i]
	return parent

def crossoverBasic(parent1,parent2,point1,point2):
	cross=[]
	cross1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
	cross2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
	cross.append(cross1)
	cross.append(cross2)
	return cross

def crossoverIncrease(parent1,parent2,point1,point2,point3,point4):
	cross=[]
	prob = random.randint(0,2)
	print('increase',prob)
	if prob==0 or (point2==point3 and point1==point4):
		cross = crossoverBasic(parent1,parent2,point1,point2)
	elif prob==1 and point2!=point3:
		cross1 = parent1[:point1] + parent2[point1:point3] + parent1[point3:]
		cross2 = parent2[:point1] + parent1[point1:point2] + parent2[point1:]
		cross.append(cross1)
		cross.append(cross2)
	elif prob==2 and point1!=point4:
		cross1 = parent1[:point4] + parent2[point4:point2] + parent1[point2:]
		cross2 = parent2[:point4] + parent1[point1:point2] + parent2[point2:]
		cross.append(cross1)
		cross.append(cross2)
	else:
		cross.append(cross1)
		cross.append(cross2)
	return cross

def crossoverIncreaseDecrease(parent1,parent2,point1,point2,point3,point4):
	cross=[]
	prob = random.randint(0,2)
	print('increase-decrease',prob)
	if prob==0 or (point2==point3 and point1==point4):
		cross = crossoverBasic(parent1,parent2,point1,point2)
	elif (prob==1 and point2!=point3):
		cross1 = parent1[:point1] + parent2[point1:point3] + parent1[point2:]
		cross2 = parent2[:point1] + parent1[point1:point2] + parent2[point1:]
		cross.append(cross1)
		cross.append(cross2)
	elif prob==2 and point1!=point4:
		cross1 = parent1[:point4] + parent2[point4:point2] + parent1[point2:]
		cross2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
		cross.append(cross1)
		cross.append(cross2)
	else:
		cross.append(cross1)
		cross.append(cross2)
	return cross

def crossover(parent1,parent2):
	cross1, cross2 = [], []
	cross = []
	prob = random.random()
	print('prob',prob)
	if (prob < 0.9):
		if len(parent1) >= len(parent2):
			minim = len(parent2)
		else:
			minim = len(parent1)
		print('p1',len(parent1))
		print('p2',len(parent2))
		print('minim',minim)
		point1 = random.randint(0,minim//2)
		point2 = random.randint((minim//2)+1,minim)
		selisih = point2-point1
		mod = selisih % 5
		point3 = point1 + mod #untuk point kedua
		point4 = point2 - mod #untuk point pertama
		print('p1',point1,'p2',point2,'p3',point3,'p4',point4)
		prob1 = random.randint(0,1)
		if prob1==0:
			cross = crossoverIncrease(parent1,parent2,point1,point2,point3,point4)
			print('increase')
		elif prob1==1:
			cross = crossoverIncreaseDecrease(parent1,parent2,point1,point2,point3,point4)
			print('increase-decrease')
	else:
		cross.append(parent1)
		cross.append(parent2)
	return cross

def mutation(cross1,cross2):
	prob = random.random()
	if (prob < 0.9):
		for i in range (len(cross1)):
			p = random.random()
			if (p < 0.1):
				if (i % 5 == 0):
					cross1[i] = random.randint(0,3)
				elif (i % 5 == 1):
					cross1[i] = random.randint(0,4)
				elif (i % 5 == 2):
					cross1[i] = random.randint(0,4)
				elif (i % 5 == 3):
					cross1[i] = random.randint(0,3)
				elif (i % 5 == 4):
					cross1[i] = random.randint(0,1)
		for i in range (len(cross2)):
			p = random.random()
			if (p < 0.1):
				if (i % 5 == 0):
					cross2[i] = random.randint(0,3)
				elif (i % 5 == 1):
					cross2[i] = random.randint(0,4)
				elif (i % 5 == 2):
					cross2[i] = random.randint(0,4)
				elif (i % 5 == 3):
					cross2[i] = random.randint(0,3)
				elif (i % 5 == 4):
					cross2[i] = random.randint(0,1)
	cross = []
	cross.append(cross1)
	cross.append(cross2)
	return cross

def theBest(pop):
    maxFit = -9999
    id = []
    for i in range(len(pop)):
        id = pop[i]
        fit = fitness(id)
        if (fit>maxFit):
            maxFit = fit
            maxId = id
    return maxId

def saveData(target):
	with open('target_uji_opsi_2.csv', mode='w') as csv_file:
	    csv_writer = csv.writer(csv_file, delimiter=',')
	    csv_writer.writerow(target)
	return csv_writer

def getTerbang(rule,data):  #membandingkan populasi dengan datauji
	suhu, waktu, langit, lembab = False, False, False, False
	terbang = 0
	if (rule[0]==int(data[0]) or rule[0]==3):
		# print('rule0',rule[0])
		# print('data0',int(data[0]))
		suhu = True
	if (rule[1]==int(data[1]) or rule[1]==4):
		# print('rule1',rule[1])
		# print('data1',int(data[1]))
		waktu = True
	if (rule[2]==int(data[2]) or rule[2]==4):
		# print('rule2',rule[2])
		# print('data2',int(data[2]))
		langit = True
	if (rule[3]==int(data[3]) or rule[3]==3):
		# print('rule3',rule[3])
		# print('data3',int(data[3]))
		lembab = True
	if suhu and waktu and langit and lembab:
		terbang = str(rule[4])
	else:
		terbang = 'Unknown'
	return terbang

def validation(chr):
	fit = 0
	target=[]
	for rule in chr:
		for data in loadData('data_uji_opsi_2.csv'):
			# print('rule',rule)
			# print('data',data)
			terbang = getTerbang(rule,data)
			target.append(terbang)
	# print(rule)
	return target

# print(loadData('data_latih_opsi_2.csv'))
# print('==============================================')
# print(decode(loadData('data_latih_opsi_2.csv')))


#MAIN PROGRAM INTEGER

pop = population()
generation=1
while(generation<4):
	id = []
	fit = []
	list_fit = []
	newpop = []
	# child = []
	# crossover = []
	# p1, p2 = [], []
	minim, point1, point1 = 0, 0, 0
	best = theBest(pop)
	total = 0
	print("Population ",generation,"=")
	for chr in pop:
		print(chr)
	for i in range(len(pop)):
		id = pop[i]
		fit = fitness(id)
		list_fit.append(fitness(id)) #Tampung isi fitnes populasi di array
		total += fit
		print("Fitness",i,"=",fit) 
	print("Total Fitness = ",total)
	print("________________________________________________") 
	for j in range(len(pop)//2):
		parent1 = RouletteWheelSelection(pop,list_fit,total)
		parent2 = RouletteWheelSelection(pop,list_fit,total)
		print("Parent 1 =",parent1)
		print("Parent 2 =",parent2)
		p1 = combinechromosome(parent1)
		p2 = combinechromosome(parent2)
		print(p1,'-------',p2)
		child = crossover(p1,p2)
		print('crossover',child)
		child = mutation(child[0], child[1])
		print('mutasi',child)
		newchild0 = deletechromosome(child[0])
		newchild1 = deletechromosome(child[1])
		newpop.append(list(splitchromosome(newchild0,5)))
		newpop.append(list(splitchromosome(newchild1,5)))
		# newpop.append(child)
		print("-----------------------------------------------") 
	print("")
	print("New Population",generation,"=")
	for chr in newpop:
		print(chr)
	print("__________________________________________________________________________________________________________________________________________________________________")
	print("__________________________________________________________________________________________________________________________________________________________________")
	best = theBest(newpop)
	pop = newpop 
	generation+=1

print('=======================================================')
print('best chromosome',best)
print('fitness',fitness(best))
print('valid',validation(best))
saveData(validation(best))

