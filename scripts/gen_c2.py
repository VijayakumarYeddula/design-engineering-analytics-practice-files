# MIT License, (c) 2026 Vijayakumar Reddy Yeddula. See LICENSE-MIT.
"""Course 2 practice data: Engxtech Manufacturing, design & product engineering (synthetic).
Writes clean frames (data_c2.pkl) and the learner workbook with deliberate issues (Engxtech_Design_Data.xlsx)
plus monthly change-log CSV exports for the Power Query section."""
import numpy as np, pandas as pd, pickle, os
rng = np.random.default_rng(2026)
OUT = os.path.dirname(os.path.abspath(__file__))
D0, D1 = pd.Timestamp("2025-01-01"), pd.Timestamp("2026-09-30")

# ---------------- dimensions ----------------
products = pd.DataFrame([
    ["CP-100", "Centrifugal pump", "Pumps", "2025-03-01"],
    ["BP-200", "Booster pump set", "Pumps", "2025-02-01"],
    ["MV-300", "Motorised control valve", "Valves", "2025-04-01"],
], columns=["ProductID", "ProductName", "Family", "LaunchDate"])
products["LaunchDate"] = pd.to_datetime(products.LaunchDate)

parts = pd.DataFrame([
    ["P100", "Pump Shaft", "Machined", "Steel 42CrMo4", "S. Rao", 820, 14.0],
    ["P200", "Valve Body", "Machined", "Aluminium 6061", "M. Chen", 1450, 38.0],
    ["P300", "Valve Seat Ring", "Machined", "Stainless steel 316", "S. Rao", 210, 9.5],
    ["P400", "Mounting Bracket", "Pressed", "Steel S355", "L. Okafor", 640, 6.0],
    ["P500", "Pump Cover", "Moulded", "PA66-GF30", "M. Chen", 380, 5.5],
    ["E600", "Drive Motor", "Electrical", "Bought-out", "A. Patel", 2900, 85.0],
    ["E700", "Wire Harness", "Electrical", "Bought-out", "A. Patel", 260, 12.0],
    ["E800", "Valve Controller PCB", "Electronic", "FR-4 assembly", "R. Iyer", 95, 41.0],
], columns=["PartID", "PartName", "PartType", "Material", "DesignOwner", "TargetMass_g", "TargetCost_USD"])

bom = pd.DataFrame([
    ["CP-100", "P100", 1], ["CP-100", "P300", 2], ["CP-100", "P500", 1], ["CP-100", "P400", 1], ["CP-100", "E600", 1],
    ["BP-200", "P100", 2], ["BP-200", "P200", 1], ["BP-200", "P300", 2], ["BP-200", "P400", 2],
    ["MV-300", "P200", 1], ["MV-300", "P300", 1], ["MV-300", "E600", 1], ["MV-300", "E700", 1], ["MV-300", "E800", 1],
], columns=["ProductID", "PartID", "QtyPer"])

rev_dates = {
    "P100": [("A", "2024-11-15"), ("B", "2025-09-10")],
    "P200": [("A", "2024-12-02"), ("B", "2025-06-20")],
    "P300": [("A", "2024-11-20"), ("B", "2025-05-12"), ("C", "2026-05-18")],
    "P400": [("A", "2024-10-30")],
    "P500": [("A", "2024-12-10"), ("B", "2026-02-03")],
    "E600": [("A", "2024-11-01")],
    "E700": [("A", "2024-12-15"), ("B", "2025-11-04")],
    "E800": [("A", "2025-01-20"), ("B", "2025-08-14"), ("C", "2026-03-09")],
}
revisions = pd.DataFrame([[p, r, pd.Timestamp(d)] for p, L in rev_dates.items() for r, d in L], columns=["PartID", "Rev", "ReleaseDate"])
revisions["PartRev"] = revisions.PartID + "-" + revisions.Rev

def rev_at(part, date):
    L = revisions[(revisions.PartID == part) & (revisions.ReleaseDate <= date)]
    return L.Rev.iloc[-1] if len(L) else "A"

drawings = []
k = 0
for _, r in revisions.iterrows():
    for sheet in range(1, 3 if r.PartID in ("P200", "E800") else 2):
        k += 1
        rounds = int(rng.choice([1, 1, 1, 2, 2, 3], p=[.3, .2, .15, .15, .1, .1]))
        if r.PartRev == "P300-B": rounds = 3
        planned = r.ReleaseDate - pd.Timedelta(days=int(rng.integers(0, 6)))
        late = max(0, int(rng.normal(4, 6))) if rounds >= 2 else max(0, int(rng.normal(0, 3)))
        if r.PartRev == "P300-B": late = 19
        drawings.append([f"DRW-{1000 + k}", r.PartID, r.Rev, sheet, planned.normalize(), (planned + pd.Timedelta(days=late)).normalize(), rounds])
