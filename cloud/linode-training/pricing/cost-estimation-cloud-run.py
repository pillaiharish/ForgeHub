import requests

# Define Linode GPU pricing (update if needed)
LINODE_GPU_PRICING = {
    "g6-gpu-rtx6000-1": 100.0,  # 1x RTX 6000 (24GB VRAM) - $100/month
    "g6-gpu-rtx6000-2": 200.0,  # 2x RTX 6000 - $200/month
    "g6-gpu-a100-1": 200.0,      # 1x A100 (40GB VRAM) - $200/month
    "g6-gpu-a100-2": 400.0,      # 2x A100 - $400/month
}

def calculate_cost(gpu_type, training_hours):
    """Calculate cost based on selected GPU and training time"""
    if gpu_type not in LINODE_GPU_PRICING:
        print("Invalid GPU type. Choose from:", list(LINODE_GPU_PRICING.keys()))
        return
    
    monthly_cost = LINODE_GPU_PRICING[gpu_type]
    hourly_cost = monthly_cost / (30 * 24)  # Convert monthly price to hourly
    
    estimated_cost = hourly_cost * training_hours
    print(f"Estimated cost for {training_hours} hours on {gpu_type}: ${estimated_cost:.2f}")

gpu_type = "g6-gpu-rtx6000-1"   # Cheapest option
training_hours = 10  # Adjust this based on expected training time

calculate_cost(gpu_type, training_hours)

# harish $  python cost-estimation-cloud-run.py 
# Estimated cost for 10 hours on g6-gpu-rtx6000-1: $1.39