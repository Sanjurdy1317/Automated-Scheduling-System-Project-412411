"""
main.py
========
Command-line entry point for the Automated Scheduling System.
Generates a sample problem, optimizes it with the Genetic Algorithm,
prints the resulting timetable and any conflicts, then demonstrates the
real-time heuristic re-scheduler by simulating an instructor becoming
unavailable.

For the interactive dashboard, run:
    streamlit run dashboard/app.py
"""

import argparse

from core.data_generator import generate_dataset
from core.genetic_scheduler import GeneticScheduler
from core.cp_scheduler import CPScheduler
from core.conflict_detector import detect_conflicts
from core.heuristic_rescheduler import HeuristicRescheduler
from core.data_models import TimeSlot


def print_schedule(tasks):
    scheduled = sorted([t for t in tasks if t.is_scheduled()], key=lambda t: (t.assigned_slot.day, t.assigned_slot.start_hour))
    for t in scheduled:
        print(f"  {str(t.assigned_slot):18s} | {t.name:30s} | {t.assigned_resource:6s} | {t.assigned_room}")
    unscheduled = [t for t in tasks if not t.is_scheduled()]
    if unscheduled:
        print(f"\n  {len(unscheduled)} task(s) could not be scheduled: {[t.id for t in unscheduled]}")


def main():
    parser = argparse.ArgumentParser(description="Automated Scheduling System demo")
    parser.add_argument("--method", choices=["ga", "cp"], default="ga")
    parser.add_argument("--courses", type=int, default=18)
    parser.add_argument("--instructors", type=int, default=7)
    parser.add_argument("--rooms", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"Generating problem: {args.courses} classes, {args.instructors} instructors, {args.rooms} rooms...")
    tasks, resources, rooms = generate_dataset(args.courses, args.instructors, args.rooms, seed=args.seed)

    if args.method == "ga":
        print("\nRunning Genetic Algorithm optimizer...")
        ga = GeneticScheduler(tasks, resources, rooms, population_size=60, generations=150, seed=args.seed)
        result = ga.run()
        final_tasks = result.best_tasks
        print(f"Finished after {result.generations_run} generations. Best fitness = {result.best_fitness:.2f}")
    else:
        print("\nRunning CP-SAT exact solver...")
        cp = CPScheduler(tasks, resources, rooms)
        result = cp.solve()
        final_tasks = result.tasks
        print(f"Status: {result.status}. Solved in {result.solve_time_seconds:.2f}s")

    res_dict = {r.id: r for r in resources}
    room_dict = {r.id: r for r in rooms}
    conflicts = detect_conflicts(final_tasks, res_dict, room_dict)

    print(f"\n=== Final Schedule ({sum(1 for t in final_tasks if t.is_scheduled())}/{len(final_tasks)} scheduled) ===")
    print_schedule(final_tasks)

    print(f"\n=== Conflicts: {len(conflicts)} ===")
    for c in conflicts:
        print(f"  [{c.severity.name:8s}] {c.kind}: {c.description}")

    # --- Demonstrate real-time adaptation ---
    print("\n=== Simulating disruption: first instructor becomes unavailable Mon 10:00 ===")
    rescheduler = HeuristicRescheduler(final_tasks, resources, rooms)
    blocked = TimeSlot(day="Mon", start_hour=10, duration=1)
    reresult = rescheduler.handle_resource_unavailable(resources[0].id, blocked)
    for ev in reresult.events:
        print(f"  - {ev.explanation}")
    print(f"Conflicts before: {reresult.n_conflicts_before} -> after: {reresult.n_conflicts_after}")


if __name__ == "__main__":
    main()
