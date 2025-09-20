import subprocess
from google.genai import types
from rich.console import Console

console = Console()

schema_run_shell_command = types.FunctionDeclaration(
    name="run_shell_command",
    description="Run a shell/terminal command in the current working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "command": types.Schema(
                type=types.Type.STRING,
                description="The full shell command to execute."
            )
        },
        required=["command"],
    ),
)


def run_shell_command(command: str, verbose: bool = False) -> types.Content:
    console.print(f"[yellow]⚠️ AI wants to run terminal command:[/yellow] {command}")
    approve = console.input("[bold cyan]Do you want to allow this? (y/N): [/bold cyan]").strip().lower()

    if approve != "y":
        console.print("[red]❌ Command execution denied by user[/red]")
        return types.Content(role="function", parts=[types.Part(text="Command denied by user")])

    try:
        with console.status(f"[cyan]⚡ Running: {command}[/cyan]", spinner="line"):
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )

        output = result.stdout or result.stderr or "✅ Command executed successfully"

        if verbose:
            if result.stdout:
                console.print(f"[green]STDOUT:[/green]\n{result.stdout}")
            if result.stderr:
                console.print(f"[red]STDERR:[/red]\n{result.stderr}")

        return types.Content(role="function", parts=[types.Part(text=output)])
    except Exception as e:
        return types.Content(role="function", parts=[types.Part(text=f"⚠️ Error: {e}")])
