# import streamlit as st
# import plotly.express as px
# from data_loader import load_data
# from ai_engine import generate_ai_insight
# import pandas as pd
# # --- PAGE CONFIG ---
# st.set_page_config(page_title="RetainAI | Glocomp", layout="wide")
# st.title("🧠 RetainAI: Glocomp Action-Loop Dashboard")

# # --- LOAD DATA ---
# employees, onboarding, pulse, exit_surv, actions = load_data()

# # --- SIDEBAR: GLOBAL FILTERS & API ---
# with st.sidebar:
#     st.header("⚙️ Settings & Filters")
#     gemini_key = st.text_input("Gemini API Key", type="password", help="Get this from Google AI Studio")
    
#     st.divider()
#     st.subheader("Global Filters")
#     selected_location = st.selectbox("Location", ["All"] + list(employees['location'].unique()))
#     selected_division = st.selectbox("Division", ["All"] + list(employees['division'].unique()))

# # Apply Filters
# def filter_data(df):
#     if selected_location != "All" and 'location' in df.columns:
#         df = df[df['location'] == selected_location]
#     if selected_division != "All" and 'division' in df.columns:
#         df = df[df['division'] == selected_division]
#     return df

# f_onboarding = filter_data(onboarding)
# f_pulse = filter_data(pulse)
# f_exit = filter_data(exit_surv)

# # --- 4 TAB STRUCTURE ---
# tab1, tab2, tab3, tab4 = st.tabs(["🚀 Onboarding Hub", "🌊 Wave Analyzer", "📈 Trend & Impact", "🚨 Leavers & Flight Risk"])

# # ==========================================
# # TAB 1: ONBOARDING HUB (UPGRADED UI)
# # ==========================================
# with tab1:
#     st.header("🚀 New Joiner Onboarding Experience")

#     # 1. High-Level KPI Summary
#     col1, col2, col3, col4 = st.columns(4)
#     avg_clarity = f_onboarding['role_clarity'].mean()
#     avg_tools = f_onboarding['tools_access'].mean()
#     avg_support = f_onboarding['manager_support'].mean()
    
#     # Calculate % of joiners struggling (< 3.0 overall score)
#     low_scorers = f_onboarding[f_onboarding['overall_score'] < 3.0]
#     struggle_rate = (len(low_scorers) / len(f_onboarding) * 100) if len(f_onboarding) > 0 else 0

#     col1.metric("Avg Role Clarity", f"{avg_clarity:.1f} / 5.0")
#     col2.metric("Avg Tools Access", f"{avg_tools:.1f} / 5.0")
#     col3.metric("Avg Manager Support", f"{avg_support:.1f} / 5.0")
#     col4.metric("At-Risk Joiners (<3.0)", f"{len(low_scorers)} ({struggle_rate:.0f}%)", delta_color="inverse")

#     st.divider()

#     # 2. Top 3 Problems & Contextual AI Action Section
#     st.subheader("⚠️ Top 3 Onboarding Bottlenecks & Action Plans")
#     st.write("Identifies recurring complaints from employees rating their experience under 3.0, mapped to their specific division and location.")

#     if st.button("✨ Identify Problems & Prescribe Actions", type="primary", key="btn_onboard_ai"):
#         if low_scorers.empty:
#             st.success("🎉 No onboarding responses below 3.0 found for the selected filter.")
#         else:
#             with st.spinner("AI is synthesizing low-scoring feedback across locations and divisions..."):
#                 # Prepare a structured payload of comments + dept + location
#                 feedback_sample = low_scorers[['division', 'location', 'overall_score', 'comment']].dropna().head(12).to_dict(orient='records')
                
#                 # Fetch structured output
#                 from ai_engine import generate_structured_actions
#                 recommendations = generate_structured_actions(feedback_sample, gemini_key)

#                 if recommendations:
#                     # Display the Top 3 cards in clean containers
#                     for idx, item in enumerate(recommendations, 1):
#                         with st.container(border=True):
#                             header_col, badge_col = st.columns([3, 1])
                            
#                             severity_color = "red" if item.get("severity") == "Critical" else ("orange" if item.get("severity") == "High" else "blue")
#                             header_col.markdown(f"### #{idx}: {item.get('problem', 'Identified Issue')}")
#                             badge_col.markdown(f"**Severity:** :{severity_color}[{item.get('severity', 'High')}]")

#                             # Context tags
#                             c1, c2, c3 = st.columns(3)
#                             c1.caption(f"🏢 **Division:** {item.get('department', 'All')}")
#                             c2.caption(f"📍 **Location:** {item.get('location', 'All')}")
#                             c3.caption(f"👤 **Accountable Owner:** **{item.get('owner', 'HR Lead')}**")

#                             # Prescribed action box
#                             st.markdown(f"**💡 Targeted Action Plan:**")
#                             st.info(item.get("action", "No action provided."))
#                 else:
#                     st.error("Failed to parse AI output. Check API key or data format.")

#     # 3. Clean collapsible view for transparency
#     with st.expander("🔍 View Raw Survey Feedback (Overall Score < 3.0)"):
#         st.dataframe(
#             low_scorers[['employee_id', 'division', 'location', 'overall_score','manager_support','role_clarity', 'tools_access', 'comment']],
#             use_container_width=True,
#             hide_index=True
#         )

# # ==========================================
# # TAB 2: WAVE ANALYZER (SYNCHRONIZED WITH TAB 3)
# # ==========================================
# with tab2:
#     st.header("🌊 Pulse Survey Wave Analyzer")
#     st.caption("Inspect a single wave's metrics, flag underperforming scores (< 3.5), discover problem clusters, and generate accountable fixes.")

#     # 1. Wave Selection
#     wave_options = ["Survey 1 (2026-Q1_1)", "Survey 2 (2026-Q1_2)"]
#     selected_wave = st.selectbox("Select Survey Wave to Inspect", wave_options, index=0)
    
