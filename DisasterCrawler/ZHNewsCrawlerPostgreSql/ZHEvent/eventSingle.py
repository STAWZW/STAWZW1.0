
from postgresSingleAddress import PostgreCommand

def eventSingle():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    postgreCommand.singleAddressEvent('10010','dz',30)		#地震
    postgreCommand.singleAddressEvent('10502','slhz',30)	#森林火灾
    postgreCommand.singleAddressEvent('10002','hp',30)		#滑坡
    postgreCommand.singleAddressEvent('10001','bt',30)		#崩塌
    postgreCommand.singleAddressEvent('1000103','yb',30)    #岩塌
    postgreCommand.singleAddressEvent('1000104','stbt',30)  #山体崩塌
    postgreCommand.singleAddressEvent('10003','dznsl',30)	#泥石流
    postgreCommand.singleAddressEvent('10306','hsnsl',30)   #泥石流
    postgreCommand.singleAddressEvent('10205','hx',15)      #海啸
    postgreCommand.singleTpythoonEvent('10102','tf',30)     #台风
    postgreCommand.singleTpythoonEvent('1000101','xb',15)   #雪崩
    postgreCommand.singleTpythoonEvent('10108','hc',15)     #寒潮
    postgreCommand.singleTpythoonEvent('10115','nw',15)     #浓雾
    postgreCommand.singleTpythoonEvent('10302','sh',15)     #山洪
    postgreCommand.singleTpythoonEvent('10116','bfx',15)    #暴风雪
    postgreCommand.singleTpythoonEvent('10005','hs',15)     #火山
    postgreCommand.closePostgre()

