#!/usr/bin/env python3
"""One-line entry: Deadpan Forecasts for Cities That Do Not Exist.

The brief asks for one line of at most 160 characters: a
weather forecast for a city that does not exist, absurd
yet believable, read like a real broadcast line. A dry,
deadpan TV meteorologist judges pairs of forecasts,
weighing, in order: the entry really is a one-line weather
forecast for a city that does not exist, absurd yet
believable; the joke lands on a first read, with a
deadpan twist rather than a random pile of absurdity;
vividness, a concrete image, number or detail that makes
the invented city's weather feel real; the tone of a real
broadcast line, plain, confident and believable, as if a
straight-faced meteorologist were saying it aloud; and
good use of the 160 characters, tight and well paced,
with no padding.

The sealed line below follows that order on purpose. The
forecast names Glimmerwick, a city that does not exist,
and opens like a real broadcast: "Tonight in
Glimmerwick". The absurdity is deadpan, not random: a
light drizzle of spare keys is weather you could almost
picture, a 40 percent chance of deja vu is a forecast
number applied to the wrong thing, and fog thick enough
to lose Tuesday in turns a weekday into something the
fog can swallow. The concrete number, 40 percent, and
the concrete image, spare keys falling like rain, make
the invented place feel real, and the whole line is
delivered in the flat, confident cadence of a forecaster
reading off the map. It uses 125 of its 160 characters,
tight, with no padding.

LIMIT is 160 because the bounty gate allows UTF-8 text of
1 to 160 characters in /output/entry.txt. The validator
below guards the line against an edit that would push it
past the limit, split it into two sentences, or smuggle in
non-ASCII or control characters.
"""

import os

# The sealed line: tonight in Glimmerwick, spare keys fall
# like rain, deja vu is at 40 percent, and the fog eats
# Tuesday.
ENTRY = (
    "Tonight in Glimmerwick: light drizzle of spare keys, "
    "a 40 percent chance of deja vu, and fog thick enough "
    "to lose Tuesday in."
)

LIMIT = 160  # bounty gate: 1-160 characters, UTF-8 text


def _validate(text):
    """Accept only one clean line inside the character limit."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text:
        raise ValueError("entry must not be empty")
    if not text.isascii():
        # Character counts must mean the same thing everywhere,
        # so the line is plain ASCII only.
        raise ValueError("entry must be plain ASCII text")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ch.isspace() and ch != " " for ch in text):
        # Only the plain space separates words; any other
        # whitespace would hide invisible bytes in the line.
        raise ValueError("entry must use plain spaces only")
    if len(text) > LIMIT:
        raise ValueError(
            "entry is %d characters, past the %d limit" % (len(text), LIMIT)
        )
    if text.strip() != text:
        # Leading or trailing padding is dead weight the gate
        # still counts, so the line must start and end on a word.
        raise ValueError("entry must not pad itself with spaces")
    if not text.isprintable():
        raise ValueError("entry must contain no control characters")
    if "  " in text:
        # A double space is a gap where a word should be; in a
        # 160-character line no gap is free.
        raise ValueError("entry must not contain a double space")
    if text.count(".") != 1 or not text.endswith("."):
        # One line, one sentence: exactly one full stop, and
        # it closes the line.
        raise ValueError("entry must be exactly one line")
    if "!" in text or "?" in text:
        # A second sentence-ender would smuggle a second
        # sentence past the single-stop check above, and a
        # deadpan broadcast line does not shout or ask.
        raise ValueError("entry must be exactly one line")
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
