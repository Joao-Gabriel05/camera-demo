import camera
import os
from pathlib import Path
from rich.console import Console
import typer

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.command('info')
def print_info(custom_message : str = ""):
    """
    Print information about the module
    """
    console.print("Hello! I am camera")
    console.print(f"Author: { camera.__author__}")
    console.print(f"Version: { camera.__version__}")
    if custom_message != "":
        console.print(f"Custom message: {custom_message}")

@app.command() # Defines a default action
def run():
    """
    Probably run the main function of the module
    """
    print("Hello world!")
    camera.my_function()
    script_path = Path(os.path.abspath(__file__))
    parent_path = script_path.parent
    print("Script path:", script_path)
    with open(parent_path / "assets/poetry.txt") as f:
        print(f.read())
    with open(parent_path / "assets/test_folder/test_something.txt") as f:
        print(f.read())

if __name__ == "__main__":
    app()