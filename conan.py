import os, glob, shutil, sqlite3, datetime

def main():


    def conanize():
        print("""
            *****Welcome to Conan*****
            """)
        conan_on = 0
        while True:
            user_selection = input("Enable full Conan mode? ").lower()
            if user_selection in ['y','yes']:
                print("\nCrom accepts your offering.\n")
                conan_on = 1
                return(conan_on)
            elif user_selection in ['n','no']:
                return(conan_on)
            else:
                print("Please enter 'yes' or 'no' to proceed.\n")

    def menu():

        if conan_on:
            print("""
            What is best in life?

                ***
                To crush your auths
                See them captured before you
                And hear the lamentations of their tables
                ***
                """)

            main_menu = {'1. Prepare for battle':unpack,
                '2. Crush your auths':authcrusher,
                '3. Burn the fortress of your enemy':db_dump,
                '4. Ask Crom for guidance':help,
                '5. End your quest':quit}
            print("Welcome, warrior.")


        else:
            main_menu = {'1. Unpack':unpack,
                '2. Auth Timestamp Update':authcrusher,
                '3. Corrupted Database Fixer':db_dump,
                '4. Help':help,
                '5. Quit':quit}
            print("\nConan Main Menu\n")

        while True:
            for key in sorted(main_menu.keys()):
                print(key)
            menu_selection = input("\nSelect an option: ")
            if menu_selection in ['1','4']:
                for key in main_menu.keys():
                        if menu_selection in key:
                            main_menu[key]()
            elif menu_selection in ['2','3']:
                for key in main_menu.keys():
                    if menu_selection in key:
                        full_temple(main_menu[key])
            elif menu_selection == '5':
                os._exit(1)
                #This is a temporary (bad) workaround for a weird exit issue
            else:
                if conan_on:
                    print("\nCrom denies your request.\n")
                else:
                    print("\nThat is not a valid selection.\n")


    def full_temple(function_name):
        #check to see if temple_of_crom exists and if it has a db
        #if so, ask user if they want to use that db
        print("Checking for existing database.\n")
        while True:
            temple_file_path = os.path.expanduser('~/Desktop/temple_of_crom')
            if os.path.exists(temple_file_path):
                check_for_db = glob.glob('{}/*.adb1'.format(temple_file_path))
                if check_for_db:
                    for item in check_for_db:
                        full_db_path = os.path.expanduser(item)
                        ask_to_use = input("A database is available in the temple; would you like to use this file? ".format(item)).lower()
                        if ask_to_use in ['y','yes']:
                            function_name(full_db_path)
                        elif ask_to_use in ['n','no']:
                            print("""
                            Please run unpacking on your newly-downloaded database
                            or manually replace the database in temple_of_crom with another.
                                    """)
                            menu()
                        else:
                            print("Please enter 'yes' or 'no' to proceed.\n")
            else:
                print("No existing database found.\n")
                menu()



    def unpack():

        db_zip_path = max(glob.glob('Users/*/downloads/*.zip'), key=os.path.getctime)
        head, tail = os.path.split(db_zip_path)
        db_zip = tail
        temple_file_path = os.path.expanduser('~/Desktop/temple_of_crom')
        if os.path.exists(temple_file_path):
            shutil.rmtree(temple_file_path)
            os.mkdir(temple_file_path)
        else:
            os.mkdir(temple_file_path)

        os.rename(db_zip_path, '{}/{}'.format(temple_file_path, db_zip))
        new_db_path = os.path.expanduser('~/Desktop/temple_of_crom/{}'.format(db_zip))
        os.system('unzip -d ~/Desktop/temple_of_crom ~/Desktop/temple_of_crom/"{}"'.format(db_zip))
        if conan_on:
            print("\nCrom has revealed your database in the temple.\n")
        else:
            print("\nDatabase has been moved an unpacked.\n")

        menu()


    def authcrusher(database_path):

        def db_query(check_query, insert_query, conn_db, cursor_db):

                cursor_db.execute(check_query)
                len_hold = len(cursor_db.fetchall())
                if len_hold > 0:
                    timestamps = []
                    cursor_db.execute(check_query)
                    for row in cursor_db.fetchall():
                        for item in row:
                            timestamps.append(item)
                    for item in timestamps[-1:]:
                        last_timestamp = item

                    print("The last timestamp in this database is: "+
                        datetime.datetime.fromtimestamp(
                            float(last_timestamp)
                        ).strftime('%m-%d %H:%M:%S')
                    )

                    while True:
                        if conan_on:
                            proceed = input("Continue your quest? ").lower()
                        else:
                            proceed = input("Would you like to continue? ").lower()

                        if proceed in ['y','yes']:
                            print("\nCrushing auths.\n")

                            cursor_db.execute(insert_query, (last_timestamp,))
                            conn_db.commit()
                            print("\nAuths crushed.\n")
                            cursor_db.close()
                            conn_db.close()
                            menu()

                        elif proceed in ['n','no']:
                            if conan_on:
                                print("\nYour quest will continue with another database.\n")
                                cursor_db.close()
                                conn_db.close()
                                menu()
                            else:
                                print("\nReturning to menu.\n")
                                cursor_db.close()
                                conn_db.close()
                                menu()

                        else:
                            if conan_on:
                                print("\nCrom does not accept your answer.\n")
                            else:
                                print("\nThat is not valid input.\n")
                else:
                    if conan_on:
                        print("\nThere is nothing to crush.\nCrom has forsaken you.\n")
                        cursor_db.close()
                        conn_db.close()
                        menu()
                    else:
                        print("\nThere is nothing in this table.\n")
                        cursor_db.close()
                        conn_db.close()
                        menu()



        #Exit encapsulated function
        check_query_bridgepay = "SELECT ZP.ZDATECREATED FROM ZPAYMENT ZP WHERE ZBATCHSEQUENCENUMBER4 IS NOT NULL"
        check_query_mercury = "SELECT ZP.ZDATECREATED FROM ZPAYMENT ZP WHERE ZBATCHSEQUENCENUMBER2 IS NOT NULL"
        insert_query_bridgepay = "UPDATE ZPAYMENT SET ZDATEBATCHED4 = ? WHERE ZDATEBATCHED4 IS NULL AND ZBATCHSEQUENCENUMBER4 > 0"
        insert_query_mercury = "UPDATE ZPAYMENT SET ZDATEBATCHED2 = ? WHERE ZDATEBATCHED2 IS NULL AND ZBATCHSEQUENCENUMBER2 > 0"

        try:
            conn_db = sqlite3.connect(database_path, timeout=5000)
            cursor_db = conn_db.cursor()

        except:
            if conan_on:
                print("\nCrom has forsaken you.\n")
                menu()
            else:
                print("\nConnection to database failed.\n")
                menu()


        while True:

            proceed = user_proceed()

            if proceed in ['y','yes']:
                if conan_on:
                    ask_gateway = input("""
                Choose your foe:
                1. BridgePay
                2. Mercury
                Enter 1 or 2: """).lower()
                else:
                    ask_gateway = input("""
                Select a gateway:
                1. BridgePay
                2. Mercury
                Enter 1 or 2: """).lower()

                if ask_gateway == '1':
                    try:
                        db_query(check_query_bridgepay, insert_query_bridgepay, conn_db, cursor_db)
                    except:
                        print("\nSomething went wrong in the worst place.\nPlease notify Stache and save the database.\n")
                        menu()
                elif ask_gateway == '2':
                    try:
                        db_query(check_query_mercury, insert_query_mercury, conn_db, cursor_db)
                    except:
                        print("\nSomething went wrong in the worst place.\nPlease notify Stache and save the database.\n")
                        menu()
                else:
                    if conan_on:
                        print("\nCrom does not accept your answer.\n")
                    else:
                        print("\nThat is not valid input.\n")

            elif proceed in ['n','no']:
                if conan_on:
                    print("\nYour quest ends here, warrior.\n")
                    cursor_db.close()
                    conn_db.close()
                    menu()
                else:
                    print("\nReturning to menu.\n")
                    cursor_db.close()
                    conn_db.close()
                    menu()
            else:
                if conan_on:
                    print("\nCrom does not accept your answer.\n")
                else:
                    print("\nThat is not valid input.\n")



    def db_dump(database_path):

        try:
            conn_db = sqlite3.connect(database_path, timeout=5000)
            cursor_db = conn_db.cursor()
        except:
            if conan_on:
                print("\nCrom has forsaken you.\n")
                menu()
            else:
                print("\nConnection to database failed.\n")
                menu()

        while True:

            proceed = user_proceed()

            if proceed in ['y','yes']:
                if conan_on:
                    print("\nRazing the enemy's fortress.\n")
                else:
                    print("\nDumping corrupted database.\n")

                print("When this process is complete, you will be returned to the menu.")

                try: #this breaks on the rename; figure out what's wrong with this
                    os.rename(database_path, '~/Desktop/temple_of_crom/corruptdatabase.adb1')
                    os.system('sqlite3 ~/Desktop/temple_of_crom/corruptdatabase.adb1 ".dump" | sqlite3 uncorrupted.adb1')

                    menu()
                except:
                    print("\nSomething went wrong in the worst place.\nPlease notify Stache and save the database.\n")

            elif proceed in ['n','no']:
                if conan_on:
                    print("\nYour quest ends here, warrior.\n")
                    menu()
                else:
                    print("\nReturning to main menu.\n")
                    menu()
            else:
                print("\nThat is not valid input.\n")

    def help():
        if conan_on:

            print("""
        There are many answers to the Riddle of Steel:
            Prepare for battle
                Lo, warrior. To prepare for battle is to prepare for glory.
                Make your offerings to Crom and should he accept, you must
                drag your enemies from their homes and place them before Crom's
                judgment.

            Crush your auths
                You know what is best in life, warrior.  Go forth and crush your
                auths that you may see their captures driven before you.

            Burn the fortress of your enemy
                Warrior!  When your enemy has hidden himself in a corrupted fortress
                purify him in the fires of Crom.
            """)

        else:
            print("""
        The following functions are available:
            Unpack
                Creates a folder on the desktop called temple_of_crom and unpacks
                the most recent .zip file from downloads there. This will also delete
                an existing temple_of_crom folder and database if one exists already.

            Auth Timestamp Update
                Connects to a database in temple_of_crom, checks the most recent
                authorization timestamp and then inserts that timestamp where NULL
                entries exist.

            Corrupted Database Fixer
                Dumps the contents of a database in temple_of_crom into a sqlite text file
                and then uses the sqlite text file to rebuild a functional database. The new database
                will be saved as uncorrupted.adb1.
            """)



    def user_proceed():

        if conan_on:
            initial_prompt = input("Are you prepared for battle, warrior? ").lower()
        else:
            initial_prompt = input("Proceed with this function? ").lower()

        return(initial_prompt)


    conan_on = conanize()
    menu()

main()
