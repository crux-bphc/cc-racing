# CRUx CC Racing 🏎️

Welcome to **CRUx CC Racing**, a competitive AI racing simulation where members of CRUx develop and submit their own AI drivers to race on custom tracks.

https://github.com/user-attachments/assets/c252ef99-6449-426b-8f02-5c805b451cae

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/crux-bphc/cc-racing.git
cd cc-racing
```

### 2. Install Requirements

Make sure you have Python 3.9+ installed, then run:

```bash
pip install -r requirements.txt
```

### 3. Run the Game

```bash
python main.py
```

#### In-Game Controls

D: Toggle debug view to show sensor rays and checkpoints

T: Toggle the on-screen dashboard between current speed and last lap time

M: Mute music

## 🤖 How to Add a New AI

To participate, you'll need to create an AI script that controls your car's behavior.

### Step 1: Copy the Example

Create a new file in the `ai/` directory (e.g., `my_ai.py`) and use `example.py` as a starting point.

```bash
cp ai/example.py ai/my_ai.py
```

### Step 2: Tune Your Parameters

At the top of your script, set your car's stats. **These four must add up to 30:**

```python
TOP_SPEED = 3
ACCELARATION = 5
TURN_SPEED = 5
SENSOR_RANGE = 17
```

### Step 3: Write Your Logic

Define the `ai_step` function, which takes in sensor readings and current speed, and returns throttle and steering values.

Example:

```python
def ai_step(sensors, speed):
    # Your decision logic here
    return {"throttle": 1, "steering": 0}
```

### Step 4: Register Your AI in `config.py`

Add a new car entry in `config.py`:

```json
{
  "start_x": 600,
  "start_y": 120,
  "sprite": "game/assets/car_red.png",
  "color": "red",
  "ai_path": "ai/my_ai.py"
}
```

## 📡 Sensor Info

The `sensors` dictionary passed to `ai_step` contains:

- `front`: Distance to obstacle in front
- `left`: Distance to obstacle on the left
- `right`: Distance to obstacle on the right

Larger values mean more distance.

## 👥 Contributing

Feel free to fork the repo, add new features, or optimize the racing engine. PRs are welcome!
