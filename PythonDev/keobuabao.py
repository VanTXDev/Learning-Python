import random

def continue_playing():
	print ("----------------------------------------------------------------")
	print ("Chơi nữa không")
	print ("0 => Nghĩ")
	print ("1 => Chơi")
	continuous = input()
	if continuous == "1":
		playing()
	else:
		print ("Kết thúc game")

def playing():
	data = ["Kéo", "Búa", "Bao"]
	print ("Nhập lựa chọn của bạn: ")
	for i in range(len(data)):
		print (str(i) + " => " + str(data[i]))
	playerChoice = input()

	while int(playerChoice) >= len(data):
		if int(playerChoice) >= len(data):
			print ("Nhập xà lơ!!")
		print ("----------------------------------------------------------------")
		print ("Nhập lựa chọn của bạn: ")
		for i in range(len(data)):
			print (str(i) + " " + str(data[i]))
		playerChoice = input()

	playerChoice = str(data[int(playerChoice)])
	computerChoice = random.randint(0, 2)
	computerChoice = str(data[computerChoice])
	print ("----------------------------------------------------------------")
	print ("Player: " + playerChoice)
	print ("Computer: " + computerChoice)

	if playerChoice == computerChoice:
		print ("Hòa")
	else:
		if playerChoice == "Kéo":
			if computerChoice == "Búa":
				print ("Bạn thua!")
			else: 
				print ("Bạn thắng!")
		elif playerChoice == "Búa":
			if  computerChoice == "Bao":
				print ("Bạn thua!")
			else: 
				print ("Bạn thắng!")
		elif playerChoice == "Bao":
			if  computerChoice == "Kéo":
				print ("Bạn thua!")
			else: 
				print ("Bạn thắng!")
	continue_playing()

playing()