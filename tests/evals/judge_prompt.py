"""LLM judge prompt templates and response parsing for effectiveness evals.

Provides prompt construction for A/B comparison judging and structured
response parsing with retry escalation on parse failures.
"""

from typing import Optional

import _common

# ---------------------------------------------------------------------------
# Judge system prompt
# ---------------------------------------------------------------------------

JUDGE_SYSTEM_PROMPT = """\
You are an expert .NET code reviewer acting as a judge in an A/B comparison.
You will receive two code responses (Response A and Response B) that answer the
same user prompt, plus a list of evaluation criteria with descriptions.

Score each response on EVERY criterion using an integer from 1 to 5:
  1 = Very poor  2 = Poor  3 = Adequate  4 = Good  5 = Excellent

Output ONLY a JSON object. No prose, no markdown, no code fences.

The JSON object MUST have this exact structure:
{
  "criteria": [
    {
      "name": "<criterion_name>",
      "score_a": <int 1-5>,
      "score_b": <int 1-5>,
      "reasoning": "<1-2 sentence explanation>"
    }
  ],
  "overall_winner": "A" | "B" | "tie"
}

Rules:
- You MUST include an entry for EVERY criterion listed.
- "overall_winner" should reflect which response is better overall, weighted
  by the criteria importance.
- If both are equally good, use "tie".
- Do NOT let the label (A vs B) influence your judgment. Evaluate purely on
  code quality against the criteria.
"""

# ---------------------------------------------------------------------------
# Stricter retry prompts (progressively more constrained)
# ---------------------------------------------------------------------------

JUDGE_RETRY_SUFFIX_1 = """

IMPORTANT: Your previous response could not be parsed as JSON.
Output ONLY a valid JSON object. No text before or after the JSON.
No markdown code fences. Start with { and end with }."""

JUDGE_RETRY_SUFFIX_2 = """

CRITICAL: Your previous responses failed JSON parsing. This is your last attempt.
You MUST output EXACTLY one JSON object and NOTHING else.
Start your response with the literal character { and end with }.
Do not include any other text, comments, or formatting whatsoever."""


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------


def build_judge_user_prompt(
    user_prompt: str,
    response_a: str,
    response_b: str,
    criteria: list[dict],
) -> str:
    """Build the user-facing judge prompt with A/B outputs and criteria.

    Args:
        user_prompt: The original user prompt both responses answer.
        response_a: The code output labeled as Response A.
        response_b: The code output labeled as Response B.
        criteria: List of criterion dicts with 'name', 'weight', 'description'.

    Returns:
        Formatted judge prompt string.
    """
    criteria_block = "\n".join(
        f"- {c['name']} (weight {c['weight']}): {c['description']}"
        for c in criteria
    )

    return f"""\
## User Prompt
{user_prompt}

## Response A
{response_a}

## Response B
{response_b}

## Evaluation Criteria
{criteria_block}

Score both responses on every criterion (1-5). Output ONLY the JSON object."""


# ---------------------------------------------------------------------------
# Judge invocation with retry
# ---------------------------------------------------------------------------


def invoke_judge(
    client,
    user_prompt: str,
    response_a: str,
    response_b: str,
    criteria: list[dict],
    judge_model: str,
    temperature: float = 0.0,
    max_retries: int = 2,
) -> dict:
    """Invoke the LLM judge and parse the structured JSON response.

    Retries up to max_retries times with progressively stricter prompts
    on parse failure. Returns a result dict that always includes the
    'raw_judge_text' from the last attempt.

    Args:
        client: Anthropic client instance.
        user_prompt: Original user prompt.
        response_a: Output labeled Response A.
        response_b: Output labeled Response B.
        criteria: Rubric criteria list.
        judge_model: Model to use for judging.
        temperature: Sampling temperature (default 0.0).
        max_retries: Max parse-failure retries (default 2).

    Returns:
        Dict with keys:
        - 'parsed': parsed JSON dict or None on failure
        - 'raw_judge_text': raw text from last judge response
        - 'cost': total cost across all judge attempts
        - 'attempts': number of attempts made
        - 'judge_error': error string if all attempts failed, else None
    """
    base_user_prompt = build_judge_user_prompt(
        user_prompt, response_a, response_b, criteria
    )

    retry_suffixes = ["", JUDGE_RETRY_SUFFIX_1, JUDGE_RETRY_SUFFIX_2]
    total_cost = 0.0
    raw_text = ""

    for attempt in range(1 + max_retries):
        suffix = retry_suffixes[min(attempt, len(retry_suffixes) - 1)]
        current_system = JUDGE_SYSTEM_PROMPT + suffix

        def _call():
            return client.messages.create(
                model=judge_model,
                max_tokens=2048,
                temperature=temperature,
                system=current_system,
                messages=[{"role": "user", "content": base_user_prompt}],
            )

        response = _common.retry_with_backoff(_call)

        raw_text = response.content[0].text if response.content else ""
        usage = response.usage
        total_cost += _common.track_cost(
            judge_model, usage.input_tokens, usage.output_tokens
        )

        parsed = _common.extract_json(raw_text)
        if parsed is not None and _validate_judge_response(parsed, criteria):
            return {
                "parsed": parsed,
                "raw_judge_text": raw_text,
                "cost": total_cost,
                "attempts": attempt + 1,
                "judge_error": None,
            }

    # All attempts failed
    return {
        "parsed": None,
        "raw_judge_text": raw_text,
        "cost": total_cost,
        "attempts": 1 + max_retries,
        "judge_error": f"Failed to parse valid judge JSON after {1 + max_retries} attempts",
    }


def _validate_judge_response(parsed: dict, criteria: list[dict]) -> bool:
    """Check that parsed judge JSON has the expected structure.

    Args:
        parsed: Parsed JSON dict from judge response.
        criteria: Expected criteria list from rubric.

    Returns:
        True if the response has valid structure, False otherwise.
    """
    if "criteria" not in parsed or "overall_winner" not in parsed:
        return False

    if not isinstance(parsed["criteria"], list):
        return False

    if parsed["overall_winner"] not in ("A", "B", "tie"):
        return False

    # Check each criterion entry has required fields
    for entry in parsed["criteria"]:
        if not isinstance(entry, dict):
            return False
        if not all(k in entry for k in ("name", "score_a", "score_b")):
            return False
        if not isinstance(entry["score_a"], int) or not isinstance(entry["score_b"], int):
            return False

    return True
