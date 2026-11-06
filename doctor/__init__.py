"""EarnFi connection and capability diagnostics."""

from .checks import run_doctor, run_smoke, DoctorReport

__all__ = ["run_doctor", "run_smoke", "DoctorReport"]
