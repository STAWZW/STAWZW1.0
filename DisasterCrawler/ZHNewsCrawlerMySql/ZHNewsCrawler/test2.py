#import fool
#text = '云南墨江 玉磨铁路一施工驻地发生泥石流'
#test = '南京8月20日电 (记者 朱志庚)由于台风“温比亚”的施虐，8月17日8时至8月19日14时徐州市出现区域性强降雨、伴强雷电、短时强降水、雷雨大风等强对流天气。据徐州市政府有关部门发布消息称，此次降雨过程，全市平均降雨量132.2毫米，最大降雨点沛县栖山镇系徐州地区近百年一遇标准。19日，记者走进沛县栖山镇探访，多个村庄被大水浸泡成为泽国，有的村庄被大水环绕成为孤岛。据徐州市政府有关部门初步统计，截至8月19日14时，遇难7人，924494人受灾，农作物受灾面积1029235亩，受损房屋1824间。此次降雨过程，全市平均降雨量132.2毫米，最大降水点沛县栖山镇516毫米，最大阵风达30.5m/s(11级，丰县县城)。据水文监测，降水量超过250毫米的共22个站，均位于丰县、沛县境内，降雨量在100-250毫米的共22个站。本次降水灾害致使部分民房损坏倒塌、人员伤亡、公共设施受损、在田农作物受灾等灾害，部分河流因顶托、客水过境等因素超出警戒水位。灾情发生后，徐州市委、市政府高度重视，市委书记周铁根、市长庄兆林现场指挥，市领导带队分成三个组赶赴丰县、沛县、铜山区等地区现场指导救灾和灾后恢复工作，迅速启动应急预案，及时核实灾情，全力做好伤员救治，并妥善做好受灾群众转移和安置工作等等。19日，记者在沛县栖山镇看到，多条街道都灌满水，镇政府院内积水最高也达到50厘米以上。栖山镇卫生院内积水达到人的腰部，多个科室的电脑来不及搬出，被雨水浸泡。积水还导致停电，卫生院工作几乎停滞。该镇汽车站门由于修路，导致积水下路况不明。镇政府安排的几位身穿迷彩服工作人员站膝盖深的水中，指挥过往车辆行人通过危险处。栖西村司楼、刘庄等村庄内已经被水浸泡，村道积水最深处几乎达到胸部。司楼村西头几户人家周围完全成为了孤岛，每次出来都要几乎全身湿透。养鸡棚的主人运送饲料，只能把一块门板当做小船渡过去。还好，由于最近才换了一茬鸡苗，所以都在一米多高的架子上，没有泡在水中。养殖户就张玉军不这么幸运了，他家在村子西头接近3亩的饲养棚内养殖了200余头猪，其中有20头母猪。由于这几天的大雨，猪圈内严重积水。由于周围的积水已经成片，多次排水也已经起不到作用了。眼看着辛辛苦苦养大的猪仔泡在水里，张玉军难过地说，由于积水排不出去，目前只有眼睁睁地看着，现在已经有40头小猪溺亡。虽然他先前买了养殖方面的保险，但是目前还不知道能不能给他赔偿。60岁左右的霍磊一个人在村子西头两间老房独居，18日夜里下大雨的时候，眼看着雨水哗哗地流进房间，不到一小时的光景，房间内积水就快到1米深。没办法，为了防止倒塌，只好求助村庄里的邻居，涉水赶过去在人家楼上借住一晚。“没想到，今天白天还在下雨，看来有家也回不去了。”霍磊说，以后的日子看来要找政府救助了。'
#words, ners = fool.analysis(test)
#print(ners)
#for item in ners[0]:
#    if item[2] == 'time':
#        print(item[3])



#import datetime
#startTime = datetime.datetime.strptime('01-19', '%m-%d')
#print(startTime)




#location_str = ['渤海湾']
#import cpca
#df = cpca.transform(location_str)        #, cut=False, pos_sensitive=True)
#e = df.values
#print(e[0][0] + e[0][1] + e[0][2])




#import requests
#def geocode(address):
#    parameters = {'address': address, 'key': 'f6922b393df061ffff5b3c61529ce7d0'}
#    base = 'http://restapi.amap.com/v3/geocode/geo'
#    response = requests.get(base, parameters)
#    answer = response.json()
#    jwd = (answer['geocodes'][0]['location']).split(',')
#    return jwd
#if __name__=='__main__':
#
#    address = '广东省'
#    t = geocode(address)
#    print(t)





#str_i = "2008211"
#list_i = list(str_i)    # str -> list
#print(list_i)
#
#list_i.insert(4, '0')   # 注意不用重新赋值
#print(list_i)
#
#str_i = ''.join(list_i)    # list -> str
#print(str_i)



#import datetime 
##time_original = '22-MAY-2019 21:16:32'
##time_format = (datetime.datetime.strptime(time_original, '%d-%b-%Y %H:%M:%S')).strftime('%Y%m%d%H%M%S')
##print(time_format)
##
#time_original = '12 UTC 27 May 2019'
#time_format = (datetime.datetime.strptime(time_original, '%H UTC %d %b %Y')).strftime('%Y%m%d%H%M%S')
#print(time_format)
#
#
#ss = '43.53N 43.63E 425m'
#ss = ss.split()
#print(ss)
#print(ss[0][:-1])
#if ss[0][-1] == 'S':
#    lat = '-' + ss[0][:-1]
#else:
#    lat = ss[0][:-1]
#if ss[1][-1] == 'W':
#    lon = '-' + ss[1][:-1]
#else:
#    lon = ss[1][:-1]
#print(lon)


#import time
#import datetime
#import re
#timeStamp = 1558683174478/1000
#timePeriod = time.localtime(timeStamp)
#timeLocalStr = time.strftime('%Y%m%d%H%M%S', timePeriod)
#timeLocalDate = datetime.datetime.strptime(timeLocalStr,'%Y%m%d%H%M%S')
#timel = time.mktime(timeLocalDate.timetuple())
#t = datetime.datetime.utcfromtimestamp(timel)
#print(type(t))
#tt = re.sub("\D", "", str(t))
#print(type(tt))



#import re
#occurTimeStr = 'Thunderstormasat12UTC27May2019-'
#occurTime = re.findall(r"asat(.+?)-",occurTimeStr)
#print(occurTime)





#from datetime import datetime 
#time_str = '20190504164040'# 4:23:21'
#time = datetime.strptime(time_str, '%Y%m%d%H%M%S')# 根据字符串本身的格式进行转换
#print(time.strftime('%Y-%m-%d %H:%M:%S'))
#
#from dateutil import parser
#time_string = '20190425'
#datetime_struct = parser.parse(time_string)
#time_paid = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
#
#print(type(time_paid))
