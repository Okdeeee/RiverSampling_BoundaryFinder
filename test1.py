import numpy

l = [37.54924,37.54924,37.52817,37.52817,37.52067,37.52067,37.47452,37.47452,37.46252,37.46252,37.46089,37.46089,37.42098,37.42098,37.40035,37.40035,37.34919,37.34919,37.35033,37.35033,37.31935,37.31935,37.28688,37.28688,37.23634,37.23634,37.21166,37.21166,37.18647,37.18647,37.13176,37.13176,37.18409,37.18409,37.22004,37.22004,37.11199,37.11199,37.07281,37.07281,37.14441,37.14441,37.08712,37.08712,37.14634,37.14634,37.18282,37.18282,37.22323,37.22323,37.24498,37.24498,37.27209,37.27209,37.30496,37.30496,37.31545,37.31545,37.34494,37.34494,37.3616]
threshold = 0.1

groups = []
temp_list = []
for n, i in enumerate(l) :
    # print(i)
    if n != 0 :
        if abs(i-base) > threshold :
            groups.append(temp_list)
            temp_list = []
            base = i
        temp_list.append(i)
    else :
        base = i    
        temp_list.append(i)
groups.append(temp_list)

# print(groups)

avg_list= [numpy.mean(i) for i in groups]

print(avg_list)