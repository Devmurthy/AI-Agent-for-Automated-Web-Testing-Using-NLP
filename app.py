from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()

from ai_agent import AIWebsiteTester

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Report directory
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

# Helper function to remove all emojis and special characters from text
def remove_emojis(text: str) -> str:
    """Remove all emoji and special Unicode characters that aren't supported by PDF fonts"""
    import re
    # Remove emojis and other non-ASCII characters that might cause issues
    # Keep only ASCII printable characters and common punctuation
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    return text.strip()

# Enhanced PDF generator for comprehensive test reports
def create_pdf_report(result: dict) -> str:
    """
    Generate a comprehensive PDF report from the test result.
    Includes test instructions, what was checked, detailed results, and metrics.
    Returns the PDF filename (stored in REPORTS_DIR).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.pdf"
    filepath = REPORTS_DIR / filename

    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", "B", 20)
    pdf.set_x(0)
    pdf.cell(0, 12, "AI Website Test Report", ln=1, align='C')
    pdf.ln(5)
    
    # Report metadata
    pdf.set_font("Arial", "", 10)
    report_date = result.get('timestamp', datetime.now().isoformat())
    if 'T' in report_date:
        report_date = report_date.split('T')[0] + ' ' + report_date.split('T')[1].split('.')[0]
    pdf.set_x(0)
    pdf.cell(0, 6, f"Generated: {report_date}", ln=1, align='C')
    pdf.ln(8)
    
    # Test Information Section
    pdf.set_font("Arial", "B", 14)
    pdf.set_x(10)
    pdf.cell(0, 8, "Test Information", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    # Website URL
    pdf.set_font("Arial", "B", 11)
    pdf.set_x(10)
    pdf.cell(40, 7, "Website URL:", 0)
    pdf.set_font("Arial", "", 11)
    url = result.get('websiteUrl', 'N/A')
    pdf.set_x(50)
    pdf.multi_cell(150, 7, url)
    
    # Browser
    pdf.set_font("Arial", "B", 11)
    pdf.set_x(10)
    pdf.cell(40, 7, "Browser:", 0)
    pdf.set_font("Arial", "", 11)
    browser = result.get('browser', 'N/A')
    pdf.set_x(50)
    pdf.multi_cell(150, 7, browser)
    
    # Status
    pdf.set_font("Arial", "B", 11)
    pdf.set_x(10)
    pdf.cell(40, 7, "Status:", 0)
    pdf.set_font("Arial", "B", 11)
    status = result.get('status', 'unknown')
    pdf.set_text_color(0, 128, 0) if status == 'success' else pdf.set_text_color(255, 0, 0)
    pdf.set_x(50)
    pdf.multi_cell(150, 7, status.upper())
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(3)
    
    # Test Instruction Section (What user requested)
    pdf.set_font("Arial", "B", 14)
    pdf.set_x(10)
    pdf.cell(0, 8, "Test Instruction", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Arial", "", 11)
    instruction = remove_emojis(result.get('testInstruction', 'No instruction provided'))
    pdf.set_x(10)
    pdf.multi_cell(190, 6, instruction)
    pdf.ln(3)
    
    # What Was Checked Section
    pdf.set_font("Arial", "B", 14)
    pdf.set_x(10)
    pdf.cell(0, 8, "What Was Checked", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Arial", "", 11)
    
    # Extract what was checked from validations and results
    checked_items = []
    validations = result.get("validations", [])
    for val in validations:
        val_type = val.get("type", "").replace("_", " ").title()
        # Use simple ASCII hyphen to avoid font issues in PDF
        checked_items.append(f"- {val_type}: {val.get('message', '')}")
    
    pdf.set_x(10)
    if checked_items:
        for item in checked_items:
            pdf.multi_cell(190, 6, remove_emojis(item))
    else:
        pdf.multi_cell(190, 6, "- Page navigation and basic functionality")
        pdf.multi_cell(190, 6, "- Test instruction execution")
    
    pdf.ln(3)
    
    # Test Results Section
    results = result.get("results", [])
    if results:
        pdf.set_font("Arial", "B", 14)
        pdf.set_x(10)
        pdf.cell(0, 8, "Test Results", ln=1)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        pdf.set_font("Arial", "", 11)
        pdf.set_x(10)
        for line in results:
            # Clean up emoji and formatting - remove all emojis
            clean_line = remove_emojis(str(line))
            if clean_line:
                pdf.multi_cell(190, 6, clean_line)
        pdf.ln(3)
    
    # Detailed Validations
    if validations:
        pdf.set_font("Arial", "B", 14)
        pdf.set_x(10)
        pdf.cell(0, 8, f"Detailed Validations ({len(validations)} checks)", ln=1)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        pdf.set_font("Arial", "", 10)
        pdf.set_x(10)
        for idx, val in enumerate(validations, 1):
            status = val.get("status", "").upper()
            val_type = remove_emojis(val.get("type", "").replace("_", " ").title())
            message = remove_emojis(val.get("message", ""))
            
            # Status color
            if status == "PASS":
                pdf.set_text_color(0, 128, 0)
            elif status == "WARNING":
                pdf.set_text_color(255, 165, 0)
            else:
                pdf.set_text_color(255, 0, 0)
            
            pdf.set_font("Arial", "B", 10)
            pdf.multi_cell(190, 6, f"{idx}. [{status}] {val_type}")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 10)
            pdf.set_x(10)
            pdf.multi_cell(190, 5, f"   {message}")
            pdf.ln(2)
        pdf.ln(2)
    
    # Performance Metrics
    performance = result.get("performance")
    if performance:
        pdf.set_font("Arial", "B", 14)
        pdf.set_x(10)
        pdf.cell(0, 8, "Performance Metrics", ln=1)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        pdf.set_font("Arial", "", 11)
        pdf.set_x(10)
        
        load_time = performance.get('loadTime', 0)
        if isinstance(load_time, (int, float)):
            load_time_sec = load_time / 1000
            pdf.multi_cell(190, 6, f"Page Load Time: {load_time} ms ({load_time_sec:.2f} seconds)")
        else:
            pdf.multi_cell(190, 6, f"Page Load Time: {load_time}")
        
        if "pageSize" in performance:
            page_size = performance.get('pageSize', 0)
            if isinstance(page_size, (int, float)):
                page_size_kb = page_size / 1024
                pdf.set_x(10)
                pdf.multi_cell(190, 6, f"Page Size: {page_size_kb:.2f} KB")
            else:
                pdf.set_x(10)
                pdf.multi_cell(190, 6, f"Page Size: {page_size}")
        
        pdf.ln(3)
    
    # Screenshots count
    screenshots_count = result.get("screenshots_count", 0)
    if screenshots_count > 0:
        pdf.set_font("Arial", "B", 11)
        pdf.set_x(10)
        pdf.multi_cell(190, 6, f"Note: {screenshots_count} screenshot(s) captured during test execution.")
        pdf.ln(3)
    
    # Footer
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.set_x(0)
    pdf.cell(0, 10, "Generated by AI Website Test Agent", 0, 0, 'C')
    
    pdf.output(str(filepath))
    return filename

# Initialize AI agent
try:
    ai_tester = AIWebsiteTester()
    print("✅ AI Agent initialized successfully with LangGraph + OpenAI + Playwright")
except Exception as e:
    print(f"❌ Error initializing AI Agent: {e}")
    ai_tester = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run-test', methods=['POST'])
def run_test():
    try:
        if not ai_tester:
            return jsonify({
                'error': 'AI Agent not initialized. Please check OpenAI API key and dependencies.'
            }), 500
        
        data = request.json
        website_url = data.get('websiteUrl', '').strip()
        test_instruction = data.get('testInstruction', '').strip()
        browser = data.get('browser', 'chrome')

        # Input validation
        if not website_url:
            return jsonify({
                'error': 'Website URL is required',
                'field': 'websiteUrl'
            }), 400
        
        if not test_instruction:
            return jsonify({
                'error': 'Test instruction is required',
                'field': 'testInstruction'
            }), 400
        
        # Validate URL format
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        # Validate instruction length
        if len(test_instruction) < 5:
            return jsonify({
                'error': 'Test instruction must be at least 5 characters',
                'field': 'testInstruction'
            }), 400
        
        if len(test_instruction) > 500:
            return jsonify({
                'error': 'Test instruction must be less than 500 characters',
                'field': 'testInstruction'
            }), 400

        # Run the test using AI agent (LangGraph workflow)
        result = ai_tester.run_test(website_url, test_instruction, browser)

        # Generate PDF report and attach link
        try:
            pdf_filename = create_pdf_report(result)
            result["reportUrl"] = f"/api/reports/{pdf_filename}"
        except Exception as pdf_error:
            # Do not block the main flow if PDF fails
            result["reportError"] = f"Could not generate PDF: {pdf_error}"

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'details': str(e.__traceback__) if hasattr(e, '__traceback__') else None
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/screenshots/<filename>', methods=['GET'])
def get_screenshot(filename):
    """Serve screenshot files"""
    screenshots_dir = Path("screenshots")
    screenshot_path = screenshots_dir / filename
    if screenshot_path.exists() and screenshot_path.is_file():
        return send_from_directory(str(screenshots_dir), filename)
    return jsonify({'error': 'Screenshot not found'}), 404

@app.route('/api/reports/<filename>', methods=['GET'])
def get_report(filename):
    """Serve generated PDF reports - force download"""
    report_path = REPORTS_DIR / filename
    if report_path.exists() and report_path.is_file():
        from flask import Response
        with open(report_path, 'rb') as f:
            pdf_data = f.read()
        response = Response(
            pdf_data,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'application/pdf'
            }
        )
        return response
    return jsonify({'error': 'Report not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

