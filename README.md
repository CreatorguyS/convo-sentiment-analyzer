# LiaPlus AI – Conversational Sentiment Analysis Chatbot

A production-ready chatbot built for the **LiaPlus AI internship assignment**. This project provides:

* **Tier 1** (mandatory): Conversation-level sentiment analysis.
* **Tier 2** (bonus): Statement-level sentiment analysis.

This updated version uses **VADER Sentiment Analyzer only**, ensuring lightweight, fast, and dependency‑safe execution.

---

## 📌 Features

### ✅ Tier 1 — Overall Conversation Sentiment (Mandatory)

At the end of the interaction, the system generates:

* Overall conversation sentiment (positive / neutral / negative)
* Confidence score
* Optional mood trend (improving / worsening / stable)

### ✅ Tier 2 — Per‑Message Sentiment (Bonus)

For every user message:

* Sentiment is analyzed using **VADER**
* Confidence is computed from compound score
* Chatbot chooses a **tone‑appropriate** reply

Example:

```
User: "Your service disappoints me"
→ Sentiment: negative (confidence: 0.82)
Bot: "I’m sorry you’re facing trouble. Let me help fix this."
```

---

## 📌 Rule‑Based NLU (Context Awareness)

A small NLU classifier detects intent using keyword patterns.

| Intent          | Example Keywords             |
| --------------- | ---------------------------- |
| greeting        | hi, hello, hey               |
| farewell        | bye, thanks                  |
| refund          | refund, money back           |
| delivery_issue  | late, package, not delivered |
| technical_issue | error, crash, not working    |
| billing_issue   | bill, charge, invoice        |
| account_issue   | login, password              |
| general         | fallback                     |

This allows context‑specific replies:

```
User: "my package is late"
Bot: "I’m sorry your package is delayed. Could you share your order ID?"
```

---

## 📂 Project Structure

```
src/
├── chatbot/
│   ├── chatbot.py
│   ├── conversation_manager.py
│   ├── response_generator.py
│   └── utils.py
├── components/
│   ├── sentiment_component.py
│   ├── text_cleaner.py
│   └── intent_classifier.py
├── services/
│   ├── sentiment_service.py
│   └── conversation_service.py
├── repository/
│   └── conversation_repository.py
├── analytics/
│   └── mood_shift_detector.py
├── utils/
│   ├── logger.py
│   └── formatters.py
main.py
```

---

# 🚀 How to Run the Project

### 1️⃣ Create virtual environment

```
python -m venv venv
```

Activate it:

```
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run the chatbot (CLI)

```
python main.py
```

### 4️⃣ End the conversation with:

```
quit
exit
bye
```

---

# 🧠 Sentiment Logic Explained

## ✔ Tier 2 (Statement‑Level)

The system uses **VADER only**:

* `compound` score determines sentiment label
* Confidence = absolute value of compound

| Compound Score Range | Meaning  |
| -------------------- | -------- |
| ≥ 0.05               | Positive |
| ≤ -0.05              | Negative |
| Between              | Neutral  |

This ensures predictable, consistent behavior.

---

## ✔ Tier 1 (Conversation‑Level)

At the end:

* All message compound scores are averaged
* Higher confidence weights influence final sentiment

Also computes:

* **Trend:** improving / worsening / stable

---

# 🟦 Technologies Used

### **Core NLP**

* VADER (NLTK)
* Rule-Based NLU
* Text preprocessing utilities

### **Architecture**

* Modular components
* Service layer
* Repository layer for saving conversations
* Logging utilities

### **Testing**

* `pytest` for unit tests on:

  * Text cleaner
  * Sentiment component
  * Conversation manager

---

# 🏆 Status of Tier 2 Implementation

| Feature               | Status                          |
| --------------------- | ------------------------------- |
| Per-message sentiment | ✅ Done                          |
| Confidence scoring    | ✅ Done                          |
| Sentiment-aware tone  | ✅ Done                          |
| Mood trend analysis   | ⭐ Bonus Done                    |
| Transformers model    | ❌ Removed (now uses VADER only) |

---

# 💬 Example Chat Output

```
Bot: Hello! I'm Leoplus Assistant. How can I help?

You: My package is not delivered yet.
→ Sentiment: negative (0.81)
Bot: I’m sorry your package is delayed. Could you share your order ID?

You: Also the billing was wrong.
→ Sentiment: negative (0.73)
Bot: I apologize for the billing trouble. What seems incorrect?

quit

=== Conversation Summary ===
Overall Sentiment: negative (0.77)
Trend: worsening
```

---

# 🎯 Project characteristics

* Clean, modular, production-style architecture
* Tier 1 + Tier 2 fully satisfied
* Rule-Based NLU improves realism
* Stable sentiment system using VADER
* Clear documentation
* Lightweight (no heavy ML models needed)

---

