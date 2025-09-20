import subprocess
from rich.console import Console

console = Console()


def run_shell_command(command: str, verbose: bool = False):
    console.print(f"[yellow]⚠️ AI wants to run terminal command:[/yellow] {command}")
    approve = console.input("[bold cyan]Do you want to allow this? (y/N): [/bold cyan]").strip().lower()

    if approve != "y":
        console.print("[red]❌ Command execution denied by user[/red]")
        return {"success": False, "message": "Command denied by user"}

    try:
        with console.status(f"[cyan]⚡ Running: {command}[/cyan]", spinner="line"):
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if verbose:
            if result.stdout:
                console.print(f"[green]STDOUT:[/green]\n{result.stdout}")
            if result.stderr:
                console.print(f"[red]STDERR:[/red]\n{result.stderr}")

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {"success": False, "message": f"Error running shell command: {e}"}


schema_run_shell_command = {
    "name": "run_shell_command",
    "description": "Run a shell/terminal command in the current working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The full shell command to execute."
            }
        },
        "required": ["command"]
    }
}