#     # Synchronized Scores matching Tab 3 perfectly
#     if "1" in selected_wave:
#         scores = {
#             "Overall Engagement": 2.4,
#             "Workload Stress": 1.8,
#             "Tools & Access": 2.1,
#             "Manager Support": 2.3,
#             "Career Growth": 2.9
#         }
#         unhappy_count = 45
#         total_respondents = 320
#     else:
#         scores = {
#             "Overall Engagement": 3.1,
#             "Workload Stress": 1.5,
#             "Tools & Access": 4.0,
#             "Manager Support": 2.5,
#             "Career Growth": 3.0
#         }
#         unhappy_count = 38
#         total_respondents = 315

#     # 2. Metric Scorecards
#     m1, m2, m3, m4, m5 = st.columns(5)
#     m1.metric("Engagement Score", f"{scores['Overall Engagement']:.1f} / 5.0")
#     m2.metric("Workload", f"{scores['Workload Stress']:.1f} / 5.0")
#     m3.metric("Tools & Access", f"{scores['Tools & Access']:.1f} / 5.0")
#     m4.metric("Manager Support", f"{scores['Manager Support']:.1f} / 5.0")
#     m5.metric("Career Growth", f"{scores['Career Growth']:.1f} / 5.0")

#     st.divider()

#     # 3. Underperforming Scores Watchlist (< 3.5 Threshold)
#     st.subheader("⚠️ Metric Health & Dimension Watchlist")
#     low_scores = {k: v for k, v in scores.items() if v < 3.5}
    
#     if low_scores:
#         st.warning(f"Found **{len(low_scores)} dimensions** falling below the healthy threshold (< 3.5 / 5.0):")
#         cols = st.columns(len(low_scores))
#         for idx, (dim, val) in enumerate(low_scores.items()):
#             with cols[idx]:
#                 sev = "🔴 Critical" if val < 2.0 else "🟡 Needs Attention"
#                 st.markdown(f"**{dim}**")
#                 st.markdown(f"Score: `{val:.1f}` ({sev})")
#     else:
#         st.success("All dimensions are currently performing at or above healthy baseline (>= 3.5).")

#     st.divider()

#     # Session state for persistent button outputs
#     if f"clusters_{selected_wave}" not in st.session_state:
#         st.session_state[f"clusters_{selected_wave}"] = None
#     if f"actions_{selected_wave}" not in st.session_state:
#         st.session_state[f"actions_{selected_wave}"] = None

#     # 4. STEP 1: Problem Clustering Engine
#     st.subheader("1️⃣ Problem Clustering Engine")
#     st.write(f"Clusters complaints from the **{unhappy_count} unhappiest employees** (Score < 3.0) in this wave.")

#     if st.button("🔍 Discover Problem Clusters", type="primary", key="btn_cluster"):
#         with st.spinner("Clustering complaints and ranking by severity..."):
#             from ai_engine import cluster_unhappy_feedback
#             st.session_state[f"clusters_{selected_wave}"] = cluster_unhappy_feedback(selected_wave, gemini_key)
#             st.session_state[f"actions_{selected_wave}"] = None  # Reset downstream actions

#     # Render Clusters
#     current_clusters = st.session_state[f"clusters_{selected_wave}"]
#     if current_clusters:
#         st.markdown("#### 🚨 Discovered Problem Clusters (Ranked by Urgency)")
#         for item in current_clusters:
#             with st.container(border=True):
#                 c_title, c_badge = st.columns([3, 1])
#                 sev_color = "red" if item.get("severity") == "Critical" else "orange"
#                 c_title.markdown(f"**Rank #{item.get('rank')}: {item.get('cluster_title')}**")
#                 c_badge.markdown(f"**Severity:** :{sev_color}[{item.get('severity')}]")
                
#                 st.write(f"📌 **Core Issue:** {item.get('summary')}")
#                 st.caption(f"📊 **Impact:** {item.get('affected_ratio')} | 💬 *\"{item.get('sample_quote')}\"*")

#         st.divider()

#         # 5. STEP 2: Prescribe Actions (Combines Clusters + Low Scores < 3.5)
#         st.subheader("2️⃣ Prescribe Accountable Actions")
#         st.write("Generates concrete fixes for both the **discovered clusters** and the **scores below 3.5**.")

#         if st.button("📋 Generate Targeted Action Plan", key="btn_pulse_actions"):
#             with st.spinner("Generating targeted action cards with assigned owners..."):
#                 from ai_engine import generate_actions_for_pulse_clusters
#                 st.session_state[f"actions_{selected_wave}"] = generate_actions_for_pulse_clusters(
#                     current_clusters, low_scores, selected_wave, gemini_key
#                 )

#         # Render Actions
#         current_actions = st.session_state[f"actions_{selected_wave}"]
#         if current_actions:
#             st.markdown("#### ✅ Prescribed Action Cards (Fed directly into Tab 3's Tracker)")
#             for act in current_actions:
#                 with st.container(border=True):
#                     st.markdown(f"##### 🎯 Target: {act.get('target')}")
#                     st.markdown(f"**Action Step:** {act.get('action')}")
                    
#                     a_col1, a_col2 = st.columns(2)
#                     a_col1.caption(f"👤 **Accountable Owner:** **{act.get('owner')}**")
#                     a_col2.caption(f"📈 **Target KPI:** `{act.get('target_metric')}`")

                    
# # ==========================================
# # TAB 3: TREND & ACTION IMPACT (SYNCHRONIZED LOOP)
# # ==========================================
# with tab3:
#     st.header("📈 Survey 1 vs. Survey 2: The Decision Loop")
#     st.caption("Tracking how specific management actions impacted scores and whether Survey 1's problem clusters were resolved or are still active.")

#     from ai_engine import evaluate_action_impact_and_clusters
#     report = evaluate_action_impact_and_clusters(gemini_key)

#     # 1. Multi-Metric Comparison Chart (All scores from Survey 1 to Survey 2)
#     st.subheader("1️⃣ Score Movements (Survey 1 ➡️ Survey 2)")
    
