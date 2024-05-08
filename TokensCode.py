class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_entry(self, lexeme, token):
        self.table[lexeme] = token

    def display_table(self):
        print("Symbol Table:")
        for lexeme, token in self.table.items():
            print(f"{lexeme}: {token}")


class Parser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.index = 0
        self.current_token = None
        self.symbol_table = SymbolTable()

    def next_token(self):
        if self.index < len(self.input_string):
            if self.input_string[self.index].isdigit():
                token = 'NUMBER'
                lexeme = ''
                while self.index < len(self.input_string) and self.input_string[self.index].isdigit():
                    lexeme += self.input_string[self.index]
                    self.index += 1
                self.current_token = (lexeme, token)
            elif self.input_string[self.index] in ['+', '*', '(', ')']:
                self.current_token = (self.input_string[self.index], self.input_string[self.index])
                self.index += 1
            elif self.input_string[self.index] == ' ':
                self.index += 1
                self.next_token()
            else:
                token = 'ID'
                lexeme = ''
                while self.index < len(self.input_string) and self.input_string[self.index].isalnum():
                    lexeme += self.input_string[self.index]
                    self.index += 1
                self.current_token = (lexeme, token)
        else:
            self.current_token = (None, None)

    def match(self, expected_token):
        if self.current_token[1] == expected_token:
            self.symbol_table.add_entry(self.current_token[0], self.current_token[1])
            self.next_token()
        else:
            print(f"Error: Expected {expected_token} but found {self.current_token[1]}")
            exit(1)

    def parse_E(self):
        self.parse_T()
        self.parse_E_prime()

    def parse_E_prime(self):
        if self.current_token[1] == '+':
            self.match('+')
            self.parse_T()
            self.parse_E_prime()

    def parse_T(self):
        self.parse_F()
        self.parse_T_prime()

    def parse_T_prime(self):
        if self.current_token[1] == '*':
            self.match('*')
            self.parse_F()
            self.parse_T_prime()

    def parse_F(self):
        if self.current_token[1] == '(':
            self.match('(')
            self.parse_E()
            self.match(')')
        elif self.current_token[1] == 'NUMBER' or self.current_token[1] == 'ID':
            self.match(self.current_token[1])
        else:
            print("Error: Invalid expression")
            exit(1)

    def parse(self):
        self.next_token()
        self.parse_E()
        if self.current_token[1] is None:
            print("Input accepted")
            self.symbol_table.display_table()
        else:
            print("Error: Unexpected token")
            exit(1)


def main():
    input_str = input("Enter an arithmetic expression: ")
    parser = Parser(input_str)
    parser.parse()


if __name__ == "__main__":
    main()
