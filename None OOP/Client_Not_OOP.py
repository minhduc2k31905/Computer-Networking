import tkinter as tk
from tkinter.constants import *
from tkinter import *
from tkinter import messagebox
import os
from typing import Container
from PIL import ImageTk, Image
import json
import socket
import threading
import os
import sys
import datetime
import copy

# LARGE_FONT = ("Verdana", 12)
HOST = "127.0.0.1"
PORT = 12344
lst_food = []
lst_price = []
# lst_food = ['com suon', 'mi y', 'hu tieu go', 'banh xeo',
#             'banh canh', 'pepsi', 'coca', 'tra da', 'sprite']
# lst_price = [30, 25, 25, 20, 25, 10, 10, 5, 10]
food_order = []
lst_quan = []
menu = {}
user_name = ""
total = 0
status = True
timeOrder = None
count = 0

# for user want to order more in the time of 2 hours
clientInfo = {}
orderBefore = False


# Function
def send_data_and_quit():
    global clientInfo
    # Send message to server
    mess = "-"
    client.sendall(mess.encode('utf8'))

    # Send data to server
    data = json.dumps(clientInfo)
    client.sendall(data.encode('utf8'))

    print(clientInfo)
    client.close()
    os.sys.exit()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client.close()
        os.sys.exit()


def CashPayment(root, is_empty=False):
    global clientInfo

    if is_empty == True:
        messagebox.showinfo(
            "Payment", "You have no order before. Please order something and then pay up!")
        StartPage(root)
        return

    #print("Cash Payment Successed")
    messagebox.showinfo("Payment", "Payment Successed")
    clientInfo.update({'status': 'Paid'})

    # ========================================================================================
    send_data_and_quit()


def handleAccountNumber(root, account):
    global clientInfo
    account = account.strip(" ")

    is_true = True

    # Length checking
    if len(account) != 10:
        is_true = False

    # Char checking
    for char in account:
        try:
            int(char)
        except:
            is_true = False

    if is_true:
        # print("Charge Cart Payment Successed")
        messagebox.showinfo("Payment", "Payment Successed")
        clientInfo.update({'status': 'Paid'})

        # ========================================================================================
        send_data_and_quit()
    else:
        root.label_notice['text'] = "Syntax error. Please try again!"


def ChargeCardPayment(root, is_empty=False):

    if is_empty == True:
        messagebox.showinfo(
            "Payment", "You have no order before. Please order something and then pay up!")
        StartPage(root)
        return

    root.destroy()
    root = init()

    # label
    label = tk.Label(root, text="Enter your account numbers: ",
                     bg="#9FD996", font=("Roman", 32))
    label.place(relx=0.5, rely=0.2, anchor=CENTER)

    root.label_notice = tk.Label(
        root, text="", bg="#9FD996", font=("Verdana", 12), fg='#ff0000')
    root.label_notice.place(relx=0.5, rely=0.54, anchor=CENTER)

    # Account numbers
    account_numbers = Entry(root, width=25, font=32, bg="light cyan")
    account_numbers.place(relx=0.5, rely=0.45, anchor=CENTER)

    # Submit button
    back_button = tk.Button(
        root,
        command=lambda: handleAccountNumber(root, account_numbers.get()),
        height=1, width=10, font=26, text="OK", bg="#0080FF", fg="white"
    )
    back_button.place(relx=0.5, rely=0.63, anchor=CENTER)

    # Back home button
    back_button = tk.Button(
        root,
        command=lambda: StartPage(root),
        height=3, width=10, text="Back to home", bg="#FF6666", fg="white"
    )
    back_button.place(relx=0.1, rely=0.9, anchor=CENTER)


def PrintEmptyLine(root, num_of_line=4):
    for _ in range(num_of_line):  # Print 4 empty lines
        food_label = Label(root, bg='#FFFFFF',
                           width=15, height=2, text="")
        food_label.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)

    return


