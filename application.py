from app import application
if __name__ == "__main__":
	###### MAKE FALSE BEFORE DEPLOYING!!!!######
	application.debug = False
	application.run()