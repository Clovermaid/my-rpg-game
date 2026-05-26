import random

class Enemy:
    def __init__(self, name, health, attack, defense, accuracy, critical_chance, level):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.accuracy = accuracy
        self.critical_chance = critical_chance
        self.defending = False
        self.base_attack = attack
        self.level = level
class Item:
    def __init__(self, name, description, item_type, value):
        self.name = name
        self.description = description
        self.item_type = item_type  # e.g., "heal", "attack_boost", "defense_boost", "weapon", "armor"
        self.value = value

class Quest:
    def __init__(self, name, description, target_amount):
        self.name = name
        self.description = description
        self.target_amount = target_amount
        self.progress = 0
        self.started = False
        self.is_completed = False

    def update_progress(self, amount):
        if not self.is_completed:
            self.progress += amount
            print(f"Quest updated: {self.progress}/{self.target_amount} {self.name} completed.")
            if self.progress >= self.target_amount:
                self.is_completed = True
                print(f"Quest Complete! Return to the {self.name}.")
    
    def reset_progress(self):
        self.progress = 0
        self.is_completed = False

class Player:
    def __init__(self, name, health, attack, defense, accuracy, critical_chance,):
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
        self.equipped_weapon = None 
        self.equipped_armor = None
        self.xp = 0
        self.level = 1

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Added {item.name} to your inventory!")
        

    def show_inventory(self):
        print("\n--- Inventory ---")
        if not self.inventory:
            print("Your bag is empty.")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}: {item.name} - {item.description}")

    def equip_item(self, item):
        # 1. Handle Un-equipping first (The "Clean Swap")
        if item.item_type == "weapon" and self.equipped_weapon:
            self.unequip_item(self.equipped_weapon)
        elif item.item_type == "armor" and self.equipped_armor:
            self.unequip_item(self.equipped_armor)

        # 2. Handle Equipping (The shared logic)
        if item.item_type == "weapon":
            self.equipped_weapon = item
            self.attack = self.base_attack + item.value
        elif item.item_type == "armor":
            self.equipped_armor = item
            self.defense += item.value

        print(f"Equipped {item.name}!")

    def unequip_item(self, item):
        if item.item_type == "weapon" and self.equipped_weapon == item:
            self.equipped_weapon = None
            self.attack = self.base_attack
            print(f"Unequipped {item.name}.")
        elif item.item_type == "armor" and self.equipped_armor == item:
            self.equipped_armor = None
            self.defense -= item.value
            print(f"Unequipped {item.name}.")

    def show_equipment(self):
        print("\n--- Current Equipment ---")
        weapon_name = self.equipped_weapon.name if self.equipped_weapon else "None"
        armor_name = self.equipped_armor.name if self.equipped_armor else "None"
        print(f"Weapon: {weapon_name}")
        print(f"Armor: {armor_name}")
    
    def gain_xp(self, amount):
        self.xp += amount
        print(f"Gained {amount} XP! Total XP: {self.xp}")
        
        while self.xp >= self.level * 100:  # Example XP threshold for leveling up
            self.xp -= self.level * 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.base_attack += 2
        self.defense += 1
        print(f"You leveled up to level {self.level}!")

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

def combat_loop(player, enemy, player_effects, enemy_effects, quest=None):
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
                if item.item_type == "heal":
                    player.health = min(player.max_health, player.health + item.value)
                    print(f"You used {item.name} and restored {item.value} health.")
                elif item.item_type == "attack_boost":
                    player.attack += item.value
                    print(f"You used {item.name} and gained {item.value} attack.")
                player.inventory.remove(item)
        elif action == '4':
            player.show_equipment()
                
        if enemy.health <= 0:
            print("You won!")
            player.gain_xp(enemy.level * 20) # the player gains XP based on the enemy's level
            if quest:
                quest.update_progress(1) # Update the quest progress by 1 for each enemy defeated
            return True
            
        # Enemy Phase
        perform_attack(enemy, player)
        
        if player.health <= 0:
            print("You lost!")
            return False
        turns += 1