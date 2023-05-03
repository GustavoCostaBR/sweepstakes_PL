string = "This is a sentence apple, apple, apple that contains the word apple."

# if "apple" in string:
#     index = string.index("apple")
#     print(string[:index] + string[index+len("apple"):])
# else:
#     print(string)
# my_list = [1, 2, 3, 4, 5]
# del my_list[3]
# print(my_list)  # Output: [1, 2, 3, 5]

my_list = [1, 2, 3]
my_list.extend([4, 5])
print(my_list)
