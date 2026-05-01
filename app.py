"""
Project Indolance — Flask Application
=======================================
Web dashboard backend with API routes for scan, search, analyze.
Accepts user ideas, keywords and tags to drive the analysis.
Provides dual originality scores (local + global) and plagiarism sources.
"""

import os, sys, json
from flask import Flask, render_template, jsonify, request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, DATA_DIR
from chronos.local_reader import LocalReader
from chronos.global_scraper import GlobalScraper
from chronos.comparison_engine import ComparisonEngine

app = Flask(__name__)

# Shared engine instances
reader = LocalReader()
scraper = GlobalScraper()
engine = ComparisonEngine()

# Store user-provided context
user_context = {
    "idea": "",
    "keywords": [],
    "tags": [],
}


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/scan", methods=["POST"])
def api_scan():
    """Trigger local file scan. Also stores user idea/keywords/tags."""
    try:
        data = request.get_json(silent=True) or {}

        # Store user input
        idea = data.get("idea", "")
        kw_str = data.get("keywords", "")
        tags_str = data.get("tags", "")
        user_context["idea"] = idea
        user_context["keywords"] = [
            k.strip().lower() for k in kw_str.split(",") if k.strip()
        ] if kw_str else []
        user_context["tags"] = [
            t.strip().lower() for t in tags_str.split(",") if t.strip()
        ] if tags_str else []

        # Store topics if provided
        topics = data.get("topics")
        if topics:
            scraper.topics = topics

        kb = reader.scan_all()
        return jsonify({
            "success": True,
            "message": f"Scanned {len(kb)} files",
            "total_files": len(kb),
            "keywords": reader.get_all_keywords()[:30],
            "timeline": reader.get_keyword_timeline(),
            "user_keywords": user_context["keywords"],
            "user_tags": user_context["tags"],
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    """Trigger API-based searching using user-provided topics/tags."""
    try:
        data = request.get_json(silent=True) or {}
        topics = data.get("topics")
        if topics:
            scraper.topics = topics

        # Also use tags as additional search topics
        tags = data.get("tags", "")
        if tags:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            # Add tags that aren't already in topics
            existing = set(t.lower() for t in scraper.topics)
            for tag in tag_list:
                if tag.lower() not in existing:
                    scraper.topics.append(tag)

        # Also add the idea as a search query if present
        idea = data.get("idea", "")
        if idea and len(idea) > 10:
            # Use first 100 chars of idea as a search query
            idea_query = idea[:100].strip()
            scraper.topics.insert(0, idea_query)

        # Extract keywords for deep search
        keywords_str = data.get("keywords", "")
        idea_keywords = [k.strip().lower() for k in keywords_str.split(",") if k.strip()] if keywords_str else []

        trends = scraper.scrape_all(idea_text=idea, idea_keywords=idea_keywords)

        # Count by source
        source_counts = {}
        for t in trends:
            src = t.get("source_label", t.get("source", "unknown"))
            source_counts[src] = source_counts.get(src, 0) + 1

        return jsonify({
            "success": True,
            "message": f"Found {len(trends)} results from {len(source_counts)} sources",
            "total_results": len(trends),
            "top_keywords": scraper.get_keyword_frequencies()[:20],
            "source_counts": source_counts,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """Run dual comparison analysis: local + global originality + plagiarism sources."""
    try:
        data = request.get_json(silent=True) or {}

        # Refresh user context if provided
        idea = data.get("idea", user_context.get("idea", ""))
        kw_str = data.get("keywords", "")
        tags_str = data.get("tags", "")
        extra_keywords = [
            k.strip().lower() for k in kw_str.split(",") if k.strip()
        ] if kw_str else user_context.get("keywords", [])

        # Add tags to keywords for analysis
        extra_tags = [
            t.strip().lower() for t in tags_str.split(",") if t.strip()
        ] if tags_str else user_context.get("tags", [])
        all_keywords = list(set(extra_keywords + extra_tags))

        # Ensure data is loaded
        if not reader.knowledge_base:
            reader.load_knowledge_base()
        if not scraper.global_trends:
            scraper.load_trends()

        results = engine.analyze(
            reader, scraper,
            user_idea=idea,
            user_keywords=all_keywords
        )
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/results", methods=["GET"])
def api_results():
    """Get latest analysis results."""
    try:
        results = engine.load_results()
        if results:
            return jsonify({"success": True, "results": results})
        return jsonify({"success": False, "message": "No results yet."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/timeline", methods=["GET"])
def api_timeline():
    """Get keyword timeline data."""
    try:
        if not reader.knowledge_base:
            reader.load_knowledge_base()
        return jsonify({
            "success": True,
            "timeline": reader.get_keyword_timeline(),
            "total_keywords": len(reader.get_all_keywords())
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/status", methods=["GET"])
def api_status():
    local_path = os.path.join(DATA_DIR, "local_keywords.json")
    global_path = os.path.join(DATA_DIR, "global_trends.json")
    results_path = os.path.join(DATA_DIR, "analysis_results.json")
    return jsonify({
        "has_local_data": os.path.exists(local_path),
        "has_global_data": os.path.exists(global_path),
        "has_results": os.path.exists(results_path),
    })


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PROJECT INDOLANCE — The Research Intelligence Engine")
    print("  Dashboard: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
