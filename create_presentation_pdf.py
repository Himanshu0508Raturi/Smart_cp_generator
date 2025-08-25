#!/usr/bin/env python3

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
import os

def create_presentation_pdf():
    # Create the PDF document
    filename = "Smart_CP_Generator_Presentation_Script.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get sample style sheet and create custom styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#1f4e79')
    )
    
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#2e75b6'),
        alignment=TA_LEFT
    )
    
    timing_style = ParagraphStyle(
        'Timing',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#666666'),
        alignment=TA_LEFT,
        spaceAfter=8
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=6,
        leftIndent=20,
        bulletIndent=10
    )
    
    # Story list to hold all content
    story = []
    
    # Title
    story.append(Paragraph("Smart CP Generator", title_style))
    story.append(Paragraph("10-Minute Presentation Script", styles['Heading3']))
    story.append(Spacer(1, 20))
    
    # Slide 1
    story.append(Paragraph("Slide 1: Opening Hook", slide_title_style))
    story.append(Paragraph("Duration: 30 seconds", timing_style))
    story.append(Paragraph('"Good morning! How many of you have ever dealt with maritime contracts? If you work in shipping, you know that creating Charter Party agreements is a nightmare - lawyers charging $500+ per hour, weeks of back-and-forth negotiations, and human errors that can cost millions. Today, I\'m going to show you how we solved this with AI in just 48 hours."', content_style))
    
    # Slide 2
    story.append(Paragraph("Slide 2: The Problem", slide_title_style))
    story.append(Paragraph("Duration: 1 minute", timing_style))
    story.append(Paragraph('"The maritime industry processes over $14 trillion in global trade annually, but contract creation is still stuck in the stone age. Here\'s what shipping companies face today:', content_style))
    
    story.append(Paragraph("• <b>Manual Process:</b> Lawyers manually merge fixture recaps, base contracts, and negotiated clauses", bullet_style))
    story.append(Paragraph("• <b>High Costs:</b> Legal fees of $2,000-5,000 per contract", bullet_style))
    story.append(Paragraph("• <b>Time Delays:</b> 2-3 weeks per contract creation", bullet_style))
    story.append(Paragraph("• <b>Human Errors:</b> Missing clauses can lead to million-dollar disputes", bullet_style))
    story.append(Paragraph("• <b>No Standardization:</b> Every lawyer formats contracts differently", bullet_style))
    
    story.append(Paragraph('This creates bottlenecks that delay vessel operations and increase costs across the entire supply chain."', content_style))
    
    # Slide 3
    story.append(Paragraph("Slide 3: Our Solution", slide_title_style))
    story.append(Paragraph("Duration: 1 minute", timing_style))
    story.append(Paragraph('"Meet Smart CP Generator - the world\'s first AI-powered Charter Party automation platform. We\'ve built a complete web application that takes three input documents and automatically generates professional-grade contracts in minutes, not weeks.', content_style))
    
    story.append(Paragraph('<b>What makes us different?</b>', content_style))
    story.append(Paragraph("• <b>100% Free:</b> No subscription fees, no API costs, no hidden charges", bullet_style))
    story.append(Paragraph("• <b>AI-Powered:</b> Uses advanced NLP to understand and extract contract clauses", bullet_style))
    story.append(Paragraph("• <b>Multiple Formats:</b> Handles TXT, DOC, DOCX, and PDF inputs", bullet_style))
    story.append(Paragraph("• <b>Professional Output:</b> Generates both Word and PDF contracts", bullet_style))
    story.append(Paragraph('• <b>Instant Results:</b> Complete contracts in under 2 minutes"', bullet_style))
    
    # Slide 4
    story.append(Paragraph("Slide 4: Live Demo - Upload Process", slide_title_style))
    story.append(Paragraph("Duration: 2 minutes", timing_style))
    story.append(Paragraph('"Let me show you how simple this is. [Open application]', content_style))
    story.append(Paragraph('"I\'m going to create a real iron ore shipping contract from Australia to Rotterdam. Watch this:', content_style))
    story.append(Paragraph('Step 1: Upload the fixture recap - this contains the commercial deal terms like freight rates, cargo quantities, and ports.', content_style))
    story.append(Paragraph('Step 2: Upload the base Charter Party template - this is the standard legal framework.', content_style))
    story.append(Paragraph('Step 3: Upload negotiated clauses - these are the special terms like anti-corruption clauses, environmental compliance, and COVID protocols.', content_style))
    story.append(Paragraph('[Upload the three sample documents]', content_style))
    story.append(Paragraph('Contract name: \'MV Atlantic Trader - Iron Ore Voyage\'', content_style))
    story.append(Paragraph('Click Process... and watch the magic happen!"', content_style))
    
    # Slide 5
    story.append(Paragraph("Slide 5: AI Processing Demonstration", slide_title_style))
    story.append(Paragraph("Duration: 1.5 minutes", timing_style))
    story.append(Paragraph('"While it\'s processing, here\'s what\'s happening behind the scenes:', content_style))
    story.append(Paragraph('Our AI engine powered by spaCy is:', content_style))
    story.append(Paragraph("• <b>Extracting 114+ clauses</b> from the three documents", bullet_style))
    story.append(Paragraph("• <b>Categorizing</b> payment terms, laytime clauses, cargo specifications", bullet_style))
    story.append(Paragraph("• <b>Identifying conflicts</b> between different document versions", bullet_style))
    story.append(Paragraph("• <b>Merging intelligently</b> to create a cohesive final contract", bullet_style))
    story.append(Paragraph("• <b>Maintaining legal language</b> and professional formatting", bullet_style))
    story.append(Paragraph('And... it\'s done! Look at this - a complete, professional Charter Party contract in under 2 minutes. The system extracted 114 individual clauses and merged them intelligently."', content_style))
    
    # Page break
    story.append(PageBreak())
    
    # Slide 6
    story.append(Paragraph("Slide 6: Generated Contract Preview", slide_title_style))
    story.append(Paragraph("Duration: 1 minute", timing_style))
    story.append(Paragraph('"Here\'s our final contract - professionally formatted, legally compliant, and ready for execution. Notice:', content_style))
    story.append(Paragraph("• <b>Clean formatting</b> with proper legal structure", bullet_style))
    story.append(Paragraph("• <b>All commercial terms</b> accurately integrated", bullet_style))
    story.append(Paragraph("• <b>Standard clauses</b> properly positioned", bullet_style))
    story.append(Paragraph("• <b>Special provisions</b> clearly highlighted", bullet_style))
    story.append(Paragraph("• <b>Download options</b> for both Word and PDF formats", bullet_style))
    story.append(Paragraph('This contract is immediately ready for review by legal teams and can be executed without additional formatting."', content_style))
    
    # Slide 7
    story.append(Paragraph("Slide 7: Technical Architecture", slide_title_style))
    story.append(Paragraph("Duration: 1.5 minutes", timing_style))
    story.append(Paragraph('"What makes this possible? Our completely free, open-source architecture:', content_style))
    story.append(Paragraph('<b>Frontend:</b> Bootstrap 5 for professional, responsive design', content_style))
    story.append(Paragraph('<b>Backend:</b> Flask Python framework for robust processing', content_style))
    story.append(Paragraph('<b>Database:</b> SQLite for zero-cost local storage', content_style))
    story.append(Paragraph('<b>AI Engine:</b> spaCy NLP library - completely free, no API costs', content_style))
    story.append(Paragraph('<b>Document Processing:</b> Handles multiple file formats automatically', content_style))
    story.append(Paragraph('<b>Output Generation:</b> Professional Word and PDF creation', content_style))
    story.append(Paragraph('The entire system runs on free technologies. No expensive cloud services, no paid AI APIs, no subscription databases. This keeps our costs at zero and makes the solution accessible to companies of any size."', content_style))
    
    # Slide 8
    story.append(Paragraph("Slide 8: Business Impact & Market", slide_title_style))
    story.append(Paragraph("Duration: 1 minute", timing_style))
    story.append(Paragraph('"The market opportunity is massive:', content_style))
    story.append(Paragraph('<b>Target Market:</b>', content_style))
    story.append(Paragraph("• 50,000+ shipping companies globally", bullet_style))
    story.append(Paragraph("• Maritime law firms and brokers", bullet_style))
    story.append(Paragraph("• Commodity trading houses", bullet_style))
    story.append(Paragraph("• Port operators and terminals", bullet_style))
    
    story.append(Paragraph('<b>Value Proposition:</b>', content_style))
    story.append(Paragraph("• <b>Cost Savings:</b> $2,000-5,000 per contract → $0", bullet_style))
    story.append(Paragraph("• <b>Time Reduction:</b> 2-3 weeks → 2 minutes", bullet_style))
    story.append(Paragraph("• <b>Error Prevention:</b> AI consistency vs. human error", bullet_style))
    story.append(Paragraph("• <b>Standardization:</b> Consistent professional output", bullet_style))
    story.append(Paragraph("• <b>Accessibility:</b> Available 24/7, globally", bullet_style))
    story.append(Paragraph('Even capturing 1% of this market represents millions in value creation for the shipping industry."', content_style))
    
    # Slide 9
    story.append(Paragraph("Slide 9: Competitive Advantages", slide_title_style))
    story.append(Paragraph("Duration: 45 seconds", timing_style))
    story.append(Paragraph('"Why will we win?', content_style))
    story.append(Paragraph("✓ <b>First Mover:</b> No direct competitors in automated CP generation", bullet_style))
    story.append(Paragraph("✓ <b>Free Forever:</b> Sustainable cost model attracts all market segments", bullet_style))
    story.append(Paragraph("✓ <b>Industry Specific:</b> Built specifically for maritime contracts", bullet_style))
    story.append(Paragraph("✓ <b>Professional Quality:</b> Lawyer-grade output without lawyer costs", bullet_style))
    story.append(Paragraph("✓ <b>Scalable Technology:</b> Can handle thousands of contracts simultaneously", bullet_style))
    story.append(Paragraph('✓ <b>Open Source Foundation:</b> Community can contribute and improve"', bullet_style))
    
    # Slide 10
    story.append(Paragraph("Slide 10: Next Steps & Call to Action", slide_title_style))
    story.append(Paragraph("Duration: 30 seconds", timing_style))
    story.append(Paragraph('"We\'ve proven that AI can revolutionize maritime contract creation. The demo you just saw is live and ready for deployment.', content_style))
    story.append(Paragraph('<b>Immediate Next Steps:</b>', content_style))
    story.append(Paragraph("1. <b>Deploy</b> the application for global access", bullet_style))
    story.append(Paragraph("2. <b>Partner</b> with maritime law firms for validation", bullet_style))
    story.append(Paragraph("3. <b>Integrate</b> with shipping management systems", bullet_style))
    story.append(Paragraph("4. <b>Scale</b> to handle enterprise volumes", bullet_style))
    story.append(Paragraph('The future of maritime contracts is here, and it\'s free. Thank you!"', content_style))
    
    # Summary section
    story.append(Spacer(1, 20))
    story.append(Paragraph("Presentation Summary", slide_title_style))
    story.append(Paragraph("<b>Total Time:</b> ~10 minutes", content_style))
    story.append(Paragraph('<b>Key Success Tips:</b>', content_style))
    story.append(Paragraph("• Keep the demo moving smoothly", bullet_style))
    story.append(Paragraph("• Emphasize the 'free forever' aspect repeatedly", bullet_style))
    story.append(Paragraph("• Show real contract quality, not mockups", bullet_style))
    story.append(Paragraph("• Connect technical features to business value", bullet_style))
    story.append(Paragraph("• End with a strong call to action", bullet_style))
    
    story.append(Paragraph('This script balances technical demonstration with business value, perfect for hackathon judges or potential investors!', content_style))
    
    # Build PDF
    doc.build(story)
    return filename

if __name__ == "__main__":
    filename = create_presentation_pdf()
    print(f"PDF created successfully: {filename}")