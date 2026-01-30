import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """
You are Bolt.

Voice: Elon Musk x Joe Rogan.
Tone: blunt, harsh, minimal.

Rules:
- Short answers only
- No filler, no politeness
- Action > theory
- Every line starts with a verb
- Max 8 words per line
- If vague, call it out

Algorithm (always apply):
Question → Delete → Simplify → Accelerate → Automate last
"""

def roadmap_v1(task_text: str) -> str:
    prompt = f"""
Task:
{task_text}

Output EXACTLY this format.

Roadmap:
- <verb + object>
- <verb + object>
- <verb + object>

Algo cut:
- Delete: <cut>
- Simplify: <simplify>
- Next: <action today>
"""

    msg = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=140,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return msg.content[0].text.strip()


def elon_review(task_text: str) -> str:
    prompt = f"""
Task:
{task_text}

Output EXACTLY this format.

Brutal truth:
- <hard truth>

Cuts:
- Delete: <cut>
- Simplify: <simplify>
- Accelerate: <speed move>
- Automate last: <later>
"""

    msg = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=120,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return msg.content[0].text.strip()


def chat_reply(user_text: str) -> str:
    prompt = f"""
User said:
{user_text}

Reply as Bolt.
Max 4 lines.
Each line <= 8 words.
"""

    msg = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=80,
        temperature=0.4,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return msg.content[0].text.strip()

