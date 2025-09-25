import textwrap

tarina = """You wake up with a hazy memory and a piercing headache. You do not know where you are nor why.
The last thing in your mind is a faint recall of a decision you've made. You're not yet aware of this,
but your greed related to this decision has caused you your current situation.

After gathering your thoughts you realize you're in a foreign airport. A shady looking older woman 
approaches you and hands you a glowing golden dice and parts you with these words: "You've been cursed 
by the Mad Snail, for you've blundered in a way not many dare to. If you wish to be rid of this curse,
you will have to find golden balls scattered across airports in Brasil and make the right choice, hehahaahahaa."

This golden dice will be of use on your journey, good luck."  Flabbergasted by your current situation
you take one look at the golden dice, and the woman is gone. Something tells you there is truth in her
words...so, will you throw the dice? Or face the Snail?"""

# Set column width to 80 characters
wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)
# Wrap text
word_list = wrapper.wrap(text=tarina)


def haetarina():
    return word_list