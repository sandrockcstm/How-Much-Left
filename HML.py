import argparse
import sqlite3
from progress.bar import FillingSquaresBar
from time import sleep


class QuotaBar(FillingSquaresBar):
    suffix = '%(index)d/%(max)d'

# Main block.
def main():
    # Peforms a check to see if quota_table exists.
    if table_check():
        # Argparse setup.
        parser = argparse.ArgumentParser(description='Create and track quotas and your progress towards meeting them.')
        # parser.add_argument("--list", "-l", help="Show all quotas before taking an action")
        parser.add_argument("action", help="[add/sub/set/new/del/show/show_all].  "
                                           "'add' = Increase quota count."
                                           "'sub' = Decrease quota count. "
                                           "'set' = Set current count and quota count directly."
                                           "'new' = New quota."
                                           "'del' = Delete quota."
                                           "'show' = Show a specific quota."
                                           "'show_all' = Show all quotas.",
                            type=str)
        args = parser.parse_args()
        # Pass the user's chosen action to quota_action()
        quota_action(args.action)
    else:
        # No table was found and user chose not to create one.  Exit the program.
        print("No table to work with.  Exiting.")


# Checks that the quota_table exists, and if not, creates it.  Returns True or False.
def table_check():
    # Connect to the db
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    # Check that quota_table exists.  Return 1 if it does, 0 if it doesn't.
    curs.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='quota_table'")
    result = curs.fetchone()
    try:
        # If quota_table doesn't exist, ask if user wants to create it.
        if result[0] == 0:
            query = input("Quota table not found.  This is required to use quota_cli.  Would you like to create one?\
             (y/n)")
            # If user says yes, create quota_table and return True
            if query == "y" or query == "Y":
                try:
                    curs.execute('CREATE TABLE quota_table ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,\
                     current INT NOT NULL DEFAULT 0 , quota INTEGER NOT NULL DEFAULT 1)')
                    conn.commit()
                    print("Quota table created.")
                    conn.close()
                    return True
                except Exception as e:
                    print("table_check level 2 error")
                    print(e)
                    conn.rollback()
                    conn.close()
                    return False
            # If user says no, undo all changes and return False.
            else:
                conn.rollback()
                conn.close()
                return False
        # If quota_table was found, return True.
        elif result[0] == 1:
            # print("Quota table found.")
            conn.close()
            return True
        # Something weird happened.
        else:
            print("Unexpected result returned.  " + result)
            conn.close()
            return False
    except Exception as e:
        print("table_check level 1 error")
        print(e)
        conn.close()


# Checks the current count against the quota.  If quota reached, asks if user wants to delete quota.
def quota_check(name):
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    tup = (name,)

    curs.execute('SELECT current FROM quota_table WHERE name=?', tup)
    current = curs.fetchone()
    current_bar = current[0]
    curs.execute('SELECT quota FROM quota_table WHERE name=?', tup)
    quota = curs.fetchone()
    quota_bar = quota[0]

    bar = QuotaBar('Current progress:', max=quota_bar)
    if current_bar == 0:
        bar.update()
        bar.finish()
    elif current_bar < 10:
        for i in range(current_bar):
            bar.next()
            sleep(0.75)
        bar.finish()
    elif current_bar < 25:
        for i in range(current_bar):
            bar.next()
            sleep(0.25)
        bar.finish()
    else:
        for i in range(current_bar):
            bar.next()
            sleep(0.03)
        bar.finish()
    if current >= quota:
        print("YOU'VE REACHED YOUR QUOTA!")
        answer = input("Would you like to delete this quota? (y/n)")
        if answer == "y" or answer == "Y":
            try:
                curs.execute('DELETE FROM quota_table WHERE name=?', tup)
                print("Quota deleted.")
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
        else:
            answer2 = input("Would you like to reset the count? (y/n)")
            if answer2 == "y" or answer2 == "Y":
                try:            
                    curs.execute('UPDATE quota_table SET current=0 WHERE name=?', tup)
                    conn.commit()
                    print("Current count reset to 0.")
                except Exception as e:
                    print(e)
                    conn.rollback()
    else:
        print("Quota not yet reached.")

    conn.close()


# Call appropriate function based on chosen user action.  Exit program if invalid action given.
def quota_action(action):
    if action == "add":
        quota_add()
    elif action == "sub":
        quota_sub()
    elif action == "set":
        quota_set()
    elif action == "new":
        quota_new()
    elif action == "del":
        quota_del()
    elif action == "show":
        quota_info()
    elif action == "show_all":
        quota_table()
    else:
        print(str(action) + " is not a valid selection.  Use -h flag for help.")


