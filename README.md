# Project Indolance — The Research Intelligence Engine

Project Indolance is a powerful research intelligence tool designed to bridge the gap between your local knowledge base and global research trends. By analyzing your local files (code, papers, notes) and scraping current web trends, it uses vector mathematics (TF-IDF and Cosine Similarity) to determine the originality of your ideas and suggest new research directions.

## ✨ Features

- **Local Knowledge Scanner**: Automatically scans configured directories for PDFs, source code, and text files, extracting keywords using domain-specific regex patterns and term frequency.
- **Global Trend Scraper**: Connects to Semantic Scholar, CrossRef, OpenAlex, and GitHub to fetch the latest research papers and trending repositories based on your topics and tags.
- **Dual Originality Engine**: Compares your ideas against your local knowledge base and the global web to provide a comprehensive originality score.
- **Plagiarism Detection**: Highlights heavily overlapping sources to help you maintain academic integrity.
- **Gap Finder**: Identifies missing concepts in your local knowledge base compared to global trends, suggesting high-value research directions.
- **Interactive Dashboard**: A premium, matte-monotone, circular-UI dashboard built with Flask and Vanilla CSS for visualizing your research timeline, originality scores, and keyword connections.

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Flask
- **Data Processing**: NumPy, Pandas, scikit-learn (TF-IDF, Cosine Similarity)
- **Document Parsing**: pdfplumber
- **Web Scraping**: BeautifulSoup4, Requests
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript, Chart.js

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/project-indolance.git
   cd project-indolance
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration:**
   Open `config.py` to configure your local scan directories and API limits.
   ```python
   # Example: Update your scan directories
   SCAN_DIRECTORIES = [
       SAMPLE_DIR,
       # r"C:\Users\YourName\Documents\Research",
   ]
   ```

### Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open the Dashboard:**
   Navigate to `http://localhost:5000` in your web browser.

## 💡 How to Use

1. **Input Your Idea:** On the dashboard, enter your research idea, keywords, and tags.
2. **Scan Local Files:** Click the scan button to process your local knowledge base.
3. **Scrape Web Trends:** Fetch the latest global data related to your topics.
4. **Analyze:** Run the comparison engine to receive your dual originality scores, plagiarism sources, and gap suggestions.

## ⚙️ Architecture

The engine is divided into three core components:
1. **The Past (Local Reader):** Builds a timestamped knowledge base from local files.
2. **The Present (Global Scraper):** Aggregates current trends from academic APIs and code repositories.
3. **The Future (Comparison Engine):** Uses TF-IDF vectorization and Cosine Similarity to find gaps and calculate originality.

## 📝 License

This project is licensed under the MIT License.
