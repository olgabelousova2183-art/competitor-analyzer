"""OpenAI service for analyzing competitor content"""
import json
import base64
from typing import Dict, Any, Optional
import openai
from config import OPENAI_API_KEY, USE_PROXY, PROXY_API_KEY, PROXY_API_URL

# Initialize OpenAI client
if USE_PROXY:
    # Using proxy API
    client = openai.OpenAI(
        api_key=PROXY_API_KEY,
        base_url=PROXY_API_URL
    )
else:
    # Using direct OpenAI API
    client = openai.OpenAI(api_key=OPENAI_API_KEY)


def analyze_image(image_path: str) -> Dict[str, Any]:
    """
    Analyze an image and return detailed competitor analysis with design scores
    """
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    prompt = """Analyze this competitor's visual content and provide a comprehensive analysis in JSON format.
    Focus on:
    1. Visual design quality and aesthetics (design_score: 0-10)
    2. Animation potential and motion design opportunities (animation_potential: 0-10)
    3. Brand identity and visual consistency
    4. Color scheme and typography
    5. Overall impression and competitive positioning
    
    Return a JSON object with the following structure:
    {
        "design_score": <integer 0-10>,
        "animation_potential": <integer 0-10>,
        "color_scheme": "<description>",
        "typography": "<description>",
        "brand_identity": "<description>",
        "visual_consistency": "<description>",
        "strengths": ["<strength1>", "<strength2>", ...],
        "weaknesses": ["<weakness1>", "<weakness2>", ...],
        "recommendations": ["<recommendation1>", "<recommendation2>", ...],
        "overall_impression": "<detailed analysis>",
        "competitive_positioning": "<positioning analysis>"
    }
    
    Be specific and provide actionable insights."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Extract JSON from response
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_str = content[json_start:json_end]
            result = json.loads(json_str)
        else:
            # Fallback: try to parse entire content
            result = json.loads(content)
        
        return {
            "success": True,
            "analysis": result,
            "raw_response": content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": None
        }


def analyze_text(text_content: str) -> Dict[str, Any]:
    """
    Analyze text content and return detailed competitor analysis
    """
    prompt = """Analyze this competitor's text content and provide a comprehensive analysis in JSON format.
    Focus on:
    1. Content quality and messaging effectiveness (design_score: 0-10 for overall presentation)
    2. Animation potential in content delivery and storytelling (animation_potential: 0-10)
    3. Tone and brand voice
    4. Key messaging and value propositions
    5. SEO and keyword usage
    6. Call-to-action effectiveness
    
    Return a JSON object with the following structure:
    {
        "design_score": <integer 0-10>,
        "animation_potential": <integer 0-10>,
        "tone": "<description>",
        "brand_voice": "<description>",
        "key_messaging": ["<message1>", "<message2>", ...],
        "value_propositions": ["<prop1>", "<prop2>", ...],
        "seo_keywords": ["<keyword1>", "<keyword2>", ...],
        "cta_effectiveness": "<description>",
        "strengths": ["<strength1>", "<strength2>", ...],
        "weaknesses": ["<weakness1>", "<weakness2>", ...],
        "recommendations": ["<recommendation1>", "<recommendation2>", ...],
        "overall_impression": "<detailed analysis>",
        "competitive_positioning": "<positioning analysis>"
    }
    
    Be specific and provide actionable insights.
    
    Text content to analyze:
    """ + text_content

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        
        return {
            "success": True,
            "analysis": result,
            "raw_response": content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": None
        }

