def to_fen(amount):
    return round(float(amount)*100)

def to_yuan(amount):
    return float(amount)/100

def amount_equal(a,b):
    return  to_fen(a)==to_fen(b)

def amount_change_equal(actual,original,change):  
    return  to_fen(actual)==to_fen(original)+to_fen(change) 