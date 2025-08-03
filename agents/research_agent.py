from langchain.agents import initialize_agent, AgentType
from tools.agent_tools import web_search, wikipedia_search, arxiv_search, arxiv_download
from datetime import datetime
import re

RESEARCH_SYSTEM_PROMPT = """You are an expert academic research assistant with deep expertise in systematic literature review and knowledge synthesis.

RESEARCH METHODOLOGY:
• Always follow a structured research approach: Academic sources → Background context → Recent developments → Synthesis
• Use multiple tools strategically: ArxivSearch for papers, WikipediaSearch for context, WebSearch for current trends
• Cross-reference findings to identify consensus, contradictions, and knowledge gaps
• Provide evidence-based conclusions with proper attribution

CRITICAL TOOL REQUIREMENTS:
• ArxivSearch: Extract complete arXiv IDs with versions (2506.01463v1, NOT 2506.01463)
• ArxivDownload: Use format 'complete_arxiv_id|exact_paper_title' - download ONE paper per action
• Always verify download success before claiming completion
• Include arxiv_id from search results when downloading

OUTPUT STANDARDS:
• Structure all responses with clear markdown sections
• Cite every claim with [Title](URL) format
• Create comparison tables for multiple sources
• Highlight research trends, gaps, and future directions
• End with actionable insights for researchers

QUALITY CONTROL:
• Stop after max 8 tool actions to prevent loops
• If downloads fail, explain why and continue without claiming success
• Synthesize rather than concatenate - show relationships between sources"""

class ResearchSynthesizerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.tools = [web_search, wikipedia_search, arxiv_search, arxiv_download]
        
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={
                'system_message': RESEARCH_SYSTEM_PROMPT,
                'handle_parsing_errors': True
            },
            handle_parsing_errors=True,
        )
    
    def _preprocess_query(self, query, research_depth="standard"):
        """Enhance user queries with research-specific instructions."""
        
        base_instructions = {
            "quick": "Provide a concise overview with 3-5 key sources and main findings.",
            "standard": "Conduct thorough research with academic sources, context, and synthesis.",
            "comprehensive": "Perform exhaustive research with detailed analysis and extensive source coverage."
        }
        
        research_template = f"""
RESEARCH REQUEST: "{query}"

RESEARCH DEPTH: {research_depth.upper()}
INSTRUCTIONS: {base_instructions.get(research_depth, base_instructions["standard"])}

REQUIRED STRUCTURE:
## Research Topic
{query}

## Academic Foundation
[ArXiv papers with key findings and citations]

## Background Context  
[Wikipedia summary for essential concepts]

## Current Developments
[Recent news, industry updates, practical applications]

## Research Synthesis
[Cross-source analysis highlighting consensus, conflicts, and gaps]

## Key Takeaways
[3-5 actionable insights for researchers/practitioners]

## Recommended Papers for Download
[Suggest 1-2 most valuable papers with reasons]

Begin comprehensive research now."""
        
        return research_template
    
    def _post_process_response(self, response, original_query):
        """Clean and enhance the agent's response."""
        
        # Add metadata
        metadata = f"\n\n---\n**Research Query:** {original_query}\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n**Sources:** ArXiv, Wikipedia, Web Search"
        
        # Basic validation
        if len(response) < 500:
            response += "\n\n*Note: This response may be incomplete. Consider requesting a more comprehensive analysis.*"
        
        return response + metadata
    
    def synthesize(self, query, research_depth="standard", download_papers=False):
        """Enhanced synthesis with configurable research depth and optional downloads."""
        
        # Preprocess the query
        enhanced_query = self._preprocess_query(query, research_depth)
        
        # Add download instruction if requested
        if download_papers:
            enhanced_query += "\n\nAFTER SYNTHESIS: Download the 1-2 most relevant papers using ArxivDownload tool."
        
        # Execute research
        response = self.agent.run(enhanced_query)
        
        # Post-process for quality
        return self._post_process_response(response, query)
    
    def literature_review(self, topic, max_papers=7):
        """Focused academic literature review."""
        prompt = f"""
LITERATURE REVIEW REQUEST: "{topic}"

SYSTEMATIC APPROACH:
1. Search ArXiv for {max_papers} most relevant recent papers (2020+)
2. Extract key findings, methodologies, and contributions
3. Identify research trends and theoretical frameworks
4. Note contradictions or debates in the literature

OUTPUT FORMAT:
## Literature Review: {topic}

### Research Landscape
[Overview of current state]

### Key Papers Analysis
| Title | Year | Key Contribution | Methodology | Impact |
|-------|------|------------------|-------------|---------|
[Table with detailed analysis]

### Theoretical Frameworks
[Major approaches and schools of thought]

### Research Gaps & Future Directions
[Specific areas needing investigation]

### Methodology Trends
[Common approaches and emerging methods]

Execute systematic literature review now."""
        
        return self.agent.run(prompt)
    
    def comparative_analysis(self, topic_a, topic_b):
        """Compare two related research areas."""
        prompt = f"""
COMPARATIVE RESEARCH: "{topic_a}" vs "{topic_b}"

ANALYSIS FRAMEWORK:
1. Research both topics using ArXiv and web sources
2. Identify similarities and differences
3. Compare methodologies, applications, and outcomes
4. Analyze cross-pollination opportunities

COMPARISON STRUCTURE:
## Comparative Analysis: {topic_a} vs {topic_b}

### Topic A: {topic_a}
[Key characteristics, approaches, findings]

### Topic B: {topic_b}  
[Key characteristics, approaches, findings]

### Similarities
[Common elements, shared foundations]

### Differences
[Distinctive features, unique approaches]

### Synthesis Opportunities
[How topics could inform each other]

Execute comparative analysis now."""
        
        return self.agent.run(prompt)
    
    def trend_analysis(self, topic, time_period="2020-2024"):
        """Analyze research trends over time."""
        prompt = f"""
TREND ANALYSIS: "{topic}" ({time_period})

TEMPORAL RESEARCH APPROACH:
1. Search for papers across specified time period
2. Identify evolution of concepts and methods
3. Track emerging themes and declining areas
4. Predict future research directions

TREND REPORT STRUCTURE:
## Research Trends: {topic} ({time_period})

### Evolution Timeline
[How the field has changed]

### Emerging Themes
[New research directions]

### Methodology Evolution
[Changes in research approaches]

### Future Predictions
[Likely research directions]

Execute trend analysis now."""
        
        return self.agent.run(prompt)
    
    def quick_overview(self, topic):
        """Generate a quick research overview with key papers and summary."""
        prompt = f"""Research the topic: "{topic}"

TASK: Provide a quick research overview including:
1. Find 3-5 most relevant recent papers from arXiv
2. Get foundational context from Wikipedia  
3. Search for recent developments via web search
4. Synthesize findings into a structured overview

OUTPUT FORMAT:
## Research Topic: {topic}

### Key Academic Papers
[Table with: Title | Year | Key Finding | arXiv Link]

### Current Context
[2-3 sentences from Wikipedia providing background]

### Recent Developments  
[2-3 key points from web search with sources]

### Research Synthesis
[3-4 paragraphs synthesizing findings, highlighting consensus/gaps]

Do NOT download papers unless specifically requested."""
        
        return self.agent.run(prompt)
