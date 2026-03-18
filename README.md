# Daily Brief in Melaka

### dailybrief.py
A Python script that fetches the top 3 news headlines by category in Malaysia using the NewsAPI, fetches current temperature and weather in Melaka using OpenMeteo weather API, prints a clean daily brief to the console and saves it to a timestamped txt file.

---

## What the scripts does

- Prompts the user to choose a news category at runtime
- Validates the input and re-prompts if an invalid category is entered
- Calls the NewsAPI with the API key passed securely in the `Authorization` header and designated parameters
- Calls the free OpenMeteo weather API with designated parameters
- Compute current time and time period(Morning/Afternoon/Evening/Night)
- Parses the JSON responses and extracts current temperature, weather code, headline, source, URL
- Extract weather using a weather code dictionary
- Prints a formatted brief to the console
- Saves results to a timestamped txt file

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Anon0107/dailybrief.git
cd dailybrief
```

### 2. Install dependencies

```bash
pip install requests pandas python-dotenv
```

### 3. Get a free API key

Sign up at [newsapi.org](https://newsapi.org) and copy your API key.

### 4. Create a `.env` file

Create a file called `.env` in the project root:

```
NEWS_API_KEY=your_actual_key_here
```

Never commit this file. It is already listed in `.gitignore`.

### 5. Run the script

```bash
python dailybrief.py
```