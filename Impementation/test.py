a = [[3,2],[1,2],[1,1]]
transpose = list(zip(*a))
for item in transpose:
    for single in item:
        print(single)
print(transpose)