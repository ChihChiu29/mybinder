from textblob import TextBlob


class SentimentAnalyzer(object):
  def __init__(self, txt: str):
    """Initializer.

    Args:
      txt: Text to analyze.

    """
    self._blob = TextBlob(txt)

  def GetPolarity(self) -> float:
    """Returns the polarity between -1.0 to 1.0.

    Positive number means more postive and negative means negative."""
    return self._blob.sentiment.polarity

  def GetSubjectivity(self) -> float:
    """Returns subjectivity between 0.0 to 1.0.

    Where 0 is very objective.
    """
    return self._blob.sentiment.subjectivity
