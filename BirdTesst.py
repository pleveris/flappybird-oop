import unittest

# This is the class we want to test. So, we need to import it
import Bird as BirdClass
import random

class Test(unittest.TestCase):
	"""
	The basic class that inherits unittest.TestCase
	"""
	bird = BirdClass.Bird(1)  # instantiate the Bird Class, 1 means bird index as defined in Bird class
x_coord = 0 # for setting and getting x_coord inside Bird class
y_coord = 0 # for setting and getting x_coord inside Bird class

	# test case function to check the Bird.set_x_coord function
	def test_0_set_x_coord(self):
		print("Start x_coord test\n")
		"""
		Any method which starts with ``test_`` will considered as a test case.
		"""
			# store the x_coord into the variable
			self.x_coord = random.randint(1,5)
			# get the x_coord obtained from the function
x_coord = self.bird.set_x_coord(x_coord)
			# check if the obtained xx_coord is valid
			self.assertIsNotNone(x_coord)  # null x_coord will fail the test
			# store the x coord
			self.x_coorrd = x_coord
		print("x_coord = ", self.x_coord)
		print(self.x_coord)
		print("\nFinish set_name test\n")

if __name__ == '__main__':
	# begin the unittest.main()
	unittest.main()