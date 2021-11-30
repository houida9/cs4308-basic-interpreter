from anytree import Node, RenderTree
class Number:
    def __init__(self, value):
        self.value = value

    def doOperation(self, b, op):
        if isinstance(b.value, int) or isinstance(b.value, float):
            if op == '+':
                print(self.value + b.value)
                return self.value + b.value
            if op == '-':
                print(self.value - b.value)
                return self.value - b.value
            if op == '/':
                print(self.value / b.value)
                return self.value / b.value
            if op == '*':
                print(self.value * b.value)
                return self.value * b.value




class Interpreter:
    def __init__(self, node):
        self.visit(node)
    def visit(self, node):
        name = node.name
        if node.name in ('+', '-') and len(node.children) == 1:
            name = 'unaryop'
        elif isinstance(node.name, int) or isinstance(node.name, float):
            name = 'number'
        elif node.name in ('+', '-', '/', '*') and len(node.children) > 1:
            name = 'binaryop'
        method_name = f'visit_{name}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    def visit_number(self, node):
        if isinstance(node.name, int) or isinstance(node.name, float):
            return Number(node.name)
    def visit_input(self,node):
        pass
    def visit_binaryop(self, node):
        breakpoint()
        a = self.visit(node.children[0])
        b = self.visit(node.children[1])
        if isinstance(a, Number):
            a.doOperation(b,node.name)
    def visit_unaryop(self,node):
        pass
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
n = Node('/')
p = Node(3)
p.parent = n
c = Node(4)
c.parent = n
temp = Interpreter(n)
breakpoint()
