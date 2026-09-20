from threading import Thread

from app.jobs.worker import run_job


def enqueue(job_id: int) -> None:
    """Run a job in a lightweight in-process worker thread for the MVP."""
    thread = Thread(target=run_job, args=(job_id,), daemon=True)
    thread.start()
