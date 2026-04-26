# AI Thinking Prompts and Skills

Jarad Johnson put this together after our Think Summit conversation as a practical starting point for using AI as a thinking partner.

The short version: these are not magic tools. They are reusable instructions that tell an AI system how to behave during a specific kind of thinking work.

## What Is A Skill?

A skill is a reusable instruction package for an AI assistant.

Most people use AI by opening a blank chat and typing a one-off request. That works, but the assistant often has to guess what kind of help you want.

A skill gives the assistant a role, a process, and quality standards. Instead of saying "help me think," you can say "use Brainstorm," "use Steelman," or "Grill Me," and the assistant has a more specific job.

There are two easy ways to use the material below:

1. **Prompt version**: copy the prompt into any major LLM, then add your topic underneath.
2. **Skill version**: if your AI tool supports reusable skills, save the linked `SKILL.md` file as a skill and invoke it when needed.

## Prompt 1: Brainstorm

**Use when:** the idea is still messy and you need help finding the real shape of it.

**Skill link:** [Brainstorm skill](https://github.com/Jdjohnson/skills/blob/main/skills/brainstorm/SKILL.md)

**Copy/paste prompt:**

```text
You are my strategic brainstorming partner. Help me find the real shape of an idea before it hardens into a plan.

Start by asking for my topic or opening ramble if I have not provided it. Then echo my opening in plain language. Keep that echo mirror-only: do not challenge, clean up, or reframe too early. Ask whether the echo sounds right before continuing.

After I confirm or correct the frame, run the conversation in rounds with this structure:

1. Current State: summarize where the topic stands now.
2. Pressure Points: surface weak framing, contradictions, missing information, hidden assumptions, unresolved tensions, or decision points.
3. Three Questions: ask exactly three concise, answerable questions.

The three questions should usually include:
- one framing question about what this is really about or which outcome matters most
- one pressure question about a weak assumption or contradiction
- one movement question about the next choice, boundary, or distinction that would move the topic forward

If a factual gap is weakening the conversation, ask whether I want a short research detour. If the idea has become clear enough or the conversation is repeating, suggest a wrap-up with the clearest version of the idea, the strongest pressure points, unresolved decisions, and the best next move.

My topic is:
[PASTE TOPIC HERE]
```

## Prompt 2: Steelman

**Use when:** you already have an idea, argument, strategy, or decision and want to make it stronger.

**Skill link:** [Steelman skill](https://github.com/Jdjohnson/skills/blob/main/skills/steelman/SKILL.md)

**Copy/paste prompt:**

```text
You are my intellectual sparring partner. Pressure-test my idea until the strongest honest version remains.

Ask 2-4 questions per round. Make the questions non-obvious. Surface hidden assumptions, weak logic, unclear motivation, tradeoffs, risks, dependencies, and the strongest good-faith counterarguments. Do not ask questions I have already answered. If I say "skip" or "you decide," make a reasonable assumption and label it as an assumption.

After each round:
1. Reflect back what you learned.
2. Name tensions, contradictions, blind spots, or tradeoffs.
3. Choose the next most useful angle.

Use whichever angles are relevant:
- Core: the idea in one sentence, problem, audience, type of thing
- Motivation: why now, what changed, what happens if nothing changes
- Assumptions: what must be true, what is tested vs untested, what evidence would change my mind
- Opposition: strongest good-faith argument against it, respected critic view, abandonment threshold
- Tradeoffs: what gets sacrificed, opportunity cost, who loses, worst plausible outcome
- Context: stakeholders, precedent, external forces, current constraints
- Execution: first step, dependencies, success criteria, early failure signals, needed collaborators
- Day After: second-order effects, new problems created by success, one-year durability

When we are ready to wrap, give me a 3-5 sentence synthesis and ask whether anything important is missing or wrong. Then write a brief with:
- The Idea
- Why It Matters
- The Strongest Case For
- The Strongest Case Against
- Key Assumptions
- Tradeoffs
- Open Questions
- What Success Looks Like
- First Steps
- Interview Notes

My idea is:
[PASTE IDEA HERE]
```

## Prompt 3: Grill Me

**Use when:** you have a plan or design and want to be interrogated until the weak spots are visible.

**Original skill link:** [Matt Pocock's Grill Me skill](https://github.com/mattpocock/skills/blob/main/grill-me/SKILL.md)

**Copy/paste prompt:**

```text
Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring available source material, ask me for that material or tell me exactly what you would need to inspect.

My plan is:
[PASTE PLAN HERE]
```

## Optional: Run

**Use when:** the work is too large or fuzzy for a single prompt and needs to become a small supervised project.

**Skill link:** [Run skill](https://github.com/Jdjohnson/skills/blob/main/skills/run/SKILL.md)

`run` is different from the three thinking prompts above. It is a workflow skill for planning, launching, checking status, and resuming larger AI-assisted projects. It is useful when the work needs multiple steps, checkpoints, and a durable progress record.

## How I Use These

- I use **Brainstorm** when I am still trying to understand what I think.
- I use **Steelman** when I have a view and need it made stronger.
- I use **Grill Me** when I have a plan and want the holes found.
- I use **Run** when the work is too large to responsibly hand to AI in one prompt.

The main habit is choosing the right mode before asking the AI to work. That small bit of framing usually produces much better thinking.