drawings = pd.DataFrame(drawings, columns=["DrawingNo", "PartID", "Rev", "Sheet", "PlannedRelease", "ActualRelease", "ReviewRounds"])
cats = ["Tolerance", "GD&T", "Material", "Manufacturability", "Documentation"]
findings = []
f = 0
for _, d in drawings.iterrows():
    n = int(rng.poisson(1.2 + 1.6 * (d.ReviewRounds - 1)))
    if d.PartID == "P300" and d.Rev == "B": n = 9
    for i in range(n):
        f += 1
        cat = rng.choice(cats, p=[.32, .22, .1, .21, .15]) if not (d.PartID == "P300" and i < 5) else "Tolerance"
        sev = "Major" if rng.random() < (0.35 if cat in ("Tolerance", "GD&T") else 0.15) else "Minor"
        opened = d.PlannedRelease - pd.Timedelta(days=int(rng.integers(5, 30)))
        closed = opened + pd.Timedelta(days=int(rng.integers(1, 21)))
        findings.append([f"RF-{2000 + f}", d.DrawingNo, opened.normalize(), cat, sev, closed.normalize()])
findings = pd.DataFrame(findings, columns=["FindingID", "DrawingNo", "OpenedDate", "Category", "Severity", "ClosedDate"])

mass_cost = []
for _, r in revisions.iterrows():
    p = parts.set_index("PartID").loc[r.PartID]
    m = p.TargetMass_g * rng.normal(1.03, 0.04)
    c = p.TargetCost_USD * rng.normal(1.04, 0.06)
    if r.PartRev == "P300-C": c = p.TargetCost_USD * 1.12
    mass_cost.append([r.PartID, r.Rev, round(m, 1), round(c, 2)])
mass_cost = pd.DataFrame(mass_cost, columns=["PartID", "Rev", "ActualMass_g", "ActualCost_USD"])

stacks = pd.DataFrame([
    ["STK-01", "BP-200", "Seat ring to body bore diametral clearance", 0.010, 0.080],
    ["STK-02", "CP-100", "Shaft end float", 0.050, 0.400],
    ["STK-03", "MV-300", "Motor to valve body alignment", 0.000, 0.150],
], columns=["StackID", "ProductID", "Requirement", "MinGap_mm", "MaxGap_mm"])
GEO1 = "One-sided geometric term (only uses up clearance); entered as +/- here"
contrib = pd.DataFrame([  # Rev blank = applies to all revs of the part
    ["STK-01", "P200", "", "Body bore", 1, 40.050, 0.012, ""],
    ["STK-01", "P300", "A/B", "Seat ring outer diameter", -1, 40.000, 0.015, ""],
    ["STK-01", "P300", "C", "Seat ring outer diameter", -1, 40.000, 0.008, "Tighter OD tolerance from ECR-3200"],
    ["STK-01", "P300", "", "Seat ring roundness", -1, 0.000, 0.006, GEO1],
    ["STK-01", "P100", "", "Shaft runout", -1, 0.000, 0.008, GEO1],
    ["STK-01", "P200", "", "Bore position", -1, 0.000, 0.010, GEO1],
    ["STK-02", "P100", "", "Shaft shoulder length", 1, 52.200, 0.050, ""],
    ["STK-02", "P500", "", "Cover depth", -1, 30.000, 0.080, ""],
    ["STK-02", "P400", "", "Bracket thickness", -1, 6.000, 0.060, ""],
    ["STK-02", "P300", "", "Seat ring height", -1, 16.000, 0.030, ""],
    ["STK-03", "P200", "", "Spigot diameter", 1, 60.080, 0.020, ""],
    ["STK-03", "E600", "", "Motor pilot diameter", -1, 60.000, 0.025, ""],
    ["STK-03", "P400", "", "Bracket hole position", -1, 0.000, 0.040, ""],
], columns=["StackID", "PartID", "Rev", "Feature", "Direction", "Nominal_mm", "Tol_mm", "Note"])

