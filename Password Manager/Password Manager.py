import mysql.connector
from prettytable import PrettyTable as pt, ALL
from os import system


def vault_pass_check(a):
    with open('C:\\Users\\Rudraksh\\GitHub\\Python_Files\\Password Manager\\password.txt',
              'r') as file:
        if a == str(file.read()):
            return True
        else:
            return False


def authentication():
    global passAttempt

    def pass_1st_attempt():
            global vaultPass, passAttempt
            system('cls')
            print('\n' + 30 * '-' + ' ENTER PASSWORD TO OPEN VAULT ' + 30 * '-' + '\n\n')
            vaultPass = str(input('\t\t\t\t\t'))
            passAttempt = 1
            go_home()

    def incorrect():
        global vaultPass, passAttempt
        system('cls')
        print('\n' + 35 * '-' + ' INCORRECT PASSWORD ' + 35 * '-' + '\n\n')
        vaultPass = str(input('\t\t\t\t\t'))
        passAttempt += 1
        go_home()

    def go_home():
        global vaultPass, passAttempt
        if vault_pass_check(vaultPass) is True and passAttempt <= 5:
            home()
        elif passAttempt > 5:
            system('cls')
            print('You have exceeded maximum number of password attempts\n')
            exit()
        else:
            incorrect()

    pass_1st_attempt()


def home():
    system('cls')
    print('\n\n' + '-' * 30 + " WELCOME TO PASSWORD MANAGER " + '-' * 30 +

          '''\n\n\n\tPress 1 to VIEW ALL passwords

        Press 2 to SEARCH password

        Press 3 to CHANGE a password

        Press 4 to ADD new password

        Press 5 to DELETE passwords

        Press 6 to CHANGE VAULT PASSWORD

        Hit Enter after pressing the desired key.''')

    home_action = str(input('\n\n\t'))

    if home_action == '1':
        view_all()
    elif home_action == '2':
        search_pass()
    elif home_action == '3':
        change_pass()
    elif home_action == '4':
        add_pass()
    elif home_action == '5':
        delete_pass()
    elif home_action == '6':
        change_vault_pass()
    else:
        system('cls')
        exit()

def run_query(x):

    connect = mysql.connector.connect(host='127.0.0.1', database='pass_schema',
                                      user='root', password='password')
    cursor = connect.cursor()
    cursor.execute(x)

    if 'SELECT' in x:
        return cursor.fetchall()
    else:
        connect.commit()

def view_all():
    system('cls')

    all_data = run_query("SELECT * FROM passwords")

    table = pt()
    table.field_names = ['NAME','ID','PASSWORD']
    table.add_rows(all_data)
    table.padding_width = 5
    table.hrules, table.vrules = ALL, ALL
    table.horizontal_char, table.vertical_char = '=','|'
    table.junction_char = '#'
    print(table)

    input('\n')
    home()


def search_pass():
    system('cls')
    web = str(input('\nWhich site password do you want?\n(Eg : Gmail/Yahoo/Outlook etc.)\n\n\t')).capitalize()
    result_tuple = run_query(f"SELECT * FROM passwords WHERE NAME='{web}'")

    table = pt()
    table.field_names = ['NAME','ID','PASSWORD']
    table.add_rows(result_tuple)
    table.padding_width = 5
    table.hrules, table.vrules = ALL, ALL
    table.horizontal_char, table.vertical_char = '=','|'
    table.junction_char = '#'
    print(table)

    input('\n')
    home()
    input('\n')
    home()


def change_pass():
    system('cls')
    site = str(input('\n\n ' + 29 * '-' + ' ENTER NAME ' + 29 * '-' + '\n\n' + '\t\t\t\t')).capitalize()
    new_pass = input('\n\n ' + 25 * '-' + ' ENTER NEW PASSWORD ' + 25 * '-' + '\n\n' + '\t\t\t\t')

    run_query(f"UPDATE passwords SET PASSWORD='{new_pass}' WHERE NAME='{site}'")

    input('\n\nPassword successfully updated.\nPress Enter to return to Main Menu.')
    home()


def add_pass():
    system('cls')
    name = str(input('\n\n ' + 29 * '-' + ' ENTER NAME ' + 29 * '-' + '\n\n' + '\t\t\t\t')).capitalize()
    user_id = input('\n\n ' + 30 * '-' + ' ENTER ID ' + 30 * '-' + '\n\n' + '\t\t\t\t')
    password = input('\n\n ' + 27 * '-' + ' ENTER PASSWORD ' + 27 * '-' + '\n\n' + '\t\t\t\t')

    run_query(f"INSERT INTO passwords VALUES('{name}', '{user_id}', '{password}')")

    input('\n\nPassword successfully added.\nPress Enter to return to Main Menu.')
    home()


def delete_pass():
    system('cls')
    name_to_delete = str(input('\n\n ' + 29 * '-' + ' ENTER NAME ' + 29 * '-' + '\n\n' + '\t\t\t\t')).capitalize()
    confirm = input("\nAre you sure you want to delete " + str(name_to_delete) + '?\n\t\ty/n : ')

    if confirm == 'y':
        run_query(f"DELETE FROM passwords WHERE NAME='{name_to_delete}'")
        print('\n\nPassword Deleted.\nPress Enter to return to Main Menu.')
    else:
        home()

    input()
    home()


def change_vault_pass():
    system('cls')
    print('\n\n ' + '-' * 30 + ' ENTER CURRENT PASSWORD ' + '-' * 30 + '\n')
    current_pass = str(input('\t\t\t\t\t'))

    if vault_pass_check(current_pass) is True:
        print('\n\n ' + '-' * 32 + ' ENTER NEW PASSWORD ' + '-' * 32 + '\n')
        new_pass = str(input('\t\t\t\t\t'))
        pass_file = open('C:\\Users\\Rudraksh\\GitHub\\Python_Files\\Password Manager\\password.txt', 'w')
        pass_file.write(new_pass)
        pass_file.close()
        input('\n\nVault password successfully changed.\nPress Enter to return to Main Menu.')
        home()

    else:
        input('\n\nIncorrect Password.\nPress Enter to return to Main Menu.')
        home()


authentication()
