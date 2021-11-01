import sys

file = open("./Config/owner.txt", "r", encoding="utf-8")
listOwner = file.readlines()
owner = listOwner[0]
print(owner.split("\n")[0])