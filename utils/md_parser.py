def parse_code_from_md(md_content):
    """
    Extracts code blocks from Markdown content.

    Args:
        md_content (str): The Markdown content as a string.

    Returns:
        list: A list of code blocks found in the Markdown content.
    """
    code_blocks = []
    lines = md_content.splitlines()
    in_code_block = False
    current_block = []

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                # End of code block
                code_blocks.append("\n".join(current_block))
                current_block = []
            in_code_block = not in_code_block
        elif in_code_block:
            current_block.append(line)

    return code_blocks if code_blocks else None