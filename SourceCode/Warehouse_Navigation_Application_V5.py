"""
// Filename: WareHouse Navigation Application
// Author: HaoYu Tseng, Zipeng Yuan, Yuxuan Zhang
// Discription: This application is designed for worker in the WareHouse.
// Help them to collect products in an efficient way!
//
// History:
// Version  Date        Detail
// 2.0      05/07/23    Warehouse visualization, Product management, Setting option (start/end position,
//                      multiple product look up methods)
// 2.1      05/09/23    Path finding algorithm for single item
// 3.0      05/20/23    Reduce matrix Calculation
// 3.1      05/21/23    Branch and Bound algorthm (single access point only), Held-karp algorithm (single access point only)
// 3.2      05/22/23    Time out & Return feature, More robust error handling 
// 4.0      05/28/23    Nearest neighbor algorithm (multiple access points) 
// 4.1      05/29/23    Held-karp algorithm (multiple access points) 
// 4.2      05/30/23    Order list file support 
// 4.3      05/31/23    Branch and Bound algorithm (multiple access points)
// 5.0      06/03/23    Branch and Bound algorithm (random starting points)
// 5.1      06/04/23    Manually set timeout
// 5.2      06/05/23    Held-karp algorithm tested
// 5.3      06/10/23    Testcases. Support different start and end points again
"""

import copy
import heapq
import math
from collections import deque
import time
import tkinter as tk
from tkinter import filedialog
import numpy as np
import random

class Node:
    # TotalCost: TotalCost to reach Position
    # Route: the Route from the root to the Position
    # Position: where the position it is at
    # Children: Other Nodes it can reach
    # Products: All the product that has Gathered
    def __init__(self, TotalCost, Route, Position, Children, reduceMatrix, Products):
        self.TotalCost = TotalCost
        self.Route = Route
        self.Position = Position
        self.Children = Children
        self.reduceMatrix = reduceMatrix
        self.Products = Products

    # Comparator
    def __lt__(self, other):
        return self.TotalCost < other.TotalCost


class configuration:
    # constructor for initialization
    def __init__(self):
        self.__rows = 5
        self.__cols = 5
        self.__worker_pos_start = [1, 1]
        self.__worker_pos_end = [1, 1]
        self.__shelf_pos = [[0, 2]]
        self.__prod_pos = [[8, 16]]# [[8, 16], [4, 16], [14, 20], [14, 8], [6, 6], [6, 10], [8, 8], [6, 8], [14, 6], [8, 14], [10, 12], [0, 2], [8, 11]]
        self.__map = {}
        self.__algorithm = 2
        self.__debug = 0
        self.__orderlist = []   # Initial order list (for file input)
        self.__timeout = 60

    # getter and setter functions for those private variables
    def get_rows(self):
        return self.__rows

    def set_rows(self, value):
        self.__rows = value

    def get_cols(self):
        return self.__cols

    def set_cols(self, value):
        self.__cols = value

    def get_worker_pos_start(self):
        return self.__worker_pos_start

    def set_worker_pos_start(self, value):
        self.__worker_pos_start = value

    def get_worker_pos_end(self):
        return self.__worker_pos_end

    def set_worker_pos_end(self, value):
        self.__worker_pos_end = value

    def get_shelf_pos(self):
        return self.__shelf_pos

    def set_shelf_pos(self, value):
        self.__shelf_pos = value

    def get_prod_pos(self):
        return self.__prod_pos

    def set_prod_pos(self, value):
        self.__prod_pos = value

    def append_prod_pos(self, value):
        self.__prod_pos.append(value)

    def get_map(self):
        return self.__map

    def set_map(self, value):
        self.__map = value

    def get_algorithm(self):
        return self.__algorithm

    def set_algorithm(self, value):
        self.__algorithm = value

    def get_orderlist(self,):
        return self.__orderlist

    def set_orderlist(self, value):
        self.__orderlist = value

    def get_debug(self):
        return self.__debug

    def set_debug(self, value):
        self.__debug = value

    def get_timeout(self):
        return self.__timeout

    def set_timeout(self, value):
        self.__timeout = value


def main():
    # some random config
    config = configuration()
    while 1:
        # print the menu messages
        print("Welcome to WareHouse Navigation Application")
        print("Menu:")
        print("1) Load Product Info")
        print("2) Load Order list") 
        print("3) Go Get Products")
        print("4) Settings")
        print("5) Exit")
        # print current settings as extra info of debug mode
        if config.get_debug() == 1:
            print("Current settings:")
            print("Map rows: " + str(config.get_rows()))
            print("Map columns: " + str(config.get_cols()))
            print("Worker position: " + str(config.get_worker_pos_start()))
            print("Worker end position: " + str(config.get_worker_pos_end()))
            print("Target product position: " + str(config.get_prod_pos()))
            print("Algorithm: " + str(config.get_algorithm()))
            print("Timeout setting (in seconds): " + str(config.get_timeout()))
        option = input("Enter your choice: ")
        # choose the next step
        if option == '1':
            config = load_data(config)
        elif option == '2':
            config = load_orderlist(config)
        elif option == '3':
            start_program(config)
        elif option == '4':
            config = setting(config)
        elif option == '5':
            print("Done. Have a nice day.\n")
            exit()
        else:
            print("Please choose from 1 to 5!")