#     chart_data = pd.DataFrame({
#         "Survey Wave": ["Survey 1 (Baseline)", "Survey 2 (Follow-up)"] * 5,
#         "Metric": [
#             "Tools & Access", "Tools & Access",
#             "Workload", "Workload",
#             "Manager Support", "Manager Support",
#             "Career Growth", "Career Growth",
#             "Engagement Score", "Engagement Score"
#         ],
#         "Score": [
#             2.1, 4.0,   # Tools & Access (+1.90)
#             1.8, 1.5,   # Workload (-0.30)
#             2.3, 2.5,   # Manager Support (+0.20)
#             2.9, 3.0,   # Career Growth (+0.10)
#             2.4, 3.1    # Engagement Score (+0.70)
#         ]
#     })
    
#     fig_sync = px.line(
#         chart_data, 
#         x="Survey Wave", 
#         y="Score", 
#         color="Metric", 
#         markers=True,
#         title="Metric Trajectory Across Waves (1.0 to 5.0 Scale)"
#     )
#     fig_sync.update_yaxes(range=[1.0, 5.0])
#     st.plotly_chart(fig_sync, use_container_width=True)

#     # 2. Score Delta Summary Cards
#     d1, d2, d3, d4 = st.columns(4)
#     d1.metric("Tools & Access", "4.0 / 5.0", delta="+1.90 (Lift)", delta_color="normal")
#     d2.metric("Workload", "1.5 / 5.0", delta="-0.30 (Drop)", delta_color="inverse")
#     d3.metric("Manager Support", "2.5 / 5.0", delta="+0.20 (Minor Lift)", delta_color="normal")
#     d4.metric("Engagement Score", "3.1 / 5.0", delta="+0.70 (Recovering)", delta_color="normal")

#     st.divider()

#     # 3. Two-Column Deep Dive: Clusters vs. Actions Taken
#     col_clusters, col_actions = st.columns([1, 1])

#     # Left Column: Problem Clusters in Survey 1 vs Survey 2
#     with col_clusters:
#         st.subheader("2️⃣ Cluster Survival Tracker")
#         st.write("Did the complaints identified in Survey 1 disappear or persist in Survey 2?")
        
#         for cl in report["cluster_comparison"]:
#             with st.container(border=True):
#                 status_color = "green" if cl["status"] == "Resolved" else "red"
#                 st.markdown(f"**{cl['cluster_name']}**")
#                 st.markdown(f"**Status:** :{status_color}[**{cl['status']}**]")
#                 st.caption(f"📊 {cl['evidence']}")

#     # Right Column: Management Actions & Attributed Verdicts
#     with col_actions:
#         st.subheader("3️⃣ Action Accountability & ROI")
#         st.write("Which actions succeeded, which failed, and who is responsible?")
        
#         for act in report["actions_verdict"]:
#             with st.container(border=True):
#                 v = act["verdict"]
#                 v_color = "green" if v == "Effective" else ("red" if v == "Ineffective" else "orange")
                
#                 h1, h2 = st.columns([3, 1])
#                 h1.markdown(f"**Action:** {act['action']}")
#                 h2.markdown(f":{v_color}[**{v}**]")
                
#                 c1, c2 = st.columns(2)
#                 c1.caption(f"🎯 **Target:** {act['target_cluster']}")
#                 c2.caption(f"👤 **Owner:** **{act['owner']}**")
                
#                 st.write(f"💡 *{act['reasoning']}*")



# # ==========================================
# # TAB 4: LEAVERS & FLIGHT RISK RADAR
# # ==========================================
# with tab4:
#     st.header("🚨 Retention & Predictive Flight Risk Radar")
#     st.caption("Inspect verified exit survey data across years, identify macro retention trends, and intercept active flight risks using vector similarity.")

#     # 1. Year Filter & Primary Exit Reasons
#     col_yr, col_empty = st.columns([1, 2])
#     selected_year = col_yr.selectbox("📅 Select Exit Year to Analyze", ["2026", "2025", "2024"], index=0)

#     # Bar chart for exit reasons tailored to year
#     st.subheader(f"1️⃣ Primary Exit Reasons ({selected_year})")
    
#     mock_exit_reasons = {
#         "2026": {"Workload & Burnout": 23, "Manager Relationship": 14, "Career Opportunity": 10, "Tools & Access": 8},
#         "2025": {"Career Opportunity": 20, "Certification Deficit": 14, "Manager Relationship": 10, "Compensation": 6},
#         "2024": {"Culture / Team Fit": 18, "Manager Relationship": 15, "Compensation": 10, "Role Clarity": 7}
#     }
    
#     df_reasons = pd.DataFrame(
#         list(mock_exit_reasons[selected_year].items()), 
#         columns=["Primary Reason", "Number of Leavers"]
#     )
    
#     fig_reasons = px.bar(
#         df_reasons, 
#         x="Primary Reason", 
#         y="Number of Leavers", 
#         color="Number of Leavers",
#         color_continuous_scale="Reds",
#         title=f"Distribution of Resignation Drivers ({selected_year})"
#     )
#     st.plotly_chart(fig_reasons, use_container_width=True)

#     st.divider()

#     # 2. Top 3 Problem Clusters via Vector Similarity + Prescribed Actions
#     st.subheader(f"2️⃣ Top 3 Exit Problem Clusters ({selected_year})")
#     st.write(f"Unsupervised Vector Clustering of exit comments in **{selected_year}** synthesized into root causes and recommended actions:")

#     from ai_engine import get_exit_clusters_by_year, get_multi_year_retention_trends, find_flight_risks_mock
#     clusters = get_exit_clusters_by_year(selected_year, gemini_key)

#     for item in clusters:
#         with st.container(border=True):
#             h1, h2 = st.columns([3, 1])
#             h1.markdown(f"**Rank #{item['rank']}: {item['cluster']}**")
#             h2.caption(f"📊 `{item['frequency']}`")
            
#             st.write(f"🔍 **Root Cause:** {item['description']}")
            
#             c1, c2 = st.columns([3, 1])
#             c1.info(f"💡 **Recommended Action:** {item['action']}")
#             c2.caption(f"👤 **Owner:** **{item['owner']}**")

#     st.divider()

#     # 3. Macro Multi-Year Trend Analysis (All Years)
#     st.subheader("3️⃣ Multi-Year Macro Retention Trends")
#     st.write("Compare systemic patterns across 2024, 2025, and 2026 to see what has improved vs. what is chronic.")

