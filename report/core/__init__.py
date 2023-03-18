from .metrics import Metric
from .descriptions import Description

# Instantiate metrics
metrics = {
    "planner": Metric(
        "Planner",
        "You are good at planning your work and setting goals.",
        "static/img/planner.png",
    ),
    "guardian": Metric(
        "Guardian",
        "You are good at keeping your work organized and on track.",
        "static/img/guardian.png",
    ),
    "mentor": Metric(
        "Mentor",
        "You are good at helping others learn and grow.",
        "static/img/mentor.png",
    ),
    "motivator": Metric(
        "Motivator",
        "You are good at motivating others to do their best.",
        "static/img/motivator.png",
    ),
    "assessor": Metric(
        "Assessor",
        "You are good at assessing your own work and the work of others.",
        "static/img/assessor.png",
    ),
}

print("core loaded")