from transformers import pipeline

# Lightweight, deterministic(ish) grounded answering.
# We avoid long generative outputs by using a QA model, then fallback to templated answers.

class RAGAnswerer:
    def __init__(self):
        # DistilBERT QA is small and fast
        self.qa = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

    def answer(self, query: str, contexts: list[str]) -> str:
        context = "\n".join(contexts)[:3000]  # guard length
        try:
            if len(context.strip()) < 10:
                return "I couldn't find that in my menu or FAQs. Try asking about hours, menu items, prices, or say 'suggest a meal'."
            result = self.qa(question=query, context=context)
            text = result.get("answer", "").strip()
            if not text or text == "":  # sometimes empty
                return self._fallback(query, context)
            return text
        except Exception:
            return self._fallback(query, context)

    def _fallback(self, query: str, context: str) -> str:
        # Very simple fallback to avoid the 'repeating query' issue
        return "Here’s what I found: " + context.split(".")[0] + "."