def load_data(config):
    # reads txt
    # Create the Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to choose a file using a file dialog
    file_path = filedialog.askopenfilename()
    
    try:
        with open(file_path, 'r') as file:  # read the file by lines
            lines = file.readlines()
    except FileNotFoundError:
        print("No such file, try again.")
    id = {}
    x = []
    y = []
    d = {}
    try:
        for i in lines[1:]:  # split the lines, ignoring the first line and make them into arrays for configuration and plot
            item = int(i.split("\t")[0])
            a = math.floor(float(i.split("\t")[1]))
            b = int((i.split("\t")[2])[:-1])
            x.append(a)
            y.append(b)
            id[item] = [b, a]
            try:
                d[(b, a)] += 1
            except KeyError:
                d[(b, a)] = 1
    except:
        print("Input file format error!")
        return config
    config.set_shelf_pos(list(d.keys()))  # configure those info which we can get from txt file
    config.set_rows(max(y) + 1)
    config.set_cols(max(x) + 1)
    config.set_map(id)
    rows = config.get_rows()
    cols = config.get_cols()
    worker_pos_start = config.get_worker_pos_start()
    worker_pos_end = config.get_worker_pos_end()
    shelf_pos = config.get_shelf_pos()
    print("File analysis finished.")
    print("There are " + str(len(x)) + " products in the warehouse located on " + str(len(d.keys())) + " shelves.")
    print("Warehouse shelf dimension is " + str(rows) + " x " + str(cols) + ".\n")
    print("Change the map size in settings if the actual warehouse size doesn't match the shelf dimension.")
    print("A plot of the warehouse is shown below.")
    # print the warehouse map with shelves and worker
    if rows < 10:  # arrange the x ticks
        r1 = "  "
    else:
        r1 = "   "
    if cols < 10:
        for i in range(cols):
            r1 += str(i) + " "
    else:
        for i in range(9):
            r1 += str(i) + "  "
        for i in range(9, cols):
            r1 += str(i) + " "

    lot = [[" " for j in range(cols)] for i in range(rows)]
    for i in shelf_pos:  # set shelves
        lot[i[0]][i[1]] = "□"
    if worker_pos_start == worker_pos_end:  # set worker position(s)
        lot[worker_pos_start[0]][worker_pos_start[1]] = "W"
    else:
        lot[worker_pos_start[0]][worker_pos_start[1]] = "S"
        lot[worker_pos_end[0]][worker_pos_end[1]] = "E"
    if cols < 10:  # arrange the y ticks
        for i in range(rows - 1, -1, -1):
            if rows > 9:
                print(str(i) + " " + "  ".join(lot[i]))
            else:
                print(str(i) + " " + " ".join(lot[i]))
    else:
        for i in range(rows - 1, 9, -1):
            if rows > 9:
                print(str(i) + " " + "  ".join(lot[i]))
            else:
                print(str(i) + " " + " ".join(lot[i]))
        for i in range(9, -1, -1):
            if rows > 9:
                print(" " + str(i) + " " + "  ".join(lot[i]))
            else:
                print(" " + str(i) + " " + " ".join(lot[i]))
    print(r1)
    return config

# Load order list from txt w/ pop out screen
def load_orderlist(config):

    # Create the Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to choose a file using a file dialog
    file_path = filedialog.askopenfilename()


    try:
    # Open the selected file in read mode
        with open(file_path, 'r') as file:
            # Read the contents of the file and split it by lines
            file_content = file.read().splitlines()
    except FileNotFoundError:
        print("No such file, try again.")

    split_content = []
    try:
        for line in file_content:
            numbers = line.split(",")
            numbers = [int(num.strip()) for num in numbers]
            split_content.append(numbers)

        config.set_orderlist(split_content)
    except:
        print("Input file format error!")

    return config