fea = pd.DataFrame([
    ["P100", "B", "Peak torque", 312, 655], ["P100", "B", "Fatigue, 10^7 cycles", 248, 380],
    ["P200", "B", "Bolt preload", 96, 240], ["P200", "B", "Drop 1 m", 171, 240],
    ["P300", "B", "Seating load", 118, 180], ["P300", "C", "Seating load", 101, 180],
    ["P400", "A", "Vibration 5 g", 141, 355], ["P400", "A", "Bolt preload", 205, 355],
    ["P500", "B", "Internal pressure 10 bar", 52, 120], ["P500", "A", "Internal pressure 10 bar", 69, 120],
], columns=["PartID", "Rev", "LoadCase", "MaxStress_MPa", "Allowable_MPa"])
mfg_cpk = pd.DataFrame([
    ["P100", "CNC-L01", 1.904], ["P100", "CNC-L02", 1.632], ["P100", "CNC-L03", 1.163],
    ["P200", "CNC-M01", 1.739], ["P200", "CNC-M02", 1.707], ["P200", "CNC-M03", 1.329],
    ["P300", "GRD-01", 1.848], ["P300", "GRD-02", 0.787],
    ["P400", "PRS-01", 1.715], ["P400", "PRS-02", 1.513], ["P500", "INJ-01", 1.929], ["P500", "INJ-02", 1.412],
], columns=["PartID", "MachineID", "Cpk"])

reasons = ["Design error", "Cost reduction", "Supplier change", "Field failure", "Customer request", "Manufacturability"]
rp = [.22, .2, .14, .12, .12, .2]
changes, affected = [], []
n_changes = 168
for i in range(n_changes):
    cid = f"ECR-{3001 + i}"
    req = D0 + pd.Timedelta(days=int(((D1 - D0).days - 5) * rng.beta(1.6, 1.0)))
    reason = rng.choice(reasons, p=rp)
    pri = rng.choice(["High", "Medium", "Low"], p=[.25, .5, .25])
    part = rng.choice(parts.PartID, p=[.14, .14, .12, .1, .12, .1, .12, .16])
    tri = int(rng.gamma(2, 2)); rev = int(rng.gamma(2.2, 11 if pri != "High" else 5)); imp = int(rng.gamma(2.5, 10)); clo = int(rng.gamma(1.5, 3))
    if reason == "Supplier change": imp += int(rng.integers(10, 30))
    if part == "E800": rev += 6
    dates = [req, req + pd.Timedelta(days=tri), None, None, None]
    dates[2] = dates[1] + pd.Timedelta(days=rev)
    dates[3] = dates[2] + pd.Timedelta(days=imp)
    dates[4] = dates[3] + pd.Timedelta(days=clo)
    status = "Closed"
    for j, st in [(4, "Implemented"), (3, "Approved"), (2, "In review"), (1, "Submitted")]:
        if dates[j] > D1:
            status = st
            for jj in range(j, 5): dates[jj] = None
    cost = round(float(rng.lognormal(7.2, 0.9)), 0) * (1 if reason != "Cost reduction" else -1)
    reval = "Yes" if reason in ("Design error", "Field failure") or rng.random() < .2 else "No"
    changes.append([cid, "", reason, pri, part, *dates, status, cost, reval, rng.choice(["S. Rao", "M. Chen", "L. Okafor", "A. Patel", "R. Iyer"])])
    for p in sorted({part} | set(rng.choice(parts.PartID, size=int(rng.integers(0, 3))))):  # sorted: set order is hash-seed dependent
        affected.append([cid, p, int(rng.integers(1, 4))])
cols = ["ChangeID", "ParentChangeID", "Reason", "Priority", "PrimaryPart", "RequestDate", "TriageDate", "ApprovalDate", "ImplementDate", "CloseDate", "Status", "CostImpact_USD", "NeedsRevalidation", "Originator"]
changes = pd.DataFrame(changes, columns=cols)
story = dict(ChangeID="ECR-3200", ParentChangeID="", Reason="Field failure", Priority="High", PrimaryPart="P300",
             RequestDate=pd.Timestamp("2026-01-26"), TriageDate=pd.Timestamp("2026-01-29"), ApprovalDate=pd.Timestamp("2026-03-27"),
             ImplementDate=pd.Timestamp("2026-05-18"), CloseDate=pd.Timestamp("2026-05-29"), Status="Closed", CostImpact_USD=18400.0,
             NeedsRevalidation="Yes", Originator="S. Rao")
