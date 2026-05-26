import combat
# Text Adventure Game
# A simple text adventure game
# --- Setup Items and Quests ---
potion = combat.Item("Health Potion", "Restores 10 HP", "heal", 10)
buff = combat.Item("Attack Potion", "Adds 3 attack power", "attack_boost", 3)

# Define the quest globally so it exists for the whole game
rat_quest = combat.Quest("Rat Tails", "Kill 5 rats", 5)
# Pass the stats into the Player class constructor
# The parameters are: name, health, attack, defense, accuracy, critical_chance
# battle functions
def respawn(player):
    print("\n" + "!" * 40)
    print("      YOU HAVE BEEN DEFEATED!       ")
    print("!" * 40 + "\n")
    player.health = player.max_health
    input("Press Enter to wake up at home...")
    return 'your house'
def play_forest(player):
    print('You explore the forest more and encounter a wild boar!')
    boar = combat.Enemy("Boar", 20, 10, 6, 0.75, 0.2, 3) # The last parameter is the level of the enemy
    # Call your combat loop
    # Note: You don't need the ': dict' parts here when calling it!
    win = combat.combat_loop(player, boar, [], [])
    if win: return 'starter village' # Go back to safety
    else: return respawn(player) # Respawn the player if they lose
def play_rat_battle(player, rat_quest):
    print('You enter the old man\'s shed and see a swarm of rats!')
    rat = combat.Enemy("Rat", 10, 3, 1, 0.7, 0.05, 1) # A weak enemy for the quest
    win = combat.combat_loop(player, rat, [], [], rat_quest)
    if win: return 'quest' # Go back to the quest room to update progress
    else: return respawn(player) # Respawn the player if they lose
def display_location(location : str) -> None :
    print(f'You are currently in {location}')

# text functions
def draw_header(title):
    print("========================================")
    print(f" {title.upper().center(36)} ")
    print("========================================")

def show_status(player):
    # Make sure your player class has a 'gold' attribute
    print(f" HP: {player.health}/{player.max_health} | Gold: {getattr(player, 'gold', 0)} ")
    print("-" * 40)

def talk(npc_name, text):
    print(f"\n--- {npc_name.upper()} ---")
    print(f"'{text}'")
    input("\n[Press Enter to continue]")
    print("\n" * 2)

# rooms a lot of rooms
def room_starter_village(player):
    draw_header("Oakhaven")
    show_status(player)
    
    print("The village is quiet. The Corruption is thick in the air.")
    print("\nSelect an action:")
    print(" [1] Old Man's House")
    print(" [2] Whispering Forest")
    print(" [3] Trade Road")
    print(" [4] Go Home")
    print(" [5] Village Square")
    print("========================================")
    
    choice = input(" > ").strip()
    
    if choice == '1': return 'old man\'s house'
    if choice == '2': return 'forest'
    if choice == '3': return 'merchant_road'
    if choice == '4': return 'your house'
    if choice == '5': return 'village_square'
    return 'starter village'

def room_village_square(player):
    draw_header("Village Square")
    show_status(player)
    print('You are in the village square.')
    print('Villagers are going about their day,')
    print('but they seem wary of you.')
    print('1: Talk to the blacksmith')
    print('2: Talk to the farmer')
    print('3: Go back')
    
    choice = input("Choice: ")
    
    if choice == '1':
        talk("Blacksmith", "I don't trust outsiders, but I can tell you that the Blight is getting worse.")
        return 'village_square'
    elif choice == '2':
        talk("Farmer", "The crops are failing and the animals are sick. It's like something is poisoning the land.")
        return 'village_square'
    elif choice == '3': return 'starter village'

def room_old_mans_house(player):
    draw_header("Old Man's House")
    show_status(player) 
    print('You are in the old man\'s house.')
    print(f'what do you want to do?')
    print('1: Talk to the old man')
    print('2: Go back')
    
    action = input("choice : ").strip().lower()
    if action == '1': return 'quest'
    elif action == '2': return 'starter village'
    return 'old man\'s house'
def room_your_house(player):
    draw_header("Your House")
    show_status(player)
    print('You are in your own house.')
    print('1: Take a rest (restore health)')
    print('2: Go back to the village')
    action = input('choice')
    if action == '1':
        player.health = player.max_health
        print("You take a rest and restore your health.")
        return 'your house'
    elif action == '2': return 'starter village'
    return 'your house'

def room_forest(player):
    draw_header("Whispering Forest")
    show_status(player)
    print('You are in a dense forest.')
    print('1: Explore the forest')
    print('2: Go back')
    action = input('choice : ')
    if action == '1':
        play_forest(player)
        return 'forest battle'
    elif action == '2':
        return 'starter village'
    
