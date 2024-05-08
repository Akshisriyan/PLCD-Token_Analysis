import tkinter as tk


class SymbolTable:
    def __init__(self):
        self.table = []

    def add_entry(self, lexeme, token):
        self.table.append((lexeme, token))

    def display_table(self):
        table_str = "Symbol Table:\n"
        for lexeme, token in self.table:
            table_str += f"{lexeme}: {token}\n"
        return table_str


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)


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
        node = Node('E')
        node.add_child(self.parse_T())
        node.add_child(self.parse_E_prime())
        return node

    def parse_E_prime(self):
        node = Node('E\'')
        if self.current_token[1] == '+':
            self.match('+')
            node.add_child(('+', '+'))
            node.add_child(self.parse_T())
            node.add_child(self.parse_E_prime())
        else:
            node.add_child(('Ɛ', 'Ɛ'))
        return node

    def parse_T(self):
        node = Node('T')
        node.add_child(self.parse_F())
        node.add_child(self.parse_T_prime())
        return node

    def parse_T_prime(self):
        node = Node('T\'')
        if self.current_token[1] == '*':
            self.match('*')
            node.add_child(('*', '*'))
            node.add_child(self.parse_F())
            node.add_child(self.parse_T_prime())
        else:
            node.add_child(('Ɛ', 'Ɛ'))
        return node

    def parse_F(self):
        if self.current_token[1] == '(':
            self.match('(')
            node = self.parse_E()
            self.match(')')
            return node
        elif self.current_token[1] == 'NUMBER' or self.current_token[1] == 'ID':
            node = Node(self.current_token[0])
            self.match(self.current_token[1])
            return node
        else:
            print("Error: Invalid expression")
            exit(1)

    def parse(self):
        self.next_token()
        parse_tree_root = self.parse_E()
        if self.current_token[1] is None:
            return True, self.symbol_table.display_table(), parse_tree_root
        else:
            return False, "Error: Unexpected token", None


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Expression Parser")

        self.input_label = tk.Label(root, text="Enter an arithmetic expression:")
        self.input_label.pack()

        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack()

        self.parse_button = tk.Button(root, text="Parse", command=self.parse_input)
        self.parse_button.pack()

        self.result_text = tk.Text(root, height=20, width=50)
        self.result_text.pack()

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

    def draw_tree(self, node, x, y, level=0):
        if isinstance(node, tuple):
            self.canvas.create_text(x, y, text=node[0], anchor=tk.CENTER)
        elif isinstance(node, Node):
            self.canvas.create_text(x, y, text=node.data, anchor=tk.CENTER)
            num_children = len(node.children)
            if num_children > 0:
                step = 100
                next_y = y + 50
                start_x = x - (num_children - 1) * step / 2
                for child in node.children:
                    child_x = start_x + node.children.index(child) * step
                    child_y = next_y
                    self.canvas.create_line(x, y + 10, child_x, child_y - 20)
                    self.draw_tree(child, child_x, child_y, level + 1)

    def parse_input(self):
        input_str = self.input_entry.get()
        parser = Parser(input_str)
        is_accepted, result, parse_tree_root = parser.parse()
        self.result_text.delete(1.0, tk.END)
        if is_accepted:
            self.result_text.insert(tk.END, "Input accepted\n")
            self.result_text.insert(tk.END, result)
            self.canvas.delete("all")
            if parse_tree_root:
                self.draw_tree(parse_tree_root, 400, 50)
        else:
            self.result_text.insert(tk.END, result)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
