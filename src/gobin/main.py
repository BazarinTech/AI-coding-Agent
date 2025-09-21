import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from .functions.get_files_info import schema_get_files_info
from .functions.get_file_content import schema_get_file_content
from .functions.run_python import schema_run_python_file
from .functions.write_file import schema_write_file
from .functions.run_shell import schema_run_shell_command
from .functions.create_directory import schema_create_directory
from .call_function import call_function
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

console = Console()


def load_api_key():
    """Try loading GEMINI_API_KEY from .env or environment."""
    package_root = Path(__file__).resolve().parent.parent
    env_path = package_root / ".env"

    if env_path.exists():
        load_dotenv(env_path)
    load_dotenv(dotenv_path=Path(".") / ".env")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        console.print(
            "[bold red]❌ GEMINI_API_KEY not found![/bold red]\n"
            "Set it in your environment:\n\n"
            "   export GEMINI_API_KEY='your_api_key_here'\n\n"
            "Or create a .env file with:\n\n"
            "   GEMINI_API_KEY=your_api_key_here\n"
        )
        sys.exit(1)
    return api_key


def main():
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    cwd = os.getcwd()

    system_prompt = f"""
        You are a helpful AI coding agent.

        Current working directory: {cwd}

        When a user asks a question or makes a request, make a function call plan. 
        You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite file
        - Run shell commands (with user approval)

        All paths must be relative to this working directory unless the user specifies otherwise.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_run_python_file,
            schema_get_file_content,
            schema_run_shell_command,
            schema_create_directory,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    verbose_flag = "--verbose" in sys.argv

    def print_welcome():
        console.print(
            Panel.fit("🤖 [bold cyan]GOBIN AI Coding Agent[/bold cyan]", border_style="cyan")
        )
        console.print("Type 'exit' or 'quit' to stop.\n")
        console.print("[dim]Tip: Shift+Enter for a new line, Enter to submit[/dim]\n")
        console.print("[dim]Type 'clear' or 'cls' to clear the screen[/dim]\n")

    print_welcome()

    # Setup prompt_toolkit session with multiline support
    bindings = KeyBindings()

    @bindings.add("enter")
    def _(event):
        buffer = event.app.current_buffer
        if buffer.complete_state:
            buffer.complete_state = None
        elif buffer.document.is_cursor_at_the_end and not buffer.text.endswith("\n"):
            event.app.exit(result=buffer.text)
        else:
            buffer.insert_text("\n")

    session = PromptSession(key_bindings=bindings)
    messages = []

    while True:
        try:
            prompt = session.prompt(
                "\nEnter a Prompt > ", multiline=True
            ).strip()

            if prompt.lower() in ["exit", "quit"]:
                console.print("[bold red]👋 Goodbye![/bold red]")
                break

            if prompt.lower() in ["clear", "cls"]:
                console.clear()
                print_welcome()
                continue

            if not prompt:
                continue

            # Show user input panel
            console.print(
                Panel(
                    Markdown(prompt),
                    title="[bold magenta]User Prompt[/bold magenta]",
                    border_style="magenta"
                )
            )

            messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

            max_iters = 20
            for _ in range(max_iters):
                with console.status("[bold cyan]🤖 Thinking...[/bold cyan]", spinner="dots"):
                    response = client.models.generate_content(
                        model="gemini-2.0-flash-001",
                        contents=messages,
                        config=config,
                    )

                if not response or not response.usage_metadata:
                    console.print("[bold red]⚠️ Response malformed[/bold red]")
                    break

                if verbose_flag:
                    console.print(
                        Panel.fit(
                            f"[yellow]Prompt tokens:[/yellow] {response.usage_metadata.prompt_token_count}\n"
                            f"[yellow]Response tokens:[/yellow] {response.usage_metadata.candidates_token_count}",
                            title="🔎 Debug Info",
                            border_style="yellow",
                        )
                    )

                if response.candidates:
                    for candidate in response.candidates:
                        if candidate and candidate.content:
                            messages.append(candidate.content)

                if response.function_calls:
                    for function_call_part in response.function_calls:
                        # ⬇️ call_function now returns (content, dict)
                        content, response_dict = call_function(function_call_part, verbose_flag)
                        messages.append(content)

                        # --- Execution Summary ---
                        success = response_dict.get("success", False)
                        message = response_dict.get("message", "")

                        summary_text = (
                            f"[bold green]✅ Operation successful[/bold green]\n"
                            if success else f"[bold red]❌ Operation failed[/bold red]\n"
                        )
                        summary_text += f"[cyan]Function:[/cyan] {function_call_part.name}\n"
                        summary_text += f"[cyan]Message:[/cyan] {message}\n\n"

                        if success:
                            summary_text += (
                                "👉 [bold]Next step:[/bold] Continue with your next request "
                                "or run the updated code to verify changes."
                            )
                        else:
                            summary_text += (
                                "⚠️ [bold]Next step:[/bold] Review the error above and fix inputs or code."
                            )

                        console.print(
                            Panel(summary_text, title="✨ Execution Summary", border_style="cyan")
                        )

                else:
                    output = response.text or ""
                    if "```" in output:
                        for block in output.split("```"):
                            if block.strip().startswith("python"):
                                code = block.replace("python", "", 1).strip()
                                console.print(Syntax(code, "python"))
                            elif block.strip():
                                console.print(block.strip())
                    else:
                        console.print(output)
                    break

        except KeyboardInterrupt:
            console.print("\n[bold red]👋 Goodbye![/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]⚠️ Error: {e}[/bold red]")


if __name__ == "__main__":
    main()
