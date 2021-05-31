from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

print(similar("2016.01.26 (HPE ProLiant m700 Server Blade)", "2017.03.14 (HPE ProLiant m700p Server Blade)"))