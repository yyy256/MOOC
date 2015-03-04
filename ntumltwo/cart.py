def uniquecounts(rows):
	results = {}
	for row in rows:
		r = row[-1]
		if r not in results: results[r] = 0
		results[r] += 1
	return results

def giniimpurity(rows):
	total = len(rows)
	if total == 0:
		p1= 0
	else:
		counts=uniquecounts(rows)
		for k1 in counts:
			p1 = float(counts[k1]) / total

	return (1 - p1*p1 - (1-p1)*(1-p1))

train = [line.strip().split(' ') for line in file('/home/yaoyu/downloads/hw3_train.dat')]

def splitdata(rows, index, theta):
	retrows1 = []
	retrows2 = []
	for row in rows:
		if float(row[index]) > float(theta):
			retrows1.append(row)
		else:
			retrows2.append(row)
	return retrows1, retrows2
    
def choosebestfeature(rows):
	numfeature = len(rows[0]) - 1
	best_gini = 1
	best_feature = -1
	for index in range(numfeature):
		X = []
		for row in rows:
			X.append(float(row[index]))
		X.insert(1, float('-inf'))
		X.insert(1, float('inf'))
		X = sorted(X)
		thetas = []
		for i in range(len(X) - 1):
			thetas.append((X[i]+X[i+1])/2)
		for theta in thetas:
			retrows1, retrows2 = splitdata(rows, index, theta)
			gini1 = giniimpurity(retrows1)
			gini2 = giniimpurity(retrows2)
			gini = float(len(retrows1))/len(rows)*gini1 + float(len(retrows2))/len(rows)*gini2
			if gini < best_gini:
				best_gini = gini
				best_feature = index
				best_theta = theta
	return best_feature, best_theta, best_gini
# when stop
# return what
# {'0':{'>theta':'-1','<=theta':{}}}
def buildtree(rows):
	labels = [row[-1] for row in rows]
	if labels.count(labels[0]) == len(labels): 
		return labels[0]
	else:
		best_feature, best_theta, best_gini = choosebestfeature(rows)
		#if best_gini == 0:
			#return labels[0]
		
		myTree = {best_feature:{}}
		#del
		retrows1, retrows2 = splitdata(rows, best_feature, best_theta)
		myTree[best_feature]['>' + str(best_theta)] = buildtree(retrows1)
		myTree[best_feature]['<=' + str(best_theta)] = buildtree(retrows2)
	return myTree

# for i in range(len(secondDict.keys())):
#     if eval(str(key)+secondDict.keys()[i]):
#         k = i
        
        

# valueOfFeat = secondDict[secondDict.keys()[k]]

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    number = testVec[featIndex]
    keys = secondDict.keys()
    for i in range(len(keys)):
        if eval(str(number)+keys[i]):
            k = i
    valueOfFeat = secondDict[keys[k]]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel

# mytree = {1: {'<=0.626233': {0: {'<=0.2244395': {1: {'<=0.11515275': '1',
#       '>0.11515275': '-1'}},
#     '>0.2244395': {0: {'<=0.541508': {1: {'<=0.3586205': {0: {'<=0.501625': '1',
#           '>0.501625': '-1'}},
#         '>0.3586205': {0: {'<=0.2607515': '+1', '>0.2607515': '-1'}}}},
#       '>0.541508': {1: {'<=0.285925': {1: {'<=0.2660385': '1',
#           '>0.2660385': '-1'}},
#         '>0.285925': '1'}}}}}},
#   '>0.626233': {0: {'<=0.8781715': '-1', '>0.8781715': '1'}}}}



res = []
for row in test:
    r = classify(mytree, [0,1], row)
    res.append(r == row[-1])

res.count(False)

# q16
from random import choice

j = 0
falses = []
while j < 30000:
	i = 0
	t = []
	while(i < 100):
		t.append(choice(train))
		i += 1
	mytree = buildtree(t)
	res = []
	for row in train:
	    r = classify(mytree, [0,1], row)
	    res.append(r == row[-1])
	false = float(res.count(False))/100
	falses.append(false)
	j += 1

# q17
def bagging(data):
	i = 0
	t = []
	while(i < 100):
		t.append(choice(train))
		i += 1
	return t


jj = 0
falses = []
while jj < 100:
	ress = []
	j = 0
	while j < 300:
		t = bagging(train)
		mytree = buildtree_prune(t, train)
		res = []
		for row in train:
			r = classify(mytree, [0,1], row)
			res.append(r)
		j += 1
		ress.append(res)
	for num in range(100):
		nums = [line[num] for line in ress]
		if nums.count('-1') > 150:
			pre = '-1'
		else:
			pre = '1'
		falses.append(train[num][-1] == pre)

	jj += 1

def countt(data):
	a1 = [line[-1] for line in data]
	if a1.count('-1') > 50:
		return '-1'
	else:
		return '1'

def decision_stump(train, data):
  best_feature, best_theta, best_gini = choosebestfeature(train)
  pre1 = [numpy.sign(float(line[best_feature]) - best_theta) for line in data]
  pre2 = [-numpy.sign(float(line[best_feature]) - best_theta) for line in data]
  res1 = []
  res2 = []
  for i in range(len(data)):
    res1.append(pre1[i] == float(data[i][-1]))
    res2.append(pre2[i] == float(data[i][-1]))
  if res1.count(False) > res2.count(False):
    return '-1'
  else:
    return '1'

def buildtree_prune(train, data):
	best_feature, best_theta, best_gini = choosebestfeature(train)
	#retrows1, retrows2 = splitdata(rows, best_feature, best_theta)
	myTree = {best_feature:{}}
	leaf1 = decision_stump(train, data)
	leaf2 = [a for a in ['-1','1'] if a != leaf1][0]
	myTree[best_feature]['>' + str(best_theta)] = leaf1
	myTree[best_feature]['<=' + str(best_theta)] = leaf2
	return myTree

jj = 0
falses = []
while jj < 100:
	ress = []
	j = 0
	while j < 300:
		t = bagging(train)
		mytree = buildtree(t)
		res = []
		for row in train:
			r = classify(mytree, [0,1], row)
			res.append(r)
		j += 1
		ress.append(res)
	for num in range(100):
		nums = [line[num] for line in ress]
		if nums.count('-1') > 150:
			pre = '-1'
		else:
			pre = '1'
		falses.append(train[num][-1] == pre)

	jj += 1