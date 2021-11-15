import sqlite3

class SQLighter:

    def __init__(self, database):

        #Подключаемся к БД
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    def api(self):
        with self.connection:
            return self.cursor.execute(f"select api from ac ").fetchone()

    def hash(self):
       with self.connection:
           return self.cursor.execute(f"select hash from ac ").fetchone()
    def id(self):
        with self.connection:
            return self.cursor.execute(f"select chat_id from ac ").fetchone()




    def text(self,text2):
        with self.connection:
            return self.cursor.execute("select text from post where text=?",(text2,)).fetchall()

    def add_text(self,text2):
      with self.connection:
        return self. cursor.execute("insert into post (text) values(?)", (text2,))

    def token(self):
        with self.connection:
            return self.cursor.execute(f"select token from ac").fetchone()

    def vers(self):
        with self.connection:
            return self.cursor.execute(f"select ver from ac").fetchone()

    def group(self,group):
        with self.connection:
            return self.cursor.execute(f"select grup from grupp where grup=? ",(group,)).fetchone()

    def token_bot(self):
        with self.connection:
            return self.cursor.execute(f"select token_bot from ac ").fetchone()

    def chat_id(self):
        with self.connection:
            return self.cursor.execute(f"select chatid from ac").fetchone()

    def login(self):
            with self.connection:
                return self.cursor.execute(f"select login from admitad").fetchone()
    def password(self):
            with self.connection:
                return self.cursor.execute(f"select password from admitad").fetchone()


    def add_av(self,login,password):
        with self.connection:
            return self.cursor.execute("insert into admitad (login,password) values(?,?)", (login,password,))

    def add_ac(self,token,vers,group,token_bot,chatid):
        with self.connection:
            return self.cursor.execute("insert into ac (token,ver,g,token_bot,chatid) values(?,?,?,?,?)", (token,vers,group,token_bot,chatid,))

    def add_group(self, group):
            with self.connection:
                return self.cursor.execute("insert into grupp (grup) values(?)",(group,))


    def chat_notg(self):
        with self.connection:
            return self.cursor.execute(f"select username from chat ").fetchall()
#Чаты с тегами
    def chat_tg_add(self, username):
        with self.connection:
            return self.cursor.execute(f"select username from chat_tags where username=?", (username,)).fetchall()

    def add_chennal_tg(self,chennal):
        with self.connection:
            return self.cursor.execute("insert into chat_tags (username) values(?)", (chennal,))

    def chat_tg(self):
        with self.connection:
            return self.cursor.execute(f"select username from chat_tags ").fetchall()

    def chat_remove_tg(self,chennal):
        with self.connection:
            return self.cursor.execute("delete from chat_tags where username=?",(chennal,))

    def chat_remove_ntg(self, chennal):
        with self.connection:
            return self.cursor.execute("delete from chat where username=?", (chennal,))



    def close(self):
       #Закрываем соединение с базой данных
        self.connection.close()