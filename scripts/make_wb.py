# MIT License, (c) 2026 Vijayakumar Reddy Yeddula. See LICENSE-MIT.
import pickle, pandas as pd, numpy as np, os, shutil
rng = np.random.default_rng(7)
D = pickle.load(open("data_c2.pkl", "rb"))
out = "learner"; shutil.rmtree(out, ignore_errors=True); os.makedirs(f"{out}/Change_Exports")
readme = pd.DataFrame({"Engxtech Manufacturing: design and product engineering data for the Power BI course": [
    "Fictional data. 3 products, 8 parts. Design data (NPD stages, tests, revisions, drawings) from Jul 2024, change log from Jan 2025, builds from Mar 2025; data cut-off 30 Sep 2026. Built for teaching; any resemblance to a real company is coincidence.",
    "Course: Design Engineering Analytics with Power BI - Vijayakumar Yeddula | Engineering & Career Skills.",
    "The change log is NOT in this workbook: it is exported monthly as CSV files in the Change_Exports folder.",
    "Some problems are hidden on purpose (duplicates, part numbers typed differently). Clean them in Power BI, not here."]})
sheets = {"README": readme, "Products": D["products"], "Parts": D["parts"], "BOM": D["bom"], "Revisions": D["revisions"][["PartID", "Rev", "PartRev", "ReleaseDate"]],
          "Drawings": D["drawings"], "NPD_Stages": D["npd"], "ReviewFindings": D["findings"], "MassCost": D["mass_cost"], "Stacks": D["stacks"], "StackContributors": D["contrib"],
          "FEA": D["fea"], "ManufacturingCpk": D["mfg_cpk"], "ChangeAffectedItems": D["affected"], "Builds": D["builds"],
          "TestResults": D["tests"], "WarrantyClaims": D["claims"], "DFMEA": D["dfmea"]}
with pd.ExcelWriter(f"{out}/Engxtech_Design_Data.xlsx", engine="openpyxl") as xw:
    for n, df in sheets.items():
        df.to_excel(xw, sheet_name=n, index=False)
ch = D["changes"].copy()
idx = rng.choice(ch.index, size=14, replace=False)
variants = lambda p, i: [p.replace("P", "P-").replace("E", "E-"), p.lower(), p + " "][i % 3]  # cycle: hyphen, lower-case, trailing space
ch.loc[idx, "PrimaryPart"] = [variants(p, i) for i, p in enumerate(ch.loc[idx, "PrimaryPart"])]
dups = ch.sample(6, random_state=3)
ch["ExportMonth"] = ch.RequestDate.dt.to_period("M")
dups = dups.assign(ExportMonth=(dups.RequestDate + pd.Timedelta(days=31)).dt.to_period("M"))
allc = pd.concat([ch, dups])
for m, g in allc.groupby("ExportMonth"):
    g.drop(columns="ExportMonth").to_csv(f"{out}/Change_Exports/Changes_{m}.csv", index=False, date_format="%Y-%m-%d")
print(len(os.listdir(f"{out}/Change_Exports")), "monthly exports;", len(allc), "rows incl.", len(dups), "duplicates;", len(idx), "part-number variants")
