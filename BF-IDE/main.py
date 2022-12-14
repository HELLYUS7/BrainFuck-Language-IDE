from rich.console import Console
from rich.table import Table
from colorama import Fore, Back, Style
import webbrowser
import platform
import os
import sys

class BFInterpreter:
    def __init__(self):
        self.resetAll()

    def resetAll(self):
        self.console = Console()
        self.memory = [0]
        self.stackForwards = []
        self.ret = {}
        self.adress = 0
        self.counter = 0
        self.bufferCaracteres = str()

    def mapLoops(self):
        while not self.counter == len(self.code):
            opcode = self.code[self.counter]
            if opcode == '[':
                self.stackForwards.append(self.counter)
            elif opcode == ']':
                self.targetReturn = self.stackForwards.pop()
                self.ret[self.targetReturn] = self.counter
                self.ret[self.counter] = self.targetReturn
            self.counter += 1

    def Interpreter(self, code):
        self.resetAll()
        self.code = code
        self.mapLoops()
        self.bufferCaracteres = ''
        self.counter = 0
        self.adress = 0
        try:
            while not self.counter == len(self.code):
                opcode = self.code[self.counter]
                if opcode == '>':
                    self.adress += 1
                    if self.adress >= len(self.memory):
                        self.memory.append(0)
                elif opcode == '<':
                    self.adress -= 1
                elif opcode == '+':
                    self.memory[self.adress] += 1
                elif opcode == '-':
                    self.memory[self.adress] -= 1
                elif opcode == '[':
                    if self.memory[self.adress] == 0:
                        self.counter = self.ret[self.counter]
                elif opcode == ']':
                    if self.memory[self.adress] != 0:
                        self.counter = self.ret[self.counter]
                elif opcode == ',':
                    try:
                        self.memory[self.adress] = ord(input('Input: '))
                    except:
                        break
                elif opcode == '.':
                    cia = chr(self.memory[self.adress])
                    self.console.print(f'  {cia}')
                    self.bufferCaracteres += cia
                elif opcode == 'b':
                    self.console.print(f'[bold magenta]Buffer: [/bold magenta][bold yellow]{self.bufferCaracteres}[/bold yellow]')
                elif opcode == 'c':
                    self.bufferCaracteres = ''
                elif opcode == 'm':
                    self.console.print(f'[bold yellow]{self.memory}[/bold yellow]')
                self.counter += 1
            self.console.print(f'\nEnd Memory:\n [bold magenta]{self.memory}[/bold magenta]')
        except:
            pass

class Terminal:
    def __init__(self):
        self.console = Console()
        self.lineScreen = str()
        for i in range(self.console.width): self.lineScreen += '='
    def clearScreen(self):
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux':
            os.system('clear')

    def inputUser(self, question):
        self.console.print(question, end='')
        outputUser = input()
        return outputUser    

    def printLogo(self):
        self.lineScreen = str()
        for i in range(self.console.width): self.lineScreen += '='
        self.clearScreen()
        self.console.print(self.lineScreen)
        self.console.print('''[bold magenta]
===================================================
 ______   ________   _____  ______   ________  
  |_   _ \ |_   __  | |_   _||_   _ `.|_   __  | 
    | |_) |  | |_ \_|   | |    | | `. \ | |_ \_| 
  |  __'.  |  _|      | |    | |  | | |  _| _  
   _| |__) |_| |_      _| |_  _| |_.' /_| |__/ | 
  |_______/|_____|    |_____||______.'|________| 
                                               
============= [/bold magenta][bold yellow]BrainFuck IDE Make by Gabriel Pereira
[/bold yellow]''',justify='center')

    def printMenu(self):
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column('Menu', justify='left')
        table.add_column('OpCode', justify='center')
        table.add_row('Help', '1')
        table.add_row('Wikip??dia BFL', '2')
        table.add_row('Exemples', '3')
        table.add_row('Interpreter', '4')
        table.add_row('Run Program', '5')
        table.add_row('Exit', '6')
        self.console.print(table)

    def inputCodeIterpreter(self):
        code = self.inputUser('[bold magenta]Your Code Here:[/bold magenta]\n')
        self.console.print('\n')
        return code

    def printLineScreen(self):
        self.lineScreen = str()
        for i in range(self.console.width): self.lineScreen += '='
        self.console.print(self.lineScreen)
    
    def printBasicScreen(self):
        self.clearScreen()
        if self.console.width >= 55:
            self.printLogo()
            self.printLineScreen()
    
    def printHelp(self):
        self.printBasicScreen()
        self.console.print('[bold magenta]Sobre a IDE[/bold magenta]', justify='center')
        self.console.print('[bold yellow]A BF-IDE ?? um "Ambiente de Desenvolvimento Integrado",desenvolvida para dar a voc?? um dos melhores compiladores/interpretadores desta linguagem minimalista e incr??vel![/bold yellow]\n', justify='center')
        self.console.print('[bold magenta]Como funciona a linguagem BF?[/bold magenta]', justify='center')
        self.console.print('[bold yellow]A linguagem funciona com base em caracteres ??nicos que controlam c??lulas de mem??ria, que neste caso ?? a mem??ria RAM, voc?? pode manipular cada c??lula mudando seu valor com base em loops e outras opera????es muito bem ordenadas. A entrada e sa??da de dados se d?? por meio da codifica????o ASCII que est?? contida na c??lula atual.[/bold yellow]\n', justify='center')
        self.console.print('[bold magenta]Como ?? a sintaxe de BF?[/bold magenta]', justify='center')
        table = Table(show_header=True, header_style="bold magenta", expand=True, highlight=True, show_lines=True)
        table.add_column('Caracatere', justify='left', style='bold magenta')
        table.add_column('Descri????o', justify='left')
        table.add_row('>', 'Pula para a pr??xima c??lula da mem??ria')
        table.add_row('<', 'Volta uma c??lula da mem??ria')
        table.add_row('+', 'Soma 1 a c??lula atual')
        table.add_row('-', 'Subtrai 1 da c??lula atual')
        table.add_row('[', 'Se o valor da c??lula atual for igual a 0 ent??o pular para o pr??ximo "]"')
        table.add_row(']', 'Se o valor da c??lula atual for diferente de 0 ent??o voltar para o "[" de origem')
        table.add_row('.', 'Mostra o valor ASCII da c??lula atual em forma de caractere')
        table.add_row(',', 'Pede a entrada de dados do usu??rio com um caractere que virar?? um valor ASCII na c??lula atual')
        table.add_row('m', 'Mostra o estado da mem??ria atualmente')
        table.add_row('b', 'Mostra o Buffer de letras que foram impressas')
        table.add_row('c', 'Limpa o Buffer de letras')
        self.console.print(table)

    def warning(self):
        self.console.print('[bold red]Something went wrong![/bold red]')
        self.inputUser('[bold magenta]Back <-[/bold magenta]')


