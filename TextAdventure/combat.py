import random

class Enemy:
    def __init__(self, name, health, attack, defense, accuracy, critical_chance):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.accuracy = accuracy
        self.critical_chance = critical_chance
        self.defending = False
        self.base_attack = attack
class Item:
    def __init__(self, name, description, effect_type, value):
        self.name = name
        self.description = description
        self.effect_type = effect_type  # "heal" or "attack_boost"
        self.value = value
    
class Player:
    def __init__(self, name, health, attack, defense, accuracy, critical_chance):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.accuracy = accuracy
        self.critical_chance = critical_chance
        self.defending = False
        self.base_attack = attack
        self.inventory = [] # This is the "backpack"

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Added {item.name} to your inventory!")
        

    def show_inventory(self):
        print("\n--- Inventory ---")
        if not self.inventory:
            print("Your bag is empty.")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}: {item.name} - {item.description}")

def damage_calculator(attacker, defender):
    damage = attacker.attack - defender.defense
    return max(0, damage)

def display_stats(player, enemy):
    print(f'Player Health: {player.health}/{player.max_health}')
    print(f'Enemy Health: {enemy.health}/{enemy.max_health}')

def perform_attack(attacker, defender):
    if random.random() < attacker.accuracy:
        damage = damage_calculator(attacker, defender)
        if defender.defending:
            damage //= 2
            print(f'{defender.name} defends!')
        
        if random.random() < attacker.critical_chance:
            damage *= 2
            print("Critical hit!")
            
        defender.health -= damage
        print(f'{attacker.name} attacks and deals {damage} damage!')
    else:
        print(f'{attacker.name} missed!')
    attacker.defending = False

def combat_loop(player, enemy, player_effects, enemy_effects):
    print('Prepare for battle!')
    print(f'A wild {enemy.name} appears!')
    
    turns = 0
    while player.health > 0 and enemy.health > 0:
        print(f"\nTurn {turns + 1}")
        display_stats(player, enemy)
        
        # Player Phase
        action = input('Choose (1: Attack, 2: Defend, 3: Use Item): ')
        if action == '1':
            perform_attack(player, enemy)
        elif action == '2':
            player.defending = True
            print("You brace for impact!")
        elif action == '3':
            player.show_inventory()
            item_choice = input("Choose an item to use (1, 2, ...): ")
            if item_choice.isdigit() and 1 <= int(item_choice) <= len(player.inventory):
                item = player.inventory[int(item_choice) - 1]
                if item.effect_type == "heal":
                    player.health = min(player.max_health, player.health + item.value)
                    print(f"You used {item.name} and restored {item.value} health.")
                elif item.effect_type == "attack_boost":
                    player.attack += item.value
                    print(f"You used {item.name} and gained {item.value} attack.")
                player.inventory.remove(item)
                
        if enemy.health <= 0:
            print("You won!")
            return True
            
        # Enemy Phase
        perform_attack(enemy, player)
        
        if player.health <= 0:
            print("You lost!")
            return False
        turns += 1