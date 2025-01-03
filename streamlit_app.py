import streamlit as st
import random
import json
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class Character:
    name: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    gold: int
    exp: int
    level: int
    inventory: List[str]

@dataclass
class Enemy:
    name: str
    hp: int
    attack: int
    defense: int
    gold: int
    exp: int

class Game:
    def __init__(self):
        if 'character' not in st.session_state:
            st.session_state.character = Character(
                name="Hero",
                hp=100,
                max_hp=100,
                attack=10,
                defense=5,
                gold=0,
                exp=0,
                level=1,
                inventory=["Potion"]
            )
        
        self.enemies = {
            'Slime': Enemy("Slime", 30, 5, 2, 5, 10),
            'Goblin': Enemy("Goblin", 45, 8, 3, 10, 15),
            'Wolf': Enemy("Wolf", 60, 12, 4, 15, 20),
            'Dragon': Enemy("Dragon", 200, 25, 15, 100, 200)
        }
        
        self.items = {
            'Potion': {'type': 'heal', 'value': 30, 'cost': 10},
            'Sword': {'type': 'attack', 'value': 5, 'cost': 50},
            'Shield': {'type': 'defense', 'value': 3, 'cost': 40}
        }

    def level_up_check(self):
        exp_needed = st.session_state.character.level * 100
        if st.session_state.character.exp >= exp_needed:
            st.session_state.character.level += 1
            st.session_state.character.max_hp += 20
            st.session_state.character.hp = st.session_state.character.max_hp
            st.session_state.character.attack += 5
            st.session_state.character.defense += 3
            st.session_state.character.exp -= exp_needed
            return True
        return False

    def battle(self, enemy_name: str) -> str:
        enemy = self.enemies[enemy_name]
        enemy_hp = enemy.hp
        
        while enemy_hp > 0 and st.session_state.character.hp > 0:
            # Player attack
            damage = max(0, st.session_state.character.attack - enemy.defense)
            enemy_hp -= damage
            
            if enemy_hp <= 0:
                st.session_state.character.gold += enemy.gold
                st.session_state.character.exp += enemy.exp
                leveled_up = self.level_up_check()
                
                result = f"Won! Gained {enemy.gold} gold and {enemy.exp} exp."
                if leveled_up:
                    result += f"\nLevel Up! Now level {st.session_state.character.level}"
                return result
            
            # Enemy attack
            damage = max(0, enemy.attack - st.session_state.character.defense)
            st.session_state.character.hp -= damage
            
            if st.session_state.character.hp <= 0:
                st.session_state.character.hp = 1
                st.session_state.character.gold = max(0, st.session_state.character.gold - 10)
                return "Defeated! Lost 10 gold..."

    def use_item(self, item: str) -> str:
        if item not in st.session_state.character.inventory:
            return "Don't have this item!"
        
        st.session_state.character.inventory.remove(item)
        
        if item == 'Potion':
            heal = min(
                self.items[item]['value'],
                st.session_state.character.max_hp - st.session_state.character.hp
            )
            st.session_state.character.hp += heal
            return f"Healed {heal} HP!"
            
        elif item == 'Sword':
            st.session_state.character.attack += self.items[item]['value']
            return f"Attack increased by {self.items[item]['value']}!"
            
        elif item == 'Shield':
            st.session_state.character.defense += self.items[item]['value']
            return f"Defense increased by {self.items[item]['value']}!"

    def buy_item(self, item: str) -> str:
        if item not in self.items:
            return "Item doesn't exist!"
            
        if st.session_state.character.gold < self.items[item]['cost']:
            return "Not enough gold!"
            
        st.session_state.character.gold -= self.items[item]['cost']
        st.session_state.character.inventory.append(item)
        return f"Bought {item}!"

def main():
    st.title("Streamlit RPG")
    
    game = Game()
    char = st.session_state.character

    # Main game interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Character")
        st.write(f"Level: {char.level}")
        st.write(f"HP: {char.hp}/{char.max_hp}")
        st.write(f"Attack: {char.attack}")
        st.write(f"Defense: {char.defense}")
        st.write(f"Gold: {char.gold}")
        st.write(f"EXP: {char.exp}/{char.level * 100}")
        
        st.subheader("Inventory")
        for item in char.inventory:
            if st.button(f"Use {item}"):
                result = game.use_item(item)
                st.write(result)
    
    with col2:
        st.subheader("Shop")
        for item, details in game.items.items():
            cost = details['cost']
            if st.button(f"Buy {item} ({cost} gold)"):
                result = game.buy_item(item)
                st.write(result)
    
    st.subheader("Battle")
    for enemy_name in game.enemies:
        if st.button(f"Fight {enemy_name}"):
            result = game.battle(enemy_name)
            st.write(result)

    # Save button
    if st.button("Save Game"):
        save_data = {
            'name': char.name,
            'hp': char.hp,
            'max_hp': char.max_hp,
            'attack': char.attack,
            'defense': char.defense,
            'gold': char.gold,
            'exp': char.exp,
            'level': char.level,
            'inventory': char.inventory
        }
        st.download_button(
            "Download Save File",
            data=json.dumps(save_data),
            file_name="rpg_save.json"
        )

if __name__ == "__main__":
    main()
