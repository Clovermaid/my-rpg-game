import combat
# Text Adventure Game
# A simple text adventure game
npc_name : str = 'old man'
# Pass the stats into the Player class constructor
# The parameters are: name, health, attack, defense, accuracy, critical_chance
player = combat.Player(input('Enter name: '), 25, 5, 3, 0.8, 0.1)
def play_forest():
    print('You explore the forest more and encounter a wild boar!')
    boar = combat.Enemy("Boar", 20, 10, 6, 0.75, 0.2)      
    # Call your combat loop
    # Note: You don't need the ': dict' parts here when calling it!
    win = combat.combat_loop(player, boar, [], [])
    if win:
        return 'starter village' # Go back to safety
    else:
        # Maybe restart or game over logic?
        return 'your house'
def display_location(location : str) -> None :
    print(f'You are currently in {location}')
def dialogue(npc_name : str, dialogue : str) -> None :
    print(f'{npc_name} ; "{dialogue}"')
progress : int = 0
required : int = 5
current_location : str = 'starter village'
# rooms a lot of rooms
def room_starter_village(player):
    print('You are in a small village.')
    action = input(f'{player.name}, what do you want to do? (1: Go to house, 2: Forest) : ')
    if action == '1':
        return 'your house'
    elif action == '2':
        return 'forest'
    return 'starter village'
def room_old_mans_house(player):
    print('You are in the old man\'s house.')
    action = input(f'{player.name}, what do you want to do? (1: Talk to the old man, 2: Go back) : ')
    if action == '1':
        return 'old man'
    elif action == '2':
        return 'starter village'
    return 'old man\'s house'
def room_your_house(player):
    print('You are in your own house.')
    action = input(f'{player.name}, what do you want to do? (1: Rest, 2: Go back) : ')
    if action == '1':
        return 'your house'
    elif action == '2':
        return 'starter village'
    return 'your house'
def room_forest(player):
    print('You are in a dense forest.')
    action = input(f'{player.name}, what do you want to do? (1: Explore the forest, 2: Go back) : ')
    if action == '1':
        play_forest()
        return 'forest battle'
    elif action == '2':
        return 'starter village'
def room_old_man(player):
    print('You are talking to the old man.')
    action = input(f'{player.name}, what do you want to do? (1: Accept quest, 2: Go back) : ')
    if action == '1':
        dialogue(npc_name, f"Hello, {player.name}! Welcome to my house.")
        dialogue(npc_name, "I have a quest for you. Can you help me?")
        quest_choice : str = input('Do you want to help the old man? (1: Yes, 2: No) : ')
        if quest_choice == '1':
                active_quest = f'Kill the rats in the old man\'s shed {progress}/{required}'
                dialogue(npc_name, f"Thank you, {player.name}! I need you to kill some rats in my shed.")
                dialogue(npc_name, "They have been causing me a lot of trouble lately.")
                dialogue(npc_name, "Please bring me back their tails to prove you did it.")
                print(f'You have accepted the quest: {active_quest}')
                return 'quest'
        elif quest_choice == '2':
                dialogue(npc_name, "Oh, that's too bad. Maybe another time.")
                return 'old man\'s house'
        return 'quest'
    elif action == '2':        
        return 'old man\'s house'
while True :
    if current_location == 'starter village':
        current_location = room_starter_village(player)
    elif current_location == 'old man\'s house':
        current_location = room_old_mans_house(player)
    elif current_location == 'your house': # Fixed variable
        current_location = room_your_house(player) # Added ()
    elif current_location == 'forest': # Fixed variable
        current_location = room_forest(player) # Added ()
    elif current_location == 'quest': # Fixed variable
        current_location = room_old_man(player) # Added ()