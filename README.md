# MTG Database
 A simple, local database of all my Magic: The Gathering Cards


## Anatomy of a card

This is an image of a colorless creature card known as "Palladium Myr". This card is a great example of the layout of MTG cards.

![Palladium Myr MTG](palladium-myr-som.png)

Now explaining everything here would require an in depth explanation of MTG but, as you can see, at the very top, there is a name next to a number. 
This number is how much it costs to cast this creature.

Beneath the image is the term "Artifact Creature - Myr" as well as a symbol towards the right. The first bit is an explanation of the creature, it's type and subtype
(formatted as "{Type} - {Subtype}"). The symbol represents what set this specific card was a part of.

There is also an activatable ability in the large box at the bottom. Underneath that ability is some italic text, this is known as the "flavor text".
This text brings some lore and story to cards.

Finally the last box with "2/2" explains how powerful the card is. It can deal 2 damage (left) and has 2 life (right).


## Goals

#### **WIP goals**

- [ ] The first goal is to find a way to properly store the information needed for each card


- [ ] The next goal is to simplify the way to input names of cards. This may end up looking like a text file where I manually input names of cards and read that text file as the input.

#### Stretch goals
- [ ] Create or find a way to view the database or somehow search through it.

<br>

### The end goal will be to make a universal tool that can database MTG cards and can be used by many.

## Tools Used

### This databasing tool will utilize the following PiPy packages: 

*(This list may be appended or changed until I am satisfied with the project)*


| Name         | Command for pip    |
|--------------|--------------------|
| mtgsdk 1.3.1 | pip install mtgsdk |
| TinyDB 4.6.1 | pip install tinydb |


## Running journal

### 2/10/22 13:07
 - Initialized active GitHub repo
