#!/usr/bin/env python3
"""Deadpan forecast for a place that was never built.

This program writes a single 122-character line: a deadpan
weather forecast for Vexford, a city that nobody will find
on any map. The bounty wants one sentence, no more than 160
characters, funny in a flat, broadcast-voice way — the sort
of line a meteorologist delivers without smiling while the
weather behind them stops obeying physics.

Why this line works as the entry: it starts exactly like a
real forecast, "Tomorrow in Vexford", and every detail after
that stays close to real-broadcast language. A high of 61 is
unremarkable. Umbrellas scattered at noon is odd but not
shouted about. A 70 percent chance that rain falls upward
after 3 p.m. is the impossible bit, and it is reported in the
same calm voice as the temperature. The joke is the gap
between the impossible event and the unbothered tone, not a
pile of extra weirdness. Numbers anchor it — 61, 70 percent,
3 p.m. — so the invented city feels like somewhere with an
actual weather desk, and at 122 characters out of 160 there
is no filler word anywhere in it.

The rest of this file is plumbing: a guard that checks the
sealed sentence before it is written out, so no later edit
can quietly break the bounty gate (one line, plain ASCII,
no longer than 160 characters), plus a main() that writes
the line to entry.txt and echoes it to stdout.
"""

import os

# The sealed line: tomorrow in Vexford, 61 degrees, stray
# umbrellas drift overhead at noon, and the afternoon rain
# has a 70 percent chance of falling upward after 3 p.m.
ENTRY = (
    "Tomorrow in Vexford: a high of 61, scattered umbrellas "
    "at noon, and a 70 percent chance the rain falls upward "
    "after 3 p.m."
)

LIMIT = 160  # bounty gate: 1-160 characters, UTF-8 text


def _validate(text):
    """Reject anything that is not one clean line under the limit.

    Checks run in a deliberate order: shape first (type, length,
    one line), then character hygiene, then sentence structure.
    """
    if not isinstance(text, str):
        raise ValueError("expected a string, got %s" % type(text).__name__)
    if len(text) == 0:
        raise ValueError("the line is empty")
    if len(text) > LIMIT:
        raise ValueError(
            "the line is %d characters; the gate allows at most %d"
            % (len(text), LIMIT)
        )
    if text != text.strip():
        # A gate that counts characters also counts padding, so
        # the line may not start or end on a blank.
        raise ValueError("the line may not begin or end with a space")
    if "\n" in text or "\r" in text:
        raise ValueError("the entry must fit on a single line")
    if not text.isascii():
        # If a character is not ASCII, its byte length and its
        # character length stop agreeing, and the gate measures
        # one of them; keep the line plain ASCII so both agree.
        raise ValueError("only plain ASCII characters are allowed")
    if not text.isprintable():
        raise ValueError("control characters are not allowed in the line")
    if any(ch.isspace() and ch != " " for ch in text):
        # Tabs and other invisible separators would survive the
        # one-line check while smuggling odd bytes into the file.
        raise ValueError("only ordinary spaces may separate the words")
    if "  " in text:
        # Two spaces in a row is a missing word, not emphasis,
        # and this line has no characters to spare.
        raise ValueError("two spaces in a row are not allowed")
    # Sentence structure: the line is one sentence, and its only
    # abbreviation is "p.m.". Strip that abbreviation out first,
    # then the text that remains must contain no full stop at all
    # — both stops in the line belong to "p.m.", and the line
    # closes on the second of them — and no question or
    # exclamation mark anywhere.
    body = text[:-4] if text.endswith(" p.m.") else text
    if text.endswith(" p.m.") and body.count(".") != 0:
        raise ValueError("the line must be a single sentence")
    if not text.endswith(" p.m."):
        raise ValueError('the line must close on the "p.m." abbreviation')
    if "!" in body or "?" in body:
        # A deadpan forecast neither shouts nor asks; either mark
        # would also mean a second sentence hiding in the line.
        raise ValueError("the line must be a single sentence")
    return text


def main():
    entry = _validate(ENTRY)
    outdir = "/output" if os.path.isdir("/output") else "."
    path = os.path.join(outdir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(entry)
    print("%s (%d characters)" % (path, len(entry)))
    print(entry)


if __name__ == "__main__":
    main()
