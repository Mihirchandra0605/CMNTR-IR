
# CMNTR - Code Mixed Note-Taking and Retrieval

CMNTR is a **personalized note-taking application** that evolves with you, adapting to your unique writing style in code-mixed Telugu and English (Roman script). It provides a seamless experience for creating, managing, and retrieving notes with advanced features like **context-aware search**. CMNTR learns your code-switching patterns and understands your context, offering a tailored experience as you use it.

---

## Why Choose CMNTR?

- **Personalized Experience**: CMNTR grows with you, adapting to your language preferences and writing habits.
- **Seamless Code-Mixing**: Optimized for Telugu-English code-mixed notes in Roman script.
- **Powerful Search**: Retrieve notes effortlessly using natural, code-mixed queries.
- **Context-Aware Suggestions**: Generates meaningful auto-suggestions based on your patterns.
- **Efficient Organization**: Index and manage notes with ease.
- **User-Centric Design**: Ideal for students, researchers, and professionals working in bilingual contexts.

---
## Features

- **Create notes** in code-mixed Telugu and English using Roman script.
- **Edit existing notes** to update their content.
- **Index notes** for efficient searching and retrieval.
- **Search notes** using code-mixed queries to find the most relevant results.
- **Delete notes** along with their indexed embeddings.
- **Auto Suggestion** to help powerful query generation


## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.



---

## Prerequisites

Before using this tool, ensure the following:

1. **Python Version**: Python 3.7 or higher installed on your system.
2. **Dependencies**: Required libraries installed (detailed below).

---

## Installation Guide

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/vihaan-that/CMNTR
   cd CMNTR
   ```

2. Navigate to the **interface** folder:
   ```bash
   cd interface
   ```

3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure all APIs are properly set up:
   - The `IndexerAPI`, `RetrievalAPI`, and `WordPredictAPI` Python files should be located in the `API` folder.

5. Verify the `data` directories:
   - `notes` directory will hold all note files.
   - `embeddings` directory will store embeddings for indexed notes.
   - These directories are created automatically if they do not exist.

---

## Usage

Run the CLI tool using the following command:
```bash
python CLIR.py <command> [arguments]
```

### Available Commands

1. **`create`**  
   Create a new note.
   ```bash
   python CLIR.py create <filename>
   ```
   - **Example**: 
     ```bash
     python CLIR.py create my_note
     ```

2. **`edit`**  
   Edit an existing note by appending content.
   ```bash
   python CLIR.py edit <filename> <text>
   ```
   - **Example**: 
     ```bash
     python CLIR.py edit my_note "Adding new content to the note."
     ```

3. **`delete`**  
   Delete a note and its associated embeddings.
   ```bash
   python CLIR.py delete <filename>
   ```
   - **Example**:
     ```bash
     python CLIR.py delete my_note
     ```

4. **`search`**  
   Search notes for content matching the query text.
   ```bash
   python CLIR.py search <query_text> [--top-k <number>]
   ```
   - **Example**:
     ```bash
     python CLIR.py search "important content" --top-k 5
     ```

5. **`list`**  
   List all available notes with metadata (size, modification time, and indexing status).
   ```bash
   python CLIR.py list
   ```

6. **`show`**  
   Display the content of a specific note.
   ```bash
   python CLIR.py show <filename>
   ```
   - **Example**:
     ```bash
     python CLIR.py show my_note
     ```

7. **`predict`**  
   Predict the next word based on the provided context.
   ```bash
   python CLIR.py predict <context> [--top-k <number>]
   ```
   - **Example**:
     ```bash
     python CLIR.py predict "The quick brown" --top-k 3
     ```

8. **`train_predictor`**  
   Retrain the word prediction model using all notes.
   ```bash
   python CLIR.py train_predictor
   ```

9. **`debug`**  
   Display debugging information about directories and files.
   ```bash
   python CLIR.py debug
   ```

10. **`check_notes`**  
    List and debug all files in the notes directory.
    ```bash
    python CLIR.py check_notes
    ```

---

## Directory Structure

```
<repository-folder>
│
├── API/
│   ├── indexerAPI.py          # Indexing functionality
│   ├── retrievalAPI.py        # Retrieval functionality
│   └── wordPredictAPI.py      # Word prediction functionality
│
├── interface/
│   ├── CLIR.py                # Main CLI tool
│   └── requirements.txt       # Python dependencies
│
├── data/
│   ├── notes/                 # Directory for storing note files
│   └── embeddings/            # Directory for storing embeddings
│
└── README.md                  # This file
```

---

## Examples

### Creating and Editing Notes
1. Create a note:
   ```bash
   python CLIR.py create sample_note
   ```
2. Edit the note with additional content:
   ```bash
   python CLIR.py edit sample_note "This is a new line."
   ```

### Searching and Viewing Notes
1. Search for a keyword:
   ```bash
   python CLIR.py search "important data" --top-k 2
   ```
2. View a specific note:
   ```bash
   python CLIR.py show sample_note
   ```

### Debugging and Checking Notes
1. Debug directories and file setups:
   ```bash
   python CLIR.py debug
   ```
2. Check all notes in the directory:
   ```bash
   python CLIR.py check_notes
   ```

---

## Notes

- **Environment Variables**: The directories for notes and embeddings are managed using the following environment variables:
  - `NOTES_DIRECTORY`
  - `EMBEDDINGS_DIRECTORY`

- **Error Handling**: Clear error messages are provided for missing files, failed directory creation, or API-related issues.

---
## TESTING
# Creating Notes
```bash
python CLIR.py create note1 && python CLIR.py edit note1 "Nenu Hyderabad lo unna prathi chota chai kalagalanu. The Irani chai at Charminar is world-famous. Tasty food and friendly people are the highlights of this city. Nenu regular ga evening lo street food tinataniki veli untanu. Hyderabad lo, gola ice creams chala popular. The climate is unique – sometimes rainy, sometimes sunny. Chala interesting vibe undi e city ki. Charminar lo photos teeyadam is a must for tourists. The architecture is breathtaking. Meeku biryani nachite, definitely try Paradise or Shah Ghouse. Naku best anipinchindi. Hyderabad has something for everyone – techies ki IT parks, students ki education hubs, and families ki malls. The people here are known for their welcoming attitude. Visiting places like Necklace Road, Tank Bund, and Salar Jung Museum are always fun. Hyderabad lo okka sari visit chesthe, you'll definitely feel at home."

