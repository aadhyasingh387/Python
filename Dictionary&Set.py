# info ={
#     "key" : "value",
#     "name": "agamsingh",
#     "subjects" : ["python" ,"java","c"],
#     "topics" : ("dict" , "set") , 
#     "age" :22
# }

# print(info["topics"])

# info["name"] = "agam"
# info["surname"] = "singh"

# print(info["name"])

# null_dict ={}
# null_dict["name"] ="agam"
# print(null_dict)


#nested dictionary

# student ={
#     "name" : "agam",
#     "subjects" : {
#         "phy" :90,
#         "chem" :89,
#         "math" : 95,
#         "bio" :98
#     }

# }

# print(student["subjects"]["math"])

# print(student.keys())

# print(len(list(student.keys())))

# print(student.values())

# pairs = list(student.items())
# print(pairs)
# print(pairs[0])


# print(student.get("keys"))

# print(student.get("name"))  

# student.update({"my lo" : "shradha khapra"})

# print(student)


# new_dict = {"city" : "delhi", "country" : "india"}
# student.update(new_dict)
# print(student)


# Sets in python

# collection = {1,2,2,4,5,6,"hello", "agam" , 7}

# print(collection)
# print(len(collection))


# Empty set
# collection = set()
# # print(type(collection))
# collection.add(1)
# collection.add(2)
# collection.add(2)
# collection.add("hello")
# collection.remove(1)
# # collection.clear()
# collection.pop()
# print(collection)

# set1 = {1,2,3,4,5}
# set2 = {4,5,6,7,8}
# print(set1.union(set2))

# print(set1.intersection(set2))

#Q1
# dict ={
#     "cat" : "a small animal",
#     "table" : ["a piece of furniture" ,"list of fact & figures"]
# }

# print(dict)


#Q2
# subjects = {"python", "java", "c++" , "python" ,"javascript" , "java", "python" ,"java" , "c++" ,"c"}
# print("Total number of class : " ,len(subjects))


#Q3
# marks={}
# x =int(input("Enter the number phy : "))
# marks.update({"phy" : x})

# x =int(input("Enter the number math : "))
# marks.update({"math" : x})

# x =int(input("Enter the number chem : "))
# marks.update({"chem" : x})

# print(marks)

#Q4

values ={
    ("float" ,9.0),
    ("int" , 9)
}

print(values)