#     if st.button("📊 Analyze Multi-Year Trend (2024 - 2026)", key="btn_multi_year"):
#         trends = get_multi_year_retention_trends(gemini_key)
        
#         col_chronic, col_resolved = st.columns(2)
        
#         # Column A: Chronic Issues
#         with col_chronic:
#             st.markdown("#### 🔴 Chronic Issues (Exist in All Years)")
#             for ch in trends["chronic_issues"]:
#                 with st.container(border=True):
#                     st.markdown(f"**{ch['issue']}**")
#                     st.markdown(f":red[**{ch['status']}**]")
#                     st.caption(f"⚠️ {ch['impact']}")
#                     st.write(f"📌 *{ch['insight']}*")

#         # Column B: Resolved / Reduced Issues
#         with col_resolved:
#             st.markdown("#### 🟢 Resolved or Reduced Issues")
#             for res in trends["resolved_issues"]:
#                 with st.container(border=True):
#                     st.markdown(f"**{res['issue']}**")
#                     st.markdown(f":green[**{res['status']}**]")
#                     st.caption(f"📉 {res['evidence']}")
#                     st.write(f"✅ *{res['why']}*")

#     st.divider()

#     # 4. Predictive Flight Risk Radar (Vector Matching Active vs. Leavers)
#     st.subheader("4️⃣ Predictive Flight Risk Radar (Active Employees)")
#     st.write("Scans active pulse survey comments against historical exit vectors. Flags high-risk employees before they submit resignations.")

#     if st.button("🔍 Scan Active Workforce for Flight Risks", type="primary", key="btn_scan_risks"):
#         risks = find_flight_risks_mock(f_pulse, f_exit)
        
#         st.error(f"🚨 Identified **{len(risks)} Active Employees** exhibiting linguistic similarity to past leavers:")
        
#         for r in risks:
#             with st.container(border=True):
#                 top_col1, top_col2, top_col3 = st.columns([2, 1, 1])
#                 top_col1.markdown(f"👤 **Employee ID:** `{r['employee_id']}` ({r['division']} - {r['location']})")
#                 top_col2.caption(f"⏳ **Tenure:** {r['tenure_months']} months")
#                 top_col3.markdown(f"🔥 **Vector Match:** :red[**{r['similarity_score']}%**]")

#                 st.markdown(f"**Matched Exit Theme:** `{r['matched_exit_theme']}`")
#                 st.caption(f"💬 *Active Comment:* \"{r['active_comment']}\"")
                
#                 st.warning(f"⚡ **Recommended Intervention:** {r['recommended_intervention']}")

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from data_loader import load_data
from ai_engine import (
    generate_structured_actions,
    cluster_unhappy_feedback,
    generate_actions_for_pulse_clusters,
    evaluate_action_impact_and_clusters,
    get_exit_clusters_by_year,
    get_multi_year_retention_trends,
    find_flight_risks_mock
)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RetainAI | Glocomp Systems",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Ensure your base64 loader is at the top of app.py
# import base64
# import os
# import streamlit as st

# def get_image_base64(path):
#     if os.path.exists(path):
#         with open(path, "rb") as f:
#             return base64.b64encode(f.read()).decode()
#     return None

# icon_b64 = get_image_base64("glocomp_icon.png")
# logo_b64 = get_image_base64("glocomp_logo.png")

# # --- CUSTOM ENTERPRISE CSS ---
# st.markdown(f"""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

#     html, body, [class*="css"] {{
#         font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
#     }}

#     /* Light, clean base canvas background */
#     .stApp {{
#         background-color: #F8FAFC;
#     }}

#     /* Subtle Icon Watermark Background */
#     .stApp::before {{
#         content: "";
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100vw;
#         height: 100vh;
#         background-image: url("data:image/png;base64,{icon_b64 if icon_b64 else ''}");
#         background-repeat: no-repeat;
#         background-position: 85% 85%; /* Fades cleanly into the bottom-right workspace background */
#         background-size: 550px;
#         opacity: 0.035; /* Faded to keep text perfectly legible */
#         pointer-events: none;
#         z-index: -1;
#     }}

#     /* Top Navigation Banner styling */
#     .brand-header {{
#         display: flex;
#         align-items: center;
#         justify-content: space-between;
#         background: #FFFFFF;
#         padding: 1.25rem 2rem;
#         border-radius: 16px;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
#         border: 1px solid #E2E8F0;
#         margin-bottom: 1.75rem;
#     }}
#     .brand-title {{
#         font-size: 1.6rem;
#         font-weight: 800;
#         color: #0F172A;
#         letter-spacing: -0.02em;
#         margin: 0;
#     }}
#     .brand-sub {{
#         font-size: 0.85rem;
#         color: #64748B;
#         margin: 0.15rem 0 0 0;
#         font-weight: 500;
#     }}
#     .brand-badge {{
#         background: #FFF7ED;
#         color: #EA580C;
#         border: 1px solid #FFEDD5;
#         padding: 6px 14px;
#         border-radius: 9999px;
#         font-weight: 700;
#         font-size: 0.78rem;
#         text-transform: uppercase;
#         letter-spacing: 0.05em;
#     }}

#     /* KPI Metric Cards styling */
#     div[data-testid="stMetric"] {{
#         background: #FFFFFF;
#         border: 1px solid #E2E8F0;
#         border-radius: 14px;
#         padding: 1rem 1.25rem;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.04);
#     }}
    
#     /* (The rest of your CSS stays the same) */
# </style>
# """, unsafe_allow_html=True)
# --- CUSTOM ENTERPRISE CSS ---
# st.markdown("""
# <style>
#     /* Google Fonts */
#     @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

#     html, body, [class*="css"] {
#         font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
#     }

#     /* Background tone */
#     .stApp {
#         background-color: #F8FAFC;
#     }