python CLIR.py create note2 && python CLIR.py edit note2 "E weekend lo, beach ki vellamu. Vizag lo RK Beach super untundi. Morning sunrise chudadam, waves tho play cheyadam, and photography chala enjoy chesamu. Akkada fresh fish fry and cool drinks tinte chala baguntadi. Beachside stalls lo souvenirs konadam chala thrilling ga anipinchindi. Vizag city ni clean and green cheyyali ani chala efforts chestunaru government. Nenu family tho Submarine Museum ki kuda veltanu. Submarine lo entry experience matram must-try. Dolphin’s Nose view point chala scenic ga untadi. Vizag lo tourism ki baga scope undi. Weekend lo Vizag plan chesthe, miru kuda chala enjoy chestaru. Oka chinna beach vacation ki Vizag perfect destination!"

python CLIR.py create note3 && python CLIR.py edit note3 "Amma nenu konni gadgets online order chesanu. Amazon lo sales unnappudu discounts baaga vasthayi. Nenu oka smartphone, wireless earphones, and smart watch tisukunnanu. Smartphone tho photos chala clarity ga vachayi. Naaku smart watch notifications feature chala nachindi. Emi chesthunna, calls and messages alert vaste, work chala easy aipothundi. Morning lo earphones pettukoni walks kuda start chesanu. Music tho start chesina day full ga energetic ga untundi. Online shopping lo offers pedithe, offline shopping kanna better ani naaku anipistundi. Gadgets quality and return options kuda manchiga vunnayi. Na next plan home automation gadgets teesukodaniki. Smart home chala convenient untundi ani telustondi."

python CLIR.py create note4 && python CLIR.py edit note4 "Library lo spend chese time naaku chala nachindi. Books tho nenu full time busy untanu. Fiction novels chadive interest undi naaku. Daniki Telugu literature add chesanu. Peddapuli and Viswanatha Satyanarayana writings naaku favourite. Classroom lo, Telugu poetry discuss chesinappudu, discussions chala inspiring ga untayi. E weekend, Shakespeare’s plays kuda start chesanu. Online PDFs tho, mana library resources kuda use chestanu. Library atmosphere chala calm ga untadi. Chala varaku students library lo digital resources use chestunaru. Naku study breaks lo short stories chadive habit vundi. Rendu cultures blend chesukuni reading chesina feeling inko level lo untadi."

python CLIR.py create note5 && python CLIR.py edit note5 "Cinema ante naaku chala ishtam. Theatres lo Telugu movies chudadam lo euphoria untadi. Friends tho weekend lo latest movies chudatam common ga chestamu. Last week, Nani movie chusamu. Storyline, acting anni mind-blowing. Popcorn, cold drinks tho time pass cheyadam and special theatres experience antha worth untadi. Nenu OTT platforms lo old classics kuda chustanu. Amazon, Netflix lo Telugu content baaga vuntadi. Action and family drama movies are my favourite. Movies ki unna background music anni scenes ki soul istundi ani naaku anipistadi. Movies chudatam kuda oka relaxation therapy la untundi!"

```
# Testing Search
```bash
python CLIR.py search "Hyderabad lo best biryani ekkada?" --top-k 3
python CLIR.py search "Vizag lo Dolphin Nose ki ela vellali?" --top-k 2
python CLIR.py search "Amazon lo sales time lo best gadgets" --top-k 3
python CLIR.py search "Telugu poetry classroom discussions" --top-k 5
python CLIR.py search "Latest Telugu movies theatres lo chudali" --top-k 3
```

# Testing Word Prediction
```bash
python CLIR.py predict "Hyderabad lo best chai" --top-k 3
python CLIR.py predict "Vizag lo beach lo" --top-k 3
python CLIR.py predict "Amazon lo discounts" --top-k 3
python CLIR.py predict "Library lo fiction novels" --top-k 3
python CLIR.py predict "Cinema lo storylines" --top-k 3
python CLIR.py predict "Smartwatch notifications" --top-k 3
```
---

Enjoy managing your code-mixed Telugu-English notes efficiently!
