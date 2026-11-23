---
paths:
  - "<your source folder>/**"
---

# Architecture

<This is an outline, not an architecture. Run `/architecture` and let Claude fill it from your code, or from the choice you make for a new project. It loads only when a file matching the paths above is touched. Delete every line in angle brackets once it is filled.>

<One paragraph: the shape in plain words, and the one idea that explains most of the rules below.>

## Layers and the direction of dependencies

| Layer or module | Holds | May depend on | Never depends on |
|---|---|---|---|
| <name> | <what lives here> | <names> | <names> |

<One line of reason for each "never".>

## Where state lives, and how the screen learns of a change

<The pattern, in two or three checkable rules.>

## How dependencies are provided

<Constructor, a container, a framework. What is forbidden, such as reaching for a shared instance inside a feature.>

## Navigation

<Who decides where to go next, and what a screen is not allowed to do.>

## Data

<Where data is read from first. What happens offline. Who talks to the network. Which module owns each external service.>

## Errors

<How a failure travels up, where it is logged, and what the user sees. Never the system's own error text on a screen.>

## Concurrency and lifecycle

<Which work runs where, what starts it, and what cancels it.>

## Naming and file layout

<The folder shape of one feature, and the names of its parts.>

## Tests

<What is tested at each layer, what is replaced by a fake, and where tests live.>

## The reference feature

Copy from `<path of the feature that follows every rule above>`.

## Adding a feature

1. <first file to create>
2. <...>
3. <the test that proves it>

## Audit commands

Each prints nothing when the code conforms. Violations on <date of the baseline>: <count per command>.

```bash
<a search for a forbidden import in one layer>
<a search for a forbidden pattern>
```

## Known deviations

| Where | What differs | Decision |
|---|---|---|
| `<path>` | <the pattern it uses> | fix now / fix when next touched / accepted exception |
