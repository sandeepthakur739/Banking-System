import random
import time
from datetime import datetime
import json
import os

current_date = datetime.now()  #will use in file next

numbers=[0,1,2,3,4,5,6,7,8,9]

bank_accounts={}
balance={}
beneficiary={}
default_balance=0

if os.path.exists("system_data.json"):
    try:
        with open("system_data.json", "r", encoding="utf-8") as f:
            saved_data = json.load(f)

            bank_accounts = saved_data.get("all_banks", {})
            balance = saved_data.get("all_balance", {})
            beneficiary = saved_data.get("all_beneficiaries", {})

    except json.JSONDecodeError:
        pass


def save_system_data():

    all_data = {
        "all_banks" : bank_accounts,
        "all_balance" : balance,
        "all_beneficiaries" : beneficiary
    }

    with open("system_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)


def create_account(account_name):

    account_number=''.join(map(str, random.choices(numbers, k=16)))
    bank_accounts.update({account_name : account_number})
    balance.update({account_name : default_balance})
    save_system_data()



def document_verification(choose_document, is_document_verified):

    match choose_document:

        case 1:

            try:
                aadhar_number=input('\nEnter Your Aadhar Card Number: ')
                int(aadhar_number)  #for checking the length in next step
                print('\nDetails submitted succesfully.') 
                print('\nPlease wait for verification...\n')

                for time_left in range(5, 0, -1):
                    time.sleep(1)
                    print(f'{time_left} Second left\n')

                if len(aadhar_number)!=12:
                    print('Verification Failed!')
                    print('Please Input 12 Digit Aadhar Number.\n')
                    is_document_verified = False
                    return is_document_verified

                else:
                    print('Verification Succesfull.')
                    print()
                    is_document_verified=True 
                    return is_document_verified

            except ValueError:
                print('Error: Please input integrs only!')
                is_document_verified = False
                return is_document_verified

            
        
        case 2:
            print('\n(Format: ABCDE1234F)')

            pan_card=input('\nEnter Your Pan Card Number: ').upper().strip()

            print('\nDetails submitted succesfully.') 
            print('\nPlease wait for verification...')
            print()
            
            for time_left in range(5, 0, -1):
                time.sleep(1)
                print(f'{time_left} Second left\n')
            
            first_part = pan_card[0:5]
            second_part = pan_card[5:9]
            third_part = pan_card[9:]

            if first_part.isalpha() and second_part.isdigit() and third_part.isalpha():
                print('Verification Succesfull.')
                is_document_verified=True
                return is_document_verified

            elif not first_part.isalpha() or not second_part.isdigit():
                print('\nWrong Format!')
                is_document_verified=False
                return is_document_verified

            else:    
                print('\nLast character should be integer!')
                is_document_verified=False
                return is_document_verified
            

        case 3:
            input('Please Enter Document Name: ')
            input('Please Enter Document Number: ')
            print('\nDocument Added Succesfully.')
            print()
            is_document_verified = True
            return is_document_verified

        case _:
            print('Invalid Choice!')    
            is_document_verified = False
            return is_document_verified



def view_account():

    i = 1
    for key, value in bank_accounts.items():
        print(f'{i}. Account name: {key}')
        print(f'   Account number: {value}')
        print(f'   Available balance = {balance.get(key)}Rs')
        i += 1



def update_info():
            
            for key, value in bank_accounts.items():
             print(f'{key}, {value}')

            choose_name=input('\nChoose bank account name: ')

            if choose_name in bank_accounts:
                new_name=input('Enter new name: ')        
                bank_accounts[new_name]=bank_accounts.pop(choose_name)
                balance[new_name]=balance.pop(choose_name)
                print('Account name updated successfully.')    
                save_system_data()

            else:
                print('Accout name is incorrect.') 
                    


def deposit_money():

    for key, value in balance.items():
            print(f'Account name: {key}, Available balance: {value}Rs')    

    choose_name=input('Choose bank account name: ')

    if choose_name in balance:
        deposit_amount=float(input('Enter deposit amount: '))

        if deposit_amount>1_0_000_000:
            print('You cannot add more than 1 Crore')
        else:
            balance[choose_name] += deposit_amount
            print(f'\n₹{deposit_amount} deposited successfully.')
            print(f'Current Balance = ₹{balance[choose_name]}')

            #we are using function that will automatically save in file
            file_save(choose_name, deposit_amount, 'Deposit', 'Success')
            save_system_data()

    else:
        print('Account name not found.')        



def withdraw_money(choose_bank):

    if choose_bank in balance:

        if balance[choose_bank] > 0:

            withdraw_amount=float(input('Enter withdraw amount: '))

            if withdraw_amount <= balance[choose_bank]:

                balance[choose_bank]-=withdraw_amount
                print(f'\n₹{withdraw_amount} withdrawn successfully.')
                print(f'Current Balance = ₹{balance[choose_bank]}')
                file_save(choose_bank, withdraw_amount, 'Withdraw', 'Success')
                save_system_data()

            else:
                print('Withdraw amount cannot be greater than available balance!\n')

        else:
            print('Low balance!\n')

    else:
        print('The account name is incorrect!\n')



def add_beneficiary(person_name, person_bank_name, person_acc_number, person_ifsc):

    if person_name in beneficiary:
        print('Beneficiary details already exists!\n')

    else:

        beneficiary[person_name]={'bank_name':person_bank_name, 'account_number':person_acc_number, 'ifsc':person_ifsc}
        save_system_data()



def view_beneficiary():

    if beneficiary:
        i = 1
        for key, value in beneficiary.items():
            print(f'{i}. Account Holder Name: {key}')
            print(f'   Bank Name: {value["bank_name"]}')
            print(f'   Accout number: {value["account_number"]}')
            print(f'   IFSC Code: {value["ifsc"]}')
            i += 1
    else:
        print('No Benefificay exists. Please add a beneficiary to continue!')          



def delete_beneficiary(choose_ben_name):

    if choose_ben_name in beneficiary:
        beneficiary.pop(choose_ben_name)
        save_system_data()
    else:
        print('Entered name is not in beneficiary!')    



def transfer():

    i = 1
    for acc_name, acc_number in bank_accounts.items():
        print(f'{i}. Account name: {acc_name}')
        print(f' Account Number: {acc_number}')
        i += 1
    print()    

    transfer_from=input('Please choose transfer from account: ')
    print()

    if transfer_from in bank_accounts:

        i = 1
        for name, other_items in beneficiary.items():
            print(f'{i}. Account Holder Name: {name}')
            print(f' Bank Name: {other_items["bank_name"]}') 
            print(f' Account Number: {other_items["account_number"]}')
            print(f' IFSC Code: {other_items["ifsc"]}')
            i += 1

        transfer_to=input('Please choose account to transfer: ')

        if transfer_to in beneficiary:

            transfer_amount=float(input('Enter amount to transfer: '))

            if transfer_amount<=balance[transfer_from]:

                balance[transfer_from]-=transfer_amount
                #balance[transfer_to]+=transfer_amount
                #we can use upper one also
                print(f'\n₹{transfer_amount} have been transfered succesfully.')
                print(f'Current Balance = ₹{balance[transfer_from]}')
                file_save(transfer_from, transfer_amount, 'Transfer', 'Success')
                save_system_data()

            else:
                print('Transfer amount cannot be greater than balance!')

        else:
            print('Selected beneficiary is not in list!')

    else:
        print('Choosed account is not in bank accounts!')        



def delete_account():

    i = 1
    for a, b in bank_accounts.items():
        print(f'{i}. Account name: {a}')
        print(f' Account Number: {b}')
        i += 1

    delete_bank=input('Enter bank name to delete: ')
    print()
    if delete_bank in bank_accounts:
        bank_accounts.pop(delete_bank)
        print('Bank account deleted successfully.')
        save_system_data()
        print()

    else:
        print('Bank account not found!')
        print()  



def file_save(Account_Name, Amount, Type, Status):

    transaction_list=[]

    new_transaction = {
        'Account name' : Account_Name,
        'Account number' : bank_accounts.get(Account_Name),
        'Amount' : Amount,
        'Type' : Type,
        'Status' : Status,
        'Current Balance' : balance[Account_Name],
        'Date' : current_date.strftime('%d %b %Y')
        }
    
    if os.path.exists("bank_accounts.json"):
        try:
            with open("bank_accounts.json", "r", encoding="utf-8") as f:
                transaction_list = json.load(f)
        except json.JSONDecodeError:
            pass
    
    transaction_list.append(new_transaction) 
    with open("bank_accounts.json", "w", encoding="utf-8") as f:
        json.dump(transaction_list, f, indent=4)                



while True:
 
 print('Welcome to Home National Bank...\n')
 print('1. Create New Bank Account')
 print('2. View Balance/Accounts')
 print('3. Update Bank Accounts')
 print('4. Deposit Money')
 print('5. Withdraw Money')
 print('6. Add Beneficiary')
 print('7. View/Delete Benificiary')
 print('8. Transfer Money')
 print('9. Recent Transactions')
 print('10. Delete Bank Account')
 print('11. Contact Us')
 print('Owner: Sandeep Kumar')
 
 choice=int(input('\nEnter your chocie: '))
 print()
 
 match choice:
     
     case 1:
         is_document_verified=True

         if len(bank_accounts)<=3:

             account_name=input('Enter your name: ')
             age=int(input('Enter your age: '))
             
             if age<18:
                 print('You are a minor! You have to be 18 for opening an account!')
                 print()

             else: 

                print('\nDocument Verification:\n')
                print('1. Aadhar Card')
                print('2. Pan card')
                print('3. Other Document')
                choose_document=int(input('\nChoose Document Number: '))
                
                # Captured the returned verification status
                is_document_verified = document_verification(choose_document, is_document_verified)

                if not is_document_verified:
                    continue # Switched to continue instead of break to keep menu running

                else:

                    print()
                    create_account(account_name)
                    print('Your bank account is created successfully.\n')
                    print(f'Your account name is: {account_name}')
                    print(f'Your account number is: {bank_accounts.get(account_name)}')
                    print(f'Your account balance is: {balance.get(account_name)}Rs\n')
             
         else:
             print('You cannot add more than 3 accounts.\n') 
 
     case 2:
         if not bank_accounts:
             print('No bank account found! Please create a bank account first.\n')

         else:
             view_account()    
             print()

     case 3:
         if not bank_accounts:
             print('No bank account found! Please create a bank account first.\n')

         else:      
          update_info()
          print()

     case 4:
         if not bank_accounts:
             print('No bank account found! Please create a bank account first.\n')

         else:    
          deposit_money()
          print()

     case 5:
         if not bank_accounts:
             print('No Bank account found! Please create a Bank account first.')    

         else:
             
             i = 1
             for key, value in balance.items():
              print(f'{i}. Account name: {key}, Available balance: {value}Rs')
              i += 1

             choose_bank=input('Choose a Bank account name: ')
             withdraw_money(choose_bank)

     case 6:
         person_name=input('Enter Account Holder Name: ')
         person_bank_name=input('Enter Bank Name: ')
         person_acc_number=input('Enter Account Number: ')
         person_ifsc=input('Enter IFSC Code: ')
         add_beneficiary(person_name, person_bank_name, person_acc_number, person_ifsc)
         print('Benificiary details added successfully.\n')

     case 7:
         print('1 for View Beneficiary.')
         print('2 for Delete Benificiary')
         print()
         choose=int(input('Enter your choice: '))
         print()
         if choose==1:
             view_beneficiary()
             print()

         elif choose==2:
             for key in beneficiary:
                 print(key)
             choose_ben_name=input('Choose beneficiary name: ')
             delete_beneficiary(choose_ben_name)
             print(f'Beneficiary {choose_ben_name} removed successfully.\n')            

     case 8:
         transfer()

     case 9:
        try: # Added try/except to prevent crash if file doesn't exist yet
            with open("bank_accounts.txt", "r") as f:
                content = f.read()
                print(content)    
        except FileNotFoundError:
            print("No transactions yet.")

     case 10:
         delete_account()    
                 
     case 11:
         print('Owner: Sandeep Kumar')
         print('Email Id: abc@gmail.com')
         print('Phone Number: 1234567890')
         print('Website: www.abc.com')
         print()

     case _:

         print('Invalid Choice!')  
         print()