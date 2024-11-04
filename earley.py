class State:
    def __init__(self, nonterminal, expression, dot=0, origin=0):
        self.nonterminal = nonterminal
        self.expression = expression
        self.dot = dot
        self.origin = origin
        
    @property
    def finished(self):
        return self.dot >= len(self.expression)
        
    @property
    def symbol(self):
        return None if self.finished else self.expression[self.dot]
        
    @property
    def symbol_is_nonterminal(self):
        return self.symbol and self.symbol.isalpha() and self.symbol.isupper()
        
    @property
    def shift(self):
        return State(self.nonterminal, self.expression, self.dot + 1, self.origin)
        
    @property
    def tuple(self):
        return (self.nonterminal, self.expression, self.dot, self.origin)
        
    def __hash__(self):
        return hash(self.tuple)
        
    def __eq__(self, other):
        return self.tuple == other.tuple
        
    def __str__(self):
        n, e, d, o = self.tuple
        return f'[{o}] {n} -> {e[:d]}.{e[d:]}'

class Grammar:
    def __init__(self, rules):
        # Convert input rules to internal format
        self.rules = []
        for rule in rules:
            left, right = rule
            # Convert the right side from list to tuple of characters
            right_tuple = tuple(right)
            self.rules.append((left, right_tuple))
            
        # Add start rule
        if self.rules:
            start_symbol = self.rules[0][0]  # Use first rule's left side as start
            self.rules.insert(0, ('^', (start_symbol,)))
    
    @property
    def start(self):
        return self.rules[0]  # Return the start rule ('^' -> S)
    
    def __getitem__(self, nonterminal):
        return [rule for rule in self.rules if rule[0] == nonterminal]

class EarleyParser:
    def __init__(self, grammar):
        self.grammar = Grammar(grammar)
        self.states = []
        
    def parse(self, text):
        # Initialize states
        self.states = [set() for _ in range(len(text) + 1)]
        self.states[0].add(State(*self.grammar.start))
        
        # Process each character
        for k, token in enumerate(text):
            extension = list(self.states[k])
            self.states[k].clear()
            
            while extension:
                state = extension.pop()
                if state in self.states[k]:
                    continue
                    
                self.states[k].add(state)
                if state.finished:
                    self._completer(state, extension)
                elif state.symbol_is_nonterminal:
                    self._predictor(state, k, extension)
                else:
                    self._scanner(state, k, token)
                    
        # Process end of input
        k = len(text)
        extension = list(self.states[k])
        self.states[k].clear()
        while extension:
            state = extension.pop()
            if state in self.states[k]:
                continue
            self.states[k].add(state)
            if state.finished:
                self._completer(state, extension)
        
        # Check if input is accepted
        accepts = any(s.nonterminal == '^' and s.finished for s in self.states[k])
        return accepts

    def _predictor(self, state, origin, extension):
        for rule in self.grammar[state.symbol]:
            extension.append(State(*rule, origin=origin))

    def _scanner(self, state, origin, token):
        if state.symbol == token:
            self.states[origin + 1].add(state.shift)

    def _completer(self, state, extension):
        for reduce in self.states[state.origin]:
            if state.nonterminal == reduce.symbol:
                extension.append(reduce.shift)

def main():
    # Get number of rules
    NumOfNotations = int(input())
    grammar = []
    
    # Read grammar rules
    for _ in range(NumOfNotations):
        rule = input().split(" -> ")
        right_side = list(rule[1])  # Convert right side to list of characters
        grammar.append((rule[0], right_side))
    
    # Read input string
    input_string = input()
    
    # Create parser and parse input
    parser = EarleyParser(grammar)
    result = parser.parse(input_string)
    
    # Print result
    if result:
        print("Accepted")
    else:
        print("Declined")

if __name__ == "__main__":
    main()