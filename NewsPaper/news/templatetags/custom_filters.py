from django import template
import re

with open("news/wordlist.txt", "r") as file:
    CENSORED_WORDS = file.read().splitlines()

#print(CENSORED_WORDS)


register = template.Library()


@register.filter()
def validate_comment_text(text):
   words = set(re.sub("[^\w]", " ", text).split())
   if any(censored_word in words for censored_word in CENSORED_WORDS):
      raise ValidationError(f"{censored_word} is censored!")

@register.filter()
def display_some_bad_text(text):
   text = text.replace('Fishing', 'F*****g')
   text = text.replace('ackers', '*****s')
   #postfix = ' *CENSORED'
   #return f'{text} {postfix}'
   return f'{text}'