# Increment the current count of a quota.
def quota_add():
    name = input("What is the name of your quota? ")
    tup = (name,)
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()

    try:
        curs.execute('SELECT current FROM quota_table WHERE name=?', tup)
        old_num = curs.fetchone()
        current_num = 1 + int(old_num[0])
        param = (current_num, name)
        curs.execute('UPDATE quota_table SET current = ? WHERE name = ?', param)
        conn.commit()
        curs.execute('SELECT current FROM quota_table WHERE name=?', tup)
        new_num = curs.fetchone()
        print(name + " incremented, now " + str(new_num[0]))
        quota_check(name)
    except Exception as e:
        print(e)
        conn.rollback()

    conn.close()


# Decrement the current count of a quota.
def quota_sub():
    name = input("What is the name of your quota? ")
    tup = (name,)
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    try:
        curs.execute('SELECT current FROM quota_table WHERE name=?', tup)
        old_num = curs.fetchone()
        if old_num[0] > 0:
            current_num = int(old_num[0]) - 1
            param = (current_num, name)
            curs.execute('UPDATE quota_table SET current = ? WHERE name = ?', param)
            conn.commit()
            curs.execute('SELECT current FROM quota_table WHERE name=?', tup)
            new_num = curs.fetchone()
            print(name + " decreased, now " + str(new_num[0]))
            quota_check(name)
        else:
            print("Current count may not be less than 0.")
    except TypeError:
        print("Quota with that name not found.")
    except Exception as e:
        print(e)
        conn.rollback()

    conn.close()


def quota_set():
    name = input("What is the name of the quota you would like to set? ")
    current = input("What is the current count? ")
    quota = input("How many times does it need to be done? ")
    tup = (current, quota, name)
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    try:
        curs.execute('UPDATE quota_table SET current=?, quota=? WHERE name=?', tup)
        conn.commit()
        quota_check(name)
    except Exception as e:
        print(e)

    conn.close()


# Create a new quota.
def quota_new():
    name = input("What is the name of your quota? ")
    current = input("How many times have you done it? ")
    quota = input("How man times does it need to be done? ")
    tup = (name, current, quota)
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    try:
        curs.execute('INSERT INTO quota_table (name, current, quota) VALUES (?, ?, ?)', tup)
        conn.commit()
        print("Added " + name + " with a current count of " + current + " which needs to be done " + quota + " times.")
    except Exception as e:
        print(e)
        conn.rollback()
    curs.execute('SELECT * FROM quota_table WHERE name=? AND current=? AND quota=?', tup)

    conn.close()


# Delete a quota.
def quota_del():
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    id_num = input("What is the id of the quota you want to delete? (WARNING: THIS CANNOT BE UNDONE, ENTER Q TO STOP) ")
    tup = (id_num,)
    if id_num != "q" and id_num != "Q":
        try:
            curs.execute('DELETE FROM quota_table WHERE id=?', tup)
            conn.commit()
            print("Quota deleted.")
        except Exception as e:
            print(e)
            conn.rollback()
    else:
        print("Cancelling delete.")
        conn.rollback()

    conn.close()


# Return information on a single quota.
def quota_info():
    name = input("What is the name of your quota? ")
    tup = (name,)
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    try:
        curs.execute('SELECT id FROM quota_table WHERE name=?', tup)
        quota_id = curs.fetchone()
        curs.execute('SELECT current FROM quota_table WHERE name=?', tup)
        current = curs.fetchone()
        curs.execute('SELECT quota FROM quota_table WHERE name=?', tup)
        quota = curs.fetchone()
        print("id: " + str(quota_id[0]) + ", name: " + str(name) + ", current count: " + str(current[0]) + ", quota: " +
              str(quota[0]))
    except Exception as e:
        print(e)
        conn.rollback()

    conn.close()


# Return information on all quotas in quota_table.
def quota_table():
    conn = sqlite3.connect('quota.db')
    curs = conn.cursor()
    try:
        curs.execute('SELECT * FROM quota_table')
        result = curs.fetchall()
        for row in result:
            print("id: " + str(row[0]) + ", name: " + str(row[1]) + ", current count: " + str(row[2]) + ", quota: " +
                str(row[3]))
    except Exception as e:
        print(e)
        conn.rollback()

    conn.close()


if __name__ == "__main__":
    main()
