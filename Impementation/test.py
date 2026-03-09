# a = [[3,2],[1,2],[1,1]]
# transpose = list(zip(*a))
# for item in transpose:
#     for single in item:
#         print(single)
# print(transpose)
a = [[1,2,3],[3,4,6]]
b = [[1,2],[2,3],[3,4]]
# print(list(zip(*a)))
# array = []
# for idx , list in enumerate(range(len(a))):
#     f"list{idx}" = []
b = list(zip(*b))
print(b)
result = []
for row11 in a:
    row = []
    for row12 in b:
        # print(f"row11: {row11}, row12: {row12}")
        sum = 0
        for item1,item2 in zip(row11,row12):
            sum += item1*item2
        row.append(sum)
    result.append(row)

print(result)
