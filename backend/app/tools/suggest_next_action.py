from datetime import date, timedelta


async def execute_suggest_next_action(
    history: list | None = None,
) -> dict:
    if history and len(history) > 0:
        last_interaction = history[0]
        last_date_str = last_interaction.get('date', '')

        suggestions = [
            {'action': 'Schedule follow-up visit', 'reason': f'Last visit was on {last_date_str}. Follow up within 2 weeks.'},
            {'action': 'Share requested efficacy data', 'reason': 'Provide the clinical data the HCP requested.'},
            {'action': 'Arrange product samples delivery', 'reason': 'Ensure the HCP has samples for patient trials.'},
            {'action': 'Invite to medical education webinar', 'reason': 'Keep the HCP engaged with latest research.'},
            {'action': 'Send relevant literature', 'reason': 'Share brochures and publications on discussed products.'},
        ]
    else:
        suggestions = [
            {'action': 'Schedule introductory visit', 'reason': 'Establish initial contact with the HCP.'},
            {'action': 'Share product portfolio brochure', 'reason': 'Introduce your product range.'},
            {'action': 'Offer samples for evaluation', 'reason': 'Let the HCP try products with patients.'},
        ]

    return {
        'suggestions': suggestions,
        'note': 'Recommendations based on interaction history and standard CRM best practices.',
    }
