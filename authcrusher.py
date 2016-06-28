import os, shutil, sqlite3, glob, datetime

    #tl;dr:
        #Crush your auths
        #See them captured before you
        #Hear the lamentations of their tables

def main():

    def conan():
        print("""
        What is best in life?
        ***
        To crush your auths
        See them captured before you
        And hear the lamentations of their tables
        ***
        """)

    def db_unpacker():

        try:
            ambur_db_zip_path = max(glob.glob('../downloads/*.zip'), key=os.path.getctime)
            head, tail = os.path.split(ambur_db_zip_path)
            ambur_db_zip = tail
        except ValueError:
            print("\nCrom can't crush what doesn't exist.\nMake sure you actually downloaded the file.")
            quit()
        if os.path.exists('../Desktop/temple_of_crom'):
            shutil.rmtree('../Desktop/temple_of_crom')
            os.mkdir('../Desktop/temple_of_crom')
        else:
            os.mkdir('../Desktop/temple_of_crom')

        os.rename(ambur_db_zip_path, '../Desktop/temple_of_crom/{}'.format(ambur_db_zip))
        new_ambur_path = os.path.expanduser('~/Desktop/temple_of_crom/{}'.format(ambur_db_zip))
        os.system('unzip -d ~/Desktop/temple_of_crom ~/Desktop/temple_of_crom/"{}"'.format(ambur_db_zip))
        #figure out how to handle parentheses when you don't know where they'll be
        print("Ambur db moved and unzipped.")

        ambur_db_path = glob.glob('../Desktop/temple_of_crom/*.adb1')
        for item in ambur_db_path:
            ambur_db = item
            head, tail = os.path.split(item)
        ambur_db = tail
        ambur_db_path = os.path.expanduser('~/Desktop/temple_of_crom/{}'.format(ambur_db))
        return ambur_db_path



    def db_query(sqlite_query1, sqlite_query2, cursor_ambur, conn_ambur):

        cursor_ambur.execute(sqlite_query1)
        len_hold = len(cursor_ambur.fetchall())
        if len_hold > 0:
            timestamps = []
            cursor_ambur.execute(sqlite_query1)
            for row in cursor_ambur.fetchall():
                for item in row:
                    timestamps.append(item)
            for item in timestamps[-1:]:
                last_timestamp = item

            print("The last timestamp in this database is: "+
                datetime.datetime.fromtimestamp(
                    float(last_timestamp)
                ).strftime('%m-%d %H:%M:%S')
            )

            check_proceed = 0
            while check_proceed == 0:
                proceed = input("Continue your quest? ")
                if proceed in ['y','yes']:
                    print("Crushing auths.")

                    cursor_ambur.execute(sqlite_query2,(last_timestamp,))
                    conn_ambur.commit()
                    print("Auths crushed.")
                    cursor_ambur.close()
                    conn_ambur.close()
                    quit()
                elif proceed in ['n','no']:
                    print("Your quest will continue with another database.")
                    cursor_ambur.close()
                    conn_ambur.close()
                    quit()
                else:
                    print("Crom only accepts 'yes', 'y' or 'n', 'no', warrior.")
                    continue
        else:
            print("There is nothing in this table.\nCrom has forsaken you.")
            cursor_ambur.close()
            conn_ambur.close()
            quit()



    def db_connection(local_db, gateway):

        try:
            conn_ambur = sqlite3.connect(local_db, timeout=5000)
            cursor_ambur = conn_ambur.cursor()
        except:
            print("Connection to database failed.\nCrom has forsaken you.")
            quit()

        sqlite_q1_bp = "SELECT ZP.ZDATECREATED FROM ZPAYMENT ZP WHERE ZBATCHSEQUENCENUMBER4 IS NOT NULL"
        sqlite_q1_m = "SELECT ZP.ZDATECREATED FROM ZPAYMENT ZP WHERE ZBATCHSEQUENCENUMBER2 IS NOT NULL"
        sqlite_q2_bp = "UPDATE ZPAYMENT SET ZDATEBATCHED4 = ? WHERE ZDATEBATCHED4 IS NULL AND ZBATCHSEQUENCENUMBER4 > 0"
        sqlite_q2_m = "UPDATE ZPAYMENT SET ZDATEBATCHED2 = ? WHERE ZDATEBATCHED2 IS NULL AND ZBATCHSEQUENCENUMBER2 > 0"

        if gateway == "bridgepay":
            db_query(sqlite_q1_bp, sqlite_q2_bp, cursor_ambur, conn_ambur)
        elif gateway == "mercury":
            db_query(sqlite_q1_m, sqlite_q2_m, cursor_ambur, conn_ambur)
        else:
            print("Something went wrong in the worst place.\nIt is not advised to use this database.\nPlease notify Stache.")


    conan()
    waiting = 0
    while waiting == 0:
        will_you_crush_them = input("Are you ready to crush some auths? ").lower()
        if will_you_crush_them in ['y','yes']:
            ask_gateway_check = 0
            while ask_gateway_check == 0:
                ask_gateway = input("""\nWhich great enemy do your auths serve?
                1. The lord of burning bridges
                2. The god of war
                Enter 1 or 2: """).lower()
                if ask_gateway == '1':
                    gateway = "bridgepay"
                    print("\nAsking Crom the Riddle of Timestamps.")
                    ambur_db_path = db_unpacker()
                    print(ambur_db_path)
                    db_connection(ambur_db_path, gateway)
                    break
                elif ask_gateway == '2':
                    gateway = "mercury"
                    print("\nAsking Crom the Riddle of Timestamps.")
                    ambur_db_path = db_unpacker()
                    print(ambur_db_path)
                    db_connection(ambur_db_path, gateway)
                    break
                else:
                    print("\nCrom does not accept your answer, warrior\n")
                    continue
        elif will_you_crush_them in ['n','no']:
            print("\nCrom has forsaken your auths.")
            quit()

        else:
            print("Crom only accepts 'yes', 'y' or 'n', 'no', warrior.")
            continue





main()
