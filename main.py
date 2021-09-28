from src.basic.scanner import Scanner

file_names = ["example1.bas", "example2.bas", "example3.bas"]
for file_name in file_names:
  test = Scanner()
  test.scan(f'basic_programs/{file_name}')
  tokens = test.create_tokens()
  with open(f'output/{file_name}_tokens.txt', 'w+') as fn:
    for key in tokens.keys():
      if len(tokens[key]) != 0:
        fn.write(key + ": " + ', '.join(map(str, tokens[key])) + "\n")