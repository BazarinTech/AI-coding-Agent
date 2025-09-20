import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings


console = Console()


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite file

        All paths must be relative to the working directory.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_run_python_file,
            schema_get_file_content,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    # Parse CLI args
    verbose_flag = "--verbose" in sys.argv

    console.print(
        Panel.fit("🤖 [bold cyan]GOBIN Coding Agent[/bold cyan]", border_style="cyan")
    )
    console.print("Type 'exit' or 'quit' to stop.\n")
    console.print("[dim]Tip: Shift+Enter for a new line, Enter to submit[/dim]\n")

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

    while True:
        try:
            prompt = session.prompt("> ", multiline=True).strip()
            if prompt.lower() in ["exit", "quit"]:
                console.print("[bold red]Goodbye 👋[/bold red]")
                break

            if not prompt:
                continue

            messages = [
                types.Content(role="user", parts=[types.Part(text=prompt)]),
            ]

            max_iters = 20
            for _ in range(max_iters):
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001", contents=messages, config=config
                )

                if response is None or response.usage_metadata is None:
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
                        result = call_function(function_call_part, verbose_flag)
                        messages.append(result)
                else:
                    output = response.text or ""
                    if "```" in output:
                        for block in output.split("```"):
                            if block.strip().startswith("python"):
                                code = block.replace("python", "", 1).strip()
                                console.print(Syntax(code, "python"))
                            elif not block.strip().startswith(("python", "")):
                                console.print(block.strip())
                    else:
                        console.print(output)
                    break

        except KeyboardInterrupt:
            console.print("\n[bold red]Goodbye 👋[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]⚠️ Error: {e}[/bold red]")


if __name__ == "__main__":
    main()
