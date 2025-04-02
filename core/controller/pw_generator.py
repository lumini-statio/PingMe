import random

# function that creates a random password
def generator(length: str, mayusc: bool, especiales: bool, nums: bool):
    characters = list("abcdefghijklmnopqrstuvwxyz")
    generated_password = ""
    
    if mayusc == True:
        characters.extend(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")) #if parameter mayusc is True, extend the characters variable
    if especiales == True:
        characters.extend(list('!@#$%^&*.()')) #if parameter especiales is True, extend the characters variable
    if nums == True: 
        characters.extend(list('1234567890')) #if parameter nums is True, extend the characters variable
    
    # creates the password with an iteration in the length parameter
    for _ in range(int(length)):
            generated_password += random.choice(characters)
        
    return generated_password