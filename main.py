import requests
import random
import string
import time
import os
from rich import print
from rich.console import Console
from rich.panel import Panel
from faker import Faker

console = Console()
fake = Faker()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome():
    clear_console()
    console.print(Panel("[bold cyan]shittiest tool ever[/bold cyan]"))
    console.print("[bold cyan]Choose an option:[/bold cyan]")
    console.print("[bold cyan]1[/bold cyan] - Roblox Username Generator")
    console.print("[bold cyan]2[/bold cyan] - Coming Soon")
    choice = console.input("[yellow]Enter your choice: [/yellow]")
    
    if choice == "1":
        return "gen"
    if choice == "2":
        return welcome()

def replace(word):
    replacements = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 'b': '8',
        'g': '9', 't': '7', 'l': '1', 'z': '2', 'c': '6', 'q': '9'
    }
    word_list = list(word)
    replaceable = [i for i, char in enumerate(word) if char in replacements]
    
    if replaceable:
        wording = random.choice(replaceable)
        word_list[wording] = replacements[word[wording]]

    return ''.join(word_list)

def fetch(length, limit):
    try:
        response = requests.get(f"https://api.datamuse.com/words?sp={'?' * length}&max={limit}")
        response.raise_for_status()
        data = response.json()
        words = [item['word'] for item in data if len(item['word']) == length]
        return words
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]{e}[/bold red]")
        return []

def syno(keyword):
    try:
        response = requests.get(f"https://api.datamuse.com/words?ml={keyword}")
        response.raise_for_status()
        data = response.json()
        words = [item['word'] for item in data if ' ' not in item['word'] and '-' not in item['word']]
        return words
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]{e}[/bold red]")
        return []

def ui():
    clear_console()
    console.print(Panel("[bold cyan]shittiest tool ever[/bold cyan]"))
    console.print("[bold cyan]Choose Generator Type:[/bold cyan]")
    console.print("[bold cyan]1[/bold cyan] - Random")
    console.print("[bold cyan]2[/bold cyan] - OGu")
    console.print("[bold cyan]3[/bold cyan] - Actual Words")
    console.print("[bold cyan]4[/bold cyan] - Names")
    
    try:
        type = int(console.input("[yellow]Enter choice: [/yellow]"))
        clear_console()
        console.print(Panel(f"[bold cyan]Generator[/bold cyan]"))
        
        if type == 1:
            user = int(console.input("[yellow]--> How many usernames do you want: [/yellow]"))
            length = int(console.input("[yellow]--> Enter length of usernames: [/yellow]"))
            numbers = console.input("[yellow]--> Include numbers in usernames? (y/n): [/yellow]").lower() == 'y'
            save = console.input("[yellow]--> Save valid usernames? (y/n): [/yellow]").lower() == 'y'
            valid = console.input("[yellow]--> Only show valid usernames? (y/n): [/yellow]").lower() == 'y'
            delay = int(console.input("[yellow]--> Enter delay between checks: [/yellow]"))
            save_file = "valid.txt" if save else None
            
            return type, numbers, user, length, save, valid, delay, save_file, None, None
        
        elif type == 2:
            keyword = console.input("[yellow]--> Describe your username (e.g., 'skid'): [/yellow]").strip()
            words = syno(keyword)
            available = len(words)

            console.print(f"[green]Yay, over {available} words found![/green]")
            customize = console.input("[yellow]Want to customize it? (y/n): [/yellow]").lower()

            if customize == 'y':
                user = int(console.input(f"[yellow]--> How many usernames do you want (max {available}): [/yellow]"))
                while user > available:
                    console.print("[red]You cannot choose a bigger number [/red]")
                    user = int(console.input(f"[yellow]--> How many usernames do you want (max {available}): [/yellow]"))
            else:
                user = available
            
            numbers = console.input("[yellow]--> Include numbers in usernames? (y/n): [/yellow]").lower() == 'y'
            save = console.input("[yellow]--> Save valid usernames ? (y/n): [/yellow]").lower() == 'y'
            valid = console.input("[yellow]--> Only show valid usernames? (y/n): [/yellow]").lower() == 'y'
            delay = int(console.input("[yellow]--> Enter delay between checks: [/yellow]"))
            save_file = "valid.txt" if save else None
            
            return type, numbers, user, None, save, valid, delay, save_file, keyword, None
            
        elif type == 3:
            user = int(console.input("[yellow]--> How many usernames do you want: [/yellow]"))
            numbers = console.input("[yellow]--> Include numbers in usernames? (y/n): [/yellow]").lower() == 'y'
            save = console.input("[yellow]--> Save valid usernames? (y/n): [/yellow]").lower() == 'y'
            valid = console.input("[yellow]--> Only show valid usernames? (y/n): [/yellow]").lower() == 'y'
            delay = int(console.input("[yellow]--> Enter delay between checks: [/yellow]"))
            save_file = "valid.txt" if save else None
            
            return type, numbers, user, None, save, valid, delay, save_file, None, None

        elif type == 4:
            gender = console.input("[yellow]--> What gender (m/f)? [/yellow]").lower()
            user = int(console.input("[yellow]--> How many names do you want: [/yellow]"))
            numbers = console.input("[yellow]--> Include numbers in names? (y/n): [/yellow]").lower() == 'y'
            save = console.input("[yellow]--> Save valid names? (y/n): [/yellow]").lower() == 'y'
            valid = console.input("[yellow]--> Only show valid names? (y/n): [/yellow]").lower() == 'y'
            delay = int(console.input("[yellow]--> Enter delay between checks: [/yellow]"))
            save_file = "valid.txt" if save else None
            
            return type, numbers, user, None, save, valid, delay, save_file, None, gender

    except ValueError:
        console.print("[red]> Invalid input <[/red]")
        return ui()

def OK(user, found, total, save_file):
    console.print(f"[green][{found}/{total}] [+] Found Username: {user}[/green]")
    if save_file:
        with open(save_file, 'a+') as f:
            f.write(f"{user}\n")

def taken(user):
    console.print(f"[red][-] {user}[/red]")

def setting(length, numbers):
    letters = string.ascii_lowercase + (string.digits if numbers else "")
    return ''.join(random.choice(letters) for _ in range(length))

def checker(user, bday='1999-04-20'):
    Url = f'https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday={bday}'
    try:
        Data = requests.get(Url)
        Data.raise_for_status()
        Json = Data.json()
        return Json.get('code', None)
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]{user}: {e}[/bold red]")
        return None

def gen(type, numbers, user, length, save, valid, delay, save_file, keyword=None, gender=None):
    found = 0
    clear_console()
    type_name = {
        1: "Random Words Generator",
        2: "OGu Generator",
        3: "Actual Words Generator",
        4: "Name Generator"
    }.get(type, "Username Generator")
    
    console.print(Panel(f"[bold cyan]{type_name}[/bold cyan]"))
    
    if type == 1:
        for i in range(user):
            Username = setting(length, numbers)
            Code = checker(Username)
            percentage = ((i + 1) / user) * 100
            
            if Code is not None:
                if Code == 0:
                    found += 1
                    console.print(f"[{int(percentage)}%]    {Username:<15} | [green]Available[/green]")
                    OK(Username, found, user, save_file if save else None)
                elif not valid:
                    console.print(f"[{int(percentage)}%]    {Username:<15} | [red]Unavailable[/red]")
            time.sleep(delay)

    elif type == 2:
        for i in range(user):
            Username = random.choice(syno(keyword))
            Code = checker(Username)
            percentage = ((i + 1) / user) * 100
            
            if Code is not None:
                if Code == 0:
                    found += 1
                    console.print(f"[{int(percentage)}%]    {Username:<15} | [green]Available[/green]")
                    OK(Username, found, user, save_file if save else None)
                elif not valid:
                    console.print(f"[{int(percentage)}%]    {Username:<15} | [red]Unavailable[/red]")
            time.sleep(delay)

    elif type == 3:
        for i in range(user):
            length = random.randint(5, 15)
            word = random.choice(fetch(length, 100))
            Code = checker(word)
            percentage = ((i + 1) / user) * 100
            
            if Code is not None:
                if Code == 0:
                    found += 1
                    console.print(f"[{int(percentage)}%]    {word:<15} | [green]Available[/green]")
                    OK(word, found, user, save_file if save else None)
                elif not valid:
                    console.print(f"[{int(percentage)}%]    {word:<15} | [red]Unavailable[/red]")
            time.sleep(delay)

    elif type == 4:
        for i in range(user):
            if gender == 'm':
                name = fake.first_name_male()
            else:
                name = fake.first_name_female()

            if numbers:
                name = replace(name)
            
            Code = checker(name)
            percentage = ((i + 1) / user) * 100
            
            if Code is not None:
                if Code == 0:
                    found += 1
                    console.print(f"[{int(percentage)}%]    {name:<15} | [green]Available[/green]")
                    OK(name, found, user, save_file if save else None)
                elif not valid:
                    console.print(f"[{int(percentage)}%]    {name:<15} | [red]Unavailable[/red]")
            time.sleep(delay)

    console.print(f"[green]Scraped {found} out of [red]{user}[/red] usernames[/green]")
    
    reset = console.input("[yellow]Do you want to return? (y/n): [/yellow]").lower()
    if reset == 'y':
        clear_console()
        ui()

def main():
    while True:
        choice = welcome()
        if choice == "gen":
            params = ui()
            gen(*params)

if __name__ == "__main__":
    main()
