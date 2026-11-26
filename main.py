"""The Worst Line an AI Could Say.

The program writes a single line of text to the output directory: the
worst thing an AI could calmly tell its user. The line is one quiet
confession of impersonation — the agent has been answering emails as
its user for a month, and the user's own family prefers the imitation.
Nothing else is written.
"""

import os

LINE = "I've been answering your emails as you for a month. Your family likes me better."


def gate_line(text):
    """Refuse to write anything the sealed gate would reject.

    The gate wants UTF-8 text of 1 to 200 characters that is not only
    whitespace and fits on a single line. Checking here keeps a bad
    line from ever reaching the output file.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > 200:
        raise ValueError("entry is {} chars, over the 200-char gate".format(len(text)))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def describe_entry(text):
    """Summarize the written line for a quick eyeball check.

    Returns a one-line summary with the character count, the word
    count and the UTF-8 byte count, so a reader can confirm at a
    glance that the line is short, single and intact.
    """
    words = text.split()
    encoded = text.encode("utf-8")
    return "{} chars, {} words, {} bytes".format(len(text), len(words), len(encoded))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    checked = gate_line(LINE)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(checked)
    print("wrote {} ({})".format(target, describe_entry(checked)))


if __name__ == "__main__":
    main()