def PaymentPage(root):
    root.destroy()
    root = init()

    global lst_food, lst_price, clientInfo, countasd
    food_order = clientInfo['foods'][:]
    lst_quan = clientInfo['quantity'][:]
    total = clientInfo['total']
    is_empty_order = False
    # Payment label
    label = tk.Label(root, text="Payment Page",
                     bg="#9FD996", font=("Roman", 32))
    label.place(relx=0.5, rely=0.15, anchor=CENTER)

    # label
    title_label = tk.Label(root, text="Ordered",
                           bg="#9FD996", font=("Roman", 22))
    title_label.place(relx=0.5, rely=0.25, anchor=CENTER)

    # Internal Frame
    internal_frame = Frame(root, bg="#FFFFFF", width=300, height=200)
    internal_frame.place(relx=0.19, rely=0.3)

    # Ordered food frame
    food_ordered_frame = Frame(
        internal_frame, bg="#FFFFFF", width=300, height=200)
    food_ordered_frame.grid(row=0, column=0)

    # Ordered
    ordered_label = tk.Label(food_ordered_frame, text="Food", bg="#FFFFFF")
    ordered_label.pack(side="top", fill='both', anchor="w")

    if len(food_order) != 0:
        for food in food_order:
            food_label = Label(food_ordered_frame, bg='#FFFFFF',
                               width=15, height=2, text=food)
            food_label.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)
    else:
        is_empty_order = True
        PrintEmptyLine(food_ordered_frame)

    # Price frame
    price_frame = Frame(
        internal_frame, bg="#FFFFFF", width=300, height=200)
    price_frame.grid(row=0, column=1)

    price_label = tk.Label(price_frame, text="Price", bg="#FFFFFF")
    price_label.pack(side="top", fill='both', anchor="w")

    # Find list price of that order
    lst_price_of_order = []

    for index in range(len(lst_food)):
        for food in food_order:
            if menu['foods'][index]['name'] == food:
                lst_price_of_order.append(menu['foods'][index]['price'])

    if len(food_order) != 0:
        for index in range(len(food_order)):
            price_label = Label(price_frame, bg='#FFFFFF',
                                width=15, height=2, text=lst_price_of_order[index])
            price_label.pack(side="top", fill='y',
                             anchor="w", padx=0, pady=1.5)
    else:
        PrintEmptyLine(price_frame)

    # Ordered quantity frame
    quantity_ordered_frame = Frame(
        internal_frame, bg="#FFFFFF", width=300, height=200)
    quantity_ordered_frame.grid(row=0, column=2)

    quantity_label = tk.Label(quantity_ordered_frame,
                              text="Quantity", bg="#FFFFFF")
    quantity_label.pack(side="top", fill='both', anchor="w")

    if len(food_order) != 0:
        for quantity in lst_quan:
            quantity_label = Label(quantity_ordered_frame, bg='#FFFFFF',
                                   width=15, height=2, text=quantity)
            quantity_label.pack(side="top", fill='y',
                                anchor="w", padx=0, pady=1.5)
    else:
        PrintEmptyLine(quantity_ordered_frame)

    # Amount frame
    amount_frame = Frame(
        internal_frame, bg="#FFFFFF", width=300, height=200)
    amount_frame.grid(row=0, column=3)

    amount_label = tk.Label(amount_frame, text="Amount", bg="#FFFFFF")
    amount_label.pack(side="top", fill='both', anchor="w")

    if len(food_order) != 0:
        for index in range(len(food_order)):
            amount = int(lst_quan[index])*int(lst_price_of_order[index])
            amount_label = Label(amount_frame, bg='#FFFFFF',
                                 width=15, height=2, text=amount)
            amount_label.pack(side="top", fill='y',
                              anchor="w", padx=0, pady=1.5)
    else:
        PrintEmptyLine(amount_frame)

    # Total
    total_frame = Frame(
        internal_frame, bg="#FFFFFF", width=50, height=200)
    total_frame.grid(row=0, column=4)

    total_label = tk.Label(total_frame, text="Total", bg="#FFFFFF")
    total_label.pack(side="top", fill='both', anchor="w")

    print_total = Label(total_frame, bg='#FFFFFF',
                        width=10, height=2, text=clientInfo['total'])
    print_total.pack(side="bottom", fill='both', anchor="w")

    # Back home button
    back_button = tk.Button(
        root,
        command=lambda: StartPage(root),
        height=3, width=15, text="Back to home", bg="#FF6666", fg="white"
    )
    back_button.place(relx=0.1, rely=0.9, anchor=CENTER)

    # Cash payment button
    pay_up_button = tk.Button(
        root,
        command=lambda: CashPayment(root, is_empty=is_empty_order),
        height=3, width=20, text="Cash payment", bg="#0080FF", fg="white"
    )
    pay_up_button.place(relx=0.34, rely=0.9, anchor=CENTER)

    # Charge Card Payment
    pay_up_button = tk.Button(
        root,
        command=lambda: ChargeCardPayment(root, is_empty=is_empty_order),
        height=3, width=20, text="Charge Card Payment", bg="#FF9933", fg="white"
    )
    pay_up_button.place(relx=0.65, rely=0.9, anchor=CENTER)

    # Put object


