# takes an input for the subtruss start and end coords and the number of members
# and returns the coordinates for all of the joints to make it easy to draw the
# designs by hand easier.

# also includes functionality to scale the output dimensions

import math

# environment parameters #
kComp = (200) * ((60) ** 2)				# compression constant
kTens = 230								# tension constant
phi = 0.8								# reduction factor

# evaluate a given subtruss #
def evaluateSubtruss(length, triangles, precision):

	thetaStep = math.radians(10 ** (-1 * precision))				# because python works in radians
	RHS = (kTens * (length ** 2)) / (2 * kComp * (triangles ** 2))

	# run results
	success = False
	stMaxCompLoad = 0
	stMaxTensLoad = 0
	diagLength = 0
	vertLength = 0

	theta = 0			# test theta
	run = True			# flag

	while run:

		if theta > math.radians(90):
			#stop execution
			run = False

		# evaluate LHS for current value of theta
		LHS = (math.sin(theta)) * ((math.cos(theta)) ** 2)

		if LHS > RHS:
			#solution found

			# calc expected subtruss capacity
			stMaxCompLoad = (2 * kComp * phi * (math.cos(theta) ** 3) * (triangles ** 2)) / (length ** 2)
			stMaxTensLoad = (kTens * phi) / (math.tan(theta))

			# calc member lengths
			diagLength = (length) / (triangles * math.cos(theta))
			vertLength = (2 * length * math.tan(theta)) / (triangles)

			# stop execution
			run = False

			# note that run was successful
			success = True

		else:
			#no solution found
			theta += thetaStep	# increment theta
	
	return [
		success,
		round(math.degrees(theta), precision),
		round(stMaxCompLoad, 2),
		round(stMaxTensLoad, 2),
		round(diagLength, 2),
		round(vertLength, 2)
	]


# test code #
triangles = [2, 4, 6, 8]	# possible numbers of triangles
							# trusses to test

l = 0

p1 = [float(input(    "Enter start x coordinate:  ")), float(input("Enter start y coordinate: "))]
p2 = [float(input(  "\nEnter end x coordinate:    ")), float(input("Enter end y coordinate:   "))]
triangles = int(input("Input number of triangles: "))
reduction = int(input("Input scale-down factor:   "))

dx = p2[0] - p1[0]
dy = p2[1] - p1[1]

l = math.sqrt( dx**2 + dy**2 )
data = evaluateSubtruss(l, triangles, 3)

print("\nSubtruss measures ", l, "mm.")

# calculate x and y steps per joint
joint_dx = dx / triangles
joint_dy = dy / triangles

# find the joints along the centreline
for i in range(0, triangles + 1):

	# get and print the coordinates of the relevant centre point
	cp = [(joint_dx * i), (joint_dy * i)]

	# check whether there are additional points
	#if i % 2 == 1:

	print("Coordinates: (", cp[0] / reduction, ",", cp[1] / reduction, ")")
	
	

if data[0]:
	# successful run
	print("Success. Placeholder line.")

else:
	# unsuccessful run
	print("ERROR: This subtruss is invalid. You've screwed something up. Terribly sorry.")

angle = math.degrees(math.atan(dy/dx))

print("\n* Additional Stats *")
print("Length in x:  ", dx)
print("Length in y:  ", dy)
print("Incline angle:", angle, "degrees. (Note that this is not absolute.)")

print("\nEnd.")