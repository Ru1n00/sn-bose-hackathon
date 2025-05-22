from django import template

register = template.Library()

@register.filter(name='get_answer')
def get_answer(answers, quiz_id):
    """Retrieve the user's answer for a given quiz ID."""
    return answers.filter(quiz_id=quiz_id).first()