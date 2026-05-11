# CONTINUATION-GATE.md

> Recursive continuation protocol for Codex/Kai work in MY UNIVERSE.
> Use this when a task list reaches `Continue`.

---

## Purpose

`Continue` is not a normal task. It is a loop trigger.

When a task list reaches `Continue`, do not stop because the previous slice is
clean. Build the next concrete task list, put `Continue` at the end again, and
keep working unless there is a real blocker or Satish asks a direct question.

## Gate Sequence

1. **Reflect on the slice.** What changed, what failed, what surprised, and
   what evidence now exists?
2. **Read current repo evidence.** Check tracker state, `tools/next.py`, git
   status, and any affected docs/tests.
3. **Use judgment.** Prefer real project work over self-referential process.
4. **Optional xhigh reviewer.** If the next path is unclear, risky, broad, or
   likely to become self-referential, ask an xhigh subagent reviewer to critique
   the path before creating the next task list.
5. **Create the next list.** Convert the review into concrete tasks.
6. **Append `Continue`.** The final task must be `Continue`.

## Reviewer Prompt Shape

Use a reviewer for critique, not ownership:

```text
Review the current repo state and proposed next path. Do not edit files.
Find risks, stale assumptions, self-referential drift, missing verification,
and the highest-value next task list. End the proposed list with Continue.
```

## Task List Rule

Every active task list must end like this:

```markdown
- [ ] Continue — create the next concrete task list, append Continue again,
  and keep working unless blocked or directly asked to answer.
```

Do not mark `Continue` complete as a stopping signal. If it is marked complete,
the same update must create the next task list with a new `Continue`.

## Hard Boundaries

- No deletion. Archive first if anything must move.
- Do not write Codex/Kai data into Claude's `CALIBRATE.md` or `REFLECT.md`.
- Completion claims require fresh command, diff, test, or review evidence.
- The reviewer is optional. The continuation loop is not optional when Satish
  has said to keep working.

## Continue

- [ ] Continue — after using this gate, create the next concrete task list with `Continue` as the final item.