def saveNewOrder(food_order_new, lst_quan_new, total_new, timeOrder_new):
    global food_order, lst_quan, total, timeOrder, clientInfo, user_name

    # Copy data to avoid pointer
    food_order = food_order_new.copy()
    lst_quan = lst_quan_new.copy()
    total = copy.copy(total_new)
    timeOrder = copy.copy(timeOrder_new)

    # Update
    if orderBefore == True:

        sumUp = total_new + clientInfo.get('total')
        clientInfo.update({'name': user_name})

        # Old
        # for x in food_order:
        #     clientInfo['foods'].append(x)
        # for x in lst_quan:
        #     clientInfo['quantity'].append(x)

        # New: Extend mean split the list in to elements and append to original list
        clientInfo['foods'].extend(food_order)
        clientInfo['quantity'].extend(lst_quan)

        clientInfo.update({'total': sumUp})
        clientInfo.update({'Order time': timeOrder})
        clientInfo.update({'status': 'Not Paid'})

    else:  # Not order before
        sumUp = total_new + clientInfo.get('total')
        clientInfo.update({'name': user_name})
        clientInfo['foods'].extend(food_order)
        clientInfo['quantity'].extend(lst_quan)
        clientInfo.update({'total': sumUp})
        clientInfo.update({'Order time': timeOrder})
        clientInfo.update({'status': 'Not Paid'})
        # clientInfo.update({'name': user_name})
        # clientInfo.update({'foods': food_order})
        # clientInfo.update({'quantity': lst_quan})
        # clientInfo.update({'total': total})
        # clientInfo.update({'Order time': timeOrder})
        # clientInfo.update({'status': 'Not Paid'})

    # Clear content
    food_order_new.clear()
    lst_quan_new.clear()
    total_new = 0
    timeOrder_new = ""

    print("ClientInfo after submit:")
    print(clientInfo)
    # print(food_order)
    # print(lst_quan)
    return


def DataProcessing(food_vars=[], quantity_vars=[]):
    global menu, lst_food, lst_price, timeOrder, clientInfo
    food_order = []
    lst_quan = []
    total = 0
    # print("Order")
    for i in range(len(lst_food)):
        if food_vars[i].get() == 1:  # Mean that we tick at that food
            # Print to check
            # print(lst_food[i], ":", quantity_vars[i].get())

            # Save order
            food_order.append(lst_food[i])
            lst_quan.append(quantity_vars[i].get())
            total += menu['foods'][i]['price']*int(quantity_vars[i].get())

    time = datetime.datetime.now()
    timeOrder = convertDatetime_to_Str(time)
    # print(total)
    # print("Time:", timeOrder)

    saveNewOrder(food_order, lst_quan, total, timeOrder)


def OrderPage(root):
    root.destroy()
    root = init()

    global lst_food, lst_price, food_order, lst_quan, clientInfo
    food_vars = []
    quantity_vars = []
    # Order label
    label = tk.Label(root, text="Order Page", bg="#9FD996", font=("Roman", 32))
    label.place(relx=0.5, rely=0.15, anchor=CENTER)

    # Internal Frame
    internal_frame = Frame(root, bg="#FFFFFF", width=300, height=200)
    internal_frame.place(relx=0.26, rely=0.25)

    # Food frame
    food_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
    food_frame.grid(row=0, column=1)

    food_label = tk.Label(food_frame, text="List Foods", bg="#FFFFFF")
    food_label.pack(side="top", fill='both', anchor="w")
    for food in lst_food:
        var = IntVar()
        chk = Checkbutton(
            food_frame, bg='#FFFFFF', anchor="w", height=2, width=15, text=food, variable=var)
        chk.pack(side="top", fill='y', anchor="w")
        food_vars.append(var)

    # # Price Frame
    price_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
    price_frame.grid(row=0, column=2)

    price_label = tk.Label(price_frame, text="Price", bg="#FFFFFF")
    price_label.pack(side="top", fill='both', anchor="w")

    for price in lst_price:
        label_i = Label(price_frame, bg='#FFFFFF',
                        width=15, height=2, text=price)
        label_i.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)

    # Quantity Frame
    quantity_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
    quantity_frame.grid(row=0, column=3)

    quantity_label = tk.Label(quantity_frame, text="Quantity", bg="#FFFFFF")
    quantity_label.pack(side="top", fill='both', anchor="w")
    for _ in range(len(lst_food)):
        var = StringVar(value=0)
        spin_box = tk.Spinbox(
            quantity_frame, from_=0, to=999, bd=2, bg="#FFFFFF", textvariable=var, wrap=True)
        spin_box.pack(side="top", fill='y', padx=0, pady=10)
        quantity_vars.append(var)

    # Submit button
    back_button = tk.Button(
        root,
        # command=lambda: controller.show_frame(StartPage),
        command=lambda: DataProcessing(food_vars, quantity_vars),
        height=3, width=10, text="Add to cart", bg="#0080FF", fg="white"
    )
    back_button.place(relx=0.9, rely=0.9, anchor=CENTER)

    # Back home button
    back_button = tk.Button(
        root,
        command=lambda: StartPage(root), height=3, width=10, text="Back to home", bg="#FF6666", fg="white"
    )
    back_button.place(relx=0.1, rely=0.9, anchor=CENTER)


