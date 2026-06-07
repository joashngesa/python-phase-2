from tabulate import tabulate

def print_output(valids,invalids, transformed):

    print("\nvalids table")
    print(tabulate(valids, headers="keys", tablefmt="grid"))

    print("\ninvalids table")
    print(tabulate(invalids, headers="keys", tablefmt="grid"))

    print("\ntransformed table")
    print(tabulate(transformed, headers="keys", tablefmt="grid"))