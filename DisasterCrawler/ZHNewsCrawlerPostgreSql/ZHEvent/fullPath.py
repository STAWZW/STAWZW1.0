import json

def traversingPath(sourceFather,sourceSun,nodeId,sourcelink,path):
    excessivePath = {}
    excessivePathSun = {}
    if sourceFather != sourceSun:
        excessivePath['name'] = sourceFather
        excessivePath['nodeId'] = ''
        excessivePath['children'] = []
        excessivePath['link'] = ''
        excessivePathSun['name'] = sourceSun
        excessivePathSun['nodeId'] = nodeId
        excessivePathSun['children'] = []
        excessivePathSun['link'] = sourcelink
        excessivePath['children'].append(excessivePathSun)
    else:
        excessivePath['name'] = sourceFather
        excessivePath['nodeId'] = nodeId
        excessivePath['children'] = []
        excessivePath['link'] = sourcelink
    if recursive(path,excessivePath)[1]:
        pass
    else:
        path['children'].append(excessivePath)
    return path

def recursive(path,excessivePath):
    suerSun = False
    suer = False
    if excessivePath['children'] != []:
        for item in path['children']:
            if item['name'] == excessivePath['name']:
                if select(item,excessivePath['children'][0]['name']):
                    item['children'].append(excessivePath['children'][0])
                suerSun = True
                break
        if suerSun:
            suer = True
        else:
            for item in path['children']:
                result = recursive(item,excessivePath)
                suer = result[1]
                if suer:
                    break
        if suer:
            pass
        else:
            for item in path['children']:
                if item['name'] == excessivePath['children'][0]['name']:
                    removeItem = item
                    suerSun = True
                    break
            if suerSun:
                excessivePathCopy = excessivePath
                path['children'].remove(removeItem)
                excessivePathCopy['children'] = []
                excessivePathCopy['children'].append(removeItem)
                path['children'].append(excessivePathCopy)
                suer = True
            else:
                for item in path['children']:
                    result = recursive(item,excessivePath)
                    suer = result[1]
                    if suer:
                        break
    else:
        if not select(path,excessivePath['name']):
            suer = True

    return path,suer

def select(path,name):
    suer = True
    for item in path['children']:
        if item['name'] == name:
            suer = False
            break
    if suer:
        for item in path['children']:
            suer = select(item,name)
            if not suer:
                break
    return suer

def getPath(header,sourceFather,sourceSun,nodeId,sourcelink):
    path = {}
    path['name'] = header
    path['nodeId'] = ''
    path['children'] = []
    path['link'] = ''
    for item in range(0,len(sourceSun)):
        traversingPath(sourceFather[item],sourceSun[item],nodeId[item],sourcelink[item],path)
    fullPath = (json.dumps(path, ensure_ascii=False)).replace('"',"''")
    return fullPath
#     return path

# sourceFather = ['中国网','中国经济网','新华网','人民网','北京日报','北京日报','北京日报','环球日报','央视网','台风网','地震台','央视网']
# sourceSun = ['央视网','中新网','百度新闻','人民网','新浪网','新浪网','新浪网','防灾网','天气网','台风网','央视网','海南日报']
# nodeId = ['1','2','3','4','5','6','7','8','9','10','11','12']
# sourcelink = ['','','','','','','','','','','','']
# header = '灾害发生地点'
# s = getPath(header,sourceFather,sourceSun,nodeId,sourcelink)
# print(s)