def setting(config):
    # select detailed setting
    def setting_map(config):
        # ask for user input
        while 1:  # set row
            rows = input("Enter the rows of map: ")
            try:
                rows = int(rows)
            except ValueError:
                print("Invalid input. Please type an integer!")
                continue
            if rows > 0:
                config.set_rows(rows)
                break
            else:
                print("Invalid input. Please type a positive integer!")
                continue
        while 1:  # set column
            cols = input("Enter the columns of map: ")
            try:
                cols = int(cols)
            except ValueError:
                print("Invalid input. Please type an integer!")
                continue
            if cols > 0:
                config.set_cols(cols)
                break
            else:
                print("Invalid input. Please type a positive integer!")
                continue
        print("Your map size is set to " + str(config.get_rows()) + " x " + str(config.get_cols()) + ".\n")
        return config

    def setting_worker(config):
        # ask for user input
        print("Set starting position.")
        while 1:
            while 1:  # set row
                rows = input("Enter the row of worker's starting position: ")
                try:
                    rows = int(rows)
                except ValueError:
                    print("Invalid input. Please type an integer!")
                    continue
                if rows >= 0:
                    break
                else:
                    print("Invalid input. Please type a non-negative integer!")
                    continue
            while 1:  # set column
                cols = input("Enter the column of worker's starting position: ")
                try:
                    cols = int(cols)
                except ValueError:
                    print("Invalid input. Please type an integer!")
                    continue
                if cols >= 0:
                    break
                else:
                    print("Invalid input. Please type a non-negative integer!")
                    continue
            if (rows, cols) in config.get_shelf_pos():
                print("Don't try to stand on shelves. Enter another position.")
            else:
                config.set_worker_pos_start([rows, cols])
                break
        while 1:  # quick set if start and end pos are the same
            check = input("End position same as start position? (y/n) ")
            if check == "y" or check == "Y":
                config.set_worker_pos_end(config.get_worker_pos_start())
                print("\n")
                return
            elif check == "n" or check == "N":
                break
            else:
                print("Please answer yes(y) or no(n)")
                continue
        print("Set end position.")
        while 1:
            while 1:  # set row
                rows = input("Enter the row of worker's end position: ")
                try:
                    rows = int(rows)
                except ValueError:
                    print("Invalid input. Please type an integer!")
                    continue
                if rows >= 0:
                    break
                else:
                    print("Invalid input. Please type a non-negative integer!")
                    continue
            while 1:  # set column
                cols = input("Enter the column of worker's end position: ")
                try:
                    cols = int(cols)
                except ValueError:
                    print("Invalid input. Please type an integer!")
                    continue
                if cols >= 0:
                    break
                else:
                    print("Invalid input. Please type a non-negative integer!")
                    continue
            if (rows, cols) in config.get_shelf_pos():
                print("Don't try to stand on shelves. Enter another position.")
            else:
                config.set_worker_pos_end([rows, cols])
                break
        print("Worker start position set at (" + str((config.get_worker_pos_start())[0]) + ", " + str((config.get_worker_pos_start())[1]) + ").")
        print("Worker end position set at (" + str((config.get_worker_pos_end())[0]) + ", " + str((config.get_worker_pos_end())[1]) + ").")
        return config

    def setting_product(config):
        # ask for user input
        while 1:
            print("Do you want to add to current product list or start a new one?")
            print("1) Add to current list")
            print("2) Start new list")
            choice = input("Enter your choice: ")
            if choice == "1":
                while 1:
                    print("Choose how you would like to locate the product:")
                    print("1) By product ID")
                    print("2) By coordinate")
                    print("3) By Order list")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        while 1:  # search in the ID list which is the keys of map dict
                            print("Enter 'x' to finish adding.")
                            id = input("Please enter the product ID: ")
                            if id == 'x':
                                return config
                            try:
                                id = int(id)
                            except ValueError:
                                print("Invalid input. Please type an integer!")
                                continue
                            if id not in (config.get_map()).keys():
                                print("Product ID not found. Try again.")
                                continue
                            else:
                                pos = config.get_map()[id]
                                if pos not in config.get_prod_pos():
                                    config.append_prod_pos(config.get_map()[id])
                                print("Target product ID " + str(id) + " at " + str(config.get_map()[id]) + " added.")
                    elif choice == "2":
                        while 1:
                            pos = [-1, -1]

                            while 1:  # set row and column and check if it exists
                                rows = input("Enter the row of product: ")
                                try:
                                    rows = int(rows)
                                except ValueError:
                                    print("Invalid input. Please type an integer!")
                                    continue
                                if rows >= 0:
                                    pos[0] = rows
                                    break
                                else:
                                    print("Invalid input. Please type a non-negative integer!")
                                    continue
                            while 1:
                                cols = input("Enter the column of product: ")
                                try:
                                    cols = int(cols)
                                except ValueError:
                                    print("Invalid input. Please type an integer!")
                                    continue
                                if cols >= 0:
                                    pos[1] = cols
                                    break
                                else:
                                    print("Invalid input. Please type a non-negative integer!")
                                    continue
                            if tuple(pos) not in config.get_shelf_pos():
                                print("No such shelf exists. Try again.")
                                continue
                            if pos not in config.get_prod_pos():
                                config.append_prod_pos(pos)
                            print("Target product at " + str(pos) + " added.")
                            choice = input("Type in any key to continue. Type x to finish adding.")
                            if choice == 'x':
                                return config
                    elif choice == '3':
                        while 1:
                            print("Enter 'x' to finish adding.")
                            order_list = config.get_orderlist()
                            #while 1:  # search in the ID list which is the keys of map dict

                            order_num = input("Please enter the order number 1 ~ " + str(len(order_list)) + " (inclusive): ")
                            if order_num == 'x':
                                return config
                            try:
                                order_num = int(order_num)
                            except ValueError:
                                print("Invalid input. Please type an integer!")
                                continue

                            if order_num > len(order_list) or order_num < 1:
                                print("Order number is out of range. Try again.")
                                continue

                            for order in order_list[order_num - 1]:
                                # Check if the ID exist
                                if order not in (config.get_map()).keys():
                                    print("Product ID" + str(order) + "not found. Error in this order!")
                                    # config.set_prod_pos([])  # If the ID doesn't exist, reset the prod_pos
                                    break
                                else:
                                    pos = config.get_map()[order]
                                    if pos not in config.get_prod_pos():
                                        config.append_prod_pos(config.get_map()[order])
                        #return config

                    else:
                        print("Invalid choice. Please try again. \n")
                        continue
            elif choice == '2':
                while 1:
                    print("Choose how you would like to locate the product:")
                    print("1) By product ID")
                    print("2) By coordinate")
                    print("3) By Order list")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        count = 0
                        while 1:  # search in the ID list which is the keys of map dict
                            print("Enter 'x' to finish at any time.")
                            id = input("Please enter the product ID: ")
                            if id == 'x':
                                return config
                            try:
                                id = int(id)
                            except ValueError:
                                print("Invalid input. Please type an integer!")
                                continue
                            if id not in (config.get_map()).keys():
                                print("Product ID not found. Try again.")
                                continue
                            else:
                                pos = config.get_map()[id]
                                if count == 0:
                                    config.set_prod_pos([config.get_map()[id]])
                                    count += 1
                                elif pos not in config.get_prod_pos():
                                    config.append_prod_pos(config.get_map()[id])
                                print("Target product ID " + str(id) + " at " + str(config.get_map()[id]) + " added.")
                    elif choice == "2":
                        count = 0
                        while 1:
                            pos = [-1, -1]
                            while 1:  # set row and column and check if it exists
                                rows = input("Enter the row of product: ")
                                try:
                                    rows = int(rows)
                                except ValueError:
                                    print("Invalid input. Please type an integer!")
                                    continue
                                if rows >= 0:
                                    pos[0] = rows
                                    break
                                else:
                                    print("Invalid input. Please type a non-negative integer!")
                                    continue
                            while 1:
                                cols = input("Enter the column of product: ")
                                try:
                                    cols = int(cols)
                                except ValueError:
                                    print("Invalid input. Please type an integer!")
                                    continue
                                if cols >= 0:
                                    pos[1] = cols
                                    break
                                else:
                                    print("Invalid input. Please type a non-negative integer!")
                                    continue
                            if tuple(pos) not in config.get_shelf_pos():
                                print("No such shelf exists. Try again.")
                                continue
                            if count == 0:
                                config.set_prod_pos([pos])
                                count += 1
                            if pos not in config.get_prod_pos():
                                config.append_prod_pos(pos)
                            print("Target product at " + str(pos) + " added.")
                            choice = input("Type in any key to continue. Type x to finish adding.")
                            if choice == 'x':
                                return config
                            
                    elif choice == "3":
                        order_list = config.get_orderlist()
                        count = 0
                        while 1:  # search in the ID list which is the keys of map dict
                            order_num = input("Please enter the order number 1 ~ " + str(len(order_list))+ " (inclusive): " )
                            try:
                                order_num = int(order_num)
                            except ValueError:
                                print("Invalid input. Please type an integer!")
                                continue

                            if order_num <= len(order_list) or order_num >= 1:
                                break
                            else:
                                print("Order number is out of range. Try again.")
                                continue

                        for order in order_list[order_num - 1]:
                            # Check if the ID exist
                            if order not in (config.get_map()).keys():
                                print("Product ID"+ str(order)+ "not found. Error in this order!")
                                config.set_prod_pos([]) # If the ID doesn't exist, reset the prod_pos
                                break
                            else:
                                pos = config.get_map()[order]
                                if count == 0:
                                    config.set_prod_pos([config.get_map()[order]])
                                    count += 1
                                elif pos not in config.get_prod_pos():
                                    config.append_prod_pos(config.get_map()[order])
                        return config
                           
                    else:
                        print("Invalid choice. Please try again. \n")

            else:
                print("Invalid choice. Please try again. \n")
                continue
        return config

    def setting_timeout(config):
        while 1:
            print("Set a timeout for the program.")
            print("Once it doesn't finish in time, it will choose the default input order as product pickup order.")
            choice = input("Enter your desired timeout (in seconds): ")
            try:
                choice = float(choice)
            except ValueError:
                print("Invalid input. Please enter a number!")
                continue
            config.set_timeout(choice)
            return config

    def setting_algorithm(config):
        while 1:
            print("Which algorithm do you want to use?")
            print("1) Branch and bound")
            print("2) Repetitive Nearest Neighbour")
            print("3) Held-Karp")
            choice = input("Enter your choice: ")
            if choice == "1":
                config.set_algorithm(1)
                break
            elif choice == '2':
                config.set_algorithm(2)
                break
            elif choice == '3':
                config.set_algorithm(3)
            else:
                print("Invalid input. Try again.")
        return config

    def setting_debug(config):
        # ask for user input
        while 1:  # simple ON and OFF flag switch
            d = input("Enable debug mode?(Y/N) ")
            if d == "y" or d == "Y":
                config.set_debug(1)
                print("Debug mode ON!")
                return
            elif d == "n" or d == "N":
                config.set_debug(0)
                print("Debug mode OFF!")
                break
            else:
                print("Say yes or no.")
                continue
        return config

    # setting panel message and navigation
    while 1:
        print("Settings panel")
        print("1) Map size setting")
        print("2) Worker position setting")
        print("3) Product position setting")
        print("4) Algorithm setting")
        print("5) Timeout setting")
        print("6) Debug mode setting")
        print("7) Return")
        setting_option = input("Enter your choice: ")
        print("\n")

        if setting_option == "1":
            setting_map(config)
        elif setting_option == "2":
            setting_worker(config)
        elif setting_option == "3":
            setting_product(config)
        elif setting_option == "4":
            setting_algorithm(config)
        elif setting_option == "5":
            setting_timeout(config)
        elif setting_option == "6":
            setting_debug(config)
        elif setting_option == "7":
            print("Return to menu!")
            return config
        else:
            print("Invalid choice. Please try again(Input is between 1 to 7).")


