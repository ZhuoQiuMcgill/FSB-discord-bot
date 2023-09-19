import sqlite3
import SQL_Statements
from os.path import exists
from Player  import Player
from Player  import Detail_info


class DB_Manager:
    def __init__(self, db_name: str):
        if not exists(db_name):
            raise NameError("Database file [" + db_name + "] not found.")
        self.conn = sqlite3.connect(db_name)
        self.conn.execute(SQL_Statements.PRAGMA_SETTING)
        if not self.check_connection(self.conn):
            raise NameError("Database doesn't work properly.")

    @staticmethod
    def check_connection(conn: sqlite3.Connection):
        try:
            conn.execute(SQL_Statements.GET_ALL_PLAYER)
            return True
        except sqlite3.OperationalError:
            return False

    def player_exists(self, GID: str) -> bool:
        cursor = self.conn.execute(SQL_Statements.GET_PLAYER_BY_GID, (GID,))
        row    = cursor.fetchone()
        return row is not None

    def user_exists(self, UID : str) -> bool:
        cursor = self.conn.execute(SQL_Statements.GET_USER_BY_UID, (UID,))
        row    = cursor.fetchone()
        return row is not None

    def get_player_by_GID(self, GID: str) -> Player:
        if not self.player_exists(GID):
            raise ValueError("No such player with GID = " + GID)
        try:
            cursor = self.conn.execute(SQL_Statements.GET_PLAYER_BY_GID, (GID,))
            row = cursor.fetchone()

            return Player(row[0], str(row[1]), str(row[2]), self.get_detail_info_by_GID(GID))
        except sqlite3.OperationalError:
            raise ValueError("No such player with GID = " + GID)

    def get_detail_info_by_GID(self, GID: str) -> list:
        try:
            cursor = self.conn.execute(SQL_Statements.GET_DETAIL_INFO_BY_GID, (GID,))
            results = []
            for row in cursor:
                detail_info = Detail_info(str(row[2]), str(row[1]), str(row[3]))
                results.append(detail_info)
            return results
        except sqlite3.OperationalError:
            raise ValueError("No such player with GID = [" + GID + "]")

    def register_player(self, GID: str, brief_info: str) -> None:
        if self.player_exists(GID):
            raise ValueError("Player with GID = [" + GID + "] already exists.")
        else:
            self.conn.execute(SQL_Statements.INSERT_PLAYER, (None, GID, brief_info))
            self.conn.commit()

    def update_player_binfo(self, GID : str, brief_info: str) -> None:
        if not self.player_exists(GID):
            raise ValueError("No such player with GID = [" + GID + "]")
        self.conn.execute(SQL_Statements.UPDATE_PLAYER_BINFO, (GID, brief_info))
        self.conn.commit()

    def delete_player_by_GID(self, GID : str) -> None:
        if not self.player_exists(GID):
            raise ValueError("No such player with GID = [" + GID + "]")
        self.conn.execute(SQL_Statements.DELETE_PLAYER_BY_GID, (GID,))
        self.conn.commit()

    def register_user(self, UID : str) -> None:
        if self.user_exists(UID):
            return
        self.conn.execute(SQL_Statements.INSERT_USER, (UID,))
        self.conn.commit()

    def rate_player(self, GID : str, UID : str, comment : str, time : str) -> None:
        if not self.user_exists(UID):
            self.register_user(UID)
        if not self.player_exists(GID):
            raise ValueError("No such player with GID = [" + GID + "]")
        self.conn.execute(SQL_Statements.RATE_PLAYER, (GID, UID, comment, time))
        self.conn.commit()

    def list_info(self) -> dict:
        results = {}
        cursor = self.conn.execute(SQL_Statements.LIST_RATING)
        for row in cursor:
            results[str(row[0])] = (str(row[1]), row[2], str(row[3]))
        return results
    
    def count_player(self) -> int:
        cursor = self.conn.execute(SQL_Statements.COUNT_PLAYER)
        return cursor.fetchone()[0]
