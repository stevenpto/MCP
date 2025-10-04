"""Text summarization functionality"""

from typing import Optional
import re


class TextSummarizer:
    """Handles text summarization with extractive methods"""

    def __init__(self):
        """Initialize text summarizer"""
        self._ensure_nltk_data()

    def _ensure_nltk_data(self):
        """Ensure required NLTK data is available"""
        try:
            import nltk
            # Try to use punkt, download if not available
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords', quiet=True)
        except Exception:
            # If NLTK setup fails, we'll fall back to simple summarization
            pass

    def summarize(
        self,
        text: str,
        context: Optional[str] = None,
        max_sentences: Optional[int] = None
    ) -> dict:
        """
        Summarize text using extractive summarization.

        Args:
            text: The text to summarize
            context: Optional context to guide summarization
            max_sentences: Maximum number of sentences in summary (auto-calculated if None)

        Returns:
            Dictionary with:
                - summary: The summarized text
                - focus: Detected focus or theme (if context provided)
        """
        if not text or not text.strip():
            return {
                "summary": "",
                "focus": None
            }

        # Auto-calculate max_sentences based on text length if not provided
        if max_sentences is None:
            # Count total sentences in text
            total_sentences = len(re.split(r'[.!?]+', text))
            # Use 30% of sentences for summary, minimum 5, maximum 15
            max_sentences = max(5, min(15, int(total_sentences * 0.3)))

        try:
            # Try to use sumy for extractive summarization
            from sumy.parsers.plaintext import PlaintextParser
            from sumy.nlp.tokenizers import Tokenizer
            from sumy.summarizers.lsa import LsaSummarizer
            from sumy.nlp.stemmers import Stemmer
            from sumy.utils import get_stop_words

            # Parse text
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            stemmer = Stemmer("english")
            summarizer = LsaSummarizer(stemmer)
            summarizer.stop_words = get_stop_words("english")

            # Generate summary
            summary_sentences = summarizer(parser.document, max_sentences)
            summary = " ".join([str(sentence) for sentence in summary_sentences])

        except Exception:
            # Fallback to simple sentence extraction if sumy fails
            summary = self._simple_extractive_summary(text, max_sentences)

        # Detect focus if context is provided
        focus = None
        if context:
            focus = self._detect_focus(text, context)

        return {
            "summary": summary.strip(),
            "focus": focus
        }

    def _simple_extractive_summary(self, text: str, max_sentences: int = 5) -> str:
        """
        Simple extractive summarization by selecting first N sentences.

        Args:
            text: Text to summarize
            max_sentences: Maximum sentences to include

        Returns:
            Summary text
        """
        # Split into sentences (simple approach)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Take first N sentences
        summary_sentences = sentences[:max_sentences]
        return ". ".join(summary_sentences) + "."

    def _detect_focus(self, text: str, context: str) -> Optional[str]:
        """
        Detect focus/theme based on context keywords.

        Args:
            text: The text being summarized
            context: Context string with guidance

        Returns:
            Detected focus or None
        """
        context_lower = context.lower()
        text_lower = text.lower()

        # Common medical/document themes
        themes = {
            "prescription": ["prescription", "medication", "dose", "rx", "tablet", "pill"],
            "oct findings": ["oct", "optical coherence", "retinal", "macula", "thickness"],
            "diagnosis": ["diagnosis", "impression", "findings", "condition"],
            "patient information": ["patient", "name", "age", "gender", "dob"],
            "test results": ["results", "test", "lab", "value", "measurement"],
        }

        # Check which theme is most relevant
        for theme_name, keywords in themes.items():
            # Check if context mentions this theme
            if any(keyword in context_lower for keyword in keywords):
                # Verify theme is present in text
                if any(keyword in text_lower for keyword in keywords):
                    return theme_name.title()

        return None
