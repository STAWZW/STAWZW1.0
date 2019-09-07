import json

def traversingPath(sourceFather,sourceSun,nodeId,sourcelink,path):
    excessivePath = {}
    suer = False
    suerSun = False
    if sourceFather != sourceSun:                                                               #判断父节点与子节点名称是否相同
        if path['name'] == '':                                                                  #如果初始path为空则加上父节点名称
            path['name'] = sourceFather
            path['nodeId'] = nodeId
            path['children'] = []
            path['link'] = sourcelink
        result = traversingPath(sourceSun,sourceSun,nodeId,sourcelink,path)
        suerSun = result[1]
        if suerSun:                                                                             #判断子节点是否在path中存在
            result = traversingPath(sourceFather,sourceFather,nodeId,sourcelink,path)
            suer = result[1]
        else:
            if path['name'] == '':                                                              #如果初始path为空则加上父节点名称
                path['name'] = sourceFather
                path['nodeId'] = nodeId
                path['children'] = []
                path['link'] = sourcelink
            if path['name'] == sourceFather:                                                    #如果父节点为path中的name
                childrensLen = len(path['children'])
                for item in range(0,childrensLen):                                              #判断子节点是否在path的name的子节点中存在
                    if path['children'][item]['name'] == sourceSun:
                        suerSun = True
                        break
                if suerSun:                                                                     #如果存在则不插入，结束
                    suer = True
                else:                                                                           
                    excessivePath['name'] = sourceSun
                    excessivePath['nodeId'] = nodeId
                    excessivePath['children'] = []
                    excessivePath['link'] = sourcelink
                    path['children'].append(excessivePath)
                    suer = True
            else:                                                                               #如果父节点不为path中的name，继续向下递归
                childrensLen = len(path['children'])
                for item in range(0,childrensLen):  
                    result = traversingPath(sourceFather,sourceSun,nodeId,sourcelink,path['children'][item])
                    suer = result[1]
                    if suer:
                        break
    elif sourceFather == sourceSun:                                                             #判断父节点与子节点名称是否相同
        if path['name'] == '':
            path['name'] = sourceFather
            path['nodeId'] = nodeId
            path['children'] = []
            path['link'] = sourcelink
        if path['name'] == sourceFather:
            suer = True
        else:
            childrensLen = len(path['children'])
            for item in range(0,childrensLen):
                result = traversingPath(sourceFather,sourceSun,nodeId,sourcelink,path['children'][item])
                suer = result[1]
                if suer:
                    break
    return path,suer

def getPath(sourceFather,sourceSun,nodeId,sourcelink):
    path = {}
    path['name'] = ''
    path['nodeId'] = ''
    path['children'] = []
    path['link'] = ''
    for item in range(0,len(sourceSun)):
        result = traversingPath(sourceFather[item],sourceSun[item],nodeId[item],sourcelink[item],path)
        suer = result[1]
        if suer:
            pass
        else:
            if sourceFather[item] == sourceSun[item]:
                traversingPath(sourceSun[item-1],sourceSun[item],nodeId[item],sourcelink[item],path)
            else:
                traversingPath(sourceFather[item-1],sourceFather[item],nodeId[item],sourcelink[item],path)
                traversingPath(sourceFather[item],sourceSun[item],nodeId[item],sourcelink[item],path)
    fullPath = (json.dumps(path, ensure_ascii=False)).replace('"',"''")
    return fullPath
