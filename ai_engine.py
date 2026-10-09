import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

import json
import google.generativeai as genai

def generate_structured_actions(comments_data, api_key):
    """
    Sends negative onboarding feedback with department & location context to Gemini.
    Returns structured JSON with top 3 problems and location/dept-specific actions.
    """
    if not api_key:
        # Mock fallback with realistic Glocomp ICT data if no key is provided
        return [
            {
                "problem": "Hardware & Access Provisioning Delays",
                "department": "Technology",
                "location": "Penang",
                "severity": "Critical",
                "action": "Establish a regional pre-configuration protocol so laptops and VPN credentials ship 3 days prior to Day 1.",
                "owner": "Regional IT Operations Lead"
            },
            {
                "problem": "Vague Role Expectations & KPIs",
                "department": "Sales",
                "location": "Kuala Lumpur",
                "severity": "High",
                "action": "Implement a mandatory 30-day onboarding milestone template signed off by the Sales Director during Week 1.",
                "owner": "Head of Sales"
            },
            {
                "problem": "Limited Manager Check-ins & Mentorship",
                "department": "Customer Support",
                "location": "Penang",
                "severity": "Medium",
                "action": "Assign a dedicated Senior Peer Buddy for daily 15-min syncs during the initial 2-week probation ramp-up.",
                "owner": "Support Team Lead"
            }
        ]

    prompt = f"""
    You are an expert HR Operations Strategist at Glocomp Systems, a regional ICT distributor in Malaysia.
    Analyze these low-scoring onboarding survey responses (overall_score < 3.0):
    {comments_data}

    Synthesize this feedback and extract the TOP 3 most pressing root-cause problems.
    For each problem, factor in the specific department and location context, and provide a concrete, practical solution.

    Return ONLY a valid JSON array of objects with these exact keys:
    [
      {{
        "problem": "Brief problem title",
        "department": "Most impacted department(s)",
        "location": "Most impacted location(s)",
        "severity": "Critical | High | Medium",
        "action": "Specific, practical, low-cost action to solve this",
        "owner": "Specific role responsible (e.g., IT Ops Lead, Branch Manager)"
      }}
    ]
    Do not include markdown code block formatting (like ```json), just pure JSON text.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        return json.loads(text)
    except Exception as e:
        return []
    
def generate_ai_insight(prompt, api_key):
    """Sends prompt to Gemini API. Uses a mock response if no key is provided."""
    if not api_key:
        return "⚠️ *Mock AI Response (Enter Gemini API Key in sidebar):* Implement a daily standup to improve role clarity. Schedule immediate 1-on-1s with flagged employees."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.6-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"

def get_exit_clusters_by_year(year, api_key=None):
    """
    Returns top 3 root cause clusters and prescribed actions for a specific year.
    """
    year_str = str(year)
    data_by_year = {
        "2024": [
            {
                "rank": 1,
                "cluster": "Onboarding Disconnect & Culture Fit",
                "frequency": "42% of exits (18 leavers)",
                "description": "New hires felt isolated with poor documentation during rapid post-pandemic hiring.",
                "action": "Implement standardized 90-day buddy onboarding framework.",
                "owner": "People & Culture Lead"
            },
            {
                "rank": 2,
                "cluster": "Inconsistent Manager Coaching",
                "frequency": "35% of exits (15 leavers)",
                "description": "Junior engineers cited lack of constructive 1-on-1 feedback and guidance.",
                "action": "Mandatory 'Manager as Coach' training for newly promoted Team Leads.",
                "owner": "HR Learning & Development"
            },
            {
                "rank": 3,
                "cluster": "Basic Compensation & Allowance Gaps",
                "frequency": "23% of exits (10 leavers)",
                "description": "Entry-level tech salaries fell below regional MNC competitors.",
                "action": "Conduct regional salary benchmarking across KL & Penang tech hubs.",
                "owner": "Compensation & Benefits Lead"
            }
        ],
        "2025": [
            {
                "rank": 1,
                "cluster": "Career Plateau & Stagnant Promotions",
                "frequency": "45% of exits (20 leavers)",
                "description": "Engineers felt stuck at Senior level without clear paths to Staff/Architect roles.",
                "action": "Publish dual-track technical vs managerial career ladder.",
                "owner": "VP of Technology"
            },
            {
                "rank": 2,
                "cluster": "Certification & Skills Sponsorship Deficit",
                "frequency": "32% of exits (14 leavers)",
                "description": "Staff left for companies offering paid AWS/Cisco/Azure certification vouchers.",
                "action": "Establish RM 5,000 annual upskilling budget per technical headcount.",
                "owner": "Head of Technical Enablement"
            },
            {
                "rank": 3,
                "cluster": "Manager Relationship Friction",
                "frequency": "23% of exits (10 leavers)",
                "description": "Lack of empathy regarding family leave and rigid office hour enforcement.",
                "action": "Introduce core flexible working hours (10 AM - 4 PM).",
                "owner": "Managing Director"
            }
        ],
        "2026": [
            {
                "rank": 1,
                "cluster": "Production Go-Live Burnout & Weekend On-Call",
                "frequency": "51% of exits (23 leavers)",
                "description": "Engineers quitting due to unmanaged overtime on high-stakes enterprise projects.",
                "action": "Cap consecutive weekend maintenance shifts and mandate compensatory time-off.",
                "owner": "Head of PMO & Delivery"
            },
            {
                "rank": 2,
                "cluster": "Manager Relationship & Micromanagement",
                "frequency": "31% of exits (14 leavers)",
                "description": "Supervisors focusing on ticket volume rather than quality and architectural health.",
                "action": "Implement quarterly 360-degree upward managerial reviews.",
                "owner": "HR Director"
            },
            {
                "rank": 3,
                "cluster": "Tools & Demo Environment Bottlenecks",
                "frequency": "18% of exits (8 leavers)",
                "description": "Pre-sales and post-sales engineers lacking cloud sandbox environments for client POCs.",
                "action": "Fast-track cloud sandbox resource budget for solutions engineering.",
                "owner": "IT Infrastructure Lead"
            }
        ]
    }
    return data_by_year.get(year_str, data_by_year["2026"])


def get_multi_year_retention_trends(api_key=None):
    """
    Returns multi-year macro analysis showing chronic vs solved issues.
    """
    return {
        "chronic_issues": [
            {
                "issue": "Manager Coaching & Communication Gaps",
                "status": "Chronic (Active in 2024, 2025, 2026)",
                "impact": "Accounted for >25% of exits in all three years.",
                "insight": "Technical experts are promoted to managers without adequate people-leadership training."
            },
            {
                "issue": "Compensation & Career Ladder Friction",
                "status": "Chronic (Persistent)",
                "impact": "Accounts for steady mid-level engineer departures between 18-24 months tenure.",
                "insight": "Engineers jump to foreign MNCs in KL/Penang for 20-30% pay bumps after gaining 2 years experience."
            }
        ],
        "resolved_issues": [
            {
                "issue": "Onboarding Disconnect & Culture Fit",
                "status": "Resolved / Drastically Reduced",
                "evidence": "Fell from 42% of exits in 2024 to under 8% in 2026.",
                "why": "Day-1 standardized buddy onboarding and clear documentation successfully stabilized early tenure."
            },
            {
                "issue": "Hardware & IT Access Delays",
                "status": "Resolved in 2026",
                "evidence": "Mentioned by 0 leavers in late 2026 after Day-1 automated provisioning took effect.",
                "why": "IT Operations eliminated laptop and VPN waiting periods."
            }
        ]
    }


def find_flight_risks_mock(active_df, exit_df):
    """
    Returns high-confidence flight risks cross-referencing active comments with exit vectors.
    """
    return [
        {
            "employee_id": "E0142",
            "division": "Technology",
            "location": "Kuala Lumpur",
            "tenure_months": 22,
            "similarity_score": 86.4,
            "matched_exit_theme": "Weekend Go-Live Burnout",
            "active_comment": "Pulling my third consecutive Saturday deployment. Workload is completely unsustainable right now.",
            "recommended_intervention": "Immediate 1-on-1 with Department Head; assign dedicated backup engineer for upcoming sprint."
        },
        {
            "employee_id": "E0089",
            "division": "Technology",
            "location": "Penang",
            "tenure_months": 16,
            "similarity_score": 79.1,
            "matched_exit_theme": "Manager Coaching Deficit",
            "active_comment": "No guidance on my promotion pathway and feedback from team lead is non-existent.",
            "recommended_intervention": "Schedule formal quarterly performance review and pair with a Senior Technical Mentor."
        },
        {
            "employee_id": "E0231",
            "division": "Sales",
            "location": "Kuala Lumpur",
            "tenure_months": 28,
            "similarity_score": 74.8,
            "matched_exit_theme": "Career Plateau & Comp Gap",
            "active_comment": "Reaching client quotas but territory commission structure has not been updated since last year.",
            "recommended_intervention": "Sales Director account review and commission tier evaluation."
        },
        {
            "employee_id": "E0315",
            "division": "Customer Support",
            "location": "Penang",
            "tenure_months": 11,
            "similarity_score": 71.3,
            "matched_exit_theme": "On-Call Shift Fatigue",
            "active_comment": "Constant night shifts without proper rest cycles between customer escalations.",
            "recommended_intervention": "Shift re-balancing to ensure mandatory 48-hour recovery windows."
        }
    ]

def cluster_unhappy_feedback(selected_wave, api_key=None):
    """
    Returns problem clusters strictly synchronized with Tab 3.
    Survey 1 has Cluster A (IT Tools) and Cluster B (Workload).
    Survey 2 only has Cluster B (Workload persisting; IT Tools resolved).
    """
    if not api_key:
        if "1" in str(selected_wave):  # Survey 1 (Baseline)
            return [
                {
                    "rank": 1,
                    "cluster_title": "Cluster A: Day-1 Hardware & VPN Bottlenecks",
                    "severity": "Critical",
                    "affected_ratio": "48% of unhappy cohort (38 mentions)",
                    "summary": "New hires and engineers wait up to 2 weeks for developer laptops and VPN security credentials.",
                    "sample_quote": "Cannot start client project onboarding without cloud credentials."
                },
                {
                    "rank": 2,
                    "cluster_title": "Cluster B: Client Go-Live Overtime & Weekend Deployments",
                    "severity": "Critical",
                    "affected_ratio": "52% of unhappy cohort (41 mentions)",
                    "summary": "Engineers are forced into unbuffered 60+ hour workweeks during client production launches.",
                    "sample_quote": "Workload is unmanageable; second consecutive weekend on production support."
                }
            ]
        else:  # Survey 2 (Follow-up)
            return [
                {
                    "rank": 1,
                    "cluster_title": "Cluster B: Client Go-Live Overtime & Weekend Deployments",
                    "severity": "Critical",
                    "affected_ratio": "78% of unhappy cohort (47 mentions)",
                    "summary": "Persistent project crunches. Mandatory wellness meetings added meeting fatigue without addressing deadlines.",
                    "sample_quote": "Still pulling weekend shifts, and now we have extra sync meetings to talk about stress."
                }
            ]

    # Dynamic LLM fallback if an API key is active
    prompt = f"Analyze feedback for {selected_wave} and return ranked root-cause clusters in JSON."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except:
        return []


def generate_actions_for_pulse_clusters(clusters, low_score_dimensions, selected_wave, api_key=None):
    """
    Generates targeted actions matching the interventions tracked in Tab 3,
    plus recommendations for dimensions with scores below 3.5.
    """
    if not api_key:
        if "1" in str(selected_wave):
            return [
                {
                    "target": "Cluster A: Hardware & VPN Bottlenecks (Score: 2.1)",
                    "action": "Automate Day-1 VPN & Tool Access Provisioning",
                    "owner": "IT Operations Lead",
                    "target_metric": "Lift Tools & Access score from 2.1 to > 3.8 in Survey 2."
                },
                {
                    "target": "Cluster B: Client Go-Live Overtime (Score: 1.8)",
                    "action": "Restructure Tier-2 On-Call Rotation & Deployment Buffer",
                    "owner": "Delivery & PMO Lead",
                    "target_metric": "Reduce weekend shifts and lift Workload score from 1.8 to > 2.5."
                },
                {
                    "target": "Dimension Watchlist: Manager Support (Score: 2.3)",
                    "action": "Institute bi-weekly structured 1-on-1 career mapping syncs",
                    "owner": "Engineering Managers",
                    "target_metric": "Raise Manager Support from 2.3 to > 3.0."
                }
            ]
        else:
            return [
                {
                    "target": "Cluster B: Client Go-Live Overtime (Persisting at 1.5)",
                    "action": "Immediate freeze on unbudgeted client milestones + mandatory 1:1 compensatory time off",
                    "owner": "VP of Engineering & PMO",
                    "target_metric": "Halt workload decline and recover to baseline > 2.0."
                },
                {
                    "target": "Dimension Watchlist: Manager Support (Score: 2.5)",
                    "action": "Empower team leads to re-assign sprint tickets without director-level signoff",
                    "owner": "Engineering Managers",
                    "target_metric": "Accelerate 1-on-1 coaching effectiveness."
                }
            ]

    return []

def evaluate_action_impact_and_clusters(api_key=None):
    """
    Returns the synchronized evaluation of Actions taken and Cluster persistence
    based on the exact transition from Survey 1 to Survey 2.
    """
    # Synchronized data payload
    return {
        "metrics_summary": [
            {"metric": "Tools & Access", "s1": 2.1, "s2": 4.0, "delta": "+1.90", "status": "Significant Lift"},
            {"metric": "Workload Stress", "s1": 1.8, "s2": 1.5, "delta": "-0.30", "status": "Worsened"},
            {"metric": "Manager Support", "s1": 2.3, "s2": 2.5, "delta": "+0.20", "status": "Minor Improvement"},
            {"metric": "Overall Engagement", "s1": 2.4, "s2": 3.1, "delta": "+0.70", "status": "Recovering"}
        ],
        "cluster_comparison": [
            {
                "cluster_name": "Cluster A: Day-1 Hardware & VPN Bottlenecks",
                "found_in_s1": True,
                "found_in_s2": False,
                "status": "Resolved",
                "evidence": "Mentioned by 38 employees in Survey 1. Zero mentions in Survey 2 following IT provisioning automation."
            },
            {
                "cluster_name": "Cluster B: Client Go-Live Overtime & Weekend Deployments",
                "found_in_s1": True,
                "found_in_s2": True,
                "status": "Persisting (Worsened)",
                "evidence": "Mentioned by 41 employees in Survey 1 and 47 employees in Survey 2. Workload metric declined from 1.80 to 1.50."
            }
        ],
        "actions_verdict": [
            {
                "action": "Automate Day-1 VPN & Tool Access Provisioning",
                "target_cluster": "Cluster A (IT Bottlenecks)",
                "owner": "IT Operations Lead",
                "status": "Completed",
                "verdict": "Effective",
                "reasoning": "Tools score surged by +1.90 (from 2.1 to 4.0). Completely eliminated hardware onboarding bottlenecks."
            },
            {
                "action": "Mandatory Weekly 'Wellness' Check-in Meetings",
                "target_cluster": "Cluster B (Weekend Deployments)",
                "owner": "Engineering Managers",
                "status": "Completed",
                "verdict": "Ineffective",
                "reasoning": "Workload score fell by -0.30 (from 1.8 to 1.5). Adding meetings to an already overworked delivery team worsened fatigue without reducing client deadlines."
            },
            {
                "action": "Tier-2 Deployment Rotation & On-Call Restructure",
                "target_cluster": "Cluster B (Weekend Deployments)",
                "owner": "Delivery & PMO Lead",
                "status": "In Progress (30%)",
                "verdict": "Pending Progress",
                "reasoning": "Policy is still in draft phase. True operational relief has not yet reached the engineering floor."
            }
        ]
    }