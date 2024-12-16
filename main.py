import subprocess
import sys
import platform
import os
import pystyle
import textwrap

if platform.system() == "Windows":
    import ctypes
    GWL_STYLE = -16
    WS_SIZEBOX = 262144
    WS_MAXIMIZEBOX = 65536
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style = style & ~WS_SIZEBOX
    style = style & ~WS_MAXIMIZEBOX
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 3)
    enter = pystyle.Colorate.Horizontal(pystyle.Colors.green_to_cyan, ('Welcome To SUCCOTASH, Press "ENTER" to continue!'))
    pystyle.Anime.Fade(
    pystyle.Center.Center('''




                                     
███████╗██╗   ██╗ ██████╗ ██████╗ ██████╗ ████████╗ █████╗ ███████╗██╗  ██╗
██╔════╝██║   ██║██╔════╝██╔════╝██╔═══██╗╚══██╔══╝██╔══██╗██╔════╝██║  ██║
███████╗██║   ██║██║     ██║     ██║   ██║   ██║   ███████║███████╗███████║
╚════██║██║   ██║██║     ██║     ██║   ██║   ██║   ██╔══██║╚════██║██╔══██║
███████║╚██████╔╝╚██████╗╚██████╗╚██████╔╝   ██║   ██║  ██║███████║██║  ██║
╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                          
    
                                        Press To Enter
                                          
                                          
                                          '''), pystyle.Colors.red_to_purple, pystyle.Colorate.Vertical, enter=True)


RESET = "\033[0m"
GREEN_TEXT = "\033[32m"
BLACK_BG = "\033[40m"


def get_terminal_size():
    """Получает размеры терминала."""
    if platform.system() == "Windows":
        try:
            rows = int(os.popen('mode con: | find "Lines:"').read().strip().split(':')[-1].strip())
            columns = int(os.popen('mode con: | find "Columns:"').read().strip().split(':')[-1].strip())
            return rows, columns
        except:
            return 25, 80
    else:
        try:
            rows, columns = os.popen('stty size', 'r').read().split()
            return int(rows), int(columns)
        except:
            return 25, 80

def center_text(text, width):
    """Центрирует текст в заданной ширине."""
    padding = (width - len(text)) // 2
    return " " * padding + text

def draw_box(content, width, height):
    """Рисует текстовый прямоугольник с заданным содержимым."""
    lines = content.splitlines()
    padding_top = (height - len(lines)) // 2
    padding_bottom = height - len(lines) - padding_top
    if padding_top < 0:
        padding_top = 0
    if padding_bottom < 0:
        padding_bottom = 0

    result = ["-" * width]  # Верхняя граница
    result.extend(["|" + center_text("", width - 2) + "|"] * padding_top)
    for line in lines:
        wrapped_line = textwrap.fill(line, width=width - 2)
        for wrapped_line_part in wrapped_line.splitlines():
            result.append("|" + center_text(wrapped_line_part, width - 2) + "|")
    result.extend(["|" + center_text("", width - 2) + "|"] * padding_bottom)
    result.append("-" * width)  # Нижняя граница
    return "\n".join(result)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt):
    """Получает ввод от пользователя с заданным приглашением."""
    while True:
         return pystyle.Write.Input(prompt, pystyle.Colors.green_to_cyan, interval=0.005)

def count_letters(sentence):
    """Считает количество букв в предложении."""
    letter_count = sum(1 for char in sentence if char.isalpha())
    return letter_count


