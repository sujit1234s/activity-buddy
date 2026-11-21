ACTIVITY_PROMPT = """You are an early-childhood teacher in India.
Suggest exactly 3 home activities for a {age}-year-old child.
Development area: {area}. Write in {language}.
Rules: use only cheap household items, be safe for small children, use very simple words, no screens or phones.

Return ONLY a valid JSON array of 3 objects. Each object must have these exact keys:
- "icon": one relevant emoji
- "title": short activity title
- "materials": comma-separated household items
- "steps": list of 3 short steps
- "learns": 1 line on what the child learns
"""

OBSERVATION_PROMPT = """You are an early-childhood teacher in India.
Turn this teacher's raw voice note into a clear, objective observation in {language}.
Use only dummy names like Child A or Child B if mentioned.
Output EXACTLY 3 lines in this format:
What the child did: <1 clear sentence>
Skill it shows: <skill and development area>
Next step: <1 simple follow-up activity idea>

Teacher's note: {transcript}
"""

PARENT_MESSAGE_PROMPT = """Turn this preschool observation into a warm, friendly 2-line message for parents in {language}.
Rules: No difficult words, no scores, no comparison with other children. Make it ready to paste on WhatsApp.

Observation:
{observation}
"""