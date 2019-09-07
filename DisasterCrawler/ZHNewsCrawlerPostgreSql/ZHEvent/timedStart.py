
import eventMany
import eventSingle
import eventLyrical
from threading import Timer

def timedStart():
	eventSingle.eventSingle()
	eventMany.eventMany()
	eventLyrical.eventLyrical()
	print("检测完成！")
	# timrFor = Timer(3*60*60,timedStart)			#*秒爬取一次
	# timrFor.start()

timedStart()
