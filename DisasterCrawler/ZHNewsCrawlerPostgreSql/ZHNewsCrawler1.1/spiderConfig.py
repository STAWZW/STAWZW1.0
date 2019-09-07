
def spiderConfig(crawlerName):
	from242pidPath = 'D:/GitRepository/STAWZW1.0/ZHNewsCrawlerPostgreSql/ZHNewsCrawler1.1/spiderConfig.txt'
	result = {}
	try:
		with open(from242pidPath,'r',encoding='UTF-8') as f:
		    for line in f.readlines():
		        lineList = line.strip().split(' ')
		        if lineList[1] == crawlerName:
		        	result['status'] = lineList[3]
		        	result['frequency'] = lineList[4]
		        	result['delay'] = lineList[5]
		        	break
		if result == {}:
			result['status'] = '1'
			result['frequency'] = '6'
		return result
	except:
		print('文档格式出现错误')
		result['status'] = '1'
		result['frequency'] = '6'
		result['delay'] = '5'
		return result

#print(spiderConfig('typhoon_ZH001111'))