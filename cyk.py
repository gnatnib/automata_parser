def create_cyk_table(String, result):
    # inisialisasi tabel cyk list kosong
    n = len(String)
    table = [[[] for _ in range(n - j)] for j in range(n)]
    
    for i in range(n):
        for j in range(n - i):
            substring = String[j:j+i+1]
            if substring in result:
                table[i][j] = result[substring].strip('[]').split(',') if result[substring] != '[]' else []
            else:
                table[i][j] = []
    
    return table

def print_table(String, table):
    n = len(String)
    max_width = max(
        max(len(str(cell)) for row in table for cell in row),
        max(len(ch) for ch in String)
    )
    
    print("\nCYK Parsing Table:")
    print("-" * (n * (max_width + 3) + 1))
    
    for i in range(n-1, -1, -1):
        print("|", end="")
        for j in range(n-i):
            cell_content = ','.join(table[i][j]) if table[i][j] else "∅"
            print(f" {cell_content:^{max_width}} |", end="")
        print()
        print("-" * (n * (max_width + 3) + 1))
    
    # Print the input string at the bottom
    print("|", end="")
    for ch in String:
        print(f" {ch:^{max_width}} |", end="")
    print()
    print("-" * (n * (max_width + 3) + 1))

NumOfNotations = int(input())
grammar = list()

def check_grammar(grammar):
    Variables = {}
    for Notation in grammar:
        if len(Notation[0]) != 1 or not (Notation[0].isupper()):
            return False
        if Notation[0] not in Variables or Variables[Notation[0]] == "undefiend":
            Variables[Notation[0]] = "defined"
        if len(Notation[1]) > 2 or len(Notation[1]) == 0:
            return False
        if len(Notation[1]) == 1 and not (Notation[1][0].islower()):
            return False
        if len(Notation[1]) == 2:
            if not (Notation)[1][0].isupper() or not (Notation)[1][1].isupper():
                return False
            for i in range(2):
                if Notation[1][i] not in Variables:
                    Variables[Notation[1][i]] = "Undefiend"
    for Value in Variables.values():
        if Value == "undefiend":
            return False
    return True

def cyk(String, Computed={}, grammar=grammar):
    if String in Computed:
        return Computed
    else:
        if len(String) == 1:
            Computed[String] = ""
            for Notation in grammar:
                if Notation[1] == String:
                    Computed[String] += (Notation[0])
            Computed[String] = str(sorted(Computed[String])).replace(
                "'", "").replace(" ", "")
            return Computed
        else:
            Computed[String] = ""
            for i in range(1, len(String)):
                Splitted1 = String[:i]
                Splitted2 = String[i:]
                Computed1 = cyk(Splitted1, Computed)[Splitted1]
                Computed2 = cyk(Splitted2, Computed)[Splitted2]
                if Computed1 != "" and Computed2 != "":
                    for Var1 in Computed1:
                        for Var2 in Computed2:
                            for Notation in grammar:
                                if Var1+Var2 in Notation[1] and Notation[0] not in Computed[String]:
                                    Computed[String] += (Notation[0])
            Computed[String] = str(sorted(Computed[String])).replace(
                "'", "").replace(" ", "")
            return Computed

def print_cyk(String, grammar):
    result = cyk(String, {}, grammar)
    if result[String] != "[]" and "S" in result[String]:
        print("String Diterima")
        table = create_cyk_table(String, result)
        print_table(String, table)
        
        for i in range(1, len(String)+1):
            for j in range(len(String) - i):
                if String[j:j+i] in result:
                    print(String[j:j+i]+" : " +
                          result[String[j:j+i]]+" , ", end="")
                else:
                    print(String[j:j+i]+" : "+"[]"+" , ", end="")
            print(String[-i:], " : "+result[String[-i:]])
    else:
        print("NO")

# Main program
for i in range(NumOfNotations):
    Notation = input().split(" -> ")
    grammar.append(Notation)
String = input()
if check_grammar(grammar):
    print_cyk(String, grammar)
else:
    print("Wrong Grammar")