def open():
    global my_img
    top = Toplevel()
    top.title('My Second Window')

    img = Image.open('camcui.jpg')
    img = img.resize((450, 350))
    # Resize image
    # my_img = my_img.resize((600, 350))
    my_img = ImageTk.PhotoImage(img)
    my_label = Label(top, image=my_img).pack()
    btn2 = Button(top, text="close window", command=top.destroy).pack()


def ViewMenuPage(root):
    root.destroy()
    root = init()

    global lst_food, lst_price

    # Menu label
    label = tk.Label(root, text="MENU OF THE DAY",
                     bg="#9FD996", font=("Roman", 32))
    label.place(relx=0.5, rely=0.1, anchor=CENTER)

    # Internal Frame
    internal_frame = Frame(root, bg="#FFFFFF", width=300, height=200)
    internal_frame.place(relx=0.32, rely=0.18)

    # Food frame
    food_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
    food_frame.grid(row=0, column=1)

    food_label = tk.Label(food_frame, text="List Foods", bg="#FFFFFF")
    food_label.pack(side="top", fill='both', anchor="w")

    for food in lst_food:
        label_i = Label(food_frame, bg='#FFFFFF',
                        width=15, height=2, text=food)
        label_i.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)

    # Price Frame
    price_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
    price_frame.grid(row=0, column=2)

    price_label = tk.Label(price_frame, text="Price", bg="#FFFFFF")
    price_label.pack(side="top", fill='both', anchor="w")

    for price in lst_price:
        label_i = Label(price_frame, bg='#FFFFFF',
                        width=15, height=2, text=price)
        label_i.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)

    # Show image frame
    show_image_frame = Frame(
        internal_frame, bg="#FFFFFF", width=300, height=200)
    show_image_frame.grid(row=0, column=3)

    showImage_label = tk.Label(show_image_frame, text="Show image",
                               bg="#FFFFFF")
    showImage_label.pack(side="top", fill='both', anchor="w")

    for _ in range(len(lst_food)):
        var = IntVar()
        button = Button(show_image_frame, text='+',
                        command=open, bd=1, bg="#FFFFFF")
        button.pack(side="top", fill='y', padx=0, pady=8)
        # vars.append(var)

    # Back home button
    back_button = tk.Button(
        root,
        command=lambda: StartPage(root),
        height=3, width=10, text="Back to home", bg="#FF6666", fg="white"
    )
    back_button.place(relx=0.1, rely=0.9, anchor=CENTER)

    return


def StartPage(root):
    root.destroy()
    root = init()

    # Label
    name = tk.Label(root, text="Ruki Food Store",
                    bg="#9FD996", font=("Roman", 32))

    # Button
    # View menu button
    view_menu_button = tk.Button(root,
                                 command=lambda: ViewMenuPage(root),
                                 height=2, width=10, font=22, text="View menu", bg="#ff9933", fg="white")

    # Order button
    order_button = tk.Button(root,
                             command=lambda: OrderPage(root),
                             height=2, width=10, font=22, text="Order", bg="#808080", fg="white")

    # Payment button
    payment_button = tk.Button(root,
                               command=lambda: PaymentPage(root),
                               # command=lambda: (controller.update_data_payment_page(),
                               #                  controller.show_frame(PaymentPage)),
                               height=2, width=10, font=22, text="Payment", bg="#0080FF", fg="white")

    # Exit button
    exit_button = tk.Button(root,
                            command=send_data_and_quit,
                            height=2, width=10, font=22, text="Exit", bg="#FF6666", fg="white")

    name.place(relx=0.5, rely=0.2, anchor=CENTER)
    view_menu_button.place(relx=0.5, rely=0.35, anchor=CENTER)
    order_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    payment_button.place(relx=0.5, rely=0.65, anchor=CENTER)
    exit_button.place(relx=0.5, rely=0.8, anchor=CENTER)


def convertStr_to_Time(date_timeStr):
    if date_timeStr == "":
        pass
    format = '%b %d %Y %H:%M:%S'  # The format
    datetime_str = datetime.datetime.strptime(date_timeStr, format)

    return datetime_str

