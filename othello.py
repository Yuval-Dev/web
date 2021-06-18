import time
import cgi, cgitb 

# Create instance of FieldStorage 


default_game = "eeeeeeeeeeeeeeeeeeeeeeeeeeewbeeeeeebweeeeeeeeeeeeeeeeeeeeeeeeeeeb"
def move(game,move):
	if not "e" in game:
		return None
	if game==None:
		return None
	if move==-1:
		return game[:64] + ("w" if game[64]=="b" else "b")
	if not game[move]=="e":
		return None
	new_game = game
	#uhh... ok this gets pretty ugly. For efficiency sake, i figured it would be better to write everything out in a repetitive way just to save on the execution time
	flipped = False
	
	i = (move//8)
	j = (move%8)
	new_game = game[:i*8+j] + game[64] + game[i*8+j+1:]
	while i<8 and j<8:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and i-(move//8)>0:
			while i>(move//8):
				j -= 1
				i -= 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		i += 1
		j += 1
	i = (move//8)
	j = (move%8)
	while i>=0 and j>=0:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and (move//8)-i>0:
			while i<(move//8):
				j += 1
				i += 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		i -= 1
		j -= 1
	i = (move//8)
	j = (move%8)
	while i<8 and j>=0:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and i-(move//8)>0:
			while i>(move//8):
				j += 1
				i -= 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		i += 1
		j -= 1
	i = (move//8)
	j = (move%8)
	while i>=0 and j<8:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and (move//8)-i>0:
			while i<(move//8):
				j -= 1
				i += 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		i -= 1
		j += 1
	i = (move//8)
	j = (move%8)
	while i<8:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and i-(move//8)>0:
			while i>(move//8):
				i -= 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		i += 1
	i = (move//8)
	j = (move%8)
	while i>=0:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and (move//8)-i>0:
			while i<(move//8):
				i += 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		i-=1
	i = (move//8)
	j = (move%8)
	while j<8:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and j-(move%8)>0:
			while j>(move%8):
				j -= 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		j+=1
	i = (move//8)
	j = (move%8)
	while j>=0:
		if new_game[i*8+j]=="e":
			break;
		if new_game[i*8+j]==new_game[64] and (move%8)-j>0:
			while j<(move%8):
				j += 1
				if not new_game[i*8+j]==new_game[64]:
					flipped = True
				new_game = new_game[:i*8+j] + new_game[64] + new_game[i*8+j+1:]
			break;
		j-=1
	if not flipped:
		return None
	new_game = new_game[:64] + ("w" if new_game[64]=="b" else "b")
	return new_game
def evaluate_weighted(game):
	score = 0
	for i in range(64):
		coef = 1
		if i//8==0 or i//8==7:
			coef *= 2
		if i%8==0 or i%8==7:
			coef *= 2
		if game[i]=="b":
			score += coef
		elif game[i]=="w":
			score -= coef
	return score
def evaluate(game):
	score = 0
	for i in range(64):
		if game[i]=="b":
			score += 1
		elif game[i]=="w":
			score -= 1
	return score
def game_from_history(history):
	game = default_game
	for i in history:
		game = move(game,ord(i)-ord('1'))
	return game
sfn_data = {"valid_games_checked":0,"games_checked":0,"ab_skipped":0,"theoretical_amount":1}


#this is the algorithm right here
def minmax_ab(game,depth,player,alpha=None,orig_call=True,weighted=False):
	if game==None:
		return None
	if orig_call:
		sfn_data["valid_games_checked"] = 0 #this is just for stats, disregard this as it has no extra effect
		sfn_data["games_checked"] = 0 #same
		sfn_data["ab_skipped"] = 0 #same
		sfn_data["theoretical_amount"] = 64**(depth) #same
		alpha = float('inf') if game[64]=="b" else float('-inf')
	if game[64]=="b":
		best_game = None
		best_score = float('-inf')
		for i in range(64):
			sfn_data["games_checked"] += 1
			new_game = move(game,i) if depth==1 else minmax_ab(move(game,i),depth-1,player,alpha=best_score,orig_call=False,weighted=weighted)
			if (not new_game==None):
				sfn_data["valid_games_checked"] += 1
				score = evaluate_weighted(new_game) if weighted else evaluate(new_game)
				if score > alpha:
					sfn_data["ab_skipped"] += (64-i)*(64**(depth-1))
					return None
				if score > best_score:
					best_score = score
					best_game = i if orig_call else new_game
		return best_game if (not best_game==None) else (-1 if orig_call else move(game,-1))
	else:
		worst_game = None
		worst_score = float('inf')
		for i in range(64):
			sfn_data["games_checked"] += 1
			new_game = move(game,i) if depth==1 else minmax_ab(move(game,i),depth-1,player,alpha=worst_score,orig_call=False,weighted=weighted)
			if (not new_game==None):
				sfn_data["valid_games_checked"] += 1
				score = evaluate_weighted(new_game) if weighted else evaluate(new_game)
				if score < alpha:
					sfn_data["ab_skipped"] += (64-i)*(64**(depth-1))
					return None
				if score < worst_score:
					worst_score = score
					worst_game = i if orig_call else new_game
		return worst_game if (not worst_game==None) else (-1 if orig_call else move(game,-1))



def generate_page(history,player,new_move,difficulty,statsfornerds):
	start = time.time()
	history += new_move
	game = game_from_history(history)
	while not game[64]==player and "e" in game:
		tmp_move = minmax_ab(game,6 if difficulty=="hard" else (4 if difficulty=="medium" else 2),player,weighted= False if difficulty=="easy" else True)
		game = move(game,tmp_move) if (not tmp_move==None) else move(game,-1)
		history += chr(ord('1')+tmp_move) if (not tmp_move==None) else '0'
	page = """
	<!DOCTYPE html>
	<html>
	<header>
	<title> Othello AI </title>
	<link rel='stylesheet' href='style.css'>
	</header>
	<body>
	<div class='game-container'>
	<form action='othello.py'>
	<p>
	<div class='difficulty_div'>
	{AI_DIFFICULTY}
	</div>
	{STATS_FOR_NERDS}
	</br>
	</p>
	{BOARD}
	</form>
	</div>
	</body>
	</html>
	"""
	color = "<b3>" + ("White" if player=="w" else "Black") + "</b3>"
	ai_difficulty = "<div class='switch-toggle dif_select_div'>"
	ai_difficulty += "<input id='easy' name='difficulty' value='easy' type='radio'" + ("checked='checked'" if difficulty=="easy" else '') + "/>"
	ai_difficulty += "<label for='easy'>Easy</label>"
	ai_difficulty += "<input id='medium' name='difficulty' value='medium' type='radio' " + ("checked='checked'" if difficulty=="medium" else '') + "/>"
	ai_difficulty += "<label for='medium'>Medium</label>"
	ai_difficulty += "<input id='hard' name='difficulty' value='hard' type='radio' " + ("checked='checked'" if difficulty=="hard" else '') + "/>"
	ai_difficulty += "<label for='hard'>Hard</label></br></br>"
	ai_difficulty += "<p class='dif_desc_p' id='easy-description'>play against the AI using only a minmax algorithm with depth=2</p>"
	ai_difficulty += "<p class='dif_desc_p' id='medium-description'>play against the AI a minmax algorithm with depth=4 and a weighted evaluate function</p>"
	ai_difficulty += "<p class='dif_desc_p' id='hard-description'>play against the AI a minmax algorithm with depth=6 and a weighted evaluate function</p>"
	ai_difficulty += "</div>"
	ai_difficulty += "<div class='switch-toggle statsfornerds'>"
	ai_difficulty += "<input id='on' name='statsfornerds' value='on' type='radio'" + ("checked='checked'" if statsfornerds else '') + "/>"
	ai_difficulty += "<label for='on'>On</label>"
	ai_difficulty += "<input id='off' name='statsfornerds' value='off' type='radio'" + ("checked='checked'" if (not statsfornerds) else '') + "/>"
	ai_difficulty += "<label for='off'>Off</label>"
	ai_difficulty += "</br></br></br><a class='sfn_desc_p'>enable stats for nerds (lots o' numbers!)</a>"
	ai_difficulty += "</div>"
	board = "<a href='othello.py?difficulty=easy&statsfornerds=off&history=D&move=&player=w'>Play as white</a><table>" if (len(history)==0 and len(new_move)==0) else "<table>"
	board += "<input type='hidden' value='" + history + "' name='history' id='history'>"
	board += "<input type='hidden' value='" + player + "' name='player' id='history'>"
	over = True
	for i in range(8):
		board += "<tr>"
		for j in range(8):
			board += "<th>"
			if move(game,i*8+j):
				game_over = False
				board += "<button class='valid' type='submit' name='move' value='" + chr(i*8+j+ord('1')) + "'><img src='Valid.bmp'></button>"
				over = False
				continue;
			board += "<div><img src='"
			if history and (ord(history[-1])-ord('1'))==i*8+j:
				board += "BlackRecent" if game[(ord(history[-1])-ord('1'))]=="b" else "WhiteRecent"
			else:
				board += "Black" if game[i*8+j]=="b" else ("White" if game[i*8+j]=="w" else "Empty")
			board += ".bmp'></div>"
			board += "</th>"
		board += "</tr>"
	if over:
		final_score = evaluate(game)
		board += ("Black wins by " + str(final_score) + " points!!") if final_score>0 else ("White wins by " + str(-final_score) + " points!!")

	if statsfornerds:
		sfn_page = "<div class='sfn'>"
		sfn_page += "<a class='sfn_a'>Stats for Nerds:</a></br></br></br>"
		end = time.time()
		sfn_page += "<b5>Time elapsed for calculations:</b5></br><v5>" + str(int((end-start)*1000)) + "ms</v5>"
		sfn_page += "</br><b5>Theoretical amount of games checked:</b5></br><v5>" + str(sfn_data["theoretical_amount"]) + "</v5>"
		sfn_page += "</br><b5>Actual number of games checked:</b5></br><v5>" + str(sfn_data["games_checked"]) + "(" + str(int(100000000*sfn_data["games_checked"]/sfn_data["theoretical_amount"])/1000000) + "%)</v5>"
		if sfn_data["games_checked"]:
			sfn_page += "</br><b5>Time elapsed for calculations</br>per game:</b5></br><v5>" + str(int((end-start)*1000000/sfn_data["games_checked"])) + "ns</v5>"
		if sfn_data["valid_games_checked"]:
			sfn_page += "</br><b5>Time elapsed for calculations</br>per valid game:</b5></br><v5>" + str(int((end-start)*1000000/sfn_data["valid_games_checked"])) + "ns</v5>"
		if sfn_data["games_checked"]:
			sfn_page += "</br><b5>Number of valid games checked:</b5></br><v5>" + str(sfn_data["valid_games_checked"]) + "(" + str(int(100*sfn_data["valid_games_checked"]/sfn_data["games_checked"]))+ "%)</v5>"
			sfn_page += "</br><b5>Potential number of games skipped</br>using AB pruning:</b5></br><v5>" + str(sfn_data["ab_skipped"]) + "(" + str(int(1000000*sfn_data["ab_skipped"]/(sfn_data["games_checked"]+sfn_data["ab_skipped"]))/10000)+ "%)</v5>"
		sfn_page += "</br><b5>Predicted actual number of games</br>skipped using AB pruning:</b5></br><v5>" + str(int(sfn_data["games_checked"]*100/7)) + "(93%)</v5>" #this number is just a finding that i made. Typically the amount of games checked is 1400% higher without AB pruning
		sfn_page += "</div>"
		page = page.replace('{STATS_FOR_NERDS}',sfn_page)
	else:
	   page = page.replace('{STATS_FOR_NERDS}','')
	page = page.replace('{COLOR}',color)
	page = page.replace('{AI_DIFFICULTY}',ai_difficulty)
	page = page.replace('{BOARD}',board)
	return page
form = cgi.FieldStorage() 
print(generate_page(form.getvalue('history') if form.getvalue('history') else '',form.getvalue('player'),form.getvalue('move') if form.getvalue('move') else '',form.getvalue('difficulty'),form.getvalue('statsfornerds')=="on"))