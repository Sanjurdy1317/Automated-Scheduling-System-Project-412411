# Automated Scheduling System for Academic and Organizational Efficiency

An AI-based automated scheduling system built for the final year project. It
combines a **Genetic Algorithm**, an exact **Constraint Programming (CP-SAT)**
solver, and a **heuristic real-time re-scheduler**, wrapped in an interactive
**Streamlit** decision-support dashboard with Gantt-chart visualization.

## Features

- Generates realistic synthetic academic scheduling problems (courses,
  instructors with skills/availability, rooms with capacity/type).
- **Genetic Algorithm** optimizer: tournament selection, uniform crossover,
  mutation, elitism — minimizes hard-constraint violations (double bookings,
  unavailability, skill mismatches, capacity/room-type issues) and softly
  optimizes for priority placement and instructor load balance.
- **CP-SAT exact solver** (Google OR-Tools): guarantees a conflict-free
  schedule (or proves infeasibility) for smaller/medium instances; used as a
  ground-truth comparison against the GA.
- **Heuristic real-time re-scheduler**: handles live disruptions — an
  instructor becoming unavailable, or an urgent task being injected — by
  repairing only the affected tasks and producing a plain-language
  explanation of every change (decision support, not just automation).
- **Streamlit dashboard**: a multi-page, professionally themed decision-support
  app — Home, About, Dataset Explorer, Schedule Generator, Analytics,
  Evaluation, Live Comparison, Real-Time Adaptation, and Export, grouped into
  sectioned navigation — with a custom gradient design system (hover effects,
  gradient-border cards, animated buttons), a system architecture diagram,
  a live-updating Genetic Algorithm convergence chart, interactive Gantt
  visualization, conflict explanations, disruption simulation, and CSV export.
- **Benchmark suite**: compares GA vs. CP-SAT across four problem sizes on
  runtime, conflicts, and unscheduled tasks — surfaced both as a standalone
  script and as a page in the dashboard.

## Project structure

```
scheduling_system/
├── core/
│   ├── data_models.py          # Task, Resource, Room, TimeSlot, Conflict
│   ├── data_generator.py       # synthetic dataset generator
│   ├── conflict_detector.py    # shared conflict-detection logic
│   ├── genetic_scheduler.py    # Genetic Algorithm optimizer
│   ├── cp_scheduler.py         # OR-Tools CP-SAT exact solver
│   └── heuristic_rescheduler.py# real-time disruption handling
├── dashboard/
│   ├── app.py                  # entry point — sets up sectioned multi-page navigation
│   ├── styles.py                # design system: CSS + hero/card/pill/table helpers
│   ├── state.py                  # shared session-state + optimizer-calling logic
│   ├── assets/
│   │   └── architecture.png      # system architecture diagram (About page)
│   └── views/
│       ├── home.py               # Home page
│       ├── about.py              # About page — problem, aims, architecture, stack
│       ├── dataset.py            # Dataset Explorer — preview generated data as tables
│       ├── generator.py          # Schedule Generator page
│       ├── analytics.py          # Analytics page
│       ├── evaluation.py         # Evaluation page — benchmark table + charts
│       ├── live_comparison.py    # Live Comparison page (live GA convergence)
│       ├── realtime.py           # Real-Time Adaptation page
│       └── export.py             # Export page
├── utils/
│   ├── visualization.py        # Plotly charts (used by the dashboard)
│   └── report_charts.py        # Matplotlib charts (used for the report)
├── evaluation/
│   ├── benchmark.py            # GA vs CP-SAT benchmark across problem sizes
│   └── results/                 # benchmark_results.csv + chart PNGs (read by the Evaluation page)
├── main.py                      # CLI demo entry point
└── requirements.txt
```

## Setup (VS Code / local machine)

1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running the CLI demo

```bash
python main.py --method ga --courses 18 --instructors 7 --rooms 5 --seed 42
python main.py --method cp
```

## Running the dashboard

```bash
streamlit run dashboard/app.py
```

This opens the dashboard in your browser (default `http://localhost:8501`),
with a sectioned navigation rail on the left:

**Overview**
- **Home** — key stats, feature highlights, and quick links.
- **About** — the problem this project addresses, aims and objectives, the
  system architecture diagram, technology stack, and project scope.

**Explore**
- **Dataset** — preview the synthetic dataset generator's output (classes,
  instructors, rooms) as tables, independent of any generated schedule.
- **Schedule Generator** — configure problem size and optimizer, run it,
  and view the resulting Gantt chart and conflict explanations.
- **Analytics** — instructor workload, conflict severity breakdown, and
  the GA convergence curve for the current schedule.
- **Evaluation** — the GA vs. CP-SAT benchmark table and comparison charts
  across four problem sizes (the same results reported in the project report).
- **Live Comparison** — runs the Genetic Algorithm and CP-SAT back to
  back on the same instance, with the GA's convergence chart updating
  live, generation by generation, followed by a head-to-head comparison.

**Operate**
- **Real-Time Adaptation** — simulate a disruption (an instructor becomes
  unavailable, or an urgent class appears) and watch the heuristic
  re-scheduler repair the timetable with an explanation for each change.
- **Export** — the full schedule as a table, downloadable as CSV.

The Evaluation page reads `evaluation/results/benchmark_results.csv`; if it
doesn't exist yet, run `python -m evaluation.benchmark` first (see below).

## Running the benchmark

```bash
python -m evaluation.benchmark
```

Results are written to `evaluation/results/` (`benchmark_results.csv` and
comparison charts).

## Notes on the algorithms

- The **GA** is the primary, scalable optimizer used for realistic problem
  sizes; it always produces a complete (though occasionally imperfect)
  schedule quickly.
- The **CP-SAT** solver is exact: any schedule it returns has zero hard
  conflicts, but it may need to leave some tasks unscheduled if no
  conflict-free placement exists, and it slows down on larger instances.
- The dashboard lets you pick either method interchangeably, matching the
  "decision-support, not just automation" philosophy described in the
  original project proposal.
