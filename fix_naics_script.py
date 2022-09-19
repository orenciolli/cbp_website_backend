with open('naics_1975_1985.txt', 'r') as f:
    data = f.readlines()

data = [line[:4] + '    ' + line[4:] for line in data]

with open('naics_1975_1985.txt', 'w') as f:
    f.writelines(data)

