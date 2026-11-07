# Design Engineering Analytics with Power BI: free learner pack (Course 2)

Practice files for a free, 20-video YouTube course that teaches Power BI to design and product engineers with one running example: a valve seat ring that went through three revisions (A, B, C) and the question "did Rev C fix the wear problem?".

**Engxtech is a fictional company and every number in the data is synthetic.** Engxtech (pumps and valves) does not exist, and the files contain no real company, customer, supplier or personal data. Any resemblance to a real organisation is coincidence. The data were generated for teaching; do not use them to draw engineering conclusions.

- Tool: Power BI Desktop (free). Nothing else is needed.
- Cost: free. No sign-up.
- Video playlist: link coming soon.
- Author: Vijayakumar Reddy Yeddula (channel "Vijayakumar Yeddula | Engineering & Career Skills").

## What you learn

BOM explosion, where-used and revisions; NPD stage-gate Gantt; late drawings and review findings; mass and cost vs target; tolerance stacks (worst case vs RSS); FEA safety factor and Cpk; combining messy CSV exports in Power Query; engineering-change cycle time, backlog and cost; validation pass rate and field ppm with a confidence interval; DFMEA risk matrix; a one-page capstone dashboard; two portfolio dashboards built from a blank file.

## Folder guide

| Folder | What is in it |
|---|---|
| `data/` | `Engxtech_Design_Data.xlsx` (18 sheets), `Change_Exports/` (21 monthly change-log CSVs: 184 rows, 178 unique changes), `Data_Dictionary_C2.xlsx` (every column: type, meaning, example). Start here from video B1. |
| `pbix/end/` | `Engxtech_<CODE>.pbix`: the finished file at the end of each video. |
| `pbix/start/` | `SectionNN_Start.pbix`: the start file of each video from S02 onwards. From S03 on it is identical to the previous video's finished file; Section02_Start.pbix is the file exactly as it was at the start of the S02 recording. Use it if you skipped ahead or your own file went wrong. `Blank.pbix` is an empty report: the start file for B1, S12 and S13 (or choose File > New > Blank report in Power BI Desktop). |
| `pbix/portfolio_outputs/` | The finished S12 and S13 dashboards as PDF and PNG, to compare with your own. |
| `exercises/` | `Exercises/` (one page per section), `Solutions/` (worked solutions with full DAX and M code), `Formula_Cheat_Sheet.pdf`, `S11_Capstone_Brief.pdf`, `answers_check.csv` (the expected numbers, recomputed from the data). |
| `scripts/` | `gen_c2.py` and `make_wb.py`: the scripts that generated the data (seeded, so they reproduce the files in `data/` exactly). Optional. |

## Which file goes with which video

The course is one Power BI file that grows video by video: B1 > B2 > S02 > ... > S11. S12 and S13 are stand-alone portfolio projects. Sections 5 to 9 are split into Part 1 and Part 2 (file names use `S05_1`, `S05_2`, and so on).