def room_old_man(player, quest):
    draw_header("Old Man's House")
    show_status(player)
    print('You are talking to the old man.')
    if quest.is_completed:
        talk("Old Man", "Thank you so much for your help! Here is your reward.")
        # reward the player with XP and an item
        player.gain_xp(50)
        player.add_item(combat.Item("Gold Coin", "A shiny gold coin", "currency", 100))
        return 'old man\'s house'
    
    elif quest.started:
        talk("Old Man", f"How are those rats coming along? You've cleared {quest.progress}/{quest.target_amount} of them.")
        print("1: Enter the Shed to hunt rats")
        print("2: Go back")
        choice = input("Choice: ")
        if choice == '1':
            play_rat_battle(player, rat_quest)
            return 'quest'
        return 'old man\'s house'
    else:
        print('The old man looks at you with tired eyes.')
        print('1: Ask about the quest')
        print('2: Go back')
        action = input('choice : ')
        if action == '1':
            talk("Old Man", f"Hello, {player.name}! Welcome to my house.")
            talk("Old Man", "I have a quest for you. Can you help me?")
            quest_choice : str = input('Do you want to help the old man? (1: Yes, 2: No) : ')
            if quest_choice == '1':
                    active_quest = f'Kill the rats in the old man\'s shed {quest.progress}/{quest.target_amount}'
                    talk("Old Man", f"Thank you, {player.name}! I need you to kill some rats in my shed.")
                    talk("Old Man", "They have been causing me a lot of trouble lately.")
                    talk("Old Man", "Please bring me back their tails to prove you did it.")
                    print(f'You have accepted the quest: {active_quest}')
                    quest.started = True
                    return 'quest'
            elif quest_choice == '2':
                    talk("Old Man", "Oh, that's too bad. Maybe another time.")
                    return 'old man\'s house'
            
        elif action == '2': return 'old man\'s house'
def room_shop(player):
    draw_header("Trading Post")
    show_status(player)
    talk("Merchant", "Corruption's thick today, eh? Makes people desperate. Desperate people buy supplies. Lucky for you, I'm fully stocked.")
    talk("Merchant", "What would you like to buy?")
    
    # 1. Show available wares
    print("1: Buy Health Potion (20 Gold)")
    print("2: Buy Attack Potion (30 Gold)")
    print("3: Leave shop")
    
    choice = input("Choice: ")
    # 2. Logic for purchasing
    if choice == '1':
        if player.pay_gold(20):
            player.add_item(combat.Item("Health Potion", "Restores 10 HP", "heal", 10))
            talk("Merchant", "A fine choice!")
        else:
            talk("Merchant", "You don't have enough gold for that!")
            
    elif choice == '2':
        if player.pay_gold(30):
            player.add_item(combat.Item("Attack Potion", "Adds 3 attack power", "attack_boost", 3))
            talk("Merchant", "This will help you in battle!")
        else:
            talk("Merchant", "Come back when you have more gold.")
            
    elif choice == '3': return 'starter village'
        
    # Stay in the shop if we didn't leave
    return 'shop'
def room_merchant_road(player):
    draw_header("Merchant Road")
    show_status(player)
    print("You are on the Merchant Road, a path that leads to the nearby town.")
    print('you see a merchant wagon parked by the side of the road.')
    print("1: Walk towards the town")
    print('2: Talk to the merchant')
    print("3: Go back to the village")
    
    choice = input("Choice: ")
    
    if choice == '1':
        print("As you walk down the road, you are ambushed by bandits!")
        bandit = combat.Enemy("Bandit", 15, 7, 3, 0.6, 0.1, 2)
        win = combat.combat_loop(player, bandit, [], [])
        if win:
            print("You defeated the bandits and continue towards the town.")
            return 'merchant_road' # none for now, add town later
        else: return respawn(player)
    elif choice == '2': return 'shop'
    elif choice == '3': return 'starter village'
def main_menu():
    print("================================")
    print("   WELCOME TO Beyond The Gate   ")
    print("================================")
    print("   A text-based adventure game  ")
    print("1: Start Game")
    print("2: Exit")
    
    choice = input("\n[Enter number to select] > ").strip()
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
    'quest': room_old_man,
    'shop': room_shop,
    'village_square': room_village_square,
    'merchant_road': room_merchant_road
}
def run_game():
    current_location = 'starter village'
    player = combat.Player(input('Enter name: '), 25, 5, 3, 0.8, 0.1,)
    while True:
        # Get the function associated with the current location
        room_function = room_map.get(current_location)
        
        if room_function:
            # Check if the room is the quest room, which needs the extra 'rat_quest' argument
            if current_location == 'quest':
                current_location = room_function(player, rat_quest)
            elif current_location == 'shop':
                current_location = room_function(player)
            else:
                current_location = room_function(player)
        else:
            print("Error: You are lost in the void!")
            break
if __name__ == "__main__":
    if main_menu():
        run_game()