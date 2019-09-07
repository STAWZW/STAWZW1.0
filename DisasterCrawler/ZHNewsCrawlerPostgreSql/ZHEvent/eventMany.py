
from postgresManyAddress import PostgreCommand

def eventMany():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    postgreCommand.manyAddressEvent('10112','gh',30)		#干旱
    postgreCommand.manyAddressEvent('10107','by',30)		#暴雨
    postgreCommand.manyAddressEvent('10107','fbc',30)		#风暴潮
    postgreCommand.manyAddressEvent('10110','sd',30)		#霜冻
    postgreCommand.manyAddressEvent('10111','hc',30)		#寒潮
    postgreCommand.manyAddressEvent('10105','lbdf',30)		#雷暴大风
    postgreCommand.manyAddressEvent('10101','rdqx',30)		#热带气旋
    postgreCommand.closePostgre()
