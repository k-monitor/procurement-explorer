import json
from collections import Counter

import altair as alt
import pandas as pd
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from src.tendersguru.db_config import db

###############################################################################
#####                      Connecting to the dump                         #####
###############################################################################
Base = automap_base()
engine = create_engine(db)
Base.prepare(engine, reflect=True)

Session = sessionmaker(bind=engine)
session = Session()

# print(Base.classes.keys())

###############################################################################
#####                 Generating basic descriptive stats                  #####
###############################################################################
procurement_types = (
    session.query(Base.classes["hu_procurements"].type_id)
    .filter(Base.classes["hu_procurements"].awards_count > 0)
    .all()
)
procurement_names = dict(
    session.query(
        Base.classes["hu_procurements_types"].id,
        Base.classes["hu_procurements_types"].name,
    ).all()
)
procurements = [
    procurement_names[e[0]] for e in procurement_types if e[0] in procurement_names
]
type_stats = Counter(procurements)

regime = (
    session.query(Base.classes["hu_procurements"].regime)
    .filter(Base.classes["hu_procurements"].awards_count > 0)
    .all()
)
regime_stats = Counter([e[0] for e in regime])

cpv_data = (
    session.query(Base.classes["hu_procurements"].cpv_data)
    .filter(Base.classes["hu_procurements"].awards_count > 0)
    .all()
)
cpv_data = [json.loads(e[0])["main"]["l1_label_en"] for e in cpv_data if e[0]]
cpv_stats = Counter(cpv_data)

###############################################################################
#####                                 Vizs                                #####
###############################################################################
type_data = pd.DataFrame(
    {"Procurement types": list(type_stats.keys()), "Counts": list(type_stats.values())}
)
chrt_types = alt.Chart(type_data).mark_bar().encode(x="Procurement types", y="Counts")
chrt_types.save("vizs/html/types.html")

regime_data = pd.DataFrame(
    {"Regimes": list(regime_stats.keys()), "Counts": list(regime_stats.values())}
)
chrt_regime = alt.Chart(regime_data).mark_bar().encode(x="Regimes", y="Counts")
chrt_regime.save("vizs/html/regime.html")

cpv_data = pd.DataFrame(
    {"CPV L1 name": list(cpv_stats.keys()), "Counts": list(cpv_stats.values())}
)
chrt_cpv = alt.Chart(cpv_data).mark_bar().encode(x="CPV L1 name", y="Counts")
chrt_cpv.save("vizs/html/cpv.html")
