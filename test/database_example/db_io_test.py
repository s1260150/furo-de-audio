import psycopg2 as pg2
import pandas as pd
import csv

if __name__ == '__main__':
    # configuration of database
    conn = pg2.connect(
        user="postgres",
        password="post55005",
        host="localhost",
        port="5432",
        database="spotify"
    )
    cur = conn.cursor()

    with open('csv/db_io_test.csv', encoding="utf_8", newline='') as csvfile:
        read = csv.reader(csvfile)
        for row in read:
            print(row)
            sql = "INSERT INTO test_table VALUES({0},{1},'{2}') ON CONFLICT (id) DO UPDATE SET fnum = {1}, sentence = '{2}'"
            sql = sql.format(row[0],row[1],row[2]).encode('utf-8');
            #cur.execute(sql)
            # or
            cur.copy_expert("COPY test_table FROM STDIN (FORMAT CSV, ENCODING 'UTF8');", csvfile)
            #conn.commit()
            
    #csv_file = open('csv/db_io_test.csv', mode='r', encoding='utf-8')

    #cur.copy_expert("COPY {} FROM STDIN (FORMAT CSV, ENCODING 'UTF8');".format(), csv_file)
    
    #csv_file.close()

    #conn.commit()
    cur.close()
    conn.close()



    
    # 1.
    # CSVのセパレータを","から別のものに変更
    # expert と比べると手間が増える
    # with open('csv/db_io_test.csv', encoding="utf_8", newline='') as csvfile:
    #     read = csv.reader(csvfile)
    #     for row in read:
    #         print(row)
    #         sql = "INSERT INTO test_table VALUES({0},{1},'{2}') ON CONFLICT (id) DO UPDATE SET fnum = {1}, sentence = '{2}'"
    #         sql = sql.format(row[0],row[1],row[2]).encode('utf-8');

    
    # 2.
    # コンフリクトするとエラー落ちするから、先に表のデータを全部削除しなきゃならない
    # cur.copy_expert("COPY {} FROM STDIN (FORMAT CSV, ENCODING 'UTF8');".format(), csv_file)