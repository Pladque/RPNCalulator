import math
# STATIC VARIABLES #
OPERATION_SYMBOLS ={
    'dzielenie': '/',
    'mnozenie': '*',
    'dodawanie': '+',
    'odejmowanie': '-',
    'pierwiastowanie': '$',
    'potegowanie': '^',
    #'logarytmowanie': 'L',
}
OTHER_SYMBOLS = {
    'left_bracket': '(',
    'rigt_bracket': ')',
}
PRIORITY = {
    '^': 4,
    '$': 4,
    '*': 3,
    '/': 3,
    '+': 2,
    '-': 2,
    '(': 1,
}
###################


def trim(equation):
    trimmed_str = ""
    for letter in equation:
        if letter != " ":
            trimmed_str +=letter
    return trimmed_str


# checking if character is one of the OPERATION_SYMBOLS
# input: string
# output: True if found it in operation symbols, False if not
def if_operation_symbol(str_x):
    for symbol in OPERATION_SYMBOLS:
        if str_x == OPERATION_SYMBOLS.get(symbol):
            return True
    return False


# checking if character is one of the OTHER_SYMBOLS (in this case, if it is ')' or '('
# input: string
# output: True if found it in other symbols, False if not
def if_bracket(str_x):
    for symbol in OTHER_SYMBOLS:
        if str_x == OTHER_SYMBOLS.get(symbol):
            return True
    return False


# checking if character is a number
# input: string
# output: True if number, False if not
def if_number(str_x):
    try:
        float(str_x)
        return True
    except ValueError:
        return False


# converting float to int if it is possible without losing precison
# input: number as a float
# output: number as a float or int if its possible
def delete_unnecessary_float_tail(float_x):
    if len(str(float_x)) >= 3:
        if str(float_x)[-1] == '0' and str(float_x)[-2]=='.':       # for example '3.0'
            return int(float_x)
    return float_x


# checking if given symbol is an operator, dot, bracket or number
# input: symbol as a string
# output: True if given symbol is an operator, dot, bracket or number,  False if not
def if_valid_symbol(str_x):
    if if_number(str_x) is False and if_bracket(str_x) is False and if_operation_symbol(str_x) is False and str_x !='.':
        return False
    return True


# converting equation from string to list
# input: equations as a string (without white spaces and only with numbers, brackets and OPERATION_SYMBOLS)
# output: equation converted to list
def str_equation_to_list(equation):
    equation_list = []
    temp = ""

    for number_or_symbol in equation:
        if if_number(number_or_symbol):
            temp += number_or_symbol
        elif number_or_symbol == '.':
            temp += number_or_symbol
        elif temp != "":
            equation_list.append(temp)
            temp = ""
        if if_operation_symbol(number_or_symbol) or if_bracket(number_or_symbol):
            equation_list.append(number_or_symbol)

    if temp!="":
        equation_list.append(temp)

    return equation_list


# checking if given equation is valid
# input: equation as a list
# output: True if valid, False if not
def if_list_valid(list_equation):
    last_symbol = "/"
    closing_bracket = 0
    opening_bracket = 0
    try:
        if if_operation_symbol(list_equation[0]):
            return False
    finally:
        for number_or_symbol in list_equation:
            if if_valid_symbol(number_or_symbol) is False:
                return False
            if if_number(last_symbol) and if_number(number_or_symbol):
                return False
            if if_operation_symbol(last_symbol) and if_operation_symbol(number_or_symbol):
                return False
            last_symbol = number_or_symbol
            if number_or_symbol == '(':
                opening_bracket += 1
            elif number_or_symbol == ')':
                closing_bracket += 1
        if opening_bracket != closing_bracket:
            return False
        return True


# converting equation from list to string
# input: equations as a list (without white spaces and only with numbers, brackets and OPERATION_SYMBOLS)
# output: equation converted to string with white spaces between numbers and other symbols
def list_equation_to_str(equation):
    equation_in_RPN_as_string = ""
    for x in equation:
        equation_in_RPN_as_string += x + " "
    return equation_in_RPN_as_string