def start_program(config):
    # program starts
    def print_map(config, path, worker_pos):
        # print the warehouse map with shelves and worker
        rows = config.get_rows()
        cols = config.get_cols()
        worker_pos_start = config.get_worker_pos_start()
        worker_pos_end = config.get_worker_pos_end()
        shelf_pos = config.get_shelf_pos()
        prod_pos = config.get_prod_pos()
        # x ticks Come in last in our case
        if rows < 10:
            r1 = "  "
        else:
            r1 = "   "
        if cols < 10:
            for i in range(cols):
                r1 += str(i) + " "
        else:
            for i in range(9):
                r1 += str(i) + "  "
            for i in range(9, cols):
                r1 += str(i) + " "

        lot = [[" " for j in range(cols)] for i in range(rows)]
        # set shelves and product
        for i in shelf_pos:
            lot[i[0]][i[1]] = "□"
        for i in prod_pos:
            lot[i[0]][i[1]] = "■"
        # set path track
        if path != []:
            for i in path:
                lot[i[0]][i[1]] = "-"
        # set worker position
        # should cover the path at start and end points

        if path == []:
            lot[worker_pos_end[0]][worker_pos_end[1]] = "E"
            lot[worker_pos_start[0]][worker_pos_start[1]] = "W"
        else:
            lot[worker_pos[0]][worker_pos[1]] = "W"
        # print the main body of map
        if cols < 10:
            for i in range(rows - 1, -1, -1):
                if rows > 9:
                    print(str(i) + " " + "  ".join(lot[i]))
                else:
                    print(str(i) + " " + " ".join(lot[i]))
        else:
            for i in range(rows - 1, 9, -1):
                if rows > 9:
                    print(str(i) + " " + "  ".join(lot[i]))
                else:
                    print(str(i) + " " + " ".join(lot[i]))
            for i in range(9, -1, -1):
                if rows > 9:
                    print(" " + str(i) + " " + "  ".join(lot[i]))
                else:
                    print(" " + str(i) + " " + " ".join(lot[i]))
        print(r1)

    def shortest_route(config, start, end):
        rows = config.get_rows()
        cols = config.get_cols()

        if start == end:
            return []

        # Perform BFS
        queue = deque([(start, [])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            x, y = current

            if current == end:
                return path + [current]

            if current in visited:
                continue

            visited.add(current)
            # all possible direction
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

            for nx, ny in neighbors:
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in config.get_shelf_pos():
                    queue.append(((nx, ny), path + [current]))
        # if no valid path found
        return None

    def valid_ap(config, pos):
        rows = config.get_rows()
        cols = config.get_cols()
        shelf_pos = config.get_shelf_pos()
        if pos[0] >= 0 and pos[0] < rows and pos[1] >= 0 and pos[1] < cols and pos not in shelf_pos:
            return True
        return False

    def distance_matrix(config):
        start_pos = config.get_worker_pos_start()
        end_pos = config.get_worker_pos_end()
        prod_pos = config.get_prod_pos()
        m = [[np.inf for _ in range(len(prod_pos) * 4 + 2)] for _ in range(len(prod_pos) * 4 + 2)]

        for index, i in enumerate(prod_pos):
            ap = [(i[0] + 1, i[1]), (i[0], i[1] + 1), (i[0] - 1, i[1]), (i[0], i[1] - 1)]
            for index2, j in enumerate(ap):
                if valid_ap(config, j):
                    ls = len(shortest_route(config, tuple(start_pos), tuple(j)))
                    le = len(shortest_route(config, tuple(end_pos), tuple(j)))
                    if ls == 0:
                        m[0][index * 4 + index2 + 1] = 0
                        m[index * 4 + index2 + 1][0] = 0
                    else:
                        m[0][index * 4 + index2 + 1] = ls - 1
                        m[index * 4 + index2 + 1][0] = ls - 1
                    if le == 0:
                        m[len(m) - 1][index * 4 + index2 + 1] = 0
                        m[index * 4 + index2 + 1][len(m) - 1] = 0
                    else:
                        m[len(m) - 1][index * 4 + index2 + 1] = le - 1
                        m[index * 4 + index2 + 1][len(m) - 1] = le - 1
        m[0][len(m) - 1] = 0
        m[len(m) - 1][0] = 0

        for i in range(len(prod_pos)):
            for j in range(i + 1, len(prod_pos)):
                ap = [(prod_pos[i][0] + 1, prod_pos[i][1]), (prod_pos[i][0], prod_pos[i][1] + 1),
                      (prod_pos[i][0] - 1, prod_pos[i][1]), (prod_pos[i][0], prod_pos[i][1] - 1)]
                ap2 = [(prod_pos[j][0] + 1, prod_pos[j][1]), (prod_pos[j][0], prod_pos[j][1] + 1),
                       (prod_pos[j][0] - 1, prod_pos[j][1]), (prod_pos[j][0], prod_pos[j][1] - 1)]
                for x in range(4):
                    for y in range(4):
                        if valid_ap(config, ap[x]) and valid_ap(config, ap2[y]):
                            l = len(shortest_route(config, ap[x], ap2[y]))
                            if l == 0:
                                m[i * 4 + x + 1][j * 4 + y + 1] = 0
                                m[j * 4 + y + 1][i * 4 + x + 1] = 0
                            else:
                                m[i * 4 + x + 1][j * 4 + y + 1] = l - 1
                                m[j * 4 + y + 1][i * 4 + x + 1] = l - 1
        return m

    def sort_path(config, path):

        start_pos = config.get_worker_pos_start()
        end_pos = config.get_worker_pos_end()
        if path[0] == start_pos and path[-1] == end_pos:
            return path
        if start_pos == end_pos:
            while path[0] != start_pos or path[-1] != end_pos:
                t = path.pop(0)
                path.append(t)
        else:
            if path.index(end_pos) > path.index(start_pos):
                path.reverse()
            while path.index(start_pos) != 0 or path.index(end_pos) != len(path) - 1:
                t = path.pop(0)
                path.append(t)
        return path

    def algorithm_branch_and_bound(config, matrix):
        def reduce_matrix(m):
            cost = 0
            for a in range(2):
                v = min(m[0])
                if v != np.inf:
                    for j in range(len(m[0])):
                        m[0][j] -= v
                    # print(v)
                    cost += v
                for i in range(1, len(m) - 1, 4):
                    v = min(min(row) for row in m[i: i + 4])
                    # print(v)
                    if v != np.inf:
                        for j in range(len(m)):
                            m[i][j] -= v
                            m[i + 1][j] -= v
                            m[i + 2][j] -= v
                            m[i + 3][j] -= v
                        cost += v
                v = min(m[len(m) - 1])
                if v != np.inf:
                    for j in range(len(m[len(m) - 1])):
                        m[len(m) - 1][j] -= v
                    # print(v)
                    cost += v
                m = [list(row) for row in zip(*m)]

            return m, cost

        def node_matrix(matrix, a, b):
            c = matrix[a][b]
            if a == 0 or a == len(matrix) - 1:
                for i in range(len(matrix)):
                    matrix[a][i] = np.inf
            else:
                ind = (a - 1) // 4
                for i in range(len(matrix)):
                    matrix[ind * 4 + 1][i] = np.inf
                    matrix[ind * 4 + 2][i] = np.inf
                    matrix[ind * 4 + 3][i] = np.inf
                    matrix[ind * 4 + 4][i] = np.inf
            if b == 0 or b == len(matrix) - 1:
                for i in range(len(matrix)):
                    matrix[i][b] = np.inf
            else:
                ind = (b - 1) // 4
                for i in range(len(matrix)):
                    matrix[i][ind * 4 + 1] = np.inf
                    matrix[i][ind * 4 + 2] = np.inf
                    matrix[i][ind * 4 + 3] = np.inf
                    matrix[i][ind * 4 + 4] = np.inf

            retm, cost = reduce_matrix(matrix)

            return matrix, cost + c

        #  start is going to be a random start position, randomly chosen from -1 to numberOfProducts, -1 denotes the start position,
        #  numberOfProducts denotes the destination position, (0,numberOfProducts-1) denotes the randomly chosen product to get First
        def Prunning(start, adjList, numberOfProducts, matrix, initial_cost):
            # if the start position is -1 or numberOfProducts, this means that the random start point is start or end
            if start == -1:
                root = Node(0, [0], 0, adjList[0], copy.deepcopy(matrix), [])
                cost, route, default_flag = PrunningStart(root, adjList, numberOfProducts, initial_cost)
                return route, cost + initial_cost, default_flag

            if start == numberOfProducts:
                root = Node(0, [4 * numberOfProducts + 1], 4 * numberOfProducts + 1,
                            adjList[4 * numberOfProducts + 1], copy.deepcopy(matrix), [])
                cost, route, default_flag = PrunningStart(root, adjList, numberOfProducts, initial_cost)
                return route, cost + initial_cost, default_flag

            root1 = Node(0, [4 * start + 1], 4 * start + 1, adjList[4 * start + 1], copy.deepcopy(matrix),
                         [start])
            cost1, route1, default_flag1 = PrunningStart(root1, adjList, numberOfProducts, initial_cost)
            root2 = Node(0, [4 * start + 2], 4 * start + 2, adjList[4 * start + 2], copy.deepcopy(matrix),
                         [start])
            cost2, route2, default_flag2 = PrunningStart(root2, adjList, numberOfProducts, initial_cost)
            root3 = Node(0, [4 * start + 3], 4 * start + 3, adjList[4 * start + 3], copy.deepcopy(matrix),
                         [start])
            cost3, route3, default_flag3 = PrunningStart(root3, adjList, numberOfProducts, initial_cost)
            root4 = Node(0, [4 * start + 4], 4 * start + 4, adjList[4 * start + 4], copy.deepcopy(matrix),
                         [start])
            cost4, route4, default_flag4 = PrunningStart(root4, adjList, numberOfProducts, initial_cost)
            default = default_flag1 and default_flag2 and default_flag3 and default_flag4
            minimum = min(cost1, cost2, cost3, cost4)
            if minimum == cost1:
                return route1, cost1 + initial_cost, default
            if minimum == cost2:
                return route2, cost2 + initial_cost, default
            if minimum == cost3:
                return route3, cost3 + initial_cost, default
            if minimum == cost4:
                return route4, cost4 + initial_cost, default

        def PrunningStart(root, adjList, numberOfProducts, initial_cost):
            heap = []
            heapq.heappush(heap, root)
            # store the results
            heapForResult = []
            start = root.Position
            while len(heap) > 0:
                time_now = time.time()
                time_elapsed = time_now - time_start
                prod_pos = config.get_prod_pos()
                if time_elapsed >= config.get_timeout():
                    dp = [0]
                    cost = 0
                    for i in range(len(prod_pos)):
                        for x in range(4):
                            ind = i * 4 + x + 1
                            if min(dmc[ind]) != np.inf:
                                cost += dmc[dp[-1]][ind]
                                dp.append(ind)
                                break
                    cost += dmc[dp[-1]][len(dmc) - 1]
                    cost += dmc[len(dmc) - 1][0]
                    dp.append(len(dmc) - 1)
                    dp.append(0)
                    return cost - initial_cost, dp, True

                tmp = heapq.heappop(heap)
                childlist = adjList.get(tmp.Position)
                route = tmp.Route
                Products = tmp.Products
                # if we have gathered all the products, we shall return to the start point
                if len(route) == numberOfProducts + 2:
                    newmatrix, cost = node_matrix(tmp.reduceMatrix, tmp.Position, start)
                    route.append(start)
                    newcost = cost + tmp.TotalCost
                    last = Node(newcost, route, start, adjList[start], newmatrix, Products)
                    heapq.heappush(heapForResult, last)
                    continue

                # if there are any product left, we shall go get the products
                for pos in childlist:
                    correspondingProduct = (pos - 1) // 4
                    if correspondingProduct not in Products:
                        # compute new totalcost and reduceMatrix from the calculation function
                        # add the new one into the heap
                        matrixToBeChanged = copy.deepcopy(tmp.reduceMatrix)
                        newReduceMatrix, newTotalCost = node_matrix(matrixToBeChanged, tmp.Position, pos)
                        newTotalCost += tmp.TotalCost
                        newroute = []
                        newroute.extend(route)
                        newroute.append(pos)
                        newProduct = []
                        newProduct.extend(Products)
                        newProduct.append(correspondingProduct)
                        heapq.heappush(heap,
                                       Node(newTotalCost, newroute, pos, adjList.get(pos), newReduceMatrix, newProduct))
            while len(heapForResult) > 0:
                tmp = heapq.heappop(heapForResult)
                route = tmp.Route
                if CheckValidPath(route, 0, numberOfProducts * 4 + 1):
                    return tmp.TotalCost, route, False
            return np.inf, [], True

        def CheckValidPath(route, start, end):
            for i in range(0, len(route) - 1):
                if route[i] == start and route[i + 1] == end:
                    return True
                if route[i] == end and route[i + 1] == start:
                    return True
            return False

        #
        # # 2d point to index in matrix
        # # index to 2d matrix
        # # product (y,x)
        # # (y+1, x) (y, x+1) (y-1,x) (y,x-1)
        # # from start, get all the product position access points and go back to end point
        # # the end point is fully connected to other points
        def BuildHashMap(start, prod_pos, end):
            indexTo2D = {}
            TwoDToindex = {}
            indexTo2D[0] = ArrToString(start)
            TwoDToindex[ArrToString(start)] = 0
            index = 1
            for i in range(0, len(prod_pos)):
                # the First accessible point
                nodey = prod_pos[i][0] + 1
                nodex = prod_pos[i][1]
                nodefirst = [nodey, nodex]
                indexTo2D[index] = ArrToString(nodefirst)
                TwoDToindex[ArrToString(nodefirst)] = index
                index = index + 1
                # the Second accessible point
                nodey = prod_pos[i][0]
                nodex = prod_pos[i][1] + 1
                nodeSecond = [nodey, nodex]
                indexTo2D[index] = ArrToString(nodeSecond)
                TwoDToindex[ArrToString(nodeSecond)] = index
                index = index + 1
                # the Third accessible point
                nodey = prod_pos[i][0] - 1
                nodex = prod_pos[i][1]
                nodeThird = [nodey, nodex]
                indexTo2D[index] = ArrToString(nodeThird)
                TwoDToindex[ArrToString(nodeThird)] = index
                index = index + 1
                # the fourth accessible point
                nodey = prod_pos[i][0]
                nodex = prod_pos[i][1] - 1
                nodeFourth = [nodey, nodex]
                indexTo2D[index] = ArrToString(nodeFourth)
                TwoDToindex[ArrToString(nodeFourth)] = index
                index = index + 1

            totalNumberOfPoint = len(indexTo2D)
            adjList = {}
            for i in range(0, totalNumberOfPoint):
                adjList[i] = []
            # the start point is connected to all other points
            for i in range(1, totalNumberOfPoint):
                adjList[0].append(i)
                adjList[i].append(0)
            # all other points are connected to each other, except for accessible points that belongs to the same shelf
            for i in range(1, totalNumberOfPoint):
                for j in range(1, totalNumberOfPoint):
                    # if (i-1)4==(j-1)/4 it means that i and j belongs to the same shelf
                    if (i - 1) // 4 != (j - 1) // 4:
                        adjList[i].append(j)

            endPoint = len(indexTo2D)
            adjList[endPoint] = []
            # the end point should be conntected to all other points
            for i in range(0, endPoint):
                adjList[i].append(endPoint)

                adjList[endPoint].append(i)
            indexTo2D[endPoint] = ArrToString(end)
            TwoDToindex[ArrToString(end)] = endPoint
            return indexTo2D, TwoDToindex, adjList

        #
        #
        def ArrToString(node):
            return str(node[0]) + "#" + str(node[1])

        #
        def GetSingleShortestRoute(config, matrix):
            start = config.get_worker_pos_start()
            prod_pos = config.get_prod_pos()
            end = config.get_worker_pos_end()
            matrix, t = reduce_matrix(matrix)
            indexTo2D, TwoDToindex, adjList = BuildHashMap(start, prod_pos, end)
            # the start point might have already gathered some products
            hasGatheredProducts = []
            for i in range(0, len(prod_pos)):
                if prod_pos[i][0] - 1 == start[0] and prod_pos[i][1] == start[1]:
                    hasGatheredProducts.append(i)
                if prod_pos[i][0] + 1 == start[0] and prod_pos[i][1] == start[1]:
                    hasGatheredProducts.append(i)
                if prod_pos[i][0] == start[0] and prod_pos[i][1] - 1 == start[1]:
                    hasGatheredProducts.append(i)
                if prod_pos[i][0] == start[0] and prod_pos[i][1] + 1 == start[1]:
                    hasGatheredProducts.append(i)
            start = random.randint(-1, len(prod_pos))
            path, cost, default = Prunning(start, adjList, len(prod_pos), matrix, t)
            p = []
            for i in path:
                pos = indexTo2D[i].split("#")
                p.append([int(pos[0]), int(pos[1])])
                # y1 = int(pos[0])
                # x1 = int(pos[1])
                # print(y1, "#", x1)
            final_path = sort_path(config, p[:-1])

            if config.get_debug() == 1:
                if default:
                    print("Timed out! Using default product order.")
                    # print("Returning default path:", final_path)
                    # print("Length of this path is", cost)
                # else:
                #     print("Path of branch and bound is:", final_path)
                #     print("Length of this path is", cost)
            return final_path

        return GetSingleShortestRoute(config, matrix)

    def algorithm_nearest_neighbor(config, m):
        start_pos = config.get_worker_pos_start()
        prod_pos = config.get_prod_pos()
        end_pos = config.get_worker_pos_end()
        min_path = []
        min_length = np.inf
        mc = copy.deepcopy(m)
        for n in range(len(m)):
            m = copy.deepcopy(mc)

            time_now = time.time()
            time_elapsed = time_now - time_start
            if time_elapsed >= config.get_timeout():
                cost = 0
                dp = [start_pos]
                index = [0]
                for ind, i in enumerate(prod_pos):
                    if valid_ap(config, [i[0] + 1, i[1]]): # (y+1, x) (y, x+1) (y-1,x) (y,x-1)
                        cost += mc[index[-1]][ind * 4 + 1]
                        index.append(ind * 4 + 1)
                        dap = [i[0] + 1, i[1]]
                    elif valid_ap(config, [i[0], i[1] + 1]):
                        cost += mc[index[-1]][ind * 4 + 2]
                        index.append(ind * 4 + 2)
                        dap = [i[0], i[1] + 1]
                    elif valid_ap(config, [i[0] - 1, i[1]]):
                        cost += mc[index[-1]][ind * 4 + 3]
                        index.append(ind * 4 + 3)
                        dap = [i[0] - 1, i[1]]
                    else:
                        cost += mc[index[-1]][ind * 4 + 4]
                        index.append(ind * 4 + 4)
                        dap = [i[0], i[1] - 1]
                    dp.append(dap)
                dp.append(end_pos)

                cost += mc[index[-1]][len(mc) - 1]
                cost += mc[len(mc) - 1][0]
                if config.get_debug() == 1:
                    print("Timed out! Using default product order.")
                    print("Returning default path:", dp)
                    print("Length of this path is", cost)
                return dp

            start = n
            if min(m[n]) == np.inf:
                continue
            path = []
            length = 0
            while len(path) < len(prod_pos) + 2:
                if n == 0:
                    path.append(start_pos)
                    for i in range(len(m)):
                        m[i][n] = np.inf
                elif n == len(m) - 1:
                    path.append(end_pos)
                    for i in range(len(m)):
                        m[i][n] = np.inf
                else:
                    prod_ind = (n - 1) // 4
                    prod = prod_pos[(n - 1) // 4]
                    ap = (n - 1) % 4  # (y+1, x) (y, x+1) (y-1,x) (y,x-1)
                    if ap == 0:
                        path.append([prod[0] + 1, prod[1]])
                    elif ap == 1:
                        path.append([prod[0], prod[1] + 1])
                    elif ap == 2:
                        path.append([prod[0] - 1, prod[1]])
                    else:
                        path.append([prod[0], prod[1] - 1])
                    for i in range(len(m)):
                        for j in range(4):
                            m[i][prod_ind * 4 + j + 1] = np.inf

                if len(path) == len(prod_pos) + 2:
                    length += mc[n][start]
                else:
                    s = min(m[n])
                    length += s
                    n = m[n].index(s)

            if length < min_length:
                min_path = path
                min_length = length
        final_path = sort_path(config, min_path)
        # if config.get_debug() == 1:
        #     print("Path of nearest neighbor is:", final_path)
        #     print("Length of this path is", min_length)
        return final_path

    def algorithm_held_karp(config, mod_distance_matrix):

        distance_matrix = [row[:-1] for row in mod_distance_matrix[:-1]]

        rows = config.get_rows()
        cols = config.get_cols()
        worker_pos_start = config.get_worker_pos_start()
        worker_pos_end = config.get_worker_pos_end()
        shelf_pos = config.get_shelf_pos()
        prod_pos_list = config.get_prod_pos()
        debug = config.get_debug()

        # Find the path between start point and work's nearby points
        def bfs_path(rows, cols, start_pos, end_pos, shelf_pos):
            start = tuple(start_pos)
            end = tuple(end_pos)
            queue = deque([(start, [])])
            visited = set()
            key = []
            stuck = []

            # Find neighboring positions around the product position that are not occupied by shelves
            if end[0] + 1 < rows and ((end[0] + 1, end[1]) not in shelf_pos):
                key.append((end[0] + 1, end[1]))
            else:
                stuck.append(0)
            if end[1] + 1 < cols and ((end[0], end[1] + 1) not in shelf_pos):
                key.append((end[0], end[1] + 1))
            else:
                stuck.append(1)
            if end[0] - 1 >= 0 and ((end[0] - 1, end[1]) not in shelf_pos):
                key.append((end[0] - 1, end[1]))
            else:
                stuck.append(2)
            if end[1] - 1 >= 0 and ((end[0], end[1] - 1) not in shelf_pos):
                key.append((end[0], end[1] - 1))
            else:
                stuck.append(3)

            # Initialize the 2D path array
            paths = [[] for _ in range(len(key))]

            # Perform BFS to reach the key(nearby points)
            for i in range(len(key)):
                queue = deque([(start, [])])  # Initialize a queue with the start position and an empty path
                visited = set()  # Set to store visited positions (prevent repeat position)

                while queue:
                    current, path = queue.popleft()
                    x, y = current

                    if current == key[i]:
                        paths[i] = path + [current]  # Store the path from start to key position
                        break

                    if current in visited:
                        continue

                    visited.add(current)
                    # All posibilities of nearby points
                    neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

                    for nx, ny in neighbors:
                        # Check if neighboring position is valid (not exceeding the map) and not occupied by shelves
                        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in shelf_pos:
                            # Enqueue neighboring position with updated path
                            queue.append(((nx, ny), path + [current]))

                visited = set()
                queue = deque([(key[i], [])])  # Reset visited set and queue to find the path from key to end

            for i in stuck:
                paths.insert(i, float("inf"))

            # Return the distance and path from start to all key positions
            return paths

        # Held_Karp (Dynamic programming) for finding shortest path
        def tsp_held_karp(distance_matrix, rows, cols, worker_pos_start, worker_pos_end, prod_pos_list, shelf_pos):
            num_prods = len(distance_matrix)

            # Initialize the memoization table
            memo = {}

            # Build list of the distance between end point and each product
            def End_dist_cal(rows, cols, worker_pos_end, prod_pos_list, shelf_pos):
                end_dist_list = []

                for i in range(len(prod_pos_list)):
                    paths = bfs_path(rows, cols, worker_pos_end, prod_pos_list[i], shelf_pos)
                    for j in range(4):
                        # if no path between them, set it infinite
                        if paths[j] == float("inf"):
                            end_dist_list.append((paths[j]))
                        else:
                            end_dist_list.append(len(paths[j]) - 1)
                return end_dist_list

            # Define the key for memoization
            def get_key(visited, last_prod):
                return tuple(visited), last_prod

            # Define the recursive function for the Held-Karp algorithm
            def held_karp_algo(visited, last_prod, end_dist_list, worker_pos_start, worker_pos_end):

                # Base case: All prods have been visited
                if len(visited) == num_prods:
                    if worker_pos_start == worker_pos_end:
                        return distance_matrix[last_prod][0], [0]
                    elif worker_pos_start != worker_pos_end:
                        return end_dist_list[last_prod - 1], [0]

                # Check if the subproblem has already been solved
                key = get_key(visited, last_prod)
                if key in memo:
                    return memo[key]

                # Initialize the minimum distance and route
                min_distance = float('inf')
                optimal_route = None

                # Iterate over all unvisited prods
                for prod in range(num_prods):

                    if prod not in visited:
                        # Calculate the distance to the next prod
                        distance = distance_matrix[last_prod][prod]

                        # Recursively solve the subproblem
                        if prod == 0:
                            visited.append(prod)
                        else:
                            prod_temp = (prod - 1) // 4 * 4
                            for point in range(1, 5):
                                visited.append(prod_temp + point)
                        sub_distance, sub_route = held_karp_algo(visited, prod, end_dist_list, worker_pos_start, worker_pos_end)
                        if prod == 0:
                            visited.remove(prod)
                        else:
                            prod_temp = (prod - 1) // 4 * 4
                            for point in range(1, 5):
                                visited.remove(prod_temp + point)

                        # Update the minimum distance and route
                        total_distance = distance + sub_distance
                        if total_distance < min_distance:
                            min_distance = total_distance
                            optimal_route = [prod] + sub_route

                # Memoize the result
                memo[key] = min_distance, optimal_route

                return min_distance, optimal_route

            end_dist_list = End_dist_cal(rows, cols, worker_pos_end, prod_pos_list, shelf_pos)
            # Start the recursion from prod 0
            visited = [0]
            min_distance, optimal_route = held_karp_algo(visited, 0, end_dist_list, worker_pos_start, worker_pos_end)
            return [0] + optimal_route, min_distance

        # Converts product locations into exact pickup locations in order
        def nearby_point_determine(optimal_route, worker_pos_start, worker_pos_end, debug):
            # access point order list
            result_access = []
            # product order list
            result_product = []
            count = 0
            for i in optimal_route:
                temp_access = ()
                temp_prod = ()
                if i != 0:
                    if (i - 1) % 4 == 0:
                        temp_access = (prod_pos_list[(i - 1) // 4][0] + 1, prod_pos_list[(i - 1) // 4][1])
                    if (i - 1) % 4 == 1:
                        temp_access = (prod_pos_list[(i - 1) // 4][0], prod_pos_list[(i - 1) // 4][1] + 1)
                    if (i - 1) % 4 == 2:
                        temp_access = (prod_pos_list[(i - 1) // 4][0] - 1, prod_pos_list[(i - 1) // 4][1])
                    if (i - 1) % 4 == 3:
                        temp_access = (prod_pos_list[(i - 1) // 4][0], prod_pos_list[(i - 1) // 4][1] - 1)

                    temp_prod = (prod_pos_list[(i - 1) // 4][0], prod_pos_list[(i - 1) // 4][1])
                    result_access.append(temp_access)
                    result_product.append(temp_prod)
                else:
                    if worker_pos_start == worker_pos_end:
                        result_access.append(worker_pos_start)
                        result_product.append(worker_pos_start)
                    elif worker_pos_start != worker_pos_end:
                        if count:
                            result_access.append(worker_pos_end)
                            result_product.append(worker_pos_end)
                        else:
                            result_access.append(worker_pos_start)
                            result_product.append(worker_pos_start)
                        count += 1

            if debug == 1:
                print(result_access, result_product)

            return result_access, result_product

        optimal_route, min_distance = tsp_held_karp(distance_matrix, rows, cols, worker_pos_start, worker_pos_end, prod_pos_list, shelf_pos)

        if debug == 1:
            print("Optimal Route:", optimal_route)
            print("Minimum Distance:", min_distance)

        result_access, result_product = nearby_point_determine(optimal_route, worker_pos_start, worker_pos_end, debug)

        return result_access, result_product

    def print_path(path):
        # print steps to get the products based on previously calculated path
        directions = []  # List to store the directions
        current_direction = None  # Variable to track the current direction
        step_count = 0  # Variable to count the number of steps in the current direction

        # Iterate through each position in the path
        for i in range(len(path) - 1):
            y1, x1 = path[i]  # Current position coordinates
            y2, x2 = path[i + 1]  # Next position coordinate

            # Check the direction from current position to the next position
            # Moving east
            if x1 < x2:
                if current_direction == "east":
                    step_count += 1
                else:
                    if current_direction is not None:
                        directions.append(f"Go {current_direction} {step_count} steps")
                    current_direction = "east"
                    step_count = 1
            # Moving west
            elif x1 > x2:
                if current_direction == "west":
                    step_count += 1
                else:
                    if current_direction is not None:
                        directions.append(f"Go {current_direction} {step_count} steps")
                    current_direction = "west"
                    step_count = 1
            # Moving north
            elif y1 < y2:
                if current_direction == "north":
                    step_count += 1
                else:
                    if current_direction is not None:
                        directions.append(f"Go {current_direction} {step_count} steps")
                    current_direction = "north"
                    step_count = 1
            # Moving south
            elif y1 > y2:
                if current_direction == "south":
                    step_count += 1
                else:
                    if current_direction is not None:
                        directions.append(f"Go {current_direction} {step_count} steps")
                    current_direction = "south"
                    step_count = 1
            else:
                step_count += 1
        # Check if there is a current direction to add the last step count
        if current_direction is not None:
            directions.append(f"Go {current_direction} {step_count} steps")
        return directions

    print("Warehouse map with shelves marked and product highlighted:")
    print_map(config, [], config.get_worker_pos_start())
    dm = distance_matrix(config)
    dmc = copy.deepcopy(dm)
    time_start = time.time()
    if config.get_algorithm() == 1:
        algo = "Branch and Bound"
        path = algorithm_branch_and_bound(config, dm)
    elif config.get_algorithm() == 2:
        algo = "Repetitive Nearest Neighbor"
        path = algorithm_nearest_neighbor(config, dm)
    else:
        algo = "Held-Karp"
        path, prod = algorithm_held_karp(config, dm)

    print("Start from " + str(path[0]) + ".")
    length = 0
    for i in range(len(path) - 1):
        if path[i] == path[i + 1]:
            continue
        r = shortest_route(config, tuple(path[i]), tuple(path[i + 1]))
        length += len(r) - 1
        # print(r)
        print_map(config, r, path[i])
        step = print_path(r)
        for s in step:
            print(s)
        if i == len(path) - 2:
            print("Arrive at end point " + str(path[i + 1]) + ".")
        else:
            print("Get product from " + str(path[i + 1]) + ".")
    print("Product collected and arrived at end point!")

    if config.get_debug() == 1:
        print("Current algorithm:", algo)
        print("Path:", path)
        print("Total steps taken:", length)
    print("Returning to menu...\n")



if __name__ == "__main__":
    main()
