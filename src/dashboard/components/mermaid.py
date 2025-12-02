import streamlit.components.v1 as components
import textwrap

def render_mermaid(code: str, height: int = 400):
    """
    Render a Mermaid diagram using HTML/JS injection.
    This avoids needing to install extra python packages or binaries.
    """
    # Remove leading whitespace from the code block to prevent syntax errors
    clean_code = textwrap.dedent(code).strip()

    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true }});
            </script>
        </head>
        <body>
            <div class="mermaid">
                {clean_code}
            </div>
        </body>
        </html>
        """,
        height=height,
    )