changes = pd.concat([changes, pd.DataFrame([story])], ignore_index=True)
for p, n in [("P300", 2), ("P200", 2), ("P100", 1), ("P400", 1)]:
    affected.append(["ECR-3200", p, n])
affected = pd.DataFrame(affected, columns=["ChangeID", "PartID", "DrawingsAffected"]).drop_duplicates(["ChangeID", "PartID"])
kids = rng.choice(changes.index[(changes.Status == "Closed")], size=9, replace=False)
rework = []
for i, ix in enumerate(kids):
    par = changes.loc[ix]
    req = par.CloseDate + pd.Timedelta(days=int(rng.integers(10, 60)))
    if req > D1 - pd.Timedelta(days=30): continue
    rework.append(dict(ChangeID=f"ECR-{3201 + i}", ParentChangeID=par.ChangeID, Reason="Design error", Priority="High", PrimaryPart=par.PrimaryPart,
                       RequestDate=req, TriageDate=req + pd.Timedelta(days=2), ApprovalDate=req + pd.Timedelta(days=9),
                       ImplementDate=req + pd.Timedelta(days=21), CloseDate=req + pd.Timedelta(days=24), Status="Closed",
                       CostImpact_USD=float(round(rng.lognormal(7, .6))), NeedsRevalidation="Yes", Originator=par.Originator))
changes = pd.concat([changes, pd.DataFrame(rework)], ignore_index=True)
cand = changes[(changes.RequestDate >= "2026-04-01") & (changes.RequestDate <= "2026-08-15") & (changes.ParentChangeID == "") & (changes.ChangeID != "ECR-3200")].index
stuck = rng.choice(cand, size=min(12, len(cand)), replace=False)
changes.loc[stuck, ["ApprovalDate", "ImplementDate", "CloseDate"]] = pd.NaT
changes.loc[stuck, "Status"] = "In review"
for r in rework:
    affected = pd.concat([affected, pd.DataFrame([[r["ChangeID"], r["PrimaryPart"], 1]], columns=affected.columns)])

months = pd.date_range("2025-03-01", "2026-09-01", freq="MS")
builds = []
base = {"CP-100": 900, "BP-200": 650, "MV-300": 420}
for m in months:
    for pid, b in base.items():
        if m < products.set_index("ProductID").loc[pid, "LaunchDate"]: continue
        u = int(b * rng.normal(1 + 0.012 * ((m - months[0]).days / 30), 0.06))
        builds.append([pid, m, rev_at("P300", m + pd.Timedelta(days=14)), u])
builds = pd.DataFrame(builds, columns=["ProductID", "BuildMonth", "SeatRingRev", "UnitsBuilt"])

tests = []
t = 0
for _, r in revisions.iterrows():
    nlots = 14 if r.PartID in ("P300", "E800") else 8
    p_pass = {"A": .86, "B": .9, "C": .96}[r.Rev]
    if r.PartRev == "P300-B": p_pass = .82
    if r.PartRev == "P300-C": p_pass = .97
    for i in range(nlots):
        t += 1
        d = r.ReleaseDate + pd.Timedelta(days=int(rng.integers(-40, 30)))
        ok = rng.random() < p_pass
        tests.append([f"TST-{4000 + t}", r.PartID, r.Rev, d.normalize(), rng.choice(["Endurance", "Dimensional", "Environmental"]), "Pass" if ok else "Fail"])
tests = pd.DataFrame(tests, columns=["TestID", "PartID", "Rev", "TestDate", "TestType", "Result"])
fm_by_part = {"P300": ["Seat ring wear (internal leakage)", "Seat leakage noise"], "P100": ["Shaft fatigue crack"], "P200": ["Valve body leak"], "P400": ["Bracket crack"],
              "P500": ["Cover leak"], "E600": ["Motor winding failure"], "E700": ["Harness chafe"], "E800": ["PCB solder joint failure"]}
tests["FailureMode"] = [rng.choice(fm_by_part[p]) if res == "Fail" else "" for p, res in zip(tests.PartID, tests.Result)]

