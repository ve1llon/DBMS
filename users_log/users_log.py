import csv
import sqlite3
import sys
from datetime import datetime


def main(log_fname, users_fname):
    log_data = []
    with open(log_fname, encoding='koi8_r') as fin:
        for row in csv.reader(fin):
            #декодировка
            cur_row = [i.encode('koi8_r').decode('utf-8') for i in row]
            #чистка
            if cur_row[0] != "#error":
                cur_row[0] = cur_row[0].split("_")[-1]
                cur_row[1] = cur_row[1][1:]
                if datetime.strptime(cur_row[1], '%Y-%m-%d %H:%M:%S'):
                    if cur_row[1][13] != ":":
                        cur_row[1] = cur_row[1][:11] + '0' + cur_row[1][11:]
                    log_data.append(cur_row)
    log_data.sort()
    
    users_data = []
    with open(users_fname, encoding='koi8_r') as fin:
        for row in csv.reader(fin):
            #разделение строки
            cur_row = row[0].split("\t")
            #чистка
            if (cur_row[0][:5] == "User_" and cur_row[0][5:].isdigit()):
                cur_row[0] = cur_row[0][5:]
                users_data.append(cur_row)
    users_data.sort()
    
    
    with sqlite3.connect('users_log.s3db') as conn:
        cur = conn.cursor()
        for user_id, time, bet, win in log_data:
        	cur.execute('INSERT INTO LOG (user_id, time, bet, win) VALUES (?, ?, ?, ?)',(user_id, time, bet, win))
        for user_id, email, geo in users_data:
        	cur.execute('INSERT INTO USERS (user_id, email, geo) VALUES ((SELECT user_id FROM LOG WHERE user_id = ?), ?, ?)',(user_id, email, geo))
        conn.commit()


if __name__ =='__main__':
	main(sys.argv[1], sys.argv[2])