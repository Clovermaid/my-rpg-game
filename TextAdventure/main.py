import combat
# Text Adventure Game
# A simple text adventure game
# --- Setup Items and Quests ---
potion = combat.Item("Health Potion", "Restores 10 HP", "heal", 10)
buff = combat.Item("Attack Potion", "Adds 3 attack power", "attack_boost", 3)

# Define the quest globally so it exists for the whole game
rat_quest = combat.Quest("Rat Tails", "Kill 5 rats", 5)

npc_name : str = 'old man'
# Pass the stats into the Player class constructor
# The parameters are: name, health, attack, defense, accuracy, critical_chance
# battle functions
def play_forest(player):
    print('You explore the forest more and encounter a wild boar!')
    boar = combat.Enemy("Boar", 20, 10, 6, 0.75, 0.2, 3) # The last parameter is the level of the enemy
    # Call your combat loop
    # Note: You don't need the ': dict' parts here when calling it!
    win = combat.combat_loop(player, boar, [], [])
    if win:
        return 'starter village' # Go back to safety
    else:
        # Maybe restart or game over logic?
        return 'your house'
def play_rat_battle(player, rat_quest):
    print('You enter the old man\'s shed and see a swarm of rats!')
    rat = combat.Enemy("Rat", 10, 3, 1, 0.7, 0.05, 1) # A weak enemy for the quest
    win = combat.combat_loop(player, rat, [], [], rat_quest)
    if win:
        return 'quest' # Go back to the quest room to update progress
    else:
        return 'your house' # Go back to safety
def display_location(location : str) -> None :
    print(f'You are currently in {location}')
def dialogue(npc_name : str, dialogue : str) -> None :
    print(f'{npc_name} ; "{dialogue}"')
# rooms a lot of rooms
def room_starter_village(player):
    print('You are in a small village.')
    action = input('what do you want to do? (1: Go to house, 2: Forest, 3: Go to old man\'s house) : ')
    if action == '1':
        return 'your house'
    elif action == '2':
        return 'forest'
    elif action == '3':
        return 'old man\'s house'
    return 'starter village'
def room_old_mans_house(player):
    print('You are in the old man\'s house.')
    print(f'what do you want to do? (1: Talk to the old man, 2: Go back) : ')
    action = input("What do you want to do? ").strip().lower()
    if action == '1':
        return 'quest'
    elif action == '2':
        return 'starter village'
    return 'old man\'s house'
def room_your_house(player):
    print('You are in your own house.')
    action = input(f'{player.name}, what do you want to do? (1: Rest, 2: Go back) : ')
    if action == '1':
        player.health = player.max_health
        print("You take a rest and restore your health.")
        return 'your house'
    elif action == '2':
        return 'starter village'
    return 'your house'
def room_forest(player):
    print('You are in a dense forest.')
    action = input(f'{player.name}, what do you want to do? (1: Explore the forest, 2: Go back) : ')
    if action == '1':
        play_forest(player)
        return 'forest battle'
    elif action == '2':
        return 'starter village'
def room_old_man(player, quest):
    print('You are talking to the old man.')
    if quest.is_completed:
        dialogue(npc_name, "Thank you so much for your help! Here is your reward.")
        # reward the player with XP and an item
        player.gain_xp(50)
        player.add_item(combat.Item("Gold Coin", "A shiny gold coin", "currency", 100))
        return 'old man\'s house'
    
    elif quest.started:
        dialogue(npc_name, f"How are those rats coming along? You've cleared {quest.progress}/{quest.target_amount} of them.")
        print("1: Enter the Shed to hunt rats")
        print("2: Go back")
        choice = input("Choice: ")
        if choice == '1':
            play_rat_battle(player, rat_quest)
            return 'quest'
        return 'old man\'s house'
    else:
        action = input(f'{player.name}, what do you want to do? (1: Accept quest, 2: Go back) : ')
        if action == '1':
            dialogue(npc_name, f"Hello, {player.name}! Welcome to my house.")
            dialogue(npc_name, "I have a quest for you. Can you help me?")
            quest_choice : str = input('Do you want to help the old man? (1: Yes, 2: No) : ')
            if quest_choice == '1':
                    active_quest = f'Kill the rats in the old man\'s shed {quest.progress}/{quest.target_amount}'
                    dialogue(npc_name, f"Thank you, {player.name}! I need you to kill some rats in my shed.")
                    dialogue(npc_name, "They have been causing me a lot of trouble lately.")
                    dialogue(npc_name, "Please bring me back their tails to prove you did it.")
                    print(f'You have accepted the quest: {active_quest}')
                    quest.started = True
                    return 'quest'
            elif quest_choice == '2':
                    dialogue(npc_name, "Oh, that's too bad. Maybe another time.")
                    return 'old man\'s house'
            
        elif action == '2':        
            return 'old man\'s house'
def main_menu():
    print("================================")
    print("   WELCOME TO THE TEXT ADVENTURE")
    print("================================")
    print("1: Start Game")
    print("2: Exit")
    
    choice = input("Enter your choice: ")
    if choice == '1':
        return True # Continue to the game
    else:
        print("Goodbye!")
        return False # Exit the program
room_map = {
    'starter village': room_starter_village,
    'old man\'s house': room_old_mans_house,
    'your house': room_your_house,
    'forest': room_forest,
    'quest': room_old_man
}
def run_game():
    current_location = 'starter village'
    player = combat.Player(input('Enter name: '), 25, 5, 3, 0.8, 0.1,)
    player.add_item(potion)
    player.add_item(buff)
    while True:
        # Get the function associated with the current location
        room_function = room_map.get(current_location)
        
        if room_function:
            # Check if the room is the quest room, which needs the extra 'rat_quest' argument
            if current_location == 'quest':
                current_location = room_function(player, rat_quest)
            else:
                current_location = room_function(player)
        else:
            print("Error: You are lost in the void!")
            break
if __name__ == "__main__":
    if main_menu():
        run_game()