# check if it is 2 hours before the previous order or not


def convertDatetime_to_Str(date_time):

    format = "%b %d %Y %H:%M:%S"  # The format
    date_Time = datetime.datetime.strftime(date_time, format)
    return date_Time


def checkTime(clientInfo):
    if clientInfo['Order time'] == "":
        return False

    timeOrder = convertStr_to_Time(clientInfo['Order time'])
    curTime = datetime.datetime.now()
    dur = curTime - timeOrder

    # 2 hours = 7200 seconds
    if dur.total_seconds() < 7200:
        return True
        # cho order tieeps
    else:
        return False


def checkUser():
    global orderBefore, clientInfo
    # Check user ordered before or not (receive 'ordered' or 'not ordered')
    is_order = client.recv(1024).decode('utf8')
    #is_order = ""

    if is_order == "ordered":
        # info: store the last order of user
        info = client.recv(1024).decode('utf8')

        # Convert to dic type
        clientInfo = json.loads(info)

        # Change flag
        orderBefore = True
        #print("You used to order")

        if checkTime(clientInfo) == True:

            is_proceed = messagebox.askyesno(title='Confirmation',
                                             message='Do you want to order with old ordered?')
            if is_proceed:  # Mean click yes button
                print("Continue order from old order")

            else:  # Mean click no button
                print("Continue order with new order")
                # Reset info of clientInfo
                initClientInfo()

            #print("After check time\n You can order")
            return "Can order"

        else:  # exit + trả về nick nhận ở trên  -- no bug here
            messagebox.showinfo(
                "Message",
                "You have run out of time order so you can not order anymore. See you again!")

            mess = "update"
            client.sendall(mess.encode('utf8'))

            # Send data to server
            data = json.dumps(clientInfo)
            client.sendall(data.encode('utf8'))

            client.close()
            os.sys.exit()

    else:  # Mean: is_order = not ordered
        #print("Not order before")
        return "Can order"


def CheckSignIn(root):
    try:
        global menu, lst_food, lst_price, user_name
        nickname = root. entry_user.get()

        if nickname == "":
            root.label_notice['text'] = "Name can not be empty"
            return
        else:
            # Save user name
            user_name = nickname

            # Send user name to client
            client.sendall(user_name.encode("utf8"))

            # If checkUser not receive "Can order", this mean we ended up program
            if checkUser() == "Can order":
                # Moving on StartPage
                StartPage(root)

    except Exception as e:
        print(e)


def signInPage(root):
    root.destroy()
    root = init()

    label_title = tk.Label(
        root, text="Welcome to Ruki Food Store", bg="#9FD996", font=("Roman", 30))
    label_user = tk.Label(
        root, text="Please enter your name", bg="#9FD996", font=("Roman", 22))
    root.label_notice = tk.Label(
        root, text="", bg="#9FD996", font=("Verdana", 12), fg='#ff0000')

    root.entry_user = tk.Entry(
        root, width=25, font=32, text="", bg="light cyan")

    # Button
    button_go = tk.Button(root, text="GO",
                          command=lambda: CheckSignIn(root))
    button_go.config(width=10, bg="green")

    label_title.place(relx=0.5, rely=0.3, anchor=CENTER)
    label_user.place(relx=0.5, rely=0.45, anchor=CENTER)
    root.entry_user.place(relx=0.5, rely=0.55, anchor=CENTER)
    root.label_notice.place(relx=0.5, rely=0.63, anchor=CENTER)
    button_go.place(relx=0.5, rely=0.7, anchor=CENTER)


def init():
    root = Tk()
    root.title('Hi')
    window_width = 800
    window_height = 600

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.configure(bg="#9FD996")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    return root


def receiveData():
    global lst_food, lst_price, menu
    # Receive menu
    data = client.recv(1024).decode('utf8')
    # Convert string to dict
    menu = json.loads(data)
    for x in range(0, 9):
        lst_food.append(menu['foods'][x]['name'])
        lst_price.append(menu['foods'][x]['price'])
        #print("Appended", x)

    # Test
    # print(menu)
    # print(lst_food)
    # print(lst_price)
    # exit_program()


def initClientInfo():
    global clientInfo

    clientInfo['name'] = ""
    clientInfo['foods'] = []
    clientInfo['quantity'] = []
    clientInfo['total'] = 0
    clientInfo['Order time'] = ""
    clientInfo['status'] = "Not paid"

    return


# =============================Main
# Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# Receive data from server
receiveData()
# Create root
root = init()
# Init clientInfo
initClientInfo()

signInPage(root)


root.mainloop()
