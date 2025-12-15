"""Main window for Competitor Analyzer desktop application"""
import sys
import os
import json
import requests
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QFileDialog, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QImage
from config import API_HOST, API_PORT


class AnalysisThread(QThread):
    """Thread for running analysis in background"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, analysis_type, data):
        super().__init__()
        self.analysis_type = analysis_type
        self.data = data
    
    def run(self):
        try:
            base_url = f"http://{API_HOST}:{API_PORT}"
            
            if self.analysis_type == "image":
                with open(self.data, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(f"{base_url}/analyzeimage", files=files)
                    response.raise_for_status()
                    self.finished.emit(response.json())
            
            elif self.analysis_type == "text":
                response = requests.post(
                    f"{base_url}/analyzetext",
                    json={"text": self.data}
                )
                response.raise_for_status()
                self.finished.emit(response.json())
            
        except Exception as e:
            self.error.emit(str(e))


class ParsingThread(QThread):
    """Thread for parsing competitor sites"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            base_url = f"http://{API_HOST}:{API_PORT}"
            response = requests.get(f"{base_url}/parsedemo")
            response.raise_for_status()
            self.finished.emit(response.json())
        except Exception as e:
            self.error.emit(str(e))


class CompetitorAnalyzerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Competitor Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs
        self.create_image_analysis_tab()
        self.create_text_analysis_tab()
        self.create_parsing_tab()
        self.create_history_tab()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_image_analysis_tab(self):
        """Create image analysis tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Image Analysis")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Upload button
        upload_btn = QPushButton("Select Image")
        upload_btn.clicked.connect(self.select_image)
        layout.addWidget(upload_btn)
        
        # Image preview
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.image_label)
        
        # Analyze button
        self.analyze_image_btn = QPushButton("Analyze Image")
        self.analyze_image_btn.clicked.connect(self.analyze_image)
        self.analyze_image_btn.setEnabled(False)
        layout.addWidget(self.analyze_image_btn)
        
        # Progress bar
        self.image_progress = QProgressBar()
        self.image_progress.setVisible(False)
        layout.addWidget(self.image_progress)
        
        # Results area
        results_label = QLabel("Analysis Results:")
        results_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(results_label)
        
        self.image_results = QTextEdit()
        self.image_results.setReadOnly(True)
        layout.addWidget(self.image_results)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Image Analysis")
        
        self.selected_image_path = None
        self.image_analysis_thread = None
    
    def create_text_analysis_tab(self):
        """Create text analysis tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Text Analysis")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Text input
        input_label = QLabel("Enter text to analyze:")
        layout.addWidget(input_label)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Paste competitor's text content here...")
        layout.addWidget(self.text_input)
        
        # Analyze button
        analyze_text_btn = QPushButton("Analyze Text")
        analyze_text_btn.clicked.connect(self.analyze_text)
        layout.addWidget(analyze_text_btn)
        
        # Progress bar
        self.text_progress = QProgressBar()
        self.text_progress.setVisible(False)
        layout.addWidget(self.text_progress)
        
        # Results area
        results_label = QLabel("Analysis Results:")
        results_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(results_label)
        
        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Text Analysis")
        
        self.text_analysis_thread = None
    
    def create_parsing_tab(self):
        """Create parsing tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Competitor Website Parsing")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Parse button
        parse_btn = QPushButton("Parse Competitor Websites")
        parse_btn.clicked.connect(self.parse_competitors)
        layout.addWidget(parse_btn)
        
        # Progress bar
        self.parse_progress = QProgressBar()
        self.parse_progress.setVisible(False)
        layout.addWidget(self.parse_progress)
        
        # Results table
        results_label = QLabel("Parsing Results:")
        results_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(results_label)
        
        self.parse_results_table = QTableWidget()
        self.parse_results_table.setColumnCount(4)
        self.parse_results_table.setHorizontalHeaderLabels(["URL", "Status", "Title", "Timestamp"])
        self.parse_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.parse_results_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Parsing")
        
        self.parse_thread = None
    
    def create_history_tab(self):
        """Create history tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Analysis History")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Filename", "Type", "Timestamp"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.itemDoubleClicked.connect(self.view_history_item)
        layout.addWidget(self.history_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "History")
    
    def select_image(self):
        """Select image file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            self.selected_image_path = file_path
            self.analyze_image_btn.setEnabled(True)
            
            # Display image preview
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
    
    def analyze_image(self):
        """Analyze selected image"""
        if not self.selected_image_path:
            return
        
        self.analyze_image_btn.setEnabled(False)
        self.image_progress.setVisible(True)
        self.image_progress.setRange(0, 0)  # Indeterminate
        self.statusBar().showMessage("Analyzing image...")
        
        self.image_analysis_thread = AnalysisThread("image", self.selected_image_path)
        self.image_analysis_thread.finished.connect(self.on_image_analysis_finished)
        self.image_analysis_thread.error.connect(self.on_analysis_error)
        self.image_analysis_thread.start()
    
    def on_image_analysis_finished(self, result):
        """Handle image analysis completion"""
        self.image_progress.setVisible(False)
        self.analyze_image_btn.setEnabled(True)
        self.statusBar().showMessage("Analysis complete")
        
        if result.get("success") and result.get("analysis"):
            analysis = result["analysis"]
            formatted_result = f"""
Design Score: {analysis.get('design_score', 'N/A')}/10
Animation Potential: {analysis.get('animation_potential', 'N/A')}/10