claims = []
c = 0
rate = {"A": 2600e-6, "B": 3400e-6, "C": 700e-6}
for _, b in builds.iterrows():
    seat_q = int(bom[(bom.ProductID == b.ProductID) & (bom.PartID == "P300")].QtyPer.iloc[0])
    lam = rate[b.SeatRingRev] * seat_q
    n = rng.poisson(b.UnitsBuilt * lam)
    other = rng.poisson(b.UnitsBuilt * 900e-6)
    for kind, nn in (("seat", n), ("other", other)):
        for _ in range(nn):
            c += 1
            ttf = int(rng.weibull(1.6) * (95 if kind == "seat" else 200)) + 10
            fail = b.BuildMonth + pd.Timedelta(days=int(rng.integers(0, 28)) + ttf)
            if fail > D1: continue
            if kind == "seat":
                part, mode = "P300", "Seat ring wear (internal leakage)"
            else:
                comps = bom[bom.ProductID == b.ProductID].PartID.tolist()
                part = rng.choice([p for p in comps if p != "P300"])
                mode = fm_by_part[part][0]
            cost = round(float(rng.normal(420 if kind == "seat" else 260, 60)), 2)
            claims.append([f"WC-{5000 + c}", b.ProductID, part, rev_at(part, b.BuildMonth + pd.Timedelta(days=14)), b.BuildMonth, fail.normalize(), mode, cost])
claims = pd.DataFrame(claims, columns=["ClaimID", "ProductID", "PartID", "Rev", "BuildMonth", "FailureDate", "FailureMode", "WarrantyCost_USD"])

dfmea = pd.DataFrame([
    ["DF-01", "P300", "Seat ring wear (internal leakage)", "Internal leakage, valve fails to shut off", 8, 7, 5, "Tighter OD tolerance, rev C", "ECR-3200", 8, 3, 3],
    ["DF-02", "P300", "Seat ring migration in body bore", "Leakage past seat, loss of shut-off", 6, 4, 5, "Interference fit check added", "", 6, 3, 4],
    ["DF-03", "P100", "Shaft fatigue crack", "Loss of drive", 9, 3, 4, "Fillet radius increased, rev B", "", 9, 2, 3],
    ["DF-04", "P200", "Valve body leak at flange joint", "External fluid leak", 7, 5, 4, "", "", 7, 5, 4],
    ["DF-05", "P400", "Bracket crack under vibration", "Unit detaches", 9, 2, 6, "Vibration test added", "", 9, 2, 3],
    ["DF-06", "P500", "Cover leak", "Fluid loss", 6, 4, 4, "Rib redesign, rev B", "", 6, 2, 4],
    ["DF-07", "E600", "Motor winding failure", "Unit stops", 8, 3, 5, "", "", 8, 3, 5],
    ["DF-08", "E700", "Harness chafe on bracket", "Short circuit", 9, 4, 6, "Grommet added, rev B", "", 9, 2, 4],
    ["DF-09", "E800", "Solder joint failure", "Intermittent stop", 7, 5, 6, "Thermal profile change, rev C", "", 7, 3, 4],
    ["DF-10", "E800", "Connector misassembly", "Unit does not start", 6, 4, 3, "", "", 6, 4, 3],
], columns=["LineID", "PartID", "FailureMode", "Effect", "S", "O", "D", "Action", "ChangeID", "S_after", "O_after", "D_after"])


# ---------------- NPD stage-gate (own generator, seed 2027; added after every seed-2026 draw so no existing table changes) ----------------
NPD_STAGES = ["Requirements & specification", "Preliminary concepts", "Preliminary drawings", "Concept finalization (gate)",
              "Final 3D modeling", "Design verification (FEA, tolerance stacks, DFMEA)", "Detailing (2D drawings, GD&T)",
              "Checking", "Design review", "Release", "Prototype & validation", "Production handover"]
# planned duration ranges in days (low, high inclusive): rev A = full concept work, rev B/C = change revision with carry-over
DUR_A = [(10, 15), (12, 18), (8, 12), (3, 5), (15, 25), (10, 15), (10, 15), (4, 6), (3, 5), (2, 3), (20, 35), (7, 14)]
DUR_BC = [(2, 4), (1, 3), (2, 4), (1, 2), (6, 10), (5, 8), (5, 8), (3, 5), (2, 3), (1, 2), (14, 21), (5, 10)]

def make_npd(revisions, drawings, findings, parts, cutoff):
    g = np.random.default_rng(2027)
    names = sorted(parts.DesignOwner.unique())
    d1 = drawings[drawings.Sheet == 1].set_index(["PartID", "Rev"])
    nfind = findings.DrawingNo.value_counts()
    day = lambda n: pd.Timedelta(days=int(n))
    rows = []
    for _, r in revisions.iterrows():
        dw = d1.loc[(r.PartID, r.Rev)]
        plan_rel, act_rel, rounds = dw.PlannedRelease, dw.ActualRelease, int(dw.ReviewRounds)
        late = (act_rel - plan_rel).days
        owner = parts.set_index("PartID").loc[r.PartID, "DesignOwner"]
        others = [n for n in names if n != owner]
        checker, reviewer = g.choice(others, size=2, replace=False)
        rng_d = DUR_A if r.Rev == "A" else DUR_BC
        pdur = [int(g.integers(lo, hi + 1)) for lo, hi in rng_d]
        # planned: stages 1-10 backwards from PlannedRelease, 11-12 forward from it
        pend = [None] * 12; pstart = [None] * 12
        pend[9] = plan_rel
        for s in range(9, -1, -1):
            pstart[s] = pend[s] - day(pdur[s])
            if s: pend[s - 1] = pstart[s]
        pstart[10] = plan_rel; pend[10] = plan_rel + day(pdur[10])
        pstart[11] = pend[10]; pend[11] = pstart[11] + day(pdur[11])
        # slip (actual minus planned duration) per stage 1-10; sums to the drawing's release lateness
        slip = [0] * 12
        if r.PartRev == "P300-B":
            slip[5], slip[7], slip[8] = 2, 10, 7
        elif rounds >= 2:  # review loops: earlier stages may finish a little early, the slip lands in Checking and Design review
            early = min(int(g.integers(-3, 2)), late)
            slip[int(g.integers(4, 7))] += early
            rest = late - early
            slip[7] = int(np.ceil(rest * 0.6)); slip[8] = rest - slip[7]
        else:
            if late > 0:
                slip[int(g.integers(0, 7))] += late
            a = int(g.integers(0, 6)); x = int(g.integers(0, 3))  # transient slip recovered by a later stage
            slip[a] += x; slip[int(g.integers(a + 1, 7))] -= x
        for s in (10, 11):
            slip[s] = int(g.integers(-3, 5))
        assert sum(slip[:10]) == late
        astart = [None] * 12; aend = [None] * 12
        astart[0] = pstart[0]
        for s in range(12):
            if s == 10: astart[s] = act_rel
            elif s: astart[s] = aend[s - 1]
            aend[s] = astart[s] + day(max(1, pdur[s] + slip[s]))
        assert aend[9] == act_rel
        for s in range(12):
            own = owner if s not in (7, 8) else (checker if s == 7 else reviewer)
            loops = rounds - 1 if s in (7, 8) else 0
            if s in (7, 8) and rounds >= 2:
                gate = "Rework"
            elif s in (7, 8):
                gate = "Pass with actions" if nfind.get(dw.DrawingNo, 0) > 0 else "Pass"
            elif s == 9:
                gate = "Pass"  # release is a formal sign-off once checking and review are closed
            elif r.Rev != "A" and s <= 3:
                gate = "Pass"  # carry-over of the rev A concept
            else:
                gate = "Pass with actions" if g.random() < (0.3 if s in (3, 5) else 0.15) else "Pass"
            a0, a1 = astart[s], aend[s]
            if a0 > cutoff:
                a0, a1, gate = pd.NaT, pd.NaT, ""
            elif a1 > cutoff:  # started but not finished at the data cut-off
                a1, gate = pd.NaT, ""
            rows.append([r.PartID, r.Rev, r.PartRev, s + 1, NPD_STAGES[s], pstart[s], pend[s], a0, a1, own, gate, loops])
    out = pd.DataFrame(rows, columns=["PartID", "Rev", "PartRev", "StageNo", "Stage", "PlannedStart", "PlannedEnd",
                                      "ActualStart", "ActualEnd", "Owner", "GateResult", "ReworkLoops"])
    for c in ["PlannedStart", "PlannedEnd", "ActualStart", "ActualEnd"]:
        out[c] = pd.to_datetime(out[c]).dt.normalize()
    return out

npd = make_npd(revisions, drawings, findings, parts, D1)

data = dict(products=products, parts=parts, bom=bom, revisions=revisions, drawings=drawings, findings=findings, mass_cost=mass_cost,
            stacks=stacks, contrib=contrib, fea=fea, mfg_cpk=mfg_cpk, changes=changes, affected=affected, builds=builds,
            tests=tests, claims=claims, dfmea=dfmea, npd=npd)
pickle.dump(data, open(os.path.join(OUT, "data_c2.pkl"), "wb"))
print({k: len(v) for k, v in data.items()})
