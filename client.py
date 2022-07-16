from distutils.log import info
import json
import socket
import threading
import os
import sys
import datetime

HOST = "127.0.0.1"
PORT = 12344

lst_food = ["com suon",'mi y','hu tieu go','banh xeo','banh canh','pepsi','coca','tra da','sprite']
food_order = []
lst_quan = []
total = 0
status = True
timeOrder = None

#for user want to order more in the time of 2 hours
clientInfo = {}
orderBefore = False


def print_Menu(menu):
    print("-----------  MENU OF THE DAY -----------")

    for x in range(0,9):
        print('\t' + menu['foods'][x]['index'] + '. ' 
        + menu['foods'][x]['name'] + '\t' + str(menu['foods'][x]['price']) )
    
    print("-----------  ENJOY THE MEAL! -----------")

def print_Options():
    print("-----------  RUKI FOOD STORE -----------")
    print("\t1. View menu")
    print("\t2. Order")
    print("\t3. Payment")
    print("\t4. Exit")
    print("-----------  HAVE YOUR WISH  -----------")

def deleteClient(client):
    # inform server that this client has left
    client.sendall("quit".encode('utf8'))    
    client.close()

def account_numbers_checking():
    account_numbers = input("Enter your account numbers: ")

    # Preprocessing
    account_numbers = account_numbers.strip(" ")

    # Length checking
    if len(account_numbers) != 10:
        return False

    # Char checking
    for char in account_numbers:
        try:
            int(char)
        except:
            return False

    return True


def payment():
    if status == True:
        return True
    # Input Checking
    while True:
        # Check if user has no order.
        if total == 0:
            print("Your had no order before. Please order something to pay up")
            return False
        
        if orderBefore == True:
            sumUp = total + clientInfo.get('total')
            needToPay = sumUp - total
            print(f"Total: {sumUp}")
            print(f"You need to pay: {needToPay}")
        else:    
            print(f"Total: {total}")
        
        print("--- Please Choose Payment Methods ---")
        print("1. Cash Payment")
        print("2. Charge Card Payment")
        choice = input("Enter 1 or 2: ")
        mess = ""
        if choice == '1':
            break
        elif choice == '2':
            # Account numbers checking
            if account_numbers_checking() == False:
                print("Invalid account numbers. Please try again!")
                continue
            break
        else:
            print("Invalid choice. Please try again!")
            continue

    print("Successful payment")

    os.system("PAUSE")
#    sys.exit()
    return True

def checkFoodName_Quantity(idx, quan):
    if idx >= 0 and idx <= 8:
        if quan > 0:
            return True
        else:   
            return False
    return False

# Function to convert string to datetime
def convertStr_to_Time(date_timeStr):
	format = '%b %d %Y %H:%M:%S' # The format
	datetime_str = datetime.datetime.strptime(date_timeStr, format)

	return datetime_str

# Function to convert datetime to string
def convertDatetime_to_Str(date_time):
	format = "%b %d %Y %H:%M:%S" # The format
	date_Time = datetime.datetime.strftime(date_time,format)
	return date_Time

def order(menu):
    global total
    global timeOrder
    while True:
        foodIdx = input("Input the index of foods/drinks: ")
        quantity = input("Input the quantity: ")
        idx = int(foodIdx) - 1
        while checkFoodName_Quantity(idx,int(quantity)) == False:
            print("Wrong input. Try again!")
            foodIdx = input("Input the index of foods/drinks: ")
            quantity = input("Input the quantity: ")
            idx = int(foodIdx) - 1

        food_order.append(menu['foods'][idx]['name'])
        lst_quan.append(quantity)
        total += menu['foods'][idx]['price']*int(quantity)

        ans = input("Do you want to continue ordering? yes/no ")
        if ans.lower() == 'no':
            time = datetime.datetime.now()
            timeOrder = convertDatetime_to_Str(time)
            break

def sendNewData(customer,nick,client):
    #send data to server
    customer.update({'name': nick})
    customer.update({'foods': food_order})
    customer.update({'quantity': lst_quan})
    customer.update({'total': total})
    customer.update({'Order time': timeOrder})
    customer.update({'status': 'Paid'})

    data = json.dumps(customer)
    client.sendall(data.encode('utf8'))
    
def orderMore(nick):
    # information of more order
    global clientInfo, status
    while status == False:
        status = payment()
        
    sumUp = total + clientInfo.get('total')
    
    # append to clientInfo
    print(clientInfo)
    print("----------------")
    clientInfo.update({'name': nick})
    for x in food_order:
        clientInfo['foods'].append(x)
    for x in lst_quan:
        clientInfo['quantity'].append(x)
    clientInfo.update({'total': sumUp})
    clientInfo.update({'status': 'Paid'})
    print(clientInfo)
    
    

def handle_Options(client, nick,menu):
    global status
    print_Options()

    choice = input("Choose your option: ")
    while True:
        if choice == '1':
            print_Menu(menu)
        elif choice == '2':
            status = False
            print_Menu(menu)
            order(menu)
            
            if orderBefore == True:
                print("zoo order ve")
                orderMore(nick)
            else:
                print("Total: " + str(total))
                print("Your foods have been installed successfully. Please come to pay up...")
        elif choice == '3':
            status = payment()
        elif choice == '4':   
            #if user has not paid, return
            if status == False:
                print("You have not paid your order. Please come to Payment to pay!")
            else:    
                print('**** Thank you for using our service ****')
                print('              See you again              ')    
                
                if(orderBefore == True):
                    print("update") 
                    client.sendall("update".encode('utf8'))
                    data = json.dumps(clientInfo)
                    client.sendall(data.encode('utf8'))
                else:
                    print("append")
                    client.sendall("append".encode('utf8'))
                    sendNewData(clientInfo,nick,client)
                break
        else:
            print("Invalid options. Please try again!")
        print_Options()
        choice = input("Choose your option: ")
        
    
    
# check if it is 2 hours before the previous order or not
def checkTime(clientInfo):
    timeOrder = convertStr_to_Time(clientInfo['Order time'])
    curTime = datetime.datetime.now()
    dur = curTime - timeOrder
    
    # 2 hours = 7200 seconds
    if dur.total_seconds() < 7200:
        return True
        #cho order tieeps
    else:
        return False

def receive(client):
    global orderBefore, clientInfo
    mess = client.recv(1024).decode("utf8")
    print(mess)
    
    # input name
    nick = input("Please enter your name: ")
    client.sendall(nick.encode("utf8"))
    
    mess = client.recv(1024).decode('utf8')
    print(mess) # Let's order
    
    # receive menu
    data = client.recv(1024).decode('utf8')
    # convert string to dict
    menu = json.loads(data)
    
    #check user
    mess = client.recv(1024).decode('utf8')
    if mess == "ordered":
        info = client.recv(1024).decode('utf8')
        clientInfo = json.loads(info)
        orderBefore = True
        print("used to order")
        if checkTime(clientInfo) == True:
            print("can order")
            handle_Options(client,nick,menu)
            
        else: #exit + trả về nick nhận ở trên  -- no bug here
            print("You have run out of time order so you can not order anymore. See you again")
            client.sendall("update".encode('utf8'))
            data = json.dumps(clientInfo)
            client.sendall(data.encode('utf8'))
            
    else: # no bug here
        print("not order before")
        handle_Options(client,nick,menu)

    
#    os.system('cls')

    #handle_Options(client,nick)
    
    client.close()

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    receive_thread = threading.Thread(target=receive,args=(client,))
    receive_thread.start()