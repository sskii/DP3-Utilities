import math

# like the previous options, but it instead asks for input as co-ords.

# environment parameters #
kComp = (200) * ((60) ** 2)				# compression constant
kTens = 230								# tension constant
phi = 0.8								# reduction factor

# evaluate a given subtruss
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

p1 = [float(input("Enter start x coordinate: ")), float(input("Enter start y coordinate: "))]
p2 = [float(input("\nEnter end x coordinate:   ")), float(input("Enter end y coordinate:   "))]

dx = p2[0] - p1[0]
dy = p2[1] - p1[1]

l = math.sqrt( dx**2 + dy**2 )

print("\nSolutions for", l, "mm subtruss:\nTriangles:  Half of enclosed angle:  Capacity (diags, verts)^  Length (diags, verts)")
for n in triangles:
	data = evaluateSubtruss(l, n, 3)
	
	if data[0]:
		print(
			n, "         ", data[1],
			"                    (", data[2], ",", data[3],
			")      (", data[4], ",", data[5], ")"
		)
	
	else:
		# unsuccessful run
		print(n, "          No solutions found.")

if dx != 0:
	# avoid errors for vertical trusses as we cannot divide by zero.
	angle = math.degrees(math.atan(dy/dx))
else:
	angle = 90

#if dy < 0:
	angle += 180

#if dx 

print("\n* Additional Stats *")
print("Length in x:  ", dx)
print("Length in y:  ", dy)
print("Incline angle:", angle, "degrees. (Note that this is not absolute.)")

print("\nEnd.")