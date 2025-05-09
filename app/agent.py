from app.tools.summarizer import summarize_text
from app.tools.quiz_generator import generate_quiz

def plan_and_execute(selected_tasks, text):
    results = []
    if "Summarize Document" in selected_tasks:
        results.append("### Summary:\n" + summarize_text(text))
    if "Generate Quiz" in selected_tasks:
        results.append("### Quiz:\n" + generate_quiz(text))
    return "\n\n".join(results)