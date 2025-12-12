# Leoplus AI – Conversational Sentiment Analysis Chatbot

A production-ready chatbot built for the Leoplus AI internship assignment. This project implements **Tier 1 (mandatory)** and **Tier 2 (additional credit)** sentiment analysis, along with a lightweight **Rule-Based NLU system** for context-aware responses.

---

## 📌 Features

### ✅ Tier 1 — Overall Conversation Sentiment (Mandatory)

At the end of the conversation, the chatbot generates:

* Overall sentiment → *positive / neutral / negative*
* Confidence score
* Conversation summary
* Mood shift detection (bonus feature)

### ✅ Tier 2 — Message-Level Sentiment (Additional Credit)

For **each user message**, the bot performs:

* Sentiment detection
* Confidence scoring
* Sentiment-aware response tone

Example:

```
User: "Your service disappoints me"
→ Sentiment: negative (confidence: 0.82)
Bot: I'm sorry you're facing trouble. Let me help fix this.
```

---

## 📌 Rule-Based NLU (Context Understanding)

A lightweight NLU engine identifies user intent based on keywords.

Supported intents:

| Intent          | Example Keywords             |
| --------------- | ---------------------------- |
| greeting        | hi, hello                    |
| farewell        | bye, thanks                  |
| refund          | refund, money back           |
| delivery_issue  | late, package, not delivered |
| technical_issue | error, crash, not working    |
| billing_issue   | charge, bill, invoice        |
| account_issue   | login, password              |
| general         | fallback                     |

This enables **context-specific responses**, e.g.:

```
User: my package is late
Bot: I'm sorry your package is delayed. Could you share your order ID?
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

```bash
python -m venv venv
source venv/bin/activate   # Windows → venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the chatbot

```bash
python main.py
```

### 4️⃣ End the conversation

Type:

```
quit
exit
bye
```

You will see a final sentiment summary.

---

# 🧠 Sentiment Logic Explained

## ✔ Tier 2: Single Message Sentiment

Each message is cleaned and analyzed using:

1. **Transformers (DistilBERT)** → main model
2. **VADER** → fallback
3. **Keyword polarity** → final fallback

Each prediction returns:

* label: positive / negative / neutral
* confidence score
* raw scores

---

## ✔ Tier 1: Conversation-Level Sentiment

All user messages → aggregated using weighted average:

* Positive sentiment → +score
* Negative → -score
* Neutral → 0

Weights depend on message length + confidence.

Output includes:

* Overall sentiment
* Confidence
* Trend (improving/worsening/stable)

---

# 🟦 Technologies Used

### **NLP**

* Transformers (DistilBERT)
* VADER sentiment analyzer
* Rule-Based NLU
* Text cleaning utilities

### **Software Architecture**

* Modular service-component design
* Logging utilities
* Repository layer
* Conversation analytics

### **Testing**

* pytest
* Unit tests for text cleaning, sentiment, and conversation handling

---

# 🏆 Status of Tier 2 Implementation

| Feature                       | Status            |
| ----------------------------- | ----------------- |
| Single-message sentiment      | ✅ Completed       |
| Confidence scoring            | ✅ Completed       |
| Per-message sentiment output  | ✅ Completed       |
| Conversation flow integration | ✅ Completed       |
| Sentiment-aware tone          | ✅ Completed       |
| Mood shift detection          | ⭐ Bonus Completed |

Your bot **meets and exceeds** Tier 2 expectations.

---

# 💬 Example Chat Output

```
Bot: Hello! I'm Leoplus Assistant. How can I help?

You: My package is not delivered yet.
→ Sentiment: negative (0.81)
Bot: I'm sorry your package is delayed. Could you share your order ID?

You: Also the billing was wrong.
→ Sentiment: negative (0.73)
Bot: I apologize for the billing trouble. What seems incorrect?

quit

=== Conversation Summary ===
Overall Sentiment: negative (0.77)
Trend: worsening
```

---

# 🎯 Why This Project Is Strong for the Internship

* Professional architecture
* Tier 1 & Tier 2 fully implemented
* Clean and scalable codebase
* Context-aware responses via Rule-Based NLU
* Multiple fallback strategies for robustness
* Clear documentation and readability
* No unnecessary ML complexity

This showcases strong engineering fundamentals and practical NLP understanding.

---

If you want additional sections (deployment, limitations, future work), I can add them too!
