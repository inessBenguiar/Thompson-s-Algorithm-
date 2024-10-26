state_counter = -1

def create_state():
    global state_counter
    state_counter += 1
    return 'S' + str(state_counter)

class FSM:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
        

def convert_to_postfix(expression):
    postfix, stack = "", ""
    operations = {'*': 4, '+': 3, '.': 2, '|': 1}
    for char in expression:
        if char == '(':
            stack += char
        elif char == ')':
            while stack[-1] != '(':
                postfix += stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]
        elif char in operations:
            while stack and operations.get(char, 0) <= operations.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack += char
        else:
            postfix += char

    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]
    return postfix


def convert_to_FSM(postfix):
    S = []
    X = []
    FSM_stack = []  
    instructions = []
    
    ## iteration case
    def process_star():
        FSM1 = FSM_stack.pop()
        initial, final = create_state(), create_state()
        instructions.append((initial, 'ε', FSM1.initial))
        instructions.append((initial, 'ε', final))
        instructions.append((FSM1.final, 'ε', FSM1.initial))
        instructions.append((FSM1.final, 'ε', final))
        S.append(initial)
        S.append(final)
        FSM_stack.append(FSM(initial, final))
    
    ## concatenation case
    def process_dot():
        FSM2, FSM1 = FSM_stack.pop(), FSM_stack.pop()
        instructions.append((FSM1.final, 'ε', FSM2.initial))
        FSM_stack.append(FSM(FSM1.initial, FSM2.final))
    
    ## union case
    def process_pipe():
        FSM2, FSM1 = FSM_stack.pop(), FSM_stack.pop()
        initial_state = create_state()
        instructions.append((initial_state, 'ε', FSM1.initial))
        instructions.append((initial_state, 'ε', FSM2.initial))
        S.append(initial_state)
        final_state = create_state()
        instructions.append((FSM1.final, 'ε', final_state))
        instructions.append((FSM2.final, 'ε', final_state))
        S.append(final_state)
        FSM_stack.append(FSM(initial_state, final_state)) 
    
    ## plus case
    def process_plus():
        FSM1 = FSM_stack.pop()
        initial, final = create_state(), create_state()
        instructions.append((initial, 'ε', FSM1.initial))
        instructions.append((FSM1.final, 'ε', FSM1.initial))
        instructions.append((FSM1.final, 'ε', final))
        S.append(initial)
        S.append(final)
        FSM_stack.append(FSM(initial, final))

    def process_char(char):
        initial, final = create_state(), create_state()
        instructions.append((initial, char, final))
        S.append(initial)
        S.append(final)          
        X.append(char)
        FSM_stack.append(FSM(initial, final))

    switch = {
        '*': process_star,
        '.': process_dot,
        '|': process_pipe,
        '+': process_plus,
    }

    for char in postfix:
        switch.get(char, lambda: process_char(char))()

    return FSM_stack.pop(), instructions, S, X


def finite_state_automaton(expression_type):
    if expression_type == '1':
        print("The finite state automaton for the regular expression representing an empty set is: ")
        initial, final = create_state(), create_state()
        print("The alphabet of E is empty")
        print('States S:', initial, final)
        print('Initial state:', initial)
        print('Final state:', final)
        print('Instructions: None')
        return 0
    elif expression_type == '2':
        initial_state = create_state()
        print("The finite state automaton for the regular expression representing the empty word ε is: ")
        print("The alphabet of E is the empty word: ε ")
        print('States S:', initial_state)
        print('Initial state:', initial_state)
        print('Final state:', initial_state)
        print('Instructions: None')
        return 0
    elif expression_type == '3':
        expression_input = input("Please enter the regular expression: ")
        postfix = convert_to_postfix(expression_input)
        print("The partially generalized finite state automaton for the regular expression", expression_input, "is:")
        FSM, instructions, S, X = convert_to_FSM(postfix)
        
        # Display alphabet X, states S, initial state S0, and final states
        print('Alphabet X:', set(char for char in X))
        print('States S:', set(state for state in S))
        print('Initial state:', FSM.initial)
        print('Final state:', FSM.final)
        print('Instructions:')
        for initial, symbol, final in instructions:
            print('({}, {}, {})'.format(initial, symbol, final))
        return FSM
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return None


def print_header():
    print("==      Thompson's Algorithm     ==\n")
    print("===================================")


def print_operations():
    print("\nAvailable Operations:\n")
    print("'*' : Represents 0 or more occurrences\n")
    print("'+' : Represents 1 or more occurrences\n")
    print("'.' : Represents concatenation\n")
    print("'|' : Represents union\n\n")


def print_footer():
    print("\n=======================================")


def main():
    print_header()
    print_operations()
    print("Expression Conversion:\n")
    print("1 : Empty set\n")
    print("2 : Empty word (ε)\n")
    print("3 : General regular expression\n")

    user_choice = input("Please choose the corresponding option (1, 2, or 3): \n\n")
    finite_state_automaton(user_choice)
    
    print_footer()

if __name__ == "__main__":
    main()
