#!/usr/bin/python
from string import ascii_letters
import random

true={}
with open('true.txt') as f:
    for x in f.read().strip().split('\n'):
        x = x.split(':')
        if x[0] not in true: true[x[0]]=set()
        true[x[0]].add(x[1])
false={}
with open('false.txt') as f:
    for x in f.read().strip().split('\n'):
        x = x.split(':')
        if x[0] not in false: false[x[0]]=set()
        false[x[0]].add(x[1])

all = true.copy()
for s in false:
    all[s] = all[s] | false[s]

def stage_capitals():
    state, capital = random.choice(true.items())
    capital=list(capital)[0]
    options=true[state].copy()
    while len(options)<2:
        options = options | random.choice(true.items())[1]
    while len(options)<3:
        options.add(random.choice(tuple(false[state])))
    while len(options)<5:
        options.add(random.choice(tuple(random.choice(all.items())[1])))
    options = list(options)
    random.shuffle(options)
    print("Selected state is:\t%s" % state)
    for n,o in enumerate(options):
        print('%s:\t\t%s' % (n+1,o))
    return str(options.index(capital)+1)

def stage_states():
    not_capital=0.25
    not_state=0.25
    fakeout=False
    fakestate=False
    if random.random() > not_capital: fakeout=True
    elif random.random() > not_state: fakestate=True
    if fakeout:
        state, capital = random.choice(false.items())
    else:
        state, capital = random.choice(true.items())
    capital=list(capital)[0]
    options=set([state])
    while len(options)<4:
        options.add(random.choice(true.items())[0])
        if fakestate:
            if state in options: options.remove(state)
    options = list(options)
    random.shuffle(options)
    print("Selected city is:\t%s" % capital)
    for n,o in enumerate(options):
        print('%s:\t\t%s' % (n+1,o))
    print('5:\t\tNone of the above')
    if fakestate or fakeout:
       return str(5)
    return str(options.index(state)+1)

def stage_state_spelling():
    state, capital = random.choice(true.items())
    capital = tuple(capital)[0]
    print("Selected capital is:\t%s" % capital)
    blanks = state[:]
    for l in ascii_letters:
        blanks = blanks.replace(l,'_') 
    print("Fill in the missing state:\t%s" % ' '.join(blanks))
    return state

def stage_cap_spelling():
    state, capital = random.choice(true.items())
    capital = tuple(capital)[0]
    print("Selected state is:\t%s" % state)
    blanks = capital
    for l in ascii_letters:
        blanks = blanks.replace(l,'_') 
    print("Fill in the missing capital:\t%s" % ' '.join(blanks))
    return capital

def game_loop():
    score=0
    stages=[stage_capitals,
          stage_capitals,
          stage_capitals,
          stage_capitals,
          stage_state_spelling,
          stage_states,
          stage_states,
          stage_states,
          stage_cap_spelling,
          stage_cap_spelling]
    for stage in stages:
        print('Your current score is: %s' % score)
        answer = stage()
        a = raw_input(">> ")
        if a.lower() == answer.lower():
            print('Correct.')
            score += 1
        else:
            print('Not correct. The correct answer was:\t%s' % answer)
    print('Game Over. Your score is %s of %s' % (score, len(stages)))

if __name__ == '__main__':
    game_loop()
