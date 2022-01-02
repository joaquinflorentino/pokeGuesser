import requests
import json
import random

POKE_URL = 'https://pokeapi.co/api/v2/pokemon/'
TOTAL_POKEMON_COUNT = 898

pokemonPerGen = {
        '1': range(1, 152),
        '2': range(152, 252),
        '3': range(252, 387),
        '4': range(387, 494),
        '5': range(494, 650),
        '6': range(650, 722),
        '7': range(722, 810),
        '8': range(810, 899)
    }

def main(gameLoop, exclude):
    while gameLoop:
        randNum = randomNumber(exclude)
        pokemonInfo = retrievePokemonInfo(str(randNum))
        pokemonContent = pokemonInfo['content']
        name = pokemonContent['name']

        guess = input('What Pokemon is #' + str(randNum) + ' ').lower()

        if guess == name:
            print('Correct!')
        else:
            print('Incorrect. The Pokemon is ' + str(name))
            pokemonInfo = retrievePokemonInfo(guess)
            pokemonContent = pokemonInfo['content']
            statusCode = pokemonInfo['statusCode']

            if guess != '' and statusCode == 200:
                pokemonId = pokemonContent['id']
                print(guess + ' is #' + str(pokemonId) + '. You were ' + str(abs(randNum - pokemonId)) + ' Pokemon off')
            else:
                print('The Pokemon you guessed does not exist')

        answer = input('To play again, hit Enter. To terminate the program, enter the word no ').lower()
        if answer == 'no':
            gameLoop = False

def retrievePokemonInfo(pokemonId):
    res = requests.get(POKE_URL + pokemonId)
    resContent = json.loads(res.content) if res.status_code == 200 else None
    response = {
        'content': resContent,
        'statusCode': res.status_code
    }
    return response

def randomNumber(gens):
    tempGens = gens.split(',')

    if tempGens == ['']:
        exclude = []
    else:
        exclude = [pokemonPerGen[i] for i in tempGens]

    randNum = random.randrange(1, TOTAL_POKEMON_COUNT + 1)

    for i in exclude:
        if randNum in i:
            return randomNumber(gens)
    return randNum

def validGens(inp):
    tempInp = inp.split(',')
    genNums = list(pokemonPerGen.keys())

    if tempInp == ['']:
        return True

    for i in tempInp:
        if i not in genNums:
            return False
    return len(tempInp) < 8

if __name__ == '__main__':
    askedInput = True
    while askedInput:
        gensExcluded = input('Which generations do you want to exclude? (Type in this format: 5,6,7,8) Hit Enter if you want to include all generations')

        if not validGens(gensExcluded):
            print('Invalid input.')
            continue
        else:
            askedInput = False
    main(True, gensExcluded)
