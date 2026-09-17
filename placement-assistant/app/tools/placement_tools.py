import operator
from datetime import datetime, timezone

from app.domain import AlreadyApplied, Rule, Student
from app.data import InMemoryPlacementRepo
from app.tools.dispatch import dispatch

OPS = {
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "in": lambda actual, allowed: actual in allowed.split(","),
}


def _passes(rule: Rule, student_value) -> bool:
    return OPS[rule.op](student_value, rule.typed_value())


def _unknown_student(roll_no: str) -> dict:
    return {"error": "unknown_student",
            "hint": f"No student with roll number {roll_no!r}. Ask the user for their roll number, e.g. 22CS045."}


def _unknown_drive(drive_id: int) -> dict:
    return {"error": "unknown_drive",
            "hint": f"No drive with id {drive_id}. Call list_open_drives to get valid ids."}


class PlacementTools:
    """Every method named in TOOL_NAMES is exposed to the model. Its docstring IS the prompt.

    Two tools are complete samples: check_eligibility (read-only) and apply_to_drive (side effect).
    Copy their patterns for the tools marked TODO.
    """

    READ_ONLY = ("list_open_drives", "get_student", "check_eligibility")
    SIDE_EFFECTS = ("apply_to_drive", "book_interview_slot", "notify_student")
    TOOL_NAMES = READ_ONLY + SIDE_EFFECTS

    def __init__(self, repo: InMemoryPlacementRepo, notifier, clock=lambda: datetime.now(timezone.utc)):
        self.repo = repo
        self.notifier = notifier
        self.clock = clock

    def functions(self) -> dict:
        return {name: getattr(self, name) for name in self.TOOL_NAMES}

    def call(self, name: str, args: dict) -> dict:
        return dispatch(self.functions(), name, args)

    # ================================================================== SAMPLE 1 (given): read-only

    def _evaluate(self, s: Student, drive_id: int) -> list[dict]:
        # The business rule lives in data (placement.eligibility_rule), not in the prompt or an if.
        failed = []
        for rule in self.repo.rules_for_drive(drive_id):
            actual = getattr(s, rule.field)
            if not _passes(rule, actual):
                failed.append({"rule_id": rule.id, "rule": str(rule), "actual": actual})
        return failed

    def check_eligibility(self, student_id: str, drive_id: int) -> dict:
        """Decide whether ONE student may apply to ONE drive, using the drive's eligibility rules.

        Use before apply_to_drive, or when the user asks "can I apply", "am I eligible for
        <company>", or "why can't I apply". Do NOT use to find drives; use list_open_drives.
        Read-only: changes nothing.

        Args:
            student_id: Roll number, e.g. "22CS045".
            drive_id: Integer id returned by list_open_drives. Never a company name.

        Returns:
            {"student_id", "drive_id", "eligible", "failed_rules": [{"rule_id", "rule", "actual"}]}.
            Explain every failed rule to the user; do not invent rules that are not listed.
        """
        # Failures are returned, never raised: a stable code plus a hint telling the model what to do next.
        s = self.repo.get_student(student_id)
        if s is None:
            return _unknown_student(student_id)
        if self.repo.get_drive(drive_id) is None:
            return _unknown_drive(drive_id)
        # Every failed rule, not just the first: the model explains the verdict, it never decides it.
        failed = self._evaluate(s, drive_id)
        return {"student_id": s.roll_no, "drive_id": drive_id,
                "eligible": not failed, "failed_rules": failed}

    # ================================================================== SAMPLE 2 (given): side effect

    def apply_to_drive(self, student_id: str, drive_id: int) -> dict:
        """Submit a placement application for ONE student to ONE drive.

        Side effect: creates an application record the placement cell will act on. Call it only
        when the user clearly asks to apply or register ("apply me", "sign me up"), never to
        check or explore. Eligibility is re-checked here, but call check_eligibility first so
        you can explain the result.

        Args:
            student_id: Roll number, e.g. "22CS045".
            drive_id: Integer id returned by list_open_drives.

        Returns:
            {"application_id", "student_id", "drive_id", "status": "applied",
             "available_slots": [{"slot_id", "starts_at"}]}. Offer the slots to the user;
            book one only when they choose.
        """
        # Side effects check in a fixed order and stop at the first failure.
        s = self.repo.get_student(student_id)
        if s is None:
            return _unknown_student(student_id)
        d = self.repo.get_drive(drive_id)
        if d is None:
            return _unknown_drive(drive_id)
        if d.status != "open" or d.deadline <= self.clock():
            return {"error": "drive_closed",
                    "hint": f"{d.company} is not accepting applications. Call list_open_drives for open ones."}
        # Re-check even though the description says "call check_eligibility first".
        # An instruction asks; code enforces. The model may have skipped it.
        failed = self._evaluate(s, drive_id)
        if failed:
            return {"error": "not_eligible", "failed_rules": failed,
                    "hint": "Explain the failed rules to the user. Do not retry."}
        try:
            application_id = self.repo.create_application(s.id, drive_id)
        except AlreadyApplied:
            return {"error": "already_applied",
                    "hint": "The student has already applied to this drive. Tell the user; do not retry."}
        # Return what the next step needs: the model will want to offer interview slots.
        slots = self.repo.free_slots(drive_id)
        return {"application_id": application_id, "student_id": s.roll_no, "drive_id": drive_id,
                "status": "applied",
                "available_slots": [{"slot_id": sl.id, "starts_at": sl.starts_at.isoformat()} for sl in slots]}

    # ================================================================== YOUR TOOLS

    # TODO 1 — get_student (5 min)
    # Returns {"student_id", "name", "branch", "cgpa", "backlogs", "grad_year"}.
    # student_id in the result is the roll number. Error: unknown_student.
    def get_student(self, student_id: str) -> dict:
        """Get the placement record for ONE student using their roll number.

        Use when the student asks for their placement profile, CGPA, branch,
        backlog count, or graduation year. Do NOT use this to check eligibility;
        use check_eligibility for that.

        Read-only: changes nothing.

        Args:
            student_id: Student roll number, e.g. "22CS045".

        Returns:
            {"student_id", "name", "branch", "cgpa", "backlogs", "grad_year"}.
            If the roll number does not exist, return an unknown_student error.
        """
        s = self.repo.get_student(student_id)

        if s is None:
            return _unknown_student(student_id)

        return {
            "student_id": s.roll_no,
            "name": s.name,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "backlogs": s.backlogs,
            "grad_year": s.grad_year,
        }

    # TODO 2 — list_open_drives (10 min)
    # Returns {"drives": [{"drive_id", "company", "role", "ctc_lpa", "deadline"}]}, deadline as YYYY-MM-DD.
    # Only drives with status "open" and a deadline after self.clock(), soonest deadline first
    # (repo.list_open_drives already does that). If branch is given, leave out drives whose
    # "branch" rule that branch fails; same for grad_year. Ignore rules on other fields.
    def list_open_drives(self, branch: str | None = None, grad_year: int | None = None) -> dict:
        """List currently open placement drives, optionally filtered by branch and graduation year.

        Use when the student asks which companies, roles, or placement drives
        are currently open. Do NOT use this to decide whether one student is
        eligible; use check_eligibility for that.

        Read-only: changes nothing.

        Args:
            branch: Optional branch such as "CSE", "IT", "ECE", or "MECH".
                    If provided, exclude drives whose branch rule does not
                    allow this branch.
            grad_year: Optional graduation year such as 2026. If provided,
                    exclude drives whose graduation-year rule does not match.

        Returns:
            {"drives": [{"drive_id", "company", "role", "ctc_lpa", "deadline"}]}.
            Deadlines are returned as YYYY-MM-DD and drives are ordered by
            soonest deadline first.
        """
        drives = self.repo.list_open_drives(self.clock())

        result = []

        for drive in drives:
            if branch is not None:
                branch_rules = [
                    rule for rule in self.repo.rules_for_drive(drive.id)
                    if rule.field == "branch"
                ]

                if branch_rules and not all(_passes(rule, branch) for rule in branch_rules):
                    continue

            if grad_year is not None:
                grad_rules = [
                    rule for rule in self.repo.rules_for_drive(drive.id)
                    if rule.field == "grad_year"
                ]

                if grad_rules and not all(_passes(rule, grad_year) for rule in grad_rules):
                    continue

            result.append({
                "drive_id": drive.id,
                "company": drive.company,
                "role": drive.role,
                "ctc_lpa": drive.ctc_lpa,
                "deadline": drive.deadline.date().isoformat(),
            })

        return {"drives": result}


    # TODO 3 — book_interview_slot (15 min)
    # Check in this order, stop at the first failure:
    #   unknown_student -> unknown_slot -> no_application (student has not applied to the slot's drive)
    #   -> slot_taken (repo.claim_slot returned False; include the drive's remaining "available_slots")
    # Returns {"slot_id", "drive_id", "starts_at", "status": "booked"}, starts_at as ISO-8601.
    def book_interview_slot(self, student_id: str, slot_id: int) -> dict:
        """Book ONE interview slot for ONE student who has already applied.

        Side effect: reserves the selected interview slot for the student.
        Call only when the student clearly chooses or asks to book a particular
        slot. Do NOT use it merely to view available slots.

        Args:
            student_id: Student roll number, e.g. "22CS045".
            slot_id: Integer interview slot id returned by a previous tool result.

        Returns:
            {"slot_id", "drive_id", "starts_at", "status": "booked"}.
            If the student is unknown, return unknown_student. If the slot is
            unknown, return unknown_slot. If the student has not applied to
            the slot's drive, return no_application. If another student took
            the slot first, return slot_taken and the remaining available slots.
        """
        student = self.repo.get_student(student_id)

        if student is None:
            return _unknown_student(student_id)

        slot = self.repo.get_slot(slot_id)

        if slot is None:
            return {
                "error": "unknown_slot",
                "hint": f"No interview slot with id {slot_id}. Use the available slots returned by apply_to_drive."
            }

        if not self.repo.has_application(student.id, slot.drive_id):
            return {
                "error": "no_application",
                "hint": "The student must apply to this drive before booking an interview slot."
            }

        booked = self.repo.claim_slot(slot_id, student.id)

        if not booked:
            available = self.repo.free_slots(slot.drive_id)

            return {
                "error": "slot_taken",
                "available_slots": [
                    {
                        "slot_id": s.id,
                        "starts_at": s.starts_at.isoformat()
                    }
                    for s in available
                ],
                "hint": "The selected slot was already taken. Offer the remaining available slots."
            }

        return {
            "slot_id": slot.id,
            "drive_id": slot.drive_id,
            "starts_at": slot.starts_at.isoformat(),
            "status": "booked",
        }

    # TODO 4 (lab 1) — notify_student
    # unknown_student; message empty or over 160 characters -> invalid_message;
    # otherwise notification_id = self.notifier.send(student_id, message)
    # Returns {"notification_id", "status": "queued"}.
    def notify_student(self, student_id: str, message: str) -> dict:
        """Queue a notification for ONE student.

        Side effect: sends a notification through the placement notification
        service. Use only when the user clearly asks to notify a student.
        Do NOT use it to retrieve student information or placement data.

        Args:
            student_id: Student roll number, e.g. "22CS045".
            message: Notification text. It must contain at least one character
                     and must not exceed 160 characters.

        Returns:
            {"notification_id", "status": "queued"} when successful.
            Return unknown_student for an invalid roll number and invalid_message
            when the message is empty or longer than 160 characters.
        """
        student = self.repo.get_student(student_id)

        if student is None:
            return _unknown_student(student_id)

        if not message or len(message) > 160:
            return {
                "error": "invalid_message",
                "hint": "Message must contain at least one character and be at most 160 characters."
            }

        notification_id = self.notifier.send(student_id, message)

        return {
            "notification_id": notification_id,
            "status": "queued",
        }

    # STRETCH — design a tool of your own: list_my_applications(student_id)
    # "Where have I applied? When is my interview?" Add it to READ_ONLY, write the description,
    # and use repo.list_applications(student.id), which is already given.
    # tests/test_stretch_my_applications.py switches on as soon as the method exists.
