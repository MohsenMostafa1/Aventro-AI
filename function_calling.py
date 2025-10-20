import time
from typing import Dict

class AventroFunctionCaller:
    def __init__(self):
        self.available_functions = {
            "get_hosting_plans": self.get_hosting_plans,
            "calculate_pricing": self.calculate_pricing,
            "schedule_consultation": self.schedule_consultation
        }
    
    def execute_function(self, function_name: str, parameters: Dict) -> Dict:
        try:
            if function_name in self.available_functions:
                result = self.available_functions[function_name](parameters)
                return {
                    "success": True,
                    "function_name": function_name,
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": f"Function {function_name} not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_hosting_plans(self, params: Dict) -> Dict:
        from config import AventroConfig
        return AventroConfig.HOSTING_PLANS
    
    def calculate_pricing(self, params: Dict) -> Dict:
        from config import AventroConfig
        
        plan_type = params.get("plan_type", "starter")
        duration_months = params.get("duration", 1)
        plans = AventroConfig.HOSTING_PLANS
        
        if plan_type not in plans:
            return {"error": f"Plan {plan_type} not found"}
        
        monthly_price = plans[plan_type]["price"]
        total_price = monthly_price * duration_months
        
        if duration_months >= 12:
            total_price *= 0.8
            discount_applied = True
        else:
            discount_applied = False
        
        return {
            "plan": plans[plan_type]["name"],
            "monthly_price": monthly_price,
            "total_price": round(total_price, 2),
            "discount_applied": discount_applied
        }
    
    def schedule_consultation(self, params: Dict) -> Dict:
        name = params.get("name", "Guest")
        email = params.get("email", "")
        
        return {
            "consultation_id": f"CONS_{int(time.time())}",
            "name": name,
            "email": email,
            "status": "scheduled",
            "message": f"Consultation scheduled for {name}.",
            "next_steps": "Our team will contact you within 24 hours."
        }

function_caller = AventroFunctionCaller()
