import torch
import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import logging
from typing import Dict, List, Any
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CognitiveBehaviors:
    def __init__(self):
        self.curiosity_level = 0.5
        
    def apply_curiosity(self, query: str, context: Dict) -> Dict:
        curiosity_score = self._calculate_curiosity_score(query, context)
        
        if curiosity_score > 0.7:
            return {
                "behavior": "curiosity",
                "score": curiosity_score,
                "action": "ask_follow_up",
                "questions": ["Can you tell me more about your specific requirements?"]
            }
        return {"behavior": "curiosity", "score": curiosity_score, "action": "proceed"}
    
    def apply_analysis(self, query: str, history: List) -> Dict:
        technical_terms = ["hosting", "server", "bandwidth", "storage", "ssl", "email", "domain"]
        technical_density = sum(1 for term in technical_terms if term in query.lower()) / len(technical_terms)
        
        analysis_actions = []
        if technical_density > 0.3:
            analysis_actions.append("technical_analysis")
        if any(word in query.lower() for word in ["problem", "issue", "help", "support"]):
            analysis_actions.append("support_analysis")
        if any(word in query.lower() for word in ["price", "cost", "plan", "package"]):
            analysis_actions.append("pricing_analysis")
            
        return {
            "behavior": "analysis",
            "score": technical_density,
            "actions": analysis_actions
        }
    
    def _calculate_curiosity_score(self, query: str, context: Dict) -> float:
        short_queries = len(query.split()) < 5
        vague_terms = any(term in query.lower() for term in ["help", "info", "tell me", "what"])
        
        score = 0.3
        if short_queries: score += 0.3
        if vague_terms: score += 0.2
        
        return min(score, 1.0)

class AventroAIEngine:
    def __init__(self):
        logger.info("🚀 Initializing Aventro AI Engine...")
        
        try:
            # Use smaller model for free tier
            self.chat_model = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                torch_dtype=torch.float16
            )
            logger.info("✅ DialoGPT-small loaded successfully")
        except Exception as e:
            logger.warning(f"❌ DialoGPT failed: {e}")
            self.chat_model = None
            
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cognitive = CognitiveBehaviors()
        self.conversation_memory = []
        
    def generate_cognitive_response(self, user_input: str, context: Dict = None) -> Dict:
        if context is None:
            context = {}
            
        self.conversation_memory.append({"user": user_input, "timestamp": time.time()})
        
        curiosity_result = self.cognitive.apply_curiosity(user_input, context)
        analysis_result = self.cognitive.apply_analysis(user_input, self.conversation_memory[-5:])
        
        base_response = self._generate_response_based_on_analysis(user_input, analysis_result)
        final_response = self._apply_cognitive_enhancements(base_response, curiosity_result, analysis_result)
        
        return {
            "response": final_response,
            "cognitive_analysis": {
                "curiosity": curiosity_result,
                "analysis": analysis_result
            },
            "conversation_id": len(self.conversation_memory)
        }
    
    def _generate_response_based_on_analysis(self, user_input: str, analysis: Dict) -> str:
        from config import AventroConfig
        
        actions = analysis.get("actions", [])
        
        if "pricing_analysis" in actions:
            return self._generate_pricing_response()
        elif "support_analysis" in actions:
            return self._generate_support_response()
        elif "technical_analysis" in actions:
            return self._generate_technical_response()
        else:
            return self._generate_general_response()
    
    def _generate_pricing_response(self) -> str:
        from config import AventroConfig
        
        plans = AventroConfig.HOSTING_PLANS
        response = "Here are Aventro's managed hosting plans:\n\n"
        
        for plan_key, plan_info in plans.items():
            response += f"🚀 {plan_info['name']}: ${plan_info['price']}/month\n"
            response += "Features: " + ", ".join(plan_info['features'][:3]) + "\n\n"
        
        response += "All plans include expert setup and management. Which plan interests you?"
        return response
    
    def _generate_support_response(self) -> str:
        return "I understand you need support. Aventro provides comprehensive managed hosting support including migration assistance, performance optimization, and 24/7 emergency support. Could you share more details about your specific issue?"
    
    def _generate_technical_response(self) -> str:
        return "Aventro offers high-performance managed hosting with SSD storage, free SSL, expert setup, daily backups, and security monitoring. What specific technical aspects would you like to know about?"
    
    def _generate_general_response(self) -> str:
        return "Hello! I'm the Aventro AI assistant, here to help with our managed hosting services. You can ask me about pricing, features, technical support, or getting started. How can I assist you today?"
    
    def _apply_cognitive_enhancements(self, base_response: str, curiosity: Dict, analysis: Dict) -> str:
        enhanced_response = base_response
        
        if curiosity.get("action") == "ask_follow_up":
            enhanced_response += f"\n\nCan you tell me more about your specific requirements?"
        
        return enhanced_response

# Global instance
aventro_ai = AventroAIEngine()
