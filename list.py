def printList(list):
    for item in list:
        print(str(item))



# Let's create a list with 5 colors:
colors = [ '1-red', '2-blue', '3-green', '4-yellow', '5-black' ]

# Print the list, printing all 5 colors, here are the results:
# 1-red
# 2-blue
# 3-green
# 4-yellow
# 5-black
print("Original list:")
printList(colors)

# Now, let's iterate over the list, looking for 3-green, and once we
# find it, let's delete it.  But, notice something odd.  As a result
# of deleting 3-green while iterating through the list, the loop seems
# to skip the next item in the the list, 4-yellow.  Here are the
# results:
# 1-red
# 2-blue
# 3-green
#   ^^ deleting
# 5-black
print()
print("Using 'for color in colors:' syntax:")
for color in colors:
    print(color)
    if color == '3-green':
        print("  ^^ deleting")
        colors.remove(color)

# Now print the list again, notice that it accurately represented
# 3-green having been deleted, here are the results:
# 1-red
# 2-blue
# 4-yellow
# 5-black
print()
print("Modified list after deleting of 3-green:")
printList(colors)


#==============================================================================
# What was the problem?  - Deleting an item from a list, while
# iterating over the last, is an "undefined" operation, in other
# words, it's dangerous to do, because it modifies the list you're
# currently looping through.
#
# Is there a solution?  YES!
#
# By using the "colors[:]" syntax below, python creates a copy of the
# list, and iterates through the copy.  So, when you delete an item
# from the original list, it doesn't modify the copied list you are
# iterating over, solving the problem.


# Results:
# 1-red
# 2-blue
# 3-green
#   ^^ deleting
# 4-yellow
# 5-black
colors2 = [ '1-red', '2-blue', '3-green', '4-yellow', '5-black' ]
print()
print("Using 'for color in colors[:]:' syntax:")
for color in colors2[:]:
    print(color)
    if color == '3-green':
        print("  ^^ deleting")
        colors2.remove(color)

# Results:
# 1-red
# 2-blue
# 4-yellow
# 5-black
print()
print("Modified list:")
printList(colors2)
