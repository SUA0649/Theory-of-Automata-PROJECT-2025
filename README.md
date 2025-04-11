# 🧠 Turing Machine Simulator for Binary Addition

A simulation of a Turing Machine that performs **binary addition** of two binary numbers separated by a delimiter (e.g., `101+011`). This project includes a **graphical user interface (GUI)** that visually represents the tape, head movement, state transitions, and final output.

---

## 📌 Features

- ✅ Simulates Turing Machine logic for binary addition
- 🧾 Takes input in format: `binary1+binary2` (e.g., `101+011`)
- 🧠 Bit-by-bit computation with carry logic
- 🎛️ GUI built using **Python Tkinter** (or PyQt)
- 📽️ Step-by-step execution and auto-run mode
- 🧾 Tape visualization with head and state display
- 🖼️ Snapshot feature to capture each computation step

---

## 🖥️ GUI Overview

- **Input Field**: Enter binary string in format `101+011`
- **Tape Display**: Visualizes the tape with symbols and head position
- **State Info**: Shows current Turing Machine state and step number
- **Control Buttons**: Start, Step, Auto Run, Pause, Reset
- **Output Section**: Displays the final binary sum

---

## 📷 Screenshots

> Add screenshots or GIFs here once GUI is built  
> Example:
> ![Tape Simulation](screenshots/tape_example.png)

---

## ⚙️ How It Works

1. User enters binary input (e.g., `101+011`) in the GUI.
2. Input is parsed and placed on an emulated Turing Machine tape.
3. Turing Machine begins in an initial state and processes the input bit by bit from right to left.
4. It simulates carry logic, head movement, and transitions between states.
5. Final sum is written on the tape and displayed in the output section.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Tkinter (pre-installed with Python) or PyQt5 (if using PyQt)

### Installation

```bash
git clone https://github.com/your-username/tm-binary-addition.git
cd tm-binary-addition
python main.py
```
---

## 🧩 Folder Structure

```
tm-binary-addition/
├── gui/                # GUI components
├── tm_engine/          # Core Turing Machine logic
├── assets/             # Snapshots, images, etc.
├── main.py             # Entry point
└── README.md           # This file
```

---

## 👥 Team Members

- **Shaheer Uddin Ahmed (23K-0649)**
- **Yahya Shaikh (23K-0718)**
- **Faizan Jawaid (23K-0688)**

---

## 📚 References

- Course: Theory of Automata – FAST NUCES Karachi
- Turing Machine Theory: Sipser, Michael – "Introduction to the Theory of Computation"
- Binary addition logic and Turing simulations (YouTube, GitHub open repos)

---

## 📜 License

This project is for academic use only. All rights reserved © 2025.

