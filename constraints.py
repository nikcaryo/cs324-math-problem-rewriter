import random
import random

commands = ["randint", "rand"]

import ast, math


# https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
locals =  {key: value for (key,value) in vars(math).items() if key[0] != '_'}
locals.update({"abs": abs, "complex": complex, "min": min, "max": max, "pow": pow, "round": round})

class Visitor(ast.NodeVisitor):
    def visit(self, node):
       if not isinstance(node, self.whitelist):
           raise ValueError(node)
       return super().visit(node)

    whitelist = (ast.Module, ast.Expr, ast.Load, ast.Expression, ast.Add, ast.Sub, ast.UnaryOp, ast.Num, ast.BinOp,
            ast.Mult, ast.Div, ast.Pow, ast.BitOr, ast.BitAnd, ast.BitXor, ast.USub, ast.UAdd, ast.FloorDiv, ast.Mod,
            ast.LShift, ast.RShift, ast.Invert, ast.Call, ast.Name)

def evaluate(expr, locals = {}):
    if any(elem in expr for elem in '\n#') : raise ValueError(expr)
    try:
        node = ast.parse(expr.strip(), mode='eval')
        Visitor().visit(node)
        return eval(compile(node, "<string>", "eval"), {'__builtins__': None}, locals)
    except Exception: raise ValueError(expr)

def is_command(command_string):
  for command in commands:
     if command_string.startswith(command + '(') and command_string.endswith(')'):
        if command == 'randint':
          return random.randint(*list(map(int, "".join(filter(lambda x: x.isdigit() or x == ",", command_string)).split(',') )))
        if command == 'rand':
          return round(random.uniform(*list(map(int, "".join(filter(lambda x: x.isdigit() or x == ",", command_string)).split(',') ))), 1)
  return None

def parse_constraints(constraints_textbox, split_char='\n'):
  # Evaluate constants
  # Order by 
  lines = constraints_textbox.strip().split(split_char)
  popped_one = True

  locals = {}

  while len(lines) and popped_one:
    popped_one = False
    evaluated_constant = False
    for i, line in enumerate(lines):
      print(line)
      letter, expression = line.split('=')
      letter = letter.strip()
      expression = expression.strip()
      if len(expression) == 1 and expression.isdigit():
        locals[letter] = int(expression) # change
        lines.pop(i)
        evaluated_constant = True
        popped_one = True
        break
      res = is_command(expression)
      if res:
        locals[letter] = res
        lines.pop(i)
        evaluated_constant = True
        popped_one = True
        break
      if expression == "?":
        locals[letter] = expression
        lines.pop(i)
        evaluated_constant = True
        popped_one = True
        break
      
         

    if evaluated_constant: continue
    for i, line in enumerate(lines):
      letter, expression = line.split('=')
      letter = letter.strip()
      expression = expression.strip()
      try:
        locals[letter] = evaluate(expression.strip(), locals=locals)
        lines.pop(i)
        popped_one = True
        break
      except ValueError as e:
        pass
  if not lines:

    return locals
  else:
     raise(Exception('Bad!'))
  
def default_constraint_text(constraints):
  t = []
  for i, num in enumerate(constraints):
    letter = chr(i + ord('A'))
    t.append(f"{letter} = {num}")
  return (" | ".join(t) + "| answer = ?").strip()


# if __name__ == "__main__":
  # try:
  #   parse_constraints("""C = A + B
  #   A = 1
  #   B = 2
  #   D = C
  #   F = G + 2
  #   """)
  # except Exception as e:
  #    print(e)
  
  # print(parse_constraints("""C = A + B
  #   A = 1
  #   B = 2
  #   D = C
  #   """))
  
  # print(parse_constraints("""C = A + B
  #   A = 1
  #   B = 2
  #   D = randint(2,4)
  #   answer = A * B + D * C
  #   """))
  
  # print(parse_constraints("A=randint(20,40)\nB=2*A\nC=rand(2,4)\nanswer= 2 * C - B"))