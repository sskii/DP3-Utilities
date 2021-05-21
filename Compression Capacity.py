# quick calculator that programatically determines member compression capacity

# member type factors, types 1 through 4
factors = [1, 8, 27, 26]

# compression calculation parameters
kComp = (200) * ((60) ** 2)				# compression constant
phi = 0.8

def calcCompression():
	length = float(input("Enter member length, mm: "))
	type = int(input(    "Enter member type, 1-4:  "))

	singleCapacity = phi * kComp / (length ** 2)
	capacity = singleCapacity * factors[type - 1]

	print("\nMember type", type, "of length", length, "mm has a capacity of", capacity, "N.")

calcCompression()
while input("\nEnter any key except 'x' to run again:") != "x":
	calcCompression()
