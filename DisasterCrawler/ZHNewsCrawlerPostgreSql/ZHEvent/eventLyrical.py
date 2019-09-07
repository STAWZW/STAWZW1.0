from postgresLyricalEvebt import PostgreCommand

def eventLyrical():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    postgreCommand.updataLyricalEvent()
    postgreCommand.closePostgre()
