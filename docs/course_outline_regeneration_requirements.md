# PAICE Studio - Course Outline Regeneration Requirements

## Executive Summary
This document consolidates the end-to-end requirements, acceptance criteria, user flows, prompt capabilities, validation logic, undo/save workflows, and technical/API specifications for **Course Outline Regeneration** in PAICE Studio, derived from key Jira epics and stories (including `STUDIOPE-6`, `STUDIOPE-94`, `STUDIOPE-277`, `STUDIOPE-279`, `STUDIOPE-291`, `STUDIOPE-300`, `STUDIOPE-324`, `STUDIOPE-329`, `STUDIOPE-340`, `STUDIOPE-341`, `STUDIOPE-353`, `STUDIOPE-389`, `STUDIOPE-448`, `STUDIOPE-473`, `STUDIOPE-496`, `STUDIOPE-530`, `STUDIOPE-532`, `STUDIOPE-589`, and related tickets).

---

## 1. Feature Overview & Objectives
The Course Outline Regeneration capability enables PVS Content Developers ("Users/Authors") to re-trigger AI generation across the entire course outline or targeted container scopes (Unit, Lesson, Module, or Learning Goal). 

**Key Goals:**
- Provide alternative wording, structures, and pacing while maintaining full alignment with accepted Learning Goals (LGs) and course inputs.
- Support prompt-guided structural modifications (splitting, combining, re-ordering, and adjusting lesson counts).
- Ensure safe authoring via explicit Review, Save, and Undo mechanisms without data loss.

---

## 2. Regeneration Hierarchy & Granularity

PAICE Studio supports regeneration across multiple levels of the course hierarchy:

| Granularity / Scope | Scope Parameter | Impact / Description | Exceptions / Exclusions | Relevant Tickets |
| :--- | :--- | :--- | :--- | :--- |
| **Full Course Outline** | `all` | Regenerates the entire course outline tree (Units → Lessons → Modules → Slates). | None | `STUDIOPE-324`, `STUDIOPE-328`, `STUDIOPE-329` |
| **Unit Level** | `unit` | Regenerates all Lessons and Module titles within the selected Unit without altering LG alignment or overall course inputs. | Overview & Semester A/B units follow specific standard rules. | `STUDIOPE-94`, `STUDIOPE-193`, `STUDIOPE-353` |
| **Lesson Level** | `lesson` | Regenerates all Module titles within the selected Lesson without altering LG alignment. | **Course Introduction** and **Semester Reflect & Review** lessons do NOT have/need regenerate functions. | `STUDIOPE-94`, `STUDIOPE-193`, `STUDIOPE-353` |
| **Learning Goal (LG)** | `single_objective` / `full_standard` | Regenerates wording or breakdown for individual LGs or full standard LG sets. | Must satisfy standard instructional intent. | `STUDIOPE-17`, `STUDIOPE-73`, `STUDIOPE-88`, `STUDIOPE-117` |

---

## 3. User Experience & Prompt-Guided Regeneration

### 3.1 Prompt Modal Interaction
- Selecting any "Regenerate" button (Full Outline, Unit, or Lesson) triggers a **Guided Regeneration Modal** with a text prompt input field (`STUDIOPE-94`).
- Authors can either execute a **Standard Regeneration** (no prompt) or a **Guided Regeneration** (custom natural language instructions).

### 3.2 Supported Guided Regeneration Prompts
The AI graph must interpret and execute structural and wording feedback based on author prompts (`STUDIOPE-279`, `STUDIOPE-389`, `STUDIOPE-448`):

1. **Unit-Level Structural Prompts:**
   - **Split Units:** Divide a large unit into two separate units.
   - **Combine Units:** Merge two small/under-filled units into a single cohesive unit.
   - **Unit Progression Shift:** Change unit-to-unit progression (e.g., Theme-based, Chronological, Skills-based, Standards-driven).
   - **Parallel Structure:** Enforce parallel unit frameworks across the course.
   
2. **Lesson-Level Structural Prompts:**
   - **Consolidate/Reduce Lessons:** e.g., "Consolidate into 4 or fewer lessons" or "Reduce to X lessons in this Unit".
   - **Split Lessons / Combine Lessons:** Divide a complex lesson into two or merge similar lessons into one.
   - **Add/Remove Topic Lessons:** e.g., "Add a lesson about [topic]" or "Remove duplicate practice lessons".
   - **Thematic Progression within Unit:** Order lessons sequentially or thematically within the unit.