#     /* Top Navigation Banner */
#     .brand-header {
#         display: flex;
#         align-items: center;
#         justify-content: space-between;
#         background: #FFFFFF;
#         padding: 1.25rem 2rem;
#         border-radius: 16px;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
#         border: 1px solid #E2E8F0;
#         margin-bottom: 1.75rem;
#     }
#     .brand-title {
#         font-size: 1.6rem;
#         font-weight: 800;
#         color: #0F172A;
#         letter-spacing: -0.02em;
#         margin: 0;
#     }
#     .brand-sub {
#         font-size: 0.85rem;
#         color: #64748B;
#         margin: 0.15rem 0 0 0;
#         font-weight: 500;
#     }
#     .brand-badge {
#         background: #FFF7ED;
#         color: #EA580C;
#         border: 1px solid #FFEDD5;
#         padding: 6px 14px;
#         border-radius: 9999px;
#         font-weight: 700;
#         font-size: 0.78rem;
#         text-transform: uppercase;
#         letter-spacing: 0.05em;
#     }

#     /* KPI Metric Cards */
#     div[data-testid="stMetric"] {
#         background: #FFFFFF;
#         border: 1px solid #E2E8F0;
#         border-radius: 14px;
#         padding: 1rem 1.25rem;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.04);
#     }
#     div[data-testid="stMetricLabel"] p {
#         font-size: 0.82rem !important;
#         font-weight: 600 !important;
#         color: #64748B !important;
#         text-transform: uppercase;
#         letter-spacing: 0.04em;
#     }
#     div[data-testid="stMetricValue"] div {
#         font-size: 1.85rem !important;
#         font-weight: 800 !important;
#         color: #0F172A !important;
#     }

#     /* Tab bar styling */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#         background-color: #E2E8F0;
#         padding: 6px;
#         border-radius: 12px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 8px;
#         padding: 10px 20px;
#         font-weight: 600;
#         color: #475569;
#         background: transparent;
#         border: none !important;
#         transition: all 0.2s ease;
#     }
#     .stTabs [aria-selected="true"] {
#         background: #FFFFFF !important;
#         color: #F36F21 !important;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.1);
#         font-weight: 700;
#     }

#     /* Custom Content Card Wrapper */
#     .saas-card {
#         background: #FFFFFF;
#         border: 1px solid #E2E8F0;
#         border-radius: 14px;
#         padding: 1.25rem 1.5rem;
#         margin-bottom: 1rem;
#         box-shadow: 0 1px 2px rgba(0,0,0,0.03);
#     }
#     .saas-card-danger {
#         border-left: 5px solid #EF4444;
#     }
#     .saas-card-warning {
#         border-left: 5px solid #F59E0B;
#     }
#     .saas-card-success {
#         border-left: 5px solid #10B981;
#     }
#     .saas-card-brand {
#         border-left: 5px solid #F36F21;
#     }

#     /* Buttons */
#     .stButton > button {
#         border-radius: 10px;
#         font-weight: 600;
#         padding: 0.5rem 1.25rem;
#         transition: all 0.2s;
#     }
#     .stButton > button[kind="primary"] {
#         background-color: #F36F21;
#         border: none;
#     }
#     .stButton > button[kind="primary"]:hover {
#         background-color: #D95610;
#         box-shadow: 0 4px 12px rgba(243, 111, 33, 0.25);
#     }

#     /* Plotly chart container cards */
#     .plot-container {
#         background: #FFFFFF;
#         border: 1px solid #E2E8F0;
#         border-radius: 14px;
#         padding: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)
import base64
import os
import streamlit as st

import base64
import os
import streamlit as st
import plotly.express as px
import pandas as pd

# --- HELPER: BASE64 LOADER ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

icon_b64 = get_image_base64("glocomp_icon.png")
logo_b64 = get_image_base64("glocomp_logo.png")

