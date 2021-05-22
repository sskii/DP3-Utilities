# quick calculator that programatically determines member compression capacity

# member type factors, types 1 through 4
factors = [1, 8, 27, 26]

# compression calculation parameters
kComp = (200) * ((60) ** 2)				# compression constant
phi = 0.8

# if we want something nice as an output
output = ""
show = False

def calcCompression():
	name = input(        "Enter member name:              ")
	demand = float(input("Enter member demand, N:         "))

	length = float(input("Enter member length, mm:        "))
	type = int(input(    "Enter member type, 1-4:         "))
	mult = int(input(    "Enter multiplier (1 if unsure): "))

	singleCapacity = phi * kComp / (length ** 2)
	capacity = singleCapacity * factors[type - 1]

	print("\nMember type", type, "of length", length, "mm has a capacity of", capacity, "N.")

	global output
	output += ("\nMember " + name + " of type " + str(type) + " and length " + str(length) + " mm has a capacity of " + str(capacity) + " N and safety factor " + str(capacity / demand))

calcCompression()
while input("\nEnter any key except 'x' to run again:") != "x":
	show = True
	calcCompression()

if show: print(output)