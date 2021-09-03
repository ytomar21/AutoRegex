
class Stopwords:

# THE FIRST TWO SETS ARE COMMON WORDS DURING ** OVERLAP ** ACROSS DEFINITIONS OR EXAMPLES.
# THE THIRD SET IS TO PREVENT FREQUENT WORDS FROM BEING COMPARED WITH OTHER TOKENS.

    CLOSED_CLASS_WORDS = [".", ",", "THE",
    "AND", "A", "\"", "IN", "I", ":", "YOU", "IS", "TO", "OF",
    ")", "(", "IT", "FOR", "!", "?", "THAT", "ON", "WITH", "HAVE"]

# ** @ invisible * /
    STOP_WORDS = [
    "a", "am", "an", "and", "any", "as", "at", "is", "it", "its", "de", "by", "i",
    "ie", "if", "in", "of", "off", "or", "eg", "the", "too", "are", "the", "he"]

# tokens containing these words aren't compared with other tokens, because they don't add any meaning
    FREQUENT_WORDS = ["a", "am", "an", "and", "any", "as",
    "at", "are", "be", "by", "can", "did", "do", "does", "is", "it", "its", "i", "ie", "if", "in", "no",
    "or", "eg", "me", "my", "of", "off", "oh", "our", "ours", "was", "have", "has",
    "so", "she", "the", "too", "to", "they", "their", "theirs", "that", "this", "then",
    "there", "than", "up", "us", "u", "his", "her", "hers",
    "we", "with", "were", "you", "your", "yours", "'s"]

    suffixes = ["able", "ible", "eded", "ed", "en", "est", "ful", "ic", "ing", "ion",
    "tion", "ation", "ition", "ty", "ive", "ative", "itive", "less", "ly", "ment", "ness", "ous", "eous", "es", "y", "s", "or"]