# --- EXECUTIVE RICH SLATE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #E2E8F0;
    }

    /* 
       EXECUTIVE DEEP CANVAS:
       Layered Dark Slate (#0B0F17) with ambient Glocomp Orange & Indigo mesh lighting
    */
    [data-testid="stAppViewContainer"] {
        background-color: #0B0F17 !important;
        background-image: 
            radial-gradient(at 90% 10%, rgba(243, 111, 33, 0.15) 0px, transparent 55%),
            radial-gradient(at 10% 90%, rgba(30, 58, 138, 0.18) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(17, 24, 39, 0.8) 0px, transparent 100%) !important;
        background-attachment: fixed !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0E131F !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Top Sticky Brand Bar */
    .brand-header-glass {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 1.1rem 1.75rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(21, 28, 40, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] div {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #F8FAFC !important;
    }

    /* Segmented Tab Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(17, 24, 39, 0.8) !important;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: 600;
        color: #94A3B8;
        background: transparent;
        border: none !important;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #F36F21 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(243, 111, 33, 0.35) !important;
        font-weight: 700;
    }

    /* SaaS Dark Cards */
    .saas-card {
        background: rgba(21, 28, 40, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .saas-card-danger { border-left: 4px solid #EF4444; }
    .saas-card-warning { border-left: 4px solid #F59E0B; }
    .saas-card-success { border-left: 4px solid #10B981; }
    .saas-card-brand { border-left: 4px solid #F36F21; }

    /* Buttons */
    .stButton > button[kind="primary"] {
        background: #F36F21 !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(243, 111, 33, 0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #D95610 !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Helper function to style Plotly charts consistently
def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155"),
        title_font=dict(size=15, color="#0F172A", family="Plus Jakarta Sans"),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
        yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig
# --- TOP NAVBAR WITH GLOCOMP BRANDING ---
icon_tag = (
    f'<img src="data:image/png;base64,{icon_b64}" style="width: 44px; height: 44px; border-radius: 50%; box-shadow: 0 2px 10px rgba(0,0,0,0.4); object-fit: contain;">'
    if icon_b64 else '<div style="width:80px; height:80px; border-radius:50%; background:#1E293B; color:#F36F21; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:20px;">G</div>'
)

st.markdown(f"""
<div class="brand-header-glass">
    <div style="display: flex; align-items: center; gap: 16px;">
        {icon_tag}
        <div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <h1 style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC; margin: 0; letter-spacing: -0.02em;">
                    RetainAI
                </h1>
                <span style="background: rgba(243, 111, 33, 0.18); color: #FB923C; border: 1px solid rgba(243, 111, 33, 0.3); font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; letter-spacing: 0.05em;">
                    GLOCOMP ENTERPRISE
                </span>
            </div>
            <p style="margin: 3px 0 0 0; font-size: 0.83rem; color: #94A3B8; font-weight: 500;">
                Glocomp Systems (M) Sdn Bhd • People Operations & Predictive Retention Radar
            </p>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25); color: #34D399; padding: 6px 14px; border-radius: 9999px; font-weight: 700; font-size: 0.76rem; text-transform: uppercase;">
            ● Pulse Loop Active
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1"),
        title_font=dict(size=15, color="#F8FAFC", family="Plus Jakarta Sans"),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", zerolinecolor="rgba(255, 255, 255, 0.1)"),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", zerolinecolor="rgba(255, 255, 255, 0.1)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig
# --- TOP NAVIGATION BRAND BANNER ---
st.markdown("""
<div class="brand-header">
    <div style="display: flex; align-items: center; gap: 18px;">
        <div style="background: #0F172A; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #FA8223; font-size: 26px; font-weight: 900;">
            🌊
        </div>
        <div>
            <h1 class="brand-title">RetainAI Enterprise</h1>
            <p class="brand-sub">Glocomp Systems (M) Sdn Bhd • People Analytics & Flight Risk Radar</p>
        </div>
    </div>
    <div class="brand-badge">
        ● HR Live Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
employees, onboarding, pulse, exit_surv, actions = load_data()

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("glocomp_logo.png"):
        st.image("glocomp_logo.png", use_container_width=True)
    elif os.path.exists("glocomp_icon.png"):
        st.image("glocomp_icon.png", width=70)
        st.markdown("### **Glocomp Systems**")
    else:
        st.markdown("### 🏢 **Glocomp Systems**")

    st.caption("Partnership • Technology • Innovation")
    st.divider()

    st.subheader("🔑 AI Credentials")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Enter Google AI Studio Key")

    st.divider()
    st.subheader("🎯 Workforce Segment")
    selected_location = st.selectbox("Location", ["All"] + sorted(list(employees['location'].unique())))
    selected_division = st.selectbox("Division", ["All"] + sorted(list(employees['division'].unique())))
    
    st.info("💡 **Executive Demo Mode**: Filters apply dynamically to onboarding, pulse, and exit vectors.")

# Filter Data
def filter_data(df):
    if selected_location != "All" and 'location' in df.columns:
        df = df[df['location'] == selected_location]
    if selected_division != "All" and 'division' in df.columns:
        df = df[df['division'] == selected_division]
    return df

f_onboarding = filter_data(onboarding)
f_pulse = filter_data(pulse)
f_exit = filter_data(exit_surv)

# --- 4 TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 Onboarding Experience",
    "🌊 Pulse Wave Analyzer",
    "📈 Impact & Decision Loop",
    "🚨 Leavers & Flight Radar"
])

# ==========================================
# TAB 1: ONBOARDING HUB
# ==========================================
with tab1:
    st.subheader("New Joiner Experience & Day 1-90 Health")
    st.caption("Identify onboarding friction points before they transition into first-year attrition.")

    # High-level KPIs
    col1, col2, col3, col4 = st.columns(4)
    avg_clarity = f_onboarding['role_clarity'].mean() if not f_onboarding.empty else 0
    avg_tools = f_onboarding['tools_access'].mean() if not f_onboarding.empty else 0
    avg_support = f_onboarding['manager_support'].mean() if not f_onboarding.empty else 0
    low_scorers = f_onboarding[f_onboarding['overall_score'] < 3.0] if not f_onboarding.empty else pd.DataFrame()
    struggle_rate = (len(low_scorers) / len(f_onboarding) * 100) if len(f_onboarding) > 0 else 0

    col1.metric("Role Clarity", f"{avg_clarity:.1f} / 5.0")
    col2.metric("Tools & Equipment Access", f"{avg_tools:.1f} / 5.0")
    col3.metric("Manager Enablement", f"{avg_support:.1f} / 5.0")
    col4.metric("At-Risk Joiners (<3.0)", f"{len(low_scorers)} ({struggle_rate:.0f}%)", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Prescription Section
    st.markdown("#### ⚡ AI Synthesis: Top Bottlenecks & Interventions")
    st.caption("Synthesizes qualitative feedback from new joiners rating under 3.0, mapping root cause to owners.")

    if st.button("✨ Run Onboarding Diagnosis & Action Engine", type="primary", key="btn_onboard_ai"):
        if low_scorers.empty:
            st.success("🎉 No onboarding bottlenecks found (< 3.0) for this segment.")
        else:
            with st.spinner("Analyzing feedback vectors and assigning accountable leaders..."):
                feedback_sample = low_scorers[['division', 'location', 'overall_score', 'comment']].dropna().head(12).to_dict(orient='records')
                recommendations = generate_structured_actions(feedback_sample, gemini_key)

                if recommendations:
                    for idx, item in enumerate(recommendations, 1):
                        sev_class = "saas-card-danger" if item.get("severity") == "Critical" else "saas-card-warning"
                        sev_badge_color = "#DC2626" if item.get("severity") == "Critical" else "#D97706"

                        st.markdown(f"""
                        <div class="saas-card {sev_class}">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">
                                    #{idx}: {item.get('problem', 'Identified Issue')}
                                </div>
                                <span style="background: {sev_badge_color}1A; color: {sev_badge_color}; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 6px;">
                                    {item.get('severity', 'High')} Priority
                                </span>
                            </div>
                            <div style="display: flex; gap: 24px; margin: 10px 0 14px 0; font-size: 0.85rem; color: #64748B;">
                                <span>🏢 <b>Division:</b> {item.get('department', 'All')}</span>
                                <span>📍 <b>Location:</b> {item.get('location', 'All')}</span>
                                <span>👤 <b>Accountable Lead:</b> <strong style="color: #64748B;">{item.get('owner', 'HR Lead')}</strong></span>
                            </div>
                            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px 16px; border-radius: 8px;">
                                <strong style="color: #F36F21; font-size: 0.85rem; text-transform: uppercase;">Prescribed Intervention:</strong>
                                <p style="margin: 4px 0 0 0; color: #334155; font-size: 0.92rem;">{item.get('action', 'No action provided.')}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Failed to generate response. Check your API key.")

    with st.expander("🔍 View Raw Unfiltered Responses (Overall Score < 3.0)"):
        st.dataframe(
            low_scorers[['employee_id', 'division', 'location', 'overall_score','manager_support','role_clarity', 'tools_access', 'comment']],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# TAB 2: WAVE ANALYZER
# ==========================================
with tab2:
    st.subheader("Pulse Wave Diagnostic Engine")
    st.caption("Inspect individual survey waves, flag underperforming score thresholds, and generate targeted fixes.")

    col_pick, col_spacer = st.columns([1, 2])
    selected_wave = col_pick.selectbox("Select Survey Wave", ["Survey 1 (2026-Q1_1)", "Survey 2 (2026-Q1_2)"])

    if "1" in selected_wave:
        scores = {"Overall Engagement": 2.4, "Workload Stress": 1.8, "Tools & Access": 2.1, "Manager Support": 2.3, "Career Growth": 2.9}
        unhappy_count, total_respondents = 45, 320
    else:
        scores = {"Overall Engagement": 3.1, "Workload Stress": 1.5, "Tools & Access": 4.0, "Manager Support": 2.5, "Career Growth": 3.0}
        unhappy_count, total_respondents = 38, 315

    # Metrics Bar
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Engagement", f"{scores['Overall Engagement']:.1f}")
    m2.metric("Workload", f"{scores['Workload Stress']:.1f}")
    m3.metric("Tools & Access", f"{scores['Tools & Access']:.1f}")
    m4.metric("Manager Support", f"{scores['Manager Support']:.1f}")
    m5.metric("Career Growth", f"{scores['Career Growth']:.1f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Watchlist
    low_scores = {k: v for k, v in scores.items() if v < 3.5}
    if low_scores:
        st.markdown("##### ⚠️ Sub-threshold Warning Dimensions (< 3.5 / 5.0)")
        w_cols = st.columns(len(low_scores))
        for idx, (dim, val) in enumerate(low_scores.items()):
            badge_bg = "#FEF2F2" if val < 2.0 else "#FFFBEB"
            badge_fg = "#DC2626" if val < 2.0 else "#D97706"
            with w_cols[idx]:
                st.markdown(f"""
                <div style="background: {badge_bg}; border: 1px solid {badge_fg}40; padding: 12px; border-radius: 10px;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: {badge_fg}; text-transform: uppercase;">{dim}</div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #0F172A;">{val:.1f} <span style="font-size: 0.8rem; font-weight: 500; color: #64748B;">/ 5.0</span></div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if f"clusters_{selected_wave}" not in st.session_state:
        st.session_state[f"clusters_{selected_wave}"] = None
    if f"actions_{selected_wave}" not in st.session_state:
        st.session_state[f"actions_{selected_wave}"] = None

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔍 Step 1: Discover Problem Clusters", type="primary", use_container_width=True):
            with st.spinner("Clustering complaints..."):
                st.session_state[f"clusters_{selected_wave}"] = cluster_unhappy_feedback(selected_wave, gemini_key)
                st.session_state[f"actions_{selected_wave}"] = None

    current_clusters = st.session_state[f"clusters_{selected_wave}"]
    if current_clusters:
        st.markdown("#### 🚨 Identified Complaint Clusters")
        for item in current_clusters:
            st.markdown(f"""
            <div class="saas-card saas-card-danger">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="font-size: 1.05rem; color: #FFFFFF;">#{item.get('rank')}: {item.get('cluster_title')}</strong>
<span style="background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid #EF4444; padding: 3px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 800;">{item.get('severity')}</span>
                </div>
                <p style="margin: 8px 0; color: #FFFFFF;">{item.get('summary')}</p>
                <div style="font-size: 0.82rem; color: #64748B;">
                    📊 Impact: <b>{item.get('affected_ratio')}</b> • 💬 <i>"{item.get('sample_quote')}"</i>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_btn2:
            if st.button("📋 Step 2: Prescribe Accountable Actions", use_container_width=True):
                with st.spinner("Assigning accountable fixes..."):
                    st.session_state[f"actions_{selected_wave}"] = generate_actions_for_pulse_clusters(
                        current_clusters, low_scores, selected_wave, gemini_key
                    )

        current_actions = st.session_state[f"actions_{selected_wave}"]
        if current_actions:
            st.markdown("#### ✅ Prescribed Action Plans (Dispatched to Tab 3 Tracker)")
            for act in current_actions:
                st.markdown(f"""
                <div class="saas-card saas-card-brand">
                    <strong style="color: #F36F21; font-size: 0.95rem;">🎯 Target Issue: {act.get('target')}</strong>
                    <p style="margin: 6px 0; color: #FFFFFF; font-weight: 600;">{act.get('action')}</p>
                    <div style="display: flex; gap: 24px; font-size: 0.85rem; color: #64748B; margin-top: 6px;">
                        <span>👤 Owner: <b>{act.get('owner')}</b></span>
                        <span>📈 KPI Target: <code>{act.get('target_metric')}</code></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 3: TREND & ACTION IMPACT
# ==========================================
with tab3:
    st.subheader("The Action-Loop: Survey 1 ➡️ Survey 2 Trajectory")
    st.caption("Measure whether leadership interventions actually moved the needle or if complaints simply shifted.")

    report = evaluate_action_impact_and_clusters(gemini_key)

    # Clean Chart
    chart_data = pd.DataFrame({
        "Survey Wave": ["Survey 1 (Baseline)", "Survey 2 (Follow-up)"] * 5,
        "Metric": [
            "Tools & Access", "Tools & Access",
            "Workload", "Workload",
            "Manager Support", "Manager Support",
            "Career Growth", "Career Growth",
            "Engagement Score", "Engagement Score"
        ],
        "Score": [2.1, 4.0, 1.8, 1.5, 2.3, 2.5, 2.9, 3.0, 2.4, 3.1]
    })
    
    fig_sync = px.line(
        chart_data, 
        x="Survey Wave", 
        y="Score", 
        color="Metric", 
        markers=True,
        color_discrete_sequence=["#F36F21", "#DC2626", "#2563EB", "#059669", "#7C3AED"]
    )
    fig_sync.update_yaxes(range=[1.0, 5.0])
    apply_chart_theme(fig_sync)
    st.plotly_chart(fig_sync, use_container_width=True)

    # 4 Deltas
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Tools & Equipment", "4.0 / 5.0", delta="+1.90 (Action Success)", delta_color="normal")
    d2.metric("Workload Stress", "1.5 / 5.0", delta="-0.30 (Escalating Burnout)", delta_color="inverse")
    d3.metric("Manager Enablement", "2.5 / 5.0", delta="+0.20 (Slow Progress)", delta_color="normal")
    d4.metric("Overall Engagement", "3.1 / 5.0", delta="+0.70 (Recovering)", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)

    col_c, col_a = st.columns(2)
    with col_c:
        st.markdown("#### 🔍 Cluster Status (Survey 1 vs. 2)")
        for cl in report["cluster_comparison"]:
            is_res = cl["status"] == "Resolved"
            border_cls = "saas-card-success" if is_res else "saas-card-danger"
            status_badge = f'<span style="background: {"#D1FAE5" if is_res else "#FEE2E2"}; color: {"#047857" if is_res else "#B91C1C"}; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 0.75rem;">{cl["status"]}</span>'
            
            st.markdown(f"""
            <div class="saas-card {border_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #FFFFFF;">{cl['cluster_name']}</strong>
                    {status_badge}
                </div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">📊 {cl['evidence']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_a:
        st.markdown("#### ⚖️ Action Accountability Verdict")
        for act in report["actions_verdict"]:
            v = act["verdict"]
            is_eff = v == "Effective"
            b_cls = "saas-card-success" if is_eff else ("saas-card-danger" if v == "Ineffective" else "saas-card-warning")
            v_color = "#047857" if is_eff else ("#B91C1C" if v == "Ineffective" else "#B45309")
            
            st.markdown(f"""
            <div class="saas-card {b_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #FFFFFF; font-size: 0.95rem;">{act['action']}</strong>
                    <span style="color: {v_color}; font-weight: 700; font-size: 0.85rem;">{v}</span>
                </div>
                <div style="font-size: 0.82rem; color: #64748B; margin: 4px 0;">
                    Target: <b>{act['target_cluster']}</b> • Owner: <b>{act['owner']}</b>
                </div>
                <p style="margin: 6px 0 0 0; font-size: 0.88rem; color: #FFFF00;">💡 <i>{act['reasoning']}</i></p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 4: LEAVERS & FLIGHT RISK RADAR
# ==========================================
with tab4:
    st.subheader("Predictive Flight Risk Radar & Exit Analysis")
    st.caption("Cross-reference historical exit survey vectors with active sentiment to intercept flight risks before resignation.")

    col_yr, _ = st.columns([1, 2])
    selected_year = col_yr.selectbox("📅 Exit Cohort Year", ["2026", "2025", "2024"], index=0)

    mock_exit_reasons = {
        "2026": {"Workload & Burnout": 23, "Manager Relationship": 14, "Career Opportunity": 10, "Tools & Access": 8},
        "2025": {"Career Opportunity": 20, "Certification Deficit": 14, "Manager Relationship": 10, "Compensation": 6},
        "2024": {"Culture / Team Fit": 18, "Manager Relationship": 15, "Compensation": 10, "Role Clarity": 7}
    }
    
    df_reasons = pd.DataFrame(
        list(mock_exit_reasons[selected_year].items()), 
        columns=["Primary Reason", "Number of Leavers"]
    )
    
    fig_reasons = px.bar(
        df_reasons, 
        x="Primary Reason", 
        y="Number of Leavers",
        color="Number of Leavers",
        color_continuous_scale=["#FED7AA", "#F36F21", "#9A3412"],
        title=f"Resignation Drivers Distribution ({selected_year})"
    )
    apply_chart_theme(fig_reasons)
    st.plotly_chart(fig_reasons, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Active Flight Risk Radar (Vector Match)")
    st.caption("Matches semantic embeddings from active employee comments against historical exit interview vectors.")

    if st.button("🚨 Scan Active Workforce for Flight Risks", type="primary", key="btn_scan_risks"):
        risks = find_flight_risks_mock(f_pulse, f_exit)
        
        st.markdown(f"""
        <div style="background: #FEE2E2; border: 1px solid #FCA5A5; padding: 14px 18px; border-radius: 12px; margin-bottom: 16px; color: #991B1B;">
            <b>High Urgency:</b> Found <b>{len(risks)} Active Employees</b> exhibiting high linguistic match (&gt;80%) to past voluntary resignations.
        </div>
        """, unsafe_allow_html=True)

        for r in risks:
            st.markdown(f"""
            <div class="saas-card saas-card-danger">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 1.05rem; color: #FFFFFF;">👤 Employee ID: {r['employee_id']}</strong>
                        <span style="font-size: 0.85rem; color: #FFFFFF; margin-left: 8px;">({r['division']} • {r['location']})</span>
                    </div>
                    <span style="background: #DC2626; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: 800; font-size: 0.8rem;">
                        🔥 {r['similarity_score']}% Vector Match
                    </span>
                </div>
                <div style="margin: 8px 0; font-size: 0.85rem; color: #FFFFFF;">
                    Matched Historical Exit Vector: <b style="color: #FFFF00;">{r['matched_exit_theme']}</b> | Tenure: <b>{r['tenure_months']} months</b>
                </div>
                <div style="background: #F8FAFC; border-left: 3px solid #64748B; padding: 8px 12px; margin: 8px 0; font-size: 0.88rem; color: #334155; font-style: italic;">
                    "{r['active_comment']}"
                </div>
                <div style="background: #FFF7ED; border: 1px solid #FFEDD5; border-radius: 8px; padding: 10px 14px; margin-top: 10px;">
                    <b style="color: #C2410C; font-size: 0.82rem; text-transform: uppercase;">⚡ Recommended HR Intervention:</b>
                    <div style="color: #9A3412; font-size: 0.9rem; margin-top: 2px;">{r['recommended_intervention']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)