import tkinter as tk
from tkinter.constants import *
from tkinter import *
from tkinter import messagebox
import os
from typing import Container
from PIL import ImageTk, Image

LARGE_FONT = ("Verdana", 12)


class BasePage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.geometry("600x500")

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SignInPage, ViewMenuPage, StartPage, OrderPage, ChargeCardPayment, PaymentPage, ExitPage):

            frame = F(container, self, bg='#9FD996')

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SignInPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        # os.system("pause")

    def SignIn(self, curFrame):
        try:
            nickname = curFrame.entry_user.get()

            if nickname == "":
                curFrame.label_notice['text'] = "Name can not be empty"
                print("Hi")
                return
            else:
                self.show_frame(StartPage)
        except:
            print("error")


class SignInPage(tk.Frame):
    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)

        label_title = tk.Label(
            self, text="Welcome to Ruki Food Store", bg="#9FD996", font=("Roman", 30))
        label_user = tk.Label(
            self, text="Please enter your name", bg="#9FD996", font=("Roman", 22))
        self.label_notice = tk.Label(
            self, text="", bg="#9FD996", font=("Verdana", 12), fg='#ff0000')

        self.entry_user = tk.Entry(
            self, width=25, font=32, text="", bg="light cyan")

        # Button
        button_go = tk.Button(
            self, text="GO", command=lambda: controller.SignIn(self))
        button_go.config(width=10, bg="green")

        label_title.place(relx=0.5, rely=0.3, anchor=CENTER)
        label_user.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.entry_user.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.label_notice.place(relx=0.5, rely=0.63, anchor=CENTER)
        button_go.place(relx=0.5, rely=0.7, anchor=CENTER)


class StartPage(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)

        # Label
        name = tk.Label(self, text="Ruki Food Store",
                        bg="#9FD996", font=("Roman", 32))
        name.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Button
        # View menu button
        view_menu_button = tk.Button(
            self,
            command=lambda: controller.show_frame(ViewMenuPage),
            height=2,
            width=10,
            font=22,
            text="View menu",
            bg="#ff9933",
            fg="white"
        )
        view_menu_button.place(relx=0.5, rely=0.35, anchor=CENTER)

        # Order button
        order_button = tk.Button(
            self,
            command=lambda: controller.show_frame(OrderPage),
            height=2,
            width=10,
            font=22,
            text="Order",
            bg="#808080",
            fg="white"
        )
        order_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        # Payment button
        payment_button = tk.Button(
            self,
            command=lambda: controller.show_frame(PaymentPage),
            height=2,
            width=10,
            font=22,
            text="Payment",
            bg="#0080FF",
            fg="white"
        )
        payment_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        # Exit button
        exit_button = tk.Button(
            self,
            command=exit_program,
            height=2,
            width=10,
            font=22,
            text="Exit",
            bg="#FF6666",
            fg="white"
        )
        exit_button.place(relx=0.5, rely=0.8, anchor=CENTER)


