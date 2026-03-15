# Lincoln Entomology Observers System

## Overview
This is a small command-line system for managing members, locations, insects, and observations. The menu-driven program allows adding members, locations, and observations, and listing members, locations with observations, and member ages.

## How to run
1. Open terminal in this folder.
2. Run `python leo_admin.py`.
3. Enter menu option numbers to test features.

## Test data (manual input to verify system behavior)

### 1) Members

| # | Feature | Action | Input fields | Example input | Expected result |
|---|---|---|---|---|---|
| 1 | Add valid member | Menu 6 | First name, Family name, Email, Birth date | `John`, `Doe`, `john.doe@example.com`, `01/01/1990` | Member added and shown in list (menu 1). |
| 2 | Reject blank name | Menu 6 | First name (blank) | ``, `Smith`, `smith@example.com`, `02/02/1992` | Re-prompts with `Name cannot be blank.` |
| 3 | Reject invalid characters in name | Menu 6 | Name with digits/symbols | `A1ice`, `Brown`, `alice@example.com`, `03/03/1993` | Re-prompts with invalid name message. |
| 4 | Reject duplicate email | Menu 6 | Duplicate email | `Jane`, `Doe`, `john.doe@example.com`, `05/05/1995` | Rejected with duplicate email message. |

### 2) Locations

| # | Feature | Action | Input fields | Example input | Expected result |
|---|---|---|---|---|---|
| 5 | Add valid location | Menu 5 | Location name | `Campus Garden` | Location added, new ID created, and location appears in menu 2 and in location list. |
| 6 | Reject too short name | Menu 5 | Location name length <3 | `OK` | Re-prompts with `must be at least 3 characters`. |
| 7 | Reject invalid chars | Menu 5 | Location with symbols | `Lake@Field!` | Re-prompts with invalid characters. |
| 8 | Duplicate location check | Menu 5 | Already existing location | `Campus Garden` | Re-prompts with duplicate location message. |

### 3) Observations

| # | Feature | Action | Input fields | Example input | Expected result |
|---|---|---|---|---|---|
| 9 | Add observation for existing IDs | Menu 4 | Member ID, Insect ID, Location ID, Date | `1`, `1`, `1`, `15/03/2026` | Observation appended; shown under location in menu 2. |
| 10 | Reject missing member ID | Menu 4 | Invalid member ID | `999`, `1`, `1`, `15/03/2026` | Re-prompts with `Member ID not found`. |
| 11 | Reject missing insect ID | Menu 4 | Invalid insect ID | `1`, `999`, `1`, `15/03/2026` | Re-prompts with `Insect ID not found`. |
| 12 | Reject missing location ID | Menu 4 | Invalid location ID | `1`, `1`, `999`, `15/03/2026` | Re-prompts with `Location ID not found`. |
| 13 | Date validation | Menu 4 | Future date | `1`, `1`, `1`, `31/12/2099` | Re-prompts because date out of allowed range. |

### 4) Reporting and listing

| # | Feature | Action | Expected result |
|---|---|---|---|
| 14 | List members | Menu 1 | Shows all members with ID, first name, family name, birth date, email. |
| 15 | List locations and observations | Menu 2 | Location rows appear; observation rows show `Loc ID`, `Location`, `Member ID`, `Member Name`, `Date`, `Insect`. |
| 16 | List members and ages | Menu 3 | Shows each member’s age correctly based on birth date and current date. |

> NOTE: Enter IDs from the current list output (menu 1 for members and menu 5 for locations) when creating observations.

## Reflection
The most difficult aspect of this assessment was input date validation, because it combines parsing, format normalisation, user feedback, and range checks.

### Specific challenges
1. Accepted multiple formats. I supported many formats (`DD/MM/YYYY`, `DD-MM-YYYY`, `YYYY/MM/DD`, `YYYY-MM-DD`, `DD.MM.YYYY`, and 2-digit year versions) so users could enter dates in common ways.
2. Parse errors vs logical validation. I had to distinguish invalid formatting (`ValueError` from parsing) from invalid dates (e.g., `31/02/2024`) and then provide helpful messages.
3. Min/max date ranges. I needed to compare parsed date values to `mindate` and `maxdate` to enforce sensible ranges, while making sure the prompt includes clear boundary info.
4. Clear loop behavior. The input loop must keep prompting until valid, but not trap users in confusing repeated messages. I added explicit prints for successful entry, invalid format, and out-of-range errors.
5. Consistent display formatting. Once dates were accepted, I had to format them consistently for output tables (`%d/%m/%Y`) and ensure observers can read them aligned with the table columns.

### What I learned
- Successful validation is not just “is it valid?” but also “did the user understand the error and retry correctly?”
- Use helper functions to keep validation logic isolated and easier to test.
- Defensive programming in CLI apps is important for maintaining state and preventing inconsistent records when users make mistakes.

This detailed handling made the date code more complex, but it also improved reliability and user experience for the full system.

