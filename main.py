import argparse
import json
import os
from datetime import datetime


# create add function (this function should include the parsers --description and --amount)
# create list function (this function should display #id, date, description and amount)
# create summary function (displays the total amount)
# delete function (specify and delete --id)

def cmd_add(args):
    file_path = "data.json"

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            try:    
                data = json.load(f)
            except json.JSONDecodeError:
                data = []   
    else:
        data = []
    
    new_item = {
        
        "id": len(data) + 1,
        "date": datetime.now().isoformat(),
        "description": args.description,
        "amount": args.amount
    }


    data.append(new_item)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"# Expsense added successfully (ID: {new_item["id"]})")



def cmd_list(args):
    file_path = "data.json"

    with open(file_path, "r") as f:
        data = json.load(f)

    print(f"# {'ID':<5} {'Date':<15} {'Description':<20} {'Amount':<10}")
    print('-' * 50)

    for item in data:
        dt = datetime.fromisoformat(item['date'])
        formatted = dt.strftime("%B %d, %Y")
        print(f" # {item['id']:<5} {formatted:<15} {item['description']:<20} ${item['amount']:<10}")


def cmd_summary(args):
    month_filter = args.month
    file_path = "data.json"

    with open(file_path, "r") as f:
        data = json.load(f)

    total = 0
    for item in data:
        if month_filter:
            dt = datetime.fromisoformat(item['date'])
            if dt.month != month_filter:
                continue
        total += float(item['amount'])

    print(f"# Total expenses: ${total}")


def cmd_delete(args):
    file_path = "data.json"

    with open(file_path, "r") as f:
        data = json.load(f)

    updated_data = [item for item in data if item['id'] != args.id]

    with open(file_path, "w") as f:
        json.dump(updated_data, f, indent=4)

    
# ---------------------


def main():

    parser = argparse.ArgumentParser(description="simple CLI program")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    p_add = subparsers.add_parser("add", help="add a new item")
    p_add.add_argument("--description", type=str, required=True)
    p_add.add_argument("--amount", type=float, required=True)
    p_add.set_defaults(func=cmd_add)

    # list command
    p_list = subparsers.add_parser("list", help="list all items")
    p_list.set_defaults(func=cmd_list)

    # summary command 
    p_summary = subparsers.add_parser("summary", help="total cost of items")
    p_summary.add_argument("--month", type=int)
    p_summary.set_defaults(func=cmd_summary)

    # delete command
    p_delete = subparsers.add_parser("delete", help="delete item from list")
    p_delete.add_argument("--id", type=int)
    p_delete.set_defaults(func=cmd_delete)


    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
