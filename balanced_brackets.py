from collections import deque

def balanced_brackets(input_text, brackets):
    stack = deque()
    opening_brackets = [x[0] for x in brackets]
    closing_brackets = [x[1] for x in brackets]
    
    for char in input_text:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_brackets:
            try:
                top_char = stack.pop()
            except IndexError:
                return False

            if closing_brackets.index(char) != opening_brackets.index(top_char):
                return False
    
    if stack:
        return False
    else:
        return True


def main():
    input_text = """Python {is an easy to [learn]}, (powerful programming language. It)
                    has efficient high­level [(data structures) and a simple but
                    effective approach to object­oriented programming]. Python’s elegant
                    syntax and dynamic typing, together with its {interpreted nature,
                    make it an ideal language (for) scripting and rapid} application
                    development in many areas on most platforms."""

    brackets = [('(', ')'), ('[', ']'), ('{', '}')]

    print("Brackets are balanced.") if balanced_brackets(input_text, brackets) else print("Brackets aren't balanced.")


if __name__ == "__main__":
    main()