class CheckFood(tk.Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        tk.Frame.__init__(self, parent)
        self.vars = []

        # label
        label = tk.Label(self, text="List Foods",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for row, pick in enumerate(picks):
            var = IntVar()
            chk = Checkbutton(self, bg='#FFFFFF',
                              anchor="w",
                              height=2,
                              width=15,
                              text=pick, variable=var)
            chk.pack(side="top", fill='y', anchor="w")
            # chk.place(x=100, y=0+x)
            self.vars.append(var)
            # x += 50

    def state(self):
        return map((lambda var: var.get()), self.vars)


class CheckQuantity(tk.Frame):
    def __init__(self, parent=None, num=0, side=LEFT, anchor=W):
        tk.Frame.__init__(self, parent)
        self.vars = []

        # label
        label = tk.Label(self, text="Quantity",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for _ in range(num):
            var = StringVar(value=0)
            spin_box = tk.Spinbox(self,
                                  from_=0,
                                  to=999,
                                  bd=2,
                                  bg="#FFFFFF",
                                  textvariable=var,
                                  wrap=True
                                  )
            spin_box.pack(side="top", fill='y', padx=0, pady=10)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class PrintFood(tk.Frame):
    def __init__(self, parent=None, picks=[], side=LEFT):
        tk.Frame.__init__(self, parent)

        # label
        label = tk.Label(self, text="List Foods",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for pick in picks:
            chk = Label(self, bg='#FFFFFF',
                        width=15,
                        height=2,
                        text=pick)
            chk.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)


class PrintPrice(tk.Frame):
    def __init__(self, parent=None, picks=[], prices=[], side=LEFT):
        tk.Frame.__init__(self, parent)

        # label
        label = tk.Label(self, text="Price",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for price in prices:
            chk = Label(self, bg='#FFFFFF',
                        width=15,
                        height=2,
                        text=price)
            chk.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)


class AddShowImageButton(tk.Frame):
    def __init__(self, parent=None, num=0, side=LEFT, anchor=W):
        tk.Frame.__init__(self, parent)
        self.vars = []

        # label
        label = tk.Label(self, text="Show image",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for _ in range(num):
            var = IntVar()
            button = Button(self,
                            # height=1,
                            text='+',
                            command=open,
                            bd=1,
                            bg="#FFFFFF"
                            )
            button.pack(side="top", fill='y', padx=0, pady=8)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class ViewMenuPage(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)

        # label
        label = tk.Label(self, text="MENU OF THE DAY",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Internal Frame
        internal_frame = Frame(self, bg="#FFFFFF", width=300, height=200)
        internal_frame.place(relx=0.22, rely=0.3)

        # Food frame
        food_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
        food_frame.grid(row=0, column=1)
        # Create list to choice
        self.lst_food = ['Com Suon', 'Banh Canh', 'Hu Tieu', 'Coca', 'Pepsi']
        self.lst_price = ['30', '30', '25', '10', '8']
        print_food = PrintFood(food_frame, self.lst_food)
        print_food.pack(padx=0, pady=0)

        # Price Frame
        price_frame = Frame(internal_frame, bg="#FFFFFF",
                            width=300, height=200)
        price_frame.grid(row=0, column=2)
        price = PrintPrice(price_frame, picks=self.lst_food,
                           prices=self.lst_price)
        price.pack(padx=0, pady=0)

        # Show image frame
        show_image_frame = Frame(
            internal_frame, bg="#FFFFFF", width=300, height=200)
        show_image_frame.grid(row=0, column=3)
        image = AddShowImageButton(show_image_frame, len(self.lst_food))
        image.pack(padx=0, pady=0)

        # Back home button
        back_button = tk.Button(
            self,
            command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)


# Order page
class ExitPage(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)

        # label
        label = tk.Label(self, text="Exit Page",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.2, anchor=CENTER)


class OrderPage(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)
        # label
        label = tk.Label(self, text="Order Page",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.15, anchor=CENTER)

        # Back home button
        back_button = tk.Button(
            self,
            command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)

        # Internal Frame
        internal_frame = Frame(self, bg="#FFFFFF", width=300, height=200)
        internal_frame.place(relx=0.18, rely=0.25)

        # Food frame
        food_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
        food_frame.grid(row=0, column=1)
        # Create list to choice
        self.lst_food = ['Com Suon', 'Banh Canh', 'Hu Tieu', 'Coca', 'Pepsi']
        self.lst_price = ['30', '30', '25', '10', '8']
        order = CheckFood(food_frame, self.lst_food)
        order.pack(padx=0, pady=0)

        # Price Frame
        price_frame = Frame(internal_frame, bg="#FFFFFF",
                            width=300, height=200)
        price_frame.grid(row=0, column=2)
        price = PrintPrice(price_frame, picks=self.lst_food,
                           prices=self.lst_price)
        price.pack(padx=0, pady=0)

        # Quantity Frame
        quantity_frame = Frame(internal_frame, bg="#FFFFFF",
                               width=300, height=200)
        quantity_frame.grid(row=0, column=3)
        quantity = CheckQuantity(quantity_frame, len(self.lst_food))
        quantity.pack(padx=0, pady=0)

        # Submit button
        back_button = tk.Button(
            self,
            # command=lambda: controller.show_frame(StartPage),
            command=lambda: self.DataProcessing(order.vars, quantity.vars),
            height=2,
            width=10,
            text="Add to cart",
            bg="#0080FF",
            fg="white"
        )
        back_button.place(relx=0.5, rely=0.8, anchor=CENTER)

    def DataProcessing(self, order, quantity):
        print("Order")
        for i in range(len(order)):
            if order[i].get() == 1:
                print(self.lst_food[i], ":", quantity[i].get())


# Payment Page
class ChargeCardPayment(tk.Frame):
    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)
        self.account_numbers = 0

        # label
        label = tk.Label(self, text="Enter your account numbers: ",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Account numbers
        account_numbers = Entry(self,
                                # height=1,
                                width=25,
                                font=32,
                                bg="light cyan")
        account_numbers.place(relx=0.5, rely=0.45, anchor=CENTER)

        # Submit button
        back_button = tk.Button(
            self,
            command=lambda: self.handleAccountNumber(controller,
                                                     account_numbers.get(), ),
            height=1,
            width=10,
            font=26,
            text="OK",
            bg="#0080FF",
            fg="white"
        )
        back_button.place(relx=0.5, rely=0.55, anchor=CENTER)

        # Back home button
        back_button = tk.Button(
            self,
            command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)

    def state(self):
        return map((lambda var: var.get()), self.vars)

    def handleAccountNumber(self, controller, account_numbers):
        account_numbers = account_numbers.strip(" ")

        # # Length checking
        # if len(account_numbers) != 10:
        #     return False

        # # Char checking
        # for char in account_numbers:
        #     try:
        #         int(char)
        #     except:
        #         return False

        print("Your account numbers:", account_numbers)
        print("Charge Cart Payment Successed")
        messagebox.showinfo("Payment", "Payment Successed")
        controller.show_frame(StartPage)


class PrintOrderedFood(tk.Frame):
    def __init__(self, parent=None, foods=[], quantity=[], side=LEFT):
        tk.Frame.__init__(self, parent)

        # Ordered
        ordered_label = tk.Label(self, text="Food",
                                 bg="#FFFFFF")
        ordered_label.pack(side="top", fill='both', anchor="w")

        for food in foods:
            food_label = Label(self, bg='#FFFFFF',
                               width=15,
                               height=2,
                               text=food)
            food_label.pack(side="top", fill='y', anchor="w", padx=0, pady=1.5)


class PrintOrderedQuantity(tk.Frame):
    def __init__(self, parent=None, foods=[], quantity=[], side=LEFT):
        tk.Frame.__init__(self, parent)

        # Quantity
        quantity_label = tk.Label(self, text="Quantity",
                                  bg="#FFFFFF")
        quantity_label.pack(side="top", fill='both', anchor="w")

        for num in quantity:
            quantity_label = Label(self, bg='#FFFFFF',
                                   width=15,
                                   height=2,
                                   text=num)
            quantity_label.pack(side="top", fill='y',
                                anchor="w", padx=0, pady=1.5)


class PrintAmount(tk.Frame):
    def __init__(self, parent=None, foods=[], quantity=[], side=LEFT):
        tk.Frame.__init__(self, parent)

        # Quantity
        quantity_label = tk.Label(self, text="Amount",
                                  bg="#FFFFFF")
        quantity_label.pack(side="top", fill='both', anchor="w")

        for num in quantity:
            text = int(num)*10
            quantity_label = Label(self, bg='#FFFFFF',
                                   width=15,
                                   height=2,
                                   text=text)
            quantity_label.pack(side="top", fill='y',
                                anchor="w", padx=0, pady=1.5)


class PaymentPage(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)
        # label
        label = tk.Label(self, text="Payment Page",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.15, anchor=CENTER)

        # label
        title_label = tk.Label(self, text="Ordered",
                               bg="#9FD996", font=("Roman", 22))
        title_label.place(relx=0.5, rely=0.25, anchor=CENTER)

        # Internal Frame
        internal_frame = Frame(self, bg="#FFFFFF", width=300, height=200)
        internal_frame.place(relx=0.13, rely=0.3)

        # Create list to choice
        self.food_ordered = ['Com Suon',
                             'Banh Canh', 'Hu Tieu', 'Coca', 'Pepsi']
        self.quantity = ['2', '3', '2', '1', '8']
        self.prices = ['30', '30', '25', '10', '8']

        # Ordered food frame
        food_ordered_frame = Frame(
            internal_frame, bg="#FFFFFF", width=300, height=200)
        food_ordered_frame.grid(row=0, column=0)

        print_food_ordered = PrintOrderedFood(food_ordered_frame,
                                              foods=self.food_ordered, quantity=self.quantity)
        print_food_ordered.pack(padx=0, pady=0)

        # Price frame
        price_frame = Frame(
            internal_frame, bg="#FFFFFF", width=300, height=200)
        price_frame.grid(row=0, column=1)

        print_price = PrintPrice(price_frame, prices=self.prices)
        print_price.pack(padx=0, pady=0)

        # Ordered quantity frame
        quantity_ordered_frame = Frame(
            internal_frame, bg="#FFFFFF", width=300, height=200)
        quantity_ordered_frame.grid(row=0, column=2)

        print_quantity_ordered = PrintOrderedQuantity(quantity_ordered_frame,
                                                      foods=self.food_ordered, quantity=self.quantity)
        print_quantity_ordered.pack(padx=0, pady=0)

        # Amount frame
        amount_frame = Frame(
            internal_frame, bg="#FFFFFF", width=300, height=200)
        amount_frame.grid(row=0, column=3)

        amount = PrintAmount(amount_frame,
                             foods=self.food_ordered, quantity=self.quantity)
        amount.pack(padx=0, pady=0)

        # Total frame
        # total_frame = Frame(
        #     internal_frame, bg="#FFFFFF", width=300, height=200)
        # total_frame.grid(row=0, column=0)
        total = 100
        text = f"------------------------------------------------------------------------\nTotal:  \t\t{total}"
        print_total = Label(self, bg='#FFFFFF',
                            width=63,
                            height=2,
                            text=text)
        print_total.place(relx=0.501, rely=0.75, anchor=CENTER)

        # Back home button
        back_button = tk.Button(
            self,
            command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)

        # Cash payment button
        pay_up_button = tk.Button(
            self,
            command=lambda: self.handleCashPayment(),
            height=3,
            width=20,
            text="Cash payment",
            bg="#0080FF",
            fg="white"
        )
        pay_up_button.place(relx=0.34, rely=0.9, anchor=CENTER)

        # Charge Card Payment
        pay_up_button = tk.Button(
            self,
            command=lambda: controller.show_frame(ChargeCardPayment),
            height=3,
            width=20,
            text="Charge Card Payment",
            bg="#FF9933",
            fg="white"
        )
        pay_up_button.place(relx=0.65, rely=0.9, anchor=CENTER)

    def handleCashPayment(self):
        print("Cash Payment Successed")
        return


def exit_program():
    os.sys.exit()


def open():
    global my_img
    top = Toplevel()
    top.title('My Second Window')

    img = Image.open('camcui.jpg')
    img = img.resize((450, 350))
    # Resize image
    #my_img = my_img.resize((600, 350))
    my_img = ImageTk.PhotoImage(img)
    my_label = Label(top, image=my_img).pack()
    btn2 = Button(top, text="close window", command=top.destroy).pack()

# Exit page


class ExitPage(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)

        # label
        label = tk.Label(self, text="Exit Page",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Back home button
        back_button = tk.Button(
            self,
            # command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)


app = BasePage()
app.mainloop()
