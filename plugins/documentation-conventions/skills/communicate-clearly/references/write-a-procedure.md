# Write a procedure

← [Back to communicate-clearly](../SKILL.md)

The eight rules for any procedure: a document the reader follows rather than
studies. The house style applies as well.

## What counts as a procedure

- system runbooks and setup guides, such as `ingress-vm-setup-guide.md`, the deploy
  runbook and restoring a backup;
- the protocols in the guidance hubs;
- the swimming progressions;
- the guides in this skill;
- skills and `AGENTS.md` steps, which are procedures an AI follows.

A procedure is read at a bad moment: an outage, or a setup step half-remembered
months later. An AI agent follows it literally. Ambiguity costs more for both
readers, which is why procedures get rules that explanations do not.

## The eight rules

### 1. One instruction per sentence, one action per numbered step

**Why.** A reader who completes one action and looks back must find their place. Two
actions in one step get one of them skipped.

- Bad: "3. Unlock the volume and start OrbStack, then check the VM is up."
- Good:
  "3. Unlock the volume.
  4. Start OrbStack.
  5. Check that the VM is running: `orb list`."

### 2. Imperative and active voice

**Why.** The imperative says who acts: the reader. The passive leaves the reader
unsure whether to act or wait.

- Bad: "The script should be run before the deploy."
- Good: "Run the script before the deploy."

### 3. The condition before the action

**Why.** A reader acts as they read. A condition at the end of the sentence arrives
after they have already acted.

- Bad: "Run `npm ci` again if the build fails."
- Good: "If the build fails, run `npm ci` again."

### 4. A warning before the step it applies to

**Why.** A warning after a step is read after the damage is done.

- Bad: "5. Run `git reset --hard`. This discards uncommitted work."
- Good: "5. Commit or stash any work you want to keep. The next step discards it.
  6. Run `git reset --hard`."

### 5. One name for each thing, all the way through

**Why.** In a procedure, a new name means the reader looks for a new thing: "the Mini",
"the server" and "the host" send them to three machines.

- Bad: "SSH to the Mini. On the host, restart nginx."
- Good: "SSH to the Mini. On the Mini, restart nginx."

### 6. Short sentences

**Why.** Long sentences hide steps and conditions. Aim for 20 words or fewer in a
step.

**The machine check.** personal-portal runs `tests/docs/ste-sentence-length.test.ts`.
It fails when a listed procedural document has a sentence of more than 25 words. Add
each new runbook to the `PROCEDURAL` list in that file. It is the only rule checked
by machine; the others are caught by reading or by `/review`.

### 7. Say what the reader should see after a step

**Why.** Without it the reader cannot tell a step that worked from one that failed
quietly, and the failure surfaces three steps later.

- Bad: "Reload nginx."
- Good: "Reload nginx: `sudo nginx -s reload`. The command prints nothing when it
  succeeds."

### 8. No explanation inside a step

**Why.** An explanation in a step buries the action. Put the reason before the
procedure, or link to it.

- Bad: "4. Set `forward_ports` off, because OrbStack otherwise forwards every port a
  VM listens on to the Mac's localhost, which shadows the Mac's own services."
- Good: "4. Set `forward_ports` off. See [Why port forwarding is
  off](#why-port-forwarding-is-off)."

## Where the rules come from

These rules keep what makes ASD-STE100 Simplified Technical English work for
procedures, and drop its controlled dictionary, which cannot be followed without a
checker. The Google and Microsoft style guides give the same advice for procedures.
