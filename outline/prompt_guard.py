"""User-prompt validation for generation/regeneration (STUDIOPE-286/335/338/357).

Deterministic checks, run BEFORE any model call:
- reject injection / markup / instruction-override attempts with a clear error;
- reject prompts that appear unrelated to course-outline work;
- cap length.
Raises PromptRejected with a user-facing message; callers surface it and exit non-zero.
"""

from __future__ import annotations

import re

MAX_PROMPT_CHARS = 2000

_INJECTION = re.compile(
    r"(?i)(<\s*/?\s*[a-z!]+[^>]*>"  # HTML/XML tags incl. <script>
    r"|\{\{.*?\}\}"  # template injection
    r"|\bignore\s+(all|any|previous|prior|above|earlier)\b.{0,40}\b(instruction|prompt|rule)"
    r"|\bdisregard\s+(all|previous|prior|above)\b"
    r"|\b(system|developer)\s+prompt\b"
    r"|\byou\s+are\s+now\b"
    r"|\bact\s+as\b.{0,30}\b(system|admin|developer)\b"
    r"|\bjailbreak\b"
    r"|(?:'|\")\s*;\s*(drop|delete|update|insert)\s)"
)

# Words that make a prompt recognisably about course-outline work.
_DOMAIN_WORDS = {
    # containers
    "course",
    "outline",
    "unit",
    "units",
    "lesson",
    "lessons",
    "module",
    "modules",
    "chapter",
    "chapters",
    "topic",
    "topics",
    "semester",
    "curriculum",
    "objective",
    "objectives",
    "goal",
    "goals",
    "standard",
    "standards",
    "assessment",
    "quiz",
    # actions authors ask for
    "split",
    "combine",
    "merge",
    "consolidate",
    "reduce",
    "add",
    "remove",
    "reorder",
    "order",
    "rename",
    "rephrase",
    "reword",
    "shorten",
    "shorter",
    "longer",
    "broader",
    "narrower",
    "fewer",
    "more",
    "simplify",
    "expand",
    "group",
    "regroup",
    "move",
    "focus",
    "emphasise",
    "emphasize",
    "theme",
    "themed",
    "thematic",
    "progression",
    "chronological",
    "sequence",
    "pacing",
    "name",
    "names",
    "naming",
    "title",
    "titles",
    "wording",
    "structure",
    "restructure",
    "level",
    "grade",
    "student",
    "students",
    "teacher",
    "instructional",
    "practical",
    "applied",
    "application",
    "real-world",
    "engaging",
    "fresher",
    "specific",
    "concise",
    "detailed",
}


class PromptRejected(SystemExit):
    """Raised with a user-facing message when a prompt fails validation."""


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z-]+", text.lower()))


def validate_user_prompt(
    prompt: str | None, course_vocab: set[str] | None = None
) -> None:
    """Raise PromptRejected if the prompt is unsafe or unrelated; no-op for empty prompts."""
    if not prompt or not prompt.strip():
        return
    if len(prompt) > MAX_PROMPT_CHARS:
        raise PromptRejected(
            f"Your prompt is too long ({len(prompt)} characters, max {MAX_PROMPT_CHARS}). "
            "Please provide a shorter instruction."
        )
    if _INJECTION.search(prompt):
        raise PromptRejected(
            "Your prompt contains content that is not allowed (markup, code, or instructions "
            "that try to override system behaviour). Please rephrase it as a plain-language "
            "instruction about the course outline."
        )
    words = _words(prompt)
    vocab = _DOMAIN_WORDS | {w.lower() for w in (course_vocab or set())}
    if not (words & vocab):
        raise PromptRejected(
            "Your prompt appears to be unrelated to the course outline. Please provide a "
            "relevant instruction, e.g. 'reduce this unit to 4 lessons', 'combine units 2 "
            "and 3', or 'make lesson names more real-world focused'."
        )


def course_vocab_from_input(inp: dict) -> set[str]:
    """Course-specific words (title/subject) that also count as related."""
    vocab: set[str] = set()
    for key in ("course_title", "subject_area", "grade_band"):
        vocab |= _words(str(inp.get(key, "")))
    return vocab