# converting list with equation to list noted in RNP
# input: equation as a list in regular notation
#        (without white spaces and only with numbers, brackets and OPERATION_SYMBOLS)
# output: equation as a list in RPN, without white spaces
# for example:
#               input: ['12','-','8','*','0.4','+','(','2','-','1',')','*','3']
#               output: ['12', '8', '0.4', '*', '-', '2', '1', '-', '3', '*' '+']
def convert_to_RNP(equation_list):     # RNP = Reversed Polish Notation
    output = []
    operator_stack = []

    for number_or_symbol in equation_list:
        if if_number(number_or_symbol):
            output.append(number_or_symbol)
        elif number_or_symbol == '(':
            operator_stack.append(number_or_symbol)
        elif number_or_symbol == ')':
            while operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()    #zrzucenie '('
        elif if_operation_symbol(number_or_symbol):
            while len(operator_stack)>0 and PRIORITY[operator_stack[-1]] >= PRIORITY[number_or_symbol]:
                output.append(operator_stack.pop())
            operator_stack.append(number_or_symbol)

    while len(operator_stack) != 0:
        output.append(operator_stack.pop())

    return output


# doing basic math with given symbol and numbers
# input: operation symbol, two numbers as strings
# output: result of math operation with given 2 numbers
# comment: for dividing (or subtracting) number1 is DIVIDER(or SUBTRAHEND)
def do_math(operation_symbol, number1, number2):
    if operation_symbol == '*':
        return float(number2) * float(number1)
    if operation_symbol == '/':
        return float(number2) / float(number1)
    if operation_symbol == '+':
        return float(number2) + float(number1)
    if operation_symbol == '-':
        return float(number2) - float(number1)
    if operation_symbol == '^':
        return pow(float(number2),float(number1))
    if operation_symbol == '$':
        return pow(float(number1), 1/float(number2))


# this function prepares equation to convert to RPN and converting it
# input: equation as a string (white spaces allowed)
# output: equation as a list in RPN, without white spaces
def trim_change_to_list_and_convert_to_RPN(equation):
    equation = trim(equation)
    equation_list = str_equation_to_list(equation)

    if if_list_valid(equation_list):
        equation_in_RNP = convert_to_RNP(equation_list)
    else:
        equation_in_RNP = []

    return equation_in_RNP


# computes the equation written in RPN
# input: equation in RPN as a list (without white spaces and only with numbers, brackets and OPERATION_SYMBOLS)
# output: result of calculation as a  float
def calc_equation_in_RPN(equation_in_RPN):
    stack = []
    for number_or_symbol in equation_in_RPN:
        if if_number(number_or_symbol):
            stack.append(number_or_symbol)
        elif if_operation_symbol(number_or_symbol):
            number1 = stack.pop()
            number2 = stack.pop()
            result = do_math(number_or_symbol, number1, number2)
            stack.append(result)

    return stack[0]  #bc stack has now only one element and it is the result


# START #
if __name__ == "__main__":
    main_equation = input("Enter equation: \n")
    if main_equation:
        equation_in_RPN = trim_change_to_list_and_convert_to_RPN(main_equation)
        if len(equation_in_RPN) != 0:
            main_equation_in_RPN = trim_change_to_list_and_convert_to_RPN(main_equation)
            main_equation_in_RPN_as_string = list_equation_to_str(main_equation_in_RPN)
            main_equation_result = calc_equation_in_RPN(main_equation_in_RPN)

            print("Base equation \t\t", main_equation)
            print("Equation in RPN \t", main_equation_in_RPN_as_string)
            print("Result: \t\t\t", main_equation_result)
        else:
            print("Base equation \t\t", main_equation)
            print("Equation in RPN \t", "INPUT ERROR")
            print("Result: \t\t\t", "INPUT ERROR")
    else:
        print("Base equation \t\t", "INPUT ERROR")
        print("Equation in RPN \t", "INPUT ERROR")
        print("Result: \t\t\t", "INPUT ERROR")