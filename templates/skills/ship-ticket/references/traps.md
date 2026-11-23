# Traps from earlier runs

One headed note per trap. List the headings with `grep -n '^## ' references/traps.md`,
read every note that touches the ticket's area or the tools you are about to use, and
add a note with its date and ticket when a run teaches something.

## Example to delete: a test passes alone and fails in the full suite

Example note, invented to show the format; delete it once you have a real one. 2025-03-14, DEMO-12.
A shared date formatter kept the time zone of the first test that used it, so a time-zone test passed on its own and failed after other tests had run. Build a new formatter inside each test that changes the time zone, and run the full suite before trusting a single green test.

## Example to delete: seeding hand-test data through the API trips its rate limit

Example note, invented to show the format; delete it once you have a real one. 2025-04-02, DEMO-31.
Seeding 200 records through the staging API returned "too many requests" after the first 100, and the app showed an empty list that looked like the bug under test. Seed through the import file instead, and read the server's response before blaming the app.
