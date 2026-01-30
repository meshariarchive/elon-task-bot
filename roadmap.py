def roadmap_v1(task_text: str) -> str:
    t = task_text.strip()
    return f"""🗺️ Roadmap v1
Task: {t}

1) Define “done”
   - One sentence success criteria
   - Constraints (time/budget/tools/people)

2) Break into milestones
   - Milestone A: Requirements / inputs
   - Milestone B: First draft (v1)
   - Milestone C: Review + iterate
   - Milestone D: Finalize + deliver

3) Execution checklist
   - Gather inputs
   - Produce v1 fast
   - Get feedback early
   - Apply fixes + polish
   - Deliver + document
"""

def elon_review(task_text: str) -> str:
    t = task_text.strip()
    return f"""⚡ Elon Review (5-step filter)
Task: {t}

1) Question requirements
   - What is the real outcome?
   - Which “must-have” is actually optional?
   - What assumption could be wrong?

2) Delete
   - Remove steps that don’t change the outcome
   - Avoid perfection early

3) Simplify / optimize
   - Fewer handoffs, fewer steps
   - Use templates/checklists

4) Accelerate
   - Tight feedback loops (v1 early)
   - Parallelize where possible

5) Automate (last)
   - Only automate after deleting/simplifying
   - Add reminders + reusable templates
"""