3. **Module-Level Wording & Sequence Prompts:**
   - Move modules across lessons within the unit.
   - Rephrase module titles while retaining LG mapping.

### 3.3 Prompt Validation & Error Handling
- **Invalid / Unrelated Prompts (`STUDIOPE-286`, `STUDIOPE-335`, `STUDIOPE-357`):** If a prompt cannot be satisfied or violates course design constraints, the system must return a clear, user-facing error message (e.g., "Your prompt appears to be unrelated to the course outline. Please provide a relevant instruction...").
- **Security & Input Sanitization (`STUDIOPE-338`):** Prompts containing malicious code or injection attempts (e.g., `<script>`) must be safely rejected with proper validation errors.

---

## 4. Business Logic & Validation Constraints

### 4.1 Core Mapping & Instructional Load
1. **LG-to-Module Mapping:** Every accepted Learning Goal correlates 1:1 with a Module (`STUDIOPE-6`).
2. **Instructional Load Calculator:**
   - Total Lesson Days = `(Lessons scheduled per day) x (Total weeks)`.
   - Total Course Hours = `(Minutes per Lesson Day) x (Lesson Days per week) x (Total weeks)`.
   - Each lesson's estimated time must not exceed the configured "Minutes per Lesson Day".

### 4.2 PVS Instructional Model Rules (`STUDIOPE-291`)
- **Minimum Understand Lessons:** Every Unit must contain a **minimum of 4 "Understand" Lessons**. If a generated unit has fewer, it must be merged with an adjacent unit.
- **Quick Check Rules:** Quick Check assessments must be **removed from all "Introduce" Lessons**.

### 4.3 Naming & Display Correctness (`STUDIOPE-473`)
- Following regeneration (even after manual addition of Units, Lessons, or Modules), generated item names must follow proper naming conventions.
- Generic placeholders such as *"Unspecified New Learning Goal"* or *"New Learning Goal"* must NOT be displayed.

### 4.4 Preservation of Manual Edits (`STUDIOPE-496`)
- Advancing from Step 5 ("Learning & Assessment") to Step 6 ("Course Map") by clicking **Continue** must NOT unconditionally re-fire outline regeneration if an outline already exists.
- Manual edits made in Step 6 must be preserved unless the author explicitly clicks "Regenerate".

---

## 5. Undo and Save Capabilities (`STUDIOPE-295`, `STUDIOPE-300`, `STUDIOPE-340`, `STUDIOPE-341`, `STUDIOPE-530`, `STUDIOPE-532`, `STUDIOPE-589`)

### 5.1 Author Workflow: Review, Save & Undo
When regeneration is executed:
1. The regenerated content is generated asynchronously and returned to the UI in a **pending review state** (`is_regenerate=true`).
2. The UI displays an **Undo** option alongside the regenerated outline/container.
3. **Save Action:** Clicking "Save" commits the pending regeneration to the database and marks the superseded version as replaced (`STUDIOPE-340`).
4. **Undo Action:** Clicking "Undo" discards the regenerated output and instantly restores the previous active version without error.

### 5.2 Undo Types & DB Lifecycle (`STUDIOPE-341`)
- **`TREE` Undo (Full Outline):** Points the transaction back to the previous tree root (`courseOutlineId`), setting the restored tree to `ACTIVE` and the abandoned tree to `SUPERSEDED`.
- **`TITLES` Undo (Unit/Lesson Scope):** Restores exact container titles modified during the unit/lesson regeneration run.

### 5.3 Concurrency & Edge Case Rules
- **Independent Parallel Unit Undo (`STUDIOPE-530`, `STUDIOPE-532`):** When multiple units are regenerated in parallel, undoing Unit 1 while Unit 2 is in progress (or after Unit 2 completes) must execute cleanly for Unit 1 without throwing a `409 Conflict` error or overriding Unit 1's undo button.
- **Progression Shift Undo (`STUDIOPE-589`):** Changing progression in Step 5 and regenerating must handle undo gracefully without throwing a `409 Conflict` error.

---

