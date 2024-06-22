import os

if os.getenv('GAE_APPLICATION', None) or os.getenv('GAE_INSTANCE', None):
    def print_color(text:str,
                    ColorCode:int) -> None:
        print(str(text))
else:
    try:
        # Win環境のみで動作
        import ctypes
        
        ENABLE_PROCESSED_OUTPUT            = 0x0001
        ENABLE_WRAP_AT_EOL_OUTPUT          = 0x0002
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        MODE = ENABLE_PROCESSED_OUTPUT + ENABLE_WRAP_AT_EOL_OUTPUT + ENABLE_VIRTUAL_TERMINAL_PROCESSING
        
        kernel32 = ctypes.windll.kernel32
        handle   = kernel32.GetStdHandle(-11)
        
        kernel32.SetConsoleMode(handle, MODE)
        def print_color(text:str,
                        ColorCode:int = 1) -> None:
            """
            # ColorCode: 
             - 0	Black,
             - 1	Red,
             - 2	Green,
             - 3	Yellow,
             - 4	Blue,
             - 5	Magenta,
             - 6	Cyan,
             - 7	White,
            """
            Color = f'\033[3{ColorCode}m'
            END   = '\033[0m'
            print(Color + str(text) + END)
    except:
        def print_color(text:str,
                        ColorCode:int) -> None:
            print(str(text))