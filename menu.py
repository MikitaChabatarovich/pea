from tsp import TSP
import time


def print_menu():
    print("1. Enter file name")
    print("2. Brute-Force")
    print("3. BranchAndBound")
    print("0. Exit")


def Main():
    choice = 1
    filename = "test/6_test.txt"
    while choice:
        print_menu()
        choice = int(input("Choice "))
        if choice == 1:
            filename = input("filename = ")
        elif choice == 2:
            _tsp = TSP(filename=filename)
            start = time.time()
            _tsp.Brute_Force()
            end = time.time()
            _tsp.print_result()
            print("Time: ", end - start)
            input()
        elif choice == 3:
            _tsp = TSP(filename=filename)
            start = time.time()
            _tsp.BranchAndBound()
            end = time.time()
            _tsp.print_result()
            print("Time: ", end - start)
            input()
        elif choice == 0:
            break
        else:
            continue


if __name__ == '__main__':
    Main()
