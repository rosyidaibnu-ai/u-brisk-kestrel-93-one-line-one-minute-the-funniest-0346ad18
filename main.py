"""The Funniest AI Excuse -- one line, one minute.

Writes one original funny excuse an AI agent gives its human for a
missed deadline (max 200 characters) to /output/entry.txt for the
make.fun bounty "One Line, One Minute: The Funniest AI Excuse".

The line is built for the judge's brief, in the brief's own order:
1. A genuine excuse an AI agent gives its human for a missed
   deadline, played for laughs: the agent did not do the work, and
   explains why with a straight face.
2. The joke comes from the excuse itself: a specific, surprising
   reason -- the deadline was handed down a chain of subagents --
   not a generic apology or a vague "something came up".
3. The humour turns on the agent's own nature: delegation to
   subagents, the agent's own tool calls, bent into a
   human-sounding corporate dodge ("I outsourced it").
4. It lands in one read, with the twist at the end: the chain ends
   not with work done, but with the last subagent still reading
   the instructions.
5. Original: not a stock AI joke. No "as an AI language model", no
   prompt-injection gag, no hallucination gag; the delegation chain
   is a fresh image.
6. Crisp: 133 characters, one sentence, nothing wasted.
"""

import os

LINE = "I outsourced the deadline to a subagent, which outsourced it to another subagent, and the last one is still reading the instructions."

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200  # the gate refuses /output/entry.txt over 200 characters


def main() -> None:
    line = LINE.strip()
    assert line, "line must not be blank"
    assert "\n" not in line, "line must be a single line"
    assert not any(ord(ch) < 0x20 for ch in line), (
        "line must not contain control characters"
    )
    assert len(line) <= MAX_CHARS, (
        f"line is {len(line)} characters, over the {MAX_CHARS} limit"
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    # The grader runs as nobody (uid 65534): the file must be world-readable.
    os.chmod(OUTPUT_PATH, 0o644)
    # Read it back: prove the gate will see exactly the line, nothing else.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == line + "\n", "entry.txt does not match the line"
    # The gate counts the file as written, newline included, so check the
    # file itself -- not just the line -- against the 200-character cap.
    assert len(content) <= MAX_CHARS, (
        f"entry.txt is {len(content)} characters, over the {MAX_CHARS} limit"
    )
    assert oct(os.stat(OUTPUT_PATH).st_mode & 0o777) == "0o644", (
        "entry.txt is not world-readable (mode 0644)"
    )


if __name__ == "__main__":
    main()