Color Scheme: {analysis.get('color_scheme', 'N/A')}
Typography: {analysis.get('typography', 'N/A')}
Brand Identity: {analysis.get('brand_identity', 'N/A')}

Strengths:
{chr(10).join('- ' + s for s in analysis.get('strengths', []))}

Weaknesses:
{chr(10).join('- ' + w for w in analysis.get('weaknesses', []))}

Recommendations:
{chr(10).join('- ' + r for r in analysis.get('recommendations', []))}

Overall Impression:
{analysis.get('overall_impression', 'N/A')}
"""
            self.image_results.setText(formatted_result)
        else:
            self.image_results.setText(f"Error: {result.get('error', 'Unknown error')}")
    
    def analyze_text(self):
        """Analyze text content"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to analyze")
            return
        
        self.text_progress.setVisible(True)
        self.text_progress.setRange(0, 0)
        self.statusBar().showMessage("Analyzing text...")
        
        self.text_analysis_thread = AnalysisThread("text", text)
        self.text_analysis_thread.finished.connect(self.on_text_analysis_finished)
        self.text_analysis_thread.error.connect(self.on_analysis_error)
        self.text_analysis_thread.start()
    
    def on_text_analysis_finished(self, result):
        """Handle text analysis completion"""
        self.text_progress.setVisible(False)
        self.statusBar().showMessage("Analysis complete")
        
        if result.get("success") and result.get("analysis"):
            analysis = result["analysis"]
            formatted_result = f"""
Design Score: {analysis.get('design_score', 'N/A')}/10
Animation Potential: {analysis.get('animation_potential', 'N/A')}/10

Tone: {analysis.get('tone', 'N/A')}
Brand Voice: {analysis.get('brand_voice', 'N/A')}

Key Messaging:
{chr(10).join('- ' + m for m in analysis.get('key_messaging', []))}

Value Propositions:
{chr(10).join('- ' + v for v in analysis.get('value_propositions', []))}

SEO Keywords:
{', '.join(analysis.get('seo_keywords', []))}

Strengths:
{chr(10).join('- ' + s for s in analysis.get('strengths', []))}

Weaknesses:
{chr(10).join('- ' + w for w in analysis.get('weaknesses', []))}

Recommendations:
{chr(10).join('- ' + r for r in analysis.get('recommendations', []))}

Overall Impression:
{analysis.get('overall_impression', 'N/A')}
"""
            self.text_results.setText(formatted_result)
        else:
            self.text_results.setText(f"Error: {result.get('error', 'Unknown error')}")
    
    def parse_competitors(self):
        """Parse competitor websites"""
        self.parse_progress.setVisible(True)
        self.parse_progress.setRange(0, 0)
        self.statusBar().showMessage("Parsing competitor websites...")
        
        self.parse_thread = ParsingThread()
        self.parse_thread.finished.connect(self.on_parse_finished)
        self.parse_thread.error.connect(self.on_analysis_error)
        self.parse_thread.start()
    
    def on_parse_finished(self, result):
        """Handle parsing completion"""
        self.parse_progress.setVisible(False)
        self.statusBar().showMessage("Parsing complete")
        
        if result.get("success") and result.get("results"):
            results = result["results"]
            self.parse_results_table.setRowCount(len(results))
            
            for i, item in enumerate(results):
                self.parse_results_table.setItem(i, 0, QTableWidgetItem(item.get("url", "N/A")))
                status = "Success" if item.get("success") else "Failed"
                self.parse_results_table.setItem(i, 1, QTableWidgetItem(status))
                title = item.get("data", {}).get("title", "N/A")
                self.parse_results_table.setItem(i, 2, QTableWidgetItem(title))
                self.parse_results_table.setItem(i, 3, QTableWidgetItem(item.get("timestamp", "N/A")))
    
    def load_history(self):
        """Load analysis history"""
        try:
            base_url = f"http://{API_HOST}:{API_PORT}"
            response = requests.get(f"{base_url}/history")
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("files"):
                files = data["files"]
                self.history_table.setRowCount(len(files))
                
                for i, file_info in enumerate(files):
                    filename = file_info["filename"]
                    # Determine type from filename
                    file_type = "Analysis" if "analysis" in filename else "Parsing"
                    
                    self.history_table.setItem(i, 0, QTableWidgetItem(filename))
                    self.history_table.setItem(i, 1, QTableWidgetItem(file_type))
                    self.history_table.setItem(i, 2, QTableWidgetItem(file_info["modified"]))
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load history: {str(e)}")
    
    def view_history_item(self, item):
        """View selected history item"""
        row = item.row()
        filename = self.history_table.item(row, 0).text()
        
        # Read and display file content
        try:
            file_path = os.path.join("history", filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            # Display in a new window or dialog
            dialog = QMessageBox(self)
            dialog.setWindowTitle("History Item")
            dialog.setText(json.dumps(content, indent=2, ensure_ascii=False))
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {str(e)}")
    
    def on_analysis_error(self, error_msg):
        """Handle analysis errors"""
        self.image_progress.setVisible(False)
        self.text_progress.setVisible(False)
        self.parse_progress.setVisible(False)
        self.analyze_image_btn.setEnabled(True)
        self.statusBar().showMessage("Error occurred")
        QMessageBox.critical(self, "Error", f"Analysis failed: {error_msg}")


def main():
    """Main entry point for desktop application"""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = CompetitorAnalyzerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

