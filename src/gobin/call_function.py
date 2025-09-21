from .functions.get_files_info import get_files_info
from .functions.get_file_content import get_file_content
from .functions.run_python import run_python_file
from .functions.write_file import write_file
from .functions.run_shell import run_shell_command
from .functions.create_directory import create_directory
from google.genai import types
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
working_directory = os.getcwd()


def call_function(function_call_part, verbose=False) -> types.Content:
    """
    Calls a function based on function_call_part and wraps the output
    in exactly one types.Content with one types.Part, as required by GenAI API.
    """
    name = function_call_part.name
    args = function_call_part.args or {}

    # --- Pretty log before execution ---
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Function", style="bold magenta")
    table.add_column("Arguments", style="cyan")
    table.add_row(name, str(args) if args else "None")

    console.print(Panel(table, title="⚡ Executing Function", border_style="cyan"))

    # Default result in case function is unknown
    result = {"success": False, "message": f"Unknown function: {name}"}

    # Map function names to actual calls
    if name == "get_files_info":
        result = get_files_info(working_directory, **args)
    elif name == "get_file_content":
        result = get_file_content(working_directory, **args)
    elif name == "run_python_file":
        result = run_python_file(working_directory, **args)
    elif name == "write_file":
        result = write_file(working_directory, **args)
    elif name == "run_shell_command":
        result = run_shell_command(**args, verbose=verbose)
    elif name == "create_directory":
        result = create_directory(args.get("path"), verbose)

    # --- Normalize result ---
    if isinstance(result, str):
        result = {"success": True, "message": result}
    elif isinstance(result, (types.FunctionResponse,)):
        # If it's a FunctionResponse, extract raw dict
        result = result.to_dict() if hasattr(result, "to_dict") else {"success": True, "message": str(result)}

    # Extract safely
    success = result.get("success", True)
    message = result.get("message", "")

    # --- Pretty log after execution ---
    status = "✅ SUCCESS" if success else "❌ FAILED"
    color = "green" if success else "red"

    console.print(
        Panel(
            f"[bold {color}]{status}[/bold {color}]\n\n"
            f"[cyan]Message:[/cyan] {message}",
            title="📋 Result",
            border_style=color,
        )
    )

    return (
        types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response=result
                )
            ],
        ),
        result  # return dict separately for easy access
    )