class App:
    def __init__(self):
        self.TerminalApp = Terminal()
        self.BFInterpreterApp = BFInterpreter()
    
    def home(self):
        opt = ''
        self.TerminalApp.printBasicScreen()
        self.TerminalApp.printMenu()
        opt = self.TerminalApp.inputUser(' [bold magenta]What do you want?: [/bold magenta]')
        if opt == '1':
            self.help()
        elif opt == '2':
            webbrowser.open_new_tab('https://pt.wikipedia.org/wiki/Brainfuck')
            self.home()
        elif opt == '3':
            webbrowser.open_new_tab('http://brainfuck.org/')
            self.home()
        elif opt == '4':
            self.interpreter()
        elif opt == '5':
            self.runFile()
        elif opt == '6':
            self.TerminalApp.clearScreen()
            sys.exit(0)
        else:
            self.home()

    def interpreter(self):
        self.TerminalApp.printBasicScreen()
        code = self.TerminalApp.inputCodeIterpreter()
        self.BFInterpreterApp.Interpreter(code)
        opt = self.TerminalApp.inputUser('\n\n[bold magenta]What do you want?\n[bold yellow]Restart[1][/bold yellow] [bold magenta]or[/bold magenta] [bold yellow]Menu[2][/bold yellow]: [/bold magenta]')
        if opt == '1':
            self.interpreter()
        elif opt == '2':
            self.home()
        else:
            self.home()

    def runFile(self):
        def getFile():
            dir = self.TerminalApp.inputUser('[bold magenta]What is the directory?\n[/bold magenta]')
            return dir
        
        def runProgramFile(dir):
            try:
                with open(dir, 'r') as file:
                    data = file.read()
                    code = str().join(filter(lambda c: c in '<>+-[],.mcb', data))
                    self.TerminalApp.printBasicScreen()
                    self.TerminalApp.console.print('[bold magenta]Running File:[/bold magenta]\n')
                    self.BFInterpreterApp.Interpreter(code)
            except:
                self.TerminalApp.warning()
            finally:
                opt = self.TerminalApp.inputUser('\n\n[bold magenta]What do you want?\n[bold yellow]Try Again[1][/bold yellow] [bold magenta]or[/bold magenta] [bold yellow]Menu[2][/bold yellow]: [/bold magenta]')
                if opt == '1':
                    self.TerminalApp.printBasicScreen()
                    runProgramFile(dir)
                elif opt == '2':
                    self.home()
                else:
                    self.home()
    
        self.TerminalApp.printBasicScreen()
        optFile = self.TerminalApp.inputUser('[bold magenta]What do you want?\n[bold yellow]Get File[1][/bold yellow] [bold magenta]or[/bold magenta] [bold yellow]New File[2][/bold yellow]: [/bold magenta]')
        self.TerminalApp.printBasicScreen()
        if optFile == '1':
            runProgramFile(getFile())
        elif optFile == '2':
            self.home()
        else:
            self.runFile()
    
    def help(self):
        self.TerminalApp.printHelp()
        self.TerminalApp.inputUser(question='')
        self.home()

if __name__ == '__main__':
    Aplication = App()
    Aplication.home()