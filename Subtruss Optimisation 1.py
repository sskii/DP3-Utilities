import math

stLength = float(input("Please input subtruss length in mm:\f"))		# Subtruss length, mm

#nTriangles = [int(input("Please input the number of triangles:\f"))]	# Subtruss section count, ul
nTriangles = [2, 4, 6, 8]												# array of possibilities to try

outputBuffer = ""														# output buffer so that all the useful stuff gets printed last

# We need to find the first value of theta that satisfies the following:
# (sinθ)(cosθ)^2 = (115 stLength^2) / (k nTriangles^2)

k = (200) * ((60) ** 2)					# compression constant
phi = 0.8								# safety factor

DP = int(input("Please input desired answer precision in DP:\f"))		# decimal answer precision in DP
thetaStep = math.radians(10 ** (-1 * DP))								# because python works in radians!

print("Stepping", thetaStep, "radians per iteration.")

# METHOD #
# We will first evaluate the RHS of the expression. Then we'll evaluate values of theta from zero
# until the LHS is greater than the RHS, at which point we return theta.

for n in nTriangles:
	
	print("Beginning evaluation of", n, "triangles.")

	RHS = (115 * (stLength ** 2)) / (k * (n ** 2))
	print("RHS =", RHS)

	theta = 0			# test theta
	run = True			# flag

	while run:

		if theta > math.radians(90):
			# inputs are invalid somehow
			print("No solutions found! Check inputs.")

			# report this
			outputBuffer += str(n)
			outputBuffer += "           (No valid solutions.)\n"

			run = False

		LHS = (math.sin(theta)) * ((math.cos(theta)) ** 2)
		print("LHS =", LHS, " when θ =", math.degrees(theta))

		if LHS > RHS:
			#solution found
			print("\nSolution found. θ =", round(math.degrees(theta), DP))

			# calc expected subtruss capacity
			stMaxCompLoad = (2 * k * phi * (math.cos(theta) ** 3) * (n ** 2)) / (stLength ** 2)
			stMaxTensLoad = (230 * phi) / (math.tan(theta))

			# write the solutions out
			outputBuffer += str(n)
			outputBuffer += "           "
			outputBuffer += str(round(math.degrees(theta), DP))
			outputBuffer += "                     "
			outputBuffer += (str(stMaxCompLoad) + ", " + str(stMaxTensLoad))
			outputBuffer += "\n"

			run = False
		else:
			#no solution found
			theta += thetaStep	# increment theta
	
	print("Finished evaluating for", n, "triangles.")

#done
print("\n* * *\nExecution finished!")

print("Solutions for", stLength, "mm subtruss:\n\nTriangles:  Half of enclosed angle:  Calculated capacity (by diagonals, verticals)^")
print(outputBuffer)

print("^ Calculated capacity is valid for subtruss loading under compression assuming all constituent members are type-1. Values given in newtons.")