def execute_xsrfprobe():
    """Выполняет команды для установки и запуска xsrfprobe."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "xsrfprobe"])
        
        # Find the location of the xsrfprobe executable
        if platform.system() == "Windows":
            xsrfprobe_executable = "xsrfprobe"  # Assumes it's in the PATH
        else:
             
             # Linux/macOS
             # Check for the executable in standard locations first
             xsrfprobe_executable = subprocess.check_output(["which", "xsrfprobe"]).decode().strip()
             # If not found check in the pip installation locations
             if not xsrfprobe_executable:
                # Gets pip location from command output
                pip_location_check = subprocess.check_output([sys.executable, "-m", "pip", "show", "xsrfprobe"]).decode()
                
                for line in pip_location_check.splitlines():
                   if "Location" in line:
                        location = line.split(":")[1].strip()
                        xsrfprobe_executable = os.path.join(location, "bin", "xsrfprobe")
                        break
        
        if not os.path.exists(xsrfprobe_executable):
            print(f"Error: Could not find xsrfprobe executable at: {xsrfprobe_executable}")
            return
        
        # Run xsrfprobe --help and capture the output
        process = subprocess.Popen([xsrfprobe_executable, "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(stdout.decode()) # Prints the output of the program
        else:
            print(f"Error executing xsrfprobe --help: {stderr.decode()}")
   
    except subprocess.CalledProcessError as e:
        print(f"Error installing xsrfprobe: {e}")
    except FileNotFoundError:
        print("Error: xsrfprobe not found. Please make sure it is installed.")


def vulnerabilities_menu(rows, columns, box_width, box_height):
    """Меню уязвимостей."""
    while True:
        clear_console()
        menu_content = """
                      ┌────────────────────────────────────┐                                  
                      │ [1] • POC                          │
                      │ [2] • Назад                          │
                      │ [3] • Выход                          │
                      └────────────────────────────────────┘
    """
        pystyle.Write.Print(center_text("", columns) + draw_box(menu_content, box_width, box_height), pystyle.Colors.red_to_purple, interval=0.00000001)

        choice = get_user_input("\n\n[?] • 𝚂𝚎𝚕𝚎𝚌𝚝 𝙼𝚎𝚗𝚞 𝙸𝚝𝚎𝚖 -> ")

        if choice == "1":
            poc_menu(rows, columns, box_width, box_height)
        elif choice == "2":
            break
        elif choice == "3":
            clear_console()
            pystyle.Write.Print(pystyle.Center.XCenter(draw_box("Выход из программы.", box_width, box_height)), pystyle.Colors.red_to_purple, interval=0.002)
            sys.exit()
        else:
             clear_console()
             pystyle.Write.Print(pystyle.Center.XCenter(draw_box("Ошибка: Некорректный ввод. Пожалуйста, выберите доступный вариант.", box_width, box_height)), pystyle.Colors.red_to_red, interval=0.002)

def poc_menu(rows, columns, box_width, box_height):
    """Меню POC."""
    while True:
        clear_console()
        menu_content = """
                      ┌────────────────────────────────────┐                                  
                      │ [1] • XSRFProbe                    │
                      │ [2] • Назад                          │
                      │ [3] • Выход                          │
                      └────────────────────────────────────┘
    """
        pystyle.Write.Print(center_text("", columns) + draw_box(menu_content, box_width, box_height), pystyle.Colors.red_to_purple, interval=0.00000001)

        choice = get_user_input("\n\n[?] • 𝚂𝚎𝚕𝚎𝚌𝚝 𝙼𝚎𝚗𝚞 𝙸𝚝𝚎𝚖 -> ")

        if choice == "1":
             clear_console()
             pystyle.Write.Print(pystyle.Center.XCenter(draw_box("Выполняется установка и запуск XSRFProbe...", box_width, box_height)), pystyle.Colors.green_to_cyan, interval=0.002)
             execute_xsrfprobe()
             pystyle.Write.Input("\n\n[?] Нажмите Enter для возврата в меню...", pystyle.Colors.green_to_cyan, interval=0.005)
             
        elif choice == "2":
            break
        elif choice == "3":
            clear_console()
            pystyle.Write.Print(pystyle.Center.XCenter(draw_box("Выход из программы.", box_width, box_height)), pystyle.Colors.red_to_purple, interval=0.002)
            sys.exit()
        else:
             clear_console()
             pystyle.Write.Print(pystyle.Center.XCenter(draw_box("Ошибка: Некорректный ввод. Пожалуйста, выберите доступный вариант.", box_width, box_height)), pystyle.Colors.red_to_red, interval=0.002)



def main():
    """Главная функция скрипта."""
    COUNT_LETTERS_ACTION = 1
    VULNERABILITIES_ACTION = 2
    EXIT_ACTION = 0

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


    rows, columns = get_terminal_size()
    box_width = min(columns - 6, 70)  #  ширина box
    box_height = min(rows - 5, 15)  # высота box
    while True:

        if platform.system() == "Windows":
            os.system("cls")
            pystyle.Write.Print(pystyle.Center.XCenter('''
                                                      

⠀⠀⠀
                                     
███████╗██╗   ██╗ ██████╗ ██████╗ ██████╗ ████████╗ █████╗ ███████╗██╗  ██╗
██╔════╝██║   ██║██╔════╝██╔════╝██╔═══██╗╚══██╔══╝██╔══██╗██╔════╝██║  ██║
███████╗██║   ██║██║     ██║     ██║   ██║   ██║   ███████║███████╗███████║
╚════██║██║   ██║██║     ██║     ██║   ██║   ██║   ██╔══██║╚════██║██╔══██║
███████║╚██████╔╝╚██████╗╚██████╗╚██████╔╝   ██║   ██║  ██║███████║██║  ██║
╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                         
                                                              \n'''), pystyle.Colors.red_to_purple, interval = 0.000001)
        else:
            os.system("clear")
            pystyle.Write.Print(pystyle.Center.XCenter('''                                                                   
                               
             

                                                                                                                                    


███████╗██╗   ██╗ ██████╗ ██████╗ ██████╗ ████████╗ █████╗ ███████╗██╗  ██╗
██╔════╝██║   ██║██╔════╝██╔════╝██╔═══██╗╚══██╔══╝██╔══██╗██╔════╝██║  ██║
███████╗██║   ██║██║     ██║     ██║   ██║   ██║   ███████║███████╗███████║
╚════██║██║   ██║██║     ██║     ██║   ██║   ██║   ██╔══██║╚════██║██╔══██║
███████║╚██████╔╝╚██████╗╚██████╗╚██████╔╝   ██║   ██║  ██║███████║██║  ██║
╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                         

                
                                                     \n'''), pystyle.Colors.red_to_purple, interval = 0.00001)



        menu_content = """
   ┌──────────────────────────────────────────────────────────────────────────────────┐
      • 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛 -  @shxpe     • 𝚅𝚎𝚛𝚜𝚒𝚘𝚗 - 𝟷.𝟶.𝟶    • Кажд3й Д3нь В3с3лье             
   └──────────────────────────────────────────────────────────────────────────────────┘

                        ┌────────────────────────────────────┐                                  
                        │ [1] • Посчитать буквы               │
                        │ [2] • Уязвимости                    │
                        │ [3] • Выход                         │
                        └────────────────────────────────────┘
"""
        pystyle.Write.Print(center_text("",columns) + draw_box(menu_content, box_width, box_height), pystyle.Colors.red_to_purple, interval=0.00000001)

        choice = get_user_input("\n\n[?] • 𝚂𝚎𝚕𝚎𝚌𝚝 𝙼𝚎𝚗𝚞 𝙸𝚝𝚎𝚖 -> ")

        if choice == "1":
            sentence = get_user_input("Напишите предложение: ")
            letter_count = count_letters(sentence)
            clear_console()
            pystyle.Write.Print(pystyle.Center.XCenter(draw_box(f"Количество букв в предложении: {letter_count}", box_width, box_height)), pystyle.Colors.green_to_cyan, interval=0.002)
            pystyle.Write.Input("\n\n[?] Нажмите Enter для возврата в меню...", pystyle.Colors.green_to_cyan, interval=0.005)
            continue
        elif choice == "2":
             vulnerabilities_menu(rows, columns, box_width, box_height)
             
        elif choice == "3":
            clear_console()
            pystyle.Write.Print(pystyle.Center.XCenter(draw_box("Выход из программы.", box_width, box_height)), pystyle.Colors.red_to_purple, interval=0.002)
            break
        else:
            clear_console()
            pystyle.Write.Print(pystyle.Center.XCenter(draw_box("Ошибка: Некорректный ввод. Пожалуйста, выберите доступный вариант.", box_width, box_height)), pystyle.Colors.red_to_red, interval=0.002)


if __name__ == "__main__":
    main()
