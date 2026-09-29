# Phase 3: Project Design

## System Architecture
- **Client Tier:** Dynamic HTML5/CSS3 templates served via Jinja2.
- **Server Tier:** Asynchronous FastAPI backend running on Uvicorn.
- **AI Processing Tier:** Google Generative AI API (Gemini 1.5 Flash) for multimodal parsing.
- **Infrastructure:** Containerized web service running on Render cloud.

## Data Flow
1. User uploads a receipt image via the web client.
2. FastAPI processes the payload and forwards the image to the Gemini multimodal endpoint.
3. Gemini extracts itemized details and spending insights.
4. Jinja2 renders and returns the structured results view to the user.

- *Date:* 29 September 2026
- *Team ID:* 06
- *Project Name:* FitBuddy – AI Fitness Plan Generator using Gemini Models
- *Maximum Marks:* 3 Marks

---

# Phase 3: Project Design

| S.No | Team Member | Idea / Suggestion | Category | Group No. |
|------|-------------|-------------------|----------|-----------|
| 1 | Ponnurangam M| Multimodal receipt image parsing using Google Gemini 1.5 Flash API | AI Architecture & Vision | Group 06 |
| 2 | Saran R| Automated line-item expense categorization and tax breakdown | Data Processing & Logic | Group 06 |
| 3 | Sanjay Kumar  | Dynamic Jinja2 web interface for intuitive mobile and desktop uploads | Frontend & UI/UX | Group 06 |
|4 |Vishnu S  | Dynamic Jinja2 web interface for intuitive mobile and desktop uploads | Frontend & UI/UX | Group 06 |




 
