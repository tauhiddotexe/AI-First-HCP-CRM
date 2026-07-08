async def execute_generate_summary(
    interaction: dict | None = None,
    history: list | None = None,
) -> dict:
    if interaction:
        summary = f"""Visit Summary

HCP: {interaction.get('hcp', 'Unknown')}
Date: {interaction.get('date', 'N/A')}
Type: {interaction.get('type', 'N/A')}
Sentiment: {interaction.get('sentiment', 'N/A')}

The representative met with the healthcare professional for a {interaction.get('type', 'meeting')}. 
The interaction was {interaction.get('sentiment', 'generally positive')}. 
Key discussion points and outcomes have been recorded in the CRM.

Status: {interaction.get('status', 'completed')}"""
    elif history:
        total = len(history)
        recent = history[0] if history else {}
        summary = f"""Interaction History Summary

Total Interactions: {total}
Last Visit: {recent.get('date', 'N/A')}
Last Type: {recent.get('type', 'N/A')}

The representative has had {total} recorded interactions. 
The most recent engagement was a {recent.get('type', 'meeting')} on {recent.get('date', 'N/A')}.
Engagement frequency and quality should be reviewed for follow-up planning."""
    else:
        summary = 'No interaction data available to generate summary.'

    return {'summary': summary}