| # | Video | Title | Start file | Finished file | Exercise / solution (after the video) |
|---|---|---|---|---|---|
| 1/20 | S01 | Design Engineering Analytics with Power BI: Free Course Preview | - | - | - |
| 2/20 | B1 | Power BI Desktop for Beginners: Install, Load Excel, First Visuals | Blank.pbix | Engxtech_B1.pbix | - |
| 3/20 | B2 | Power BI First Steps: Power Query, Model View and First DAX | Engxtech_B1.pbix | Engxtech_B2.pbix | B2_Exercise.pdf / B2_Solution.pdf |
| 4/20 | S02 | Power BI BOM and Part Revisions: Find the Current Rev on Any Date | Section02_Start.pbix | Engxtech_S02.pbix | S02_Exercise.pdf / S02_Solution.pdf |
| 5/20 | S03 | Gantt Chart in Power BI: Where Do Design Stages Slip? | Section03_Start.pbix | Engxtech_S03.pbix | S03_Exercise.pdf / S03_Solution.pdf |
| 6/20 | S04 | Drawing Release in Power BI: On-Time %, Pareto, Mass vs Target | Section04_Start.pbix | Engxtech_S04.pbix | S04_Exercise.pdf / S04_Solution.pdf |
| 7/20 | S05.1 | Tolerance Stack in Power BI: Worst Case vs RSS, Step by Step | Section05_1_Start.pbix | Engxtech_S05_1.pbix | - |
| 8/20 | S05.2 | Cpk and FEA Safety Factor in Power BI, with a What-If Slider | Section05_2_Start.pbix | Engxtech_S05_2.pbix | S05_Exercise.pdf / S05_Solution.pdf |
| 9/20 | S06.1 | Power Query Folder Connector: Combine 21 CSV Files in Power BI | Section06_1_Start.pbix | Engxtech_S06_1.pbix | - |
| 10/20 | S06.2 | Power Query Data Cleaning: Fix Part Numbers, Remove Duplicates | Section06_2_Start.pbix | Engxtech_S06_2.pbix | S06_Exercise.pdf / S06_Solution.pdf |
| 11/20 | S07.1 | Power BI Date Table and USERELATIONSHIP: Two Dates, One Table | Section07_1_Start.pbix | Engxtech_S07_1.pbix | - |
| 12/20 | S07.2 | Power BI Bridge Table: Which Parts Did Each Change Touch? | Section07_2_Start.pbix | Engxtech_S07_2.pbix | S07_Exercise.pdf / S07_Solution.pdf |
| 13/20 | S08.1 | Engineering Change Cycle Time in Power BI: Median and P90 | Section08_1_Start.pbix | Engxtech_S08_1.pbix | - |
| 14/20 | S08.2 | Change Backlog and Rework in Power BI: Net vs Gross Cost | Section08_2_Start.pbix | Engxtech_S08_2.pbix | S08_Exercise.pdf / S08_Solution.pdf |
| 15/20 | S09.1 | Field ppm in Power BI: Define It Before You Calculate It | Section09_1_Start.pbix | Engxtech_S09_1.pbix | - |
| 16/20 | S09.2 | Confidence Interval in Power BI: Field ppm with CHISQ.INV | Section09_2_Start.pbix | Engxtech_S09_2.pbix | S09_Exercise.pdf / S09_Solution.pdf |
| 17/20 | S10 | DFMEA Risk in Power BI: RPN Before vs After and an S x O Matrix | Section10_Start.pbix | Engxtech_S10.pbix | S10_Exercise.pdf / S10_Solution.pdf |
| 18/20 | S11 | Power BI Capstone: Drill-Through, Tooltips and Bookmarks | Section11_Start.pbix | Engxtech_S11.pbix | S11_Exercise.pdf / S11_Solution.pdf + S11_Capstone_Brief.pdf |
| 19/20 | S12 | Power BI Project: Design Program Status Dashboard, Start to Finish | Blank.pbix | Engxtech_S12.pbix (+ .pdf, _dashboard.png) | S12_Exercise.pdf / S12_Solution.pdf |
| 20/20 | S13 | Power BI Project: Quality and Reliability Dashboard, Start to Finish | Blank.pbix | Engxtech_S13.pbix (+ .pdf, _dashboard.png) | S13_Exercise.pdf / S13_Solution.pdf |

Each exercise starts from that video's finished file (the same file as the next video's start file). The exercise for a split section (S05 to S09) follows Part 2. Each exercise is longer than the short "Your turn" inside the video; the video answers its own "Your turn". Try the exercise first, compare with "Check your answer", then open the solution.

## How to use it

1. Download the whole repository (Code > Download ZIP) and unzip it somewhere you can find again, for example `C:\Course2`.
2. Watch the video. Open its start file (or your own finished file from the previous video) and save a copy under the name used in the video, for example `Engxtech_S03.pbix`.
3. Do the exercise after the section's last video, then compare with your numbers.

### If Power BI asks for the data location

The files read the workbook and the `Change_Exports` folder from where they were built, not from your computer. If you see a "file not found" or "data source" error on refresh, either follow the video (B1 and S06.1 show how to point to your folder) or fix it yourself:

- Workbook: Home > Transform data > Data source settings > select the workbook > Change Source > browse to `data/Engxtech_Design_Data.xlsx`.
- Change log: Home > Transform data > Edit parameters > set `ChangeFolder` to the full path of `data/Change_Exports`. Apply changes.
- Regional settings: the change-log dates and costs are read as English (United States). Set File > Options > Current file > Regional settings > Locale for import = English (United States). Otherwise numbers such as 158,004 may group differently on your screen (for example 1,58,004); the values themselves are the same.

## Power BI Desktop version

The `.pbix` files were saved with Power BI Desktop release **2026.10** (October 2026 update) in the current report format (PBIR). Use that release or newer. Older Desktop versions may not open them. Menu names can differ slightly between monthly releases; the video shows the release used.

## Notes on the data

- Data cut-off: 30 September 2026. Field ppm counts matured build months only (March 2025 to June 2026).
- Rev C of the P300 seat ring is an early signal (one matured build month). The data do not show that the change fixed the wear problem; the course says so on purpose.
- Some problems are hidden in the data on purpose (duplicates, part numbers typed differently). Clean them in Power Query, not in the files.
- Table names in the DAX are the workbook sheet names. The cleaned change log query is `Changes`, the date table is `Dates`, and measures live in the `_Measures` table.

## Licence

- Content (data, exercises, solutions, cheat sheet, capstone brief, PDFs, images, Power BI files): **Creative Commons Attribution 4.0 International (CC BY 4.0)**. You may share and adapt with credit. See `LICENSE`.
- Scripts (`scripts/*.py`): **MIT**. See `LICENSE-MIT`.

## How to cite

See `CITATION.cff` (GitHub shows a "Cite this repository" button) or the Zenodo record once published. Version 1.0.0.

Microsoft Power BI is a trademark of Microsoft. This course is independent and is not affiliated with or endorsed by Microsoft.
