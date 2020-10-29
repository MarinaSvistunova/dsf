class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addReg(self, name, surename, email):
        try:
            self.__cur.execute("INSERT INTO registration VALUES(NULL, ?, ?, ?)", (name, surename, email))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Fall' + str(e))
            return False

        return True
