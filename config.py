import os

class AventroConfig:
    COMPANY_NAME = "Aventro"
    SUPPORT_EMAIL = "info@aventro.co.uk"
    WEBSITE = "https://www.aventro.co.uk"
    
    # Hosting Plans
    HOSTING_PLANS = {
        "starter": {
            "name": "Starter Managed Hosting",
            "price": 29.99,
            "features": ["10GB SSD Storage", "Unlimited Bandwidth", "Free SSL", "Email Setup", "Basic Support"]
        },
        "business": {
            "name": "Business Managed Hosting", 
            "price": 59.99,
            "features": ["25GB SSD Storage", "Unlimited Bandwidth", "Free SSL", "Priority Support", "Daily Backups"]
        },
        "enterprise": {
            "name": "Enterprise Managed Hosting",
            "price": 99.99,
            "features": ["50GB SSD Storage", "Unlimited Bandwidth", "Free SSL", "24/7 Priority Support", "Daily Backups", "Security Monitoring"]
        }
    }
