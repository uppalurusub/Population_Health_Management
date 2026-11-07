import json
import re

import pandas as pd
import streamlit as st

from utils.formatters import humanize_key, format_metric_value


def _clean_markdown_text(value):
    """Normalize agent/LLM text before rendering."""
    if value is None:
        return ""

    text = str(value).strip()

    # Remove fenced JSON/markdown wrappers without destroying content.
    text = re.sub(r"^```(?:json|markdown|text)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


def _display_scalar_rows(items):
    """Display scalar dictionary values row-wise instead of metric cards."""
    for key, value in items:
        label = humanize_key(key)
        formatted_value = format_metric_value(value)

        col_label, col_value = st.columns([1, 3], vertical_alignment="top")
        with col_label:
            st.markdown(f"**{label}**")
        with col_value:
            st.write(formatted_value)

        st.divider()


def _display_interventions(interventions):
    """Render interventions as readable cards rather than a wide dataframe."""
    if not interventions:
        st.info("No interventions available.")
        return

    for index, intervention in enumerate(interventions, start=1):
        if not isinstance(intervention, dict):
            st.write(intervention)
            continue

        intervention_type = intervention.get("intervention_type", f"Intervention {index}")
        priority = intervention.get("priority", "N/A")
        recommendation = _clean_markdown_text(
            intervention.get("recommendation", "")
        )

        with st.container(border=True):
            header_col, priority_col = st.columns([4, 1], vertical_alignment="center")

            with header_col:
                st.markdown(f"### {intervention_type}")

            with priority_col:
                st.markdown("**Priority**")
                st.write(priority)

            if recommendation:
                st.markdown("**Recommendation**")
                st.markdown(recommendation)


def _display_agent_findings(findings):
    """Render each agent finding in a separate expandable section."""
    if not findings:
        st.info("No agent findings available.")
        return

    for index, finding in enumerate(findings, start=1):
        if not isinstance(finding, dict):
            st.write(finding)
            continue

        agent_name = finding.get("agent_name", f"Agent {index}")
        agent_findings = _clean_markdown_text(finding.get("findings", ""))

        with st.expander(f"🤖 {agent_name}", expanded=True):
            if not agent_findings:
                st.info("No findings returned by this agent.")
                continue

            # If an agent returns JSON text, render it cleanly when possible.
            json_candidate = agent_findings
            try:
                parsed = json.loads(json_candidate)
                st.json(parsed)
            except (json.JSONDecodeError, TypeError):
                st.markdown(agent_findings)


def display_response(data, section_name=None):
    if isinstance(data, dict):
        scalar_items = [
            (key, value)
            for key, value in data.items()
            if not isinstance(value, (dict, list))
        ]
        nested_items = [
            (key, value)
            for key, value in data.items()
            if isinstance(value, (dict, list))
        ]

        if scalar_items:
            _display_scalar_rows(scalar_items)

        for key, value in nested_items:
            normalized_key = str(key).lower()

            st.subheader(humanize_key(key))

            if normalized_key == "interventions" and isinstance(value, list):
                _display_interventions(value)

            elif normalized_key == "agent_findings" and isinstance(value, list):
                _display_agent_findings(value)

            else:
                display_response(value, section_name=normalized_key)

    elif isinstance(data, list):
        if not data:
            st.info("No data available.")

        elif section_name == "interventions":
            _display_interventions(data)

        elif section_name == "agent_findings":
            _display_agent_findings(data)

        elif isinstance(data[0], dict):
            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True,
                hide_index=True,
            )

        else:
            for item in data:
                st.write(item)

    else:
        st.write(format_metric_value(data))


def display_segment_distribution(result):
    if isinstance(result, dict):
        df = pd.DataFrame(
            result.items(),
            columns=["Segment", "Count"],
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.bar_chart(df.set_index("Segment"))

    else:
        display_response(result)
