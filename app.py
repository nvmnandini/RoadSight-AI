import io
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import folium

from PIL import Image
from streamlit_folium import st_folium

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="RoadSight AI",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM DESIGN
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: radial-gradient(circle at top right, #172b48, #080e19 48%);
    color: #f3f6ff;
    font-family: 'DM Sans', sans-serif;
}
.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] {
    background: #0d1524;
    border-right: 1px solid #263650;
}
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #16243a, #101827);
    padding: 20px;
    border: 1px solid #2a3b56;
    border-radius: 17px;
}
[data-testid="stMetricLabel"] {
    color: #9cacc4 !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
}
.hero {
    padding: 30px;
    border: 1px solid #304766;
    border-radius: 22px;
    background: linear-gradient(120deg, #1a3150, #101827);
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 38px;
    margin-bottom: 8px;
}
.hero p {
    color: #b2c0d6;
    font-size: 15px;
}
.eyebrow {
    color: #54e3d1;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 700;
}
.panel {
    padding: 20px;
    border: 1px solid #293a53;
    border-radius: 17px;
    background: #111a2b;
}
.stButton button {
    background: linear-gradient(90deg, #39cdbc, #70e8d8);
    color: #07131d;
    border: none;
    border-radius: 11px;
    font-weight: 700;
}
div[data-testid="stTabs"] button {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SAMPLE DATA
# These are DEMO records.
# =========================
@st.cache_data
def get_data():
    return pd.DataFrame([
        {
            "ID": "RD-1042", "Area": "Athwa Gate",
            "Type": "Pothole", "Severity": "High",
            "Priority": 94, "Status": "Urgent",
            "Latitude": 21.1702, "Longitude": 72.8311
        },
        {
            "ID": "RD-1041", "Area": "Adajan Road",
            "Type": "Road crack", "Severity": "Medium",
            "Priority": 68, "Status": "Scheduled",
            "Latitude": 21.1810, "Longitude": 72.8140
        },
        {
            "ID": "RD-1040", "Area": "Pal",
            "Type": "Surface damage", "Severity": "High",
            "Priority": 88, "Status": "Urgent",
            "Latitude": 21.1950, "Longitude": 72.8190
        },
        {
            "ID": "RD-1039", "Area": "Udhna",
            "Type": "Pothole", "Severity": "Medium",
            "Priority": 61, "Status": "Scheduled",
            "Latitude": 21.1550, "Longitude": 72.8310
        },
        {
            "ID": "RD-1038", "Area": "Rander",
            "Type": "Road crack", "Severity": "Low",
            "Priority": 29, "Status": "Monitor",
            "Latitude": 21.2040, "Longitude": 72.7900
        },
        {
            "ID": "RD-1037", "Area": "Varachha",
            "Type": "Pothole", "Severity": "High",
            "Priority": 91, "Status": "Urgent",
            "Latitude": 21.1660, "Longitude": 72.8460
        },
        {
            "ID": "RD-1036", "Area": "Palanpur",
            "Type": "Edge damage", "Severity": "Medium",
            "Priority": 57, "Status": "Scheduled",
            "Latitude": 21.1900, "Longitude": 72.8050
        },
        {
            "ID": "RD-1035", "Area": "Dumas Road",
            "Type": "Road crack", "Severity": "Low",
            "Priority": 22, "Status": "Monitor",
            "Latitude": 21.1450, "Longitude": 72.7700
        }
    ])

df = get_data()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(
        "<h2>🛣️ RoadSight <span style='color:#54e3d1'>AI</span></h2>",
        unsafe_allow_html=True
    )
    st.caption("ROAD DAMAGE INTELLIGENCE")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "AI Inspector",
            "Damage Map",
            "Reports"
        ]
    )

    st.divider()
    st.markdown("### System status")
    st.success("Dashboard ready")
    st.caption("AI detection runs when you upload an image.")
    st.caption("Map markers are sample locations.")

# =========================
# HERO HEADER
# =========================
st.markdown("""
<div class="hero">
    <div class="eyebrow">SMART INFRASTRUCTURE · COMPUTER VISION</div>
    <h1>Road damage, <span style="color:#54e3d1">made visible.</span></h1>
    <p>
        An intelligent road inspection dashboard for identifying
        road defects, estimating repair priority, and visualizing
        reported damage locations.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# OVERVIEW
# =========================
if page == "Overview":

    st.subheader("Network overview")
    st.caption(
        "Illustrative Surat demo data. These are not verified "
        "municipal reports or live road conditions."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total reports", len(df))
    col2.metric(
        "High severity",
        int((df["Severity"] == "High").sum())
    )
    col3.metric(
        "Urgent repairs",
        int((df["Status"] == "Urgent").sum())
    )
    col4.metric(
        "Average priority",
        f"{df['Priority'].mean():.0f}/100"
    )

    st.write("")

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### Highest priority reports")

        queue = df.sort_values(
            "Priority", ascending=False
        ).head(6)

        st.dataframe(
            queue[
                ["ID", "Area", "Type",
                 "Severity", "Priority", "Status"]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Priority": st.column_config.ProgressColumn(
                    "Priority score",
                    min_value=0,
                    max_value=100,
                    format="%d"
                )
            }
        )

    with right:
        st.markdown("### Damage category breakdown")

        type_data = (
            df["Type"].value_counts()
            .rename_axis("Damage type")
            .reset_index(name="Reports")
        )

        fig = px.pie(
            type_data,
            names="Damage type",
            values="Reports",
            hole=0.62,
            color_discrete_sequence=[
                "#54e3d1",
                "#7195ff",
                "#ffbd69",
                "#ff718a"
            ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(t=15, b=15, l=5, r=5),
            legend=dict(orientation="h", y=-0.12)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Severity analysis")

    severity_data = (
        df["Severity"].value_counts()
        .reindex(["High", "Medium", "Low"], fill_value=0)
        .rename_axis("Severity")
        .reset_index(name="Reports")
    )

    fig = px.bar(
        severity_data,
        x="Severity",
        y="Reports",
        color="Severity",
        text="Reports",
        color_discrete_map={
            "High": "#ff647c",
            "Medium": "#ffbd69",
            "Low": "#54e3d1"
        }
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        showlegend=False,
        xaxis_title="",
        yaxis_title="Number of reports"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Inspection workflow")

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            "<div class='panel'><h3>01 · Detect</h3>"
            "<p>Inspect road images using computer vision.</p></div>",
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            "<div class='panel'><h3>02 · Prioritize</h3>"
            "<p>Estimate severity and assign a preliminary score.</p></div>",
            unsafe_allow_html=True
        )

    with c:
        st.markdown(
            "<div class='panel'><h3>03 · Visualize</h3>"
            "<p>Review reported locations and maintenance status.</p></div>",
            unsafe_allow_html=True
        )

# =========================
# AI INSPECTOR
# =========================
elif page == "AI Inspector":

    st.subheader("AI road inspection")
    st.write(
        "Upload a road image to detect candidate potholes and "
        "surface defects using a YOLO-World model."
    )

    st.info(
        "For best results, upload a sharp, daylight photograph "
        "where the damaged road surface is clearly visible."
    )

    uploaded = st.file_uploader(
        "Choose a road image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded is not None:

        image = Image.open(uploaded).convert("RGB")

        original_col, result_col = st.columns(2)

        with original_col:
            st.markdown("### Original image")
            st.image(image, use_container_width=True)

        with result_col:
            st.markdown("### Detection result")

            if st.button(
                "Run AI detection",
                type="primary",
                use_container_width=True
            ):

                try:
                    from ultralytics import YOLO

                    with st.spinner(
                        "Loading AI model and analyzing image..."
                    ):
                        # Downloads model weights on first use.
                        model = YOLO("yolov8s-world.pt")

                        model.set_classes([
                            "pothole",
                            "road crack",
                            "damaged asphalt",
                            "road surface breakup"
                        ])

                        results = model.predict(
                            np.array(image),
                            conf=0.12,
                            verbose=False
                        )

                        result = results[0]

                        # Convert annotated BGR output to RGB.
                        annotated = result.plot()[:, :, ::-1]
                        annotated = Image.fromarray(annotated)

                        st.session_state["inspection"] = {
                            "name": uploaded.name,
                            "image": annotated,
                            "rows": []
                        }

                        image_area = image.width * image.height

                        for box in result.boxes:
                            class_id = int(box.cls[0])
                            label = result.names[class_id]
                            confidence = float(box.conf[0])

                            xyxy = box.xyxy[0].tolist()

                            box_width = max(
                                0, xyxy[2] - xyxy[0]
                            )
                            box_height = max(
                                0, xyxy[3] - xyxy[1]
                            )

                            ratio = (
                                box_width * box_height
                            ) / max(1, image_area)

                            # Demonstration-only heuristic.
                            if ratio >= 0.10:
                                severity = "High"
                                priority = 85
                            elif ratio >= 0.025:
                                severity = "Medium"
                                priority = 60
                            else:
                                severity = "Low"
                                priority = 30

                            st.session_state["inspection"]["rows"].append({
                                "Detected class": label.title(),
                                "Confidence (%)": round(
                                    confidence * 100, 1
                                ),
                                "Estimated severity": severity,
                                "Estimated priority": priority
                            })

                    st.rerun()

                except Exception as error:
                    st.error(
                        "The AI model could not run. Check your "
                        "internet connection and installed packages."
                    )
                    st.code(str(error))

            inspection = st.session_state.get("inspection")

            if (
                inspection is not None
                and inspection["name"] == uploaded.name
            ):
                st.image(
                    inspection["image"],
                    use_container_width=True
                )

                rows = inspection["rows"]

                st.metric("Candidate defects", len(rows))

                if rows:
                    st.dataframe(
                        pd.DataFrame(rows),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.warning(
                        "No candidate defects detected. This does "
                        "not guarantee the road is damage-free."
                    )

                buffer = io.BytesIO()
                inspection["image"].save(buffer, format="PNG")

                st.download_button(
                    "Download annotated image",
                    data=buffer.getvalue(),
                    file_name="roadsight_detection.png",
                    mime="image/png"
                )

    else:
        st.markdown("### How to use the inspector")

        st.markdown("""
        1. Upload a road photograph.
        2. Click **Run AI detection**.
        3. Review the annotated image and detected regions.
        4. Download the annotated result for your project report.
        """)

        st.warning(
            "Severity is estimated using the detected region's "
            "relative image area. This is not a measurement of "
            "pothole depth or an engineering-certified safety score."
        )

# =========================
# INTERACTIVE DAMAGE MAP
# =========================
elif page == "Damage Map":

    st.subheader("Road damage location map")

    st.caption(
        "The markers below are sample Surat locations. "
        "They are not live reports and are not linked to uploaded images."
    )

    selected = st.multiselect(
        "Filter by severity",
        ["High", "Medium", "Low"],
        default=["High", "Medium", "Low"]
    )

    map_data = df[df["Severity"].isin(selected)]

    road_map = folium.Map(
        location=[21.175, 72.820],
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    colors = {
        "High": "red",
        "Medium": "orange",
        "Low": "green"
    }

    for _, row in map_data.iterrows():

        popup_text = f"""
        <b>{row['ID']} — {row['Type']}</b><br>
        Area: {row['Area']}<br>
        Severity: {row['Severity']}<br>
        Priority: {row['Priority']}/100<br>
        Status: {row['Status']}
        """

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=9 if row["Severity"] == "High" else 6,
            color=colors[row["Severity"]],
            fill=True,
            fill_color=colors[row["Severity"]],
            fill_opacity=0.9,
            tooltip=f"{row['Severity']} — {row['Area']}",
            popup=folium.Popup(
                popup_text,
                max_width=280
            )
        ).add_to(road_map)

    st_folium(
        road_map,
        use_container_width=True,
        height=570,
        returned_objects=[]
    )

    st.markdown("### Mapped reports")

    st.dataframe(
        map_data.sort_values(
            "Priority", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# =========================
# REPORTS
# =========================
elif page == "Reports":

    st.subheader("Inspection reports")

    col1, col2 = st.columns(2)

    with col1:
        severity_filter = st.selectbox(
            "Severity",
            ["All", "High", "Medium", "Low"]
        )

    with col2:
        status_filter = st.selectbox(
            "Maintenance status",
            ["All", "Urgent", "Scheduled", "Monitor"]
        )

    reports = df.copy()

    if severity_filter != "All":
        reports = reports[
            reports["Severity"] == severity_filter
        ]

    if status_filter != "All":
        reports = reports[
            reports["Status"] == status_filter
        ]

    st.dataframe(
        reports.sort_values(
            "Priority", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    csv_data = reports.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV report",
        data=csv_data,
        file_name="roadsight_road_reports.csv",
        mime="text/csv"
    )

    st.markdown("### Priority interpretation")

    st.markdown("""
    | Priority score | Suggested action |
    |---|---|
    | 80–100 | Urgent inspection |
    | 50–79 | Schedule maintenance review |
    | 0–49 | Monitor and verify |

    These thresholds are illustrative and must be validated before
    use in real road-maintenance decisions.
    """)

# =========================
# FOOTER
# =========================
st.divider()

st.caption(
    "RoadSight AI · Machine Learning Project · Academic prototype. "
    "Demo locations and priority scores are illustrative. "
    "AI results require human verification."
)