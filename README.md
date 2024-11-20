# Turing Machine NLP Simulator

This is a Python-based web application built using **Streamlit** that simulates a Turing Machine for natural language processing tasks like **tokenization**, **POS tagging**, **named entity recognition (NER)**, and **NDFA (Non-Deterministic Finite Automaton) representation**. Additionally, it allows users to create and simulate custom Turing Machines.

---

## Features

### 1. **Turing Machine NLP Simulation**
   - **Tokenization**: Splits sentences into tokens using a simulated Turing Machine.
   - **POS Tagging**: Assigns part-of-speech (POS) tags to tokens.
   - **Named Entity Recognition (NER)**: Identifies entities like persons, organizations, and locations in the text.
   - **NDFA Representation**: Displays a graphical representation of the finite automaton used during tokenization.

### 2. **Custom Turing Machine Simulation**
   - Users can define:
     - States, input symbols, and tape symbols.
     - Transition rules (state transitions based on input).
     - Start state and accept states.
   - Simulates the behavior of a Turing Machine step-by-step.
   - Displays the tape, head position, and machine state after each step.

---

## Requirements

- Python 3.7 or later
- **Python Packages**: 
  ```bash
  streamlit matplotlib networkx
