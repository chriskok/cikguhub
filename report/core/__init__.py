from .metrics import Metric

# Instantiate metrics
metrics = {
    "planner": Metric(
        "Planner",
        "You are good at planning your work and setting goals.",
        "fa-calendar-check",
    ),
    "guardian": Metric(
        "Guardian",
        "You are good at keeping your work organized and on track.",
        "fa-clipboard-check",
    ),
    "mentor": Metric(
        "Mentor",
        "You are good at helping others learn and grow.",
        "fa-chalkboard-teacher",
    ),
    "motivator": Metric(
        "Motivator",
        "You are good at motivating others to do their best.",
        "fa-award",
    ),
    "assessor": Metric(
        "Assessor",
        "You are good at assessing your own work and the work of others.",
        "fa-clipboard-list",
    ),
}

print("core loaded")