import json
from datetime import date


def deposit(name, amount,server):
  amount = round(amount, 2)
  users = read(server)
  if name in users:
    current_user = users[name]
    current_user["total_deposit"] = current_user.get("total_deposit", 0) + amount
    current_user["history"].append({"amount": amount, "date": str(date.today())})
  else:
    total_deposit = amount
    history = []
    history.append({"amount": amount, "date": str(date.today())})
    users[name] = {"total_deposit": total_deposit, "history": history}
  writeto(server,users)
    
def writeto(server, data):
  with open(str(server)+ "_accounts.json", "w") as json_file:
      json.dump(data, json_file, indent = 4) 

def read(server):
  try:
    with open(str(server)+ "_accounts.json", "r") as json_file:
      loaded_users = json.load(json_file)
      return loaded_users
  except FileNotFoundError:  
    return {}
  except json.decoder.JSONDecodeError:
    return {}


#CODE FOR RECPIPTS

#need a reed write and read function
#need a write function for receipts
#need a function to create valid information and pack it

def expense(server, note, cost, url):
  cost = round(cost, 2)
  count = 0
  transactions = readEX(server)
  for key in transactions:
    count += 1
  transactions["transaction_" + str(count)] = {"note" : note,
                                              "ammount" : cost,
                                              "url" : url,
                                              "date" : str(date.today())}
  writetoEX(server,transactions)

def readEX(server):
  try:
    with open(str(server)+ "_expenses.json", "r") as json_file:
      loaded_users = json.load(json_file)
      return loaded_users
  except FileNotFoundError:  
    return {}
  except json.decoder.JSONDecodeError:
    return {}

def writetoEX(server, data):
  with open(str(server)+ "_expenses.json", "w") as json_file:
      json.dump(data, json_file, indent = 4) 
  
def show_all_expenses(server, input="NA"):
  transactions = readEX(server)
  if input == "NA":
    data = []
    for key in transactions:
      data.append(key + "\nammount : $" + str(transactions[key]["ammount"]) + "\ndate : " + transactions[key]["date"] + "\nnote : " + transactions[key]["note"] + "\nurl : " + transactions[key]["url"])
    return data
  else:
    key = input
    return str(key + "\nammount : $" + str(transactions[key]["ammount"]) + "\ndate : " + transactions[key]["date"] + "\nnote : " + transactions[key]["note"] + "\nurl : " + transactions[key]["url"])
    
def show_all_users(server, input="NA"):
  users =read(server)
  if input == "NA":
    data = []
    for key in users:
      data.append(key + ":\ntotal deposit$" + str(users[key]["total_deposit"]) + "\ndeposit history : ")
      for line in users[key]["history"]:
        data.append(line["date"] + " : $" + str(line["amount"]))
    return data
  else:
    data = []
    key = input
    data.append(key + ":\ntotal deposit$" + str(users[key]["total_deposit"]) + "\ndeposit history : ")
    for line in users[key]["history"]:
      data.append(line["date"] + " : $" + str(line["amount"]))
    return data


  

