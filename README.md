
# CMNTR - Code Mixed Note Taking and Retrieval

CMNTR is a command-line tool that allows users to create, index, edit, and search notes written in a code-mixed format of Telugu and English, using Roman script. It offers an efficient way to manage notes where users can search for them using queries in the same code-mixed style.

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

Enjoy managing your code-mixed Telugu-English notes efficiently!
