as = [{'kws': [], 'id'}, {'kws': [], 'id'}]

kws = {}


for a in as:
	for kw in a['kws']:
		if kw not in kws:
			kws[kw] = set([])
		kws[kw].add(a['id'])

m = len(as)
edges = []
for i in range(0,m):
	neighbors = {}
	for j in range(0, len(a[i]['kws'])):
		for k in range(j+1, len(a[i]['kws'])):
			kw = a[i]['kws'][j]; kw2 = a[i]['kws'][k]; 
			intersect = (kws[kw] & kws[kw2]) - a[i]['id']
			for friend in intersect:
				neighbors[friend] = neighbors.get(friend,1) + 1
	for nei in neighbors:
		edges.append({'source': a[i]['id'], 'target': nei, 'value': neighbors[nei]})