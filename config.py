import os

class AventroConfig:
    COMPANY_NAME = "Aventro"
    SUPPORT_EMAIL = "info@aventro.co.uk"
    WEBSITE = "https://www.aventro.co.uk"
    
    # Hosting Plans
    HOSTING_PLANS = {
        "UK": {
            "name": "Business Managed Hosting", 
            "price": 25.99£,
            "features": ["25GB SSD Storage", "Unlimited Bandwidth", "Free SSL", "Priority Support", "Daily Backups"]
        },
        "Middle East": {
            "name": "Business Managed Hosting",
            "price": 29.99$,
            "features": ["50GB SSD Storage", "Unlimited Bandwidth", "Free SSL", "24/7 Priority Support", "Daily Backups", "Security Monitoring"]
        }
    }
