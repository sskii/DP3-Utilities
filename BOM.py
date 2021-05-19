
totalJoints = int(input("Enter number of joints in supertruss:  "))
totalMembers = 0

# supertruss config
numSubtrusses = int(input("Enter number of subtrusses present:    "))

for i in range(1, numSubtrusses + 1):
	# specific subtruss config
	msg = ("\nEnter the number of triangles in subtruss #" + str(i) + ":  ")
	numUnits = int(input(msg))

	# filter stupid inputs
	if numUnits % 2 != 0:
		# if it's an odd number
		print("Invalid input. Number of triangles must be even. Skipping subtruss.")
		continue
	numUnits /= 2

	# check for stupid inputs
	if numUnits <= 0:
		print("Invalid input. Number of units must be non-zero. Skipping subtruss.")
		continue

	# count the number of members
	members = 5*numUnits		# loaded members
	members += (numUnits - 1)	# "zero-force" members

	# count the number of joints
	joints = 4					# four joints for one unit
	joints += 3*(numUnits - 1)	# three joints per additional unit
	joints -= 2					# subtract the external joints

	print("Subtruss #" + str(i) + " requires", members, "type-1 members and", joints, "joints.")

	# add to totals
	totalMembers += members
	totalJoints += joints

print("\n* * *\n")
print("Supertruss requires", totalMembers, "type-1 members for subtrusses and", totalJoints, "joints overall.\n")