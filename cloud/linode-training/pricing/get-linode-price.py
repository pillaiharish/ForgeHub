import requests

LINODE_API_URL = "https://api.linode.com/v4/linode/types"

def get_gpu_pricing():
    response = requests.get(LINODE_API_URL)
    data = response.json()
    
    gpu_instances = [plan for plan in data['data'] if "gpu" in plan['id']]
    for instance in gpu_instances:
        hourly_cost = instance["price"]["hourly"]
        monthly_cost = instance["price"]["monthly"]
        print(f"Instance: {instance['id']}, Hourly: ${hourly_cost}, Monthly: ${monthly_cost}")

get_gpu_pricing()



# harish $ python get-linode-price.py 
# Instance: g1-gpu-rtx6000-1, Hourly: $1.5, Monthly: $1000.0
# Instance: g1-gpu-rtx6000-2, Hourly: $3.0, Monthly: $2000.0
# Instance: g1-gpu-rtx6000-3, Hourly: $4.5, Monthly: $3000.0
# Instance: g1-gpu-rtx6000-4, Hourly: $6.0, Monthly: $4000.0
# Instance: g2-gpu-rtx4000a1-s, Hourly: $0.52, Monthly: $350.0
# Instance: g2-gpu-rtx4000a1-m, Hourly: $0.67, Monthly: $446.0
# Instance: g2-gpu-rtx4000a1-l, Hourly: $0.96, Monthly: $638.0
# Instance: g2-gpu-rtx4000a1-xl, Hourly: $1.53, Monthly: $1022.0
# Instance: g2-gpu-rtx4000a2-s, Hourly: $1.05, Monthly: $700.0
# Instance: g2-gpu-rtx4000a2-m, Hourly: $1.34, Monthly: $892.0
# Instance: g2-gpu-rtx4000a2-hs, Hourly: $1.49, Monthly: $992.0
# Instance: g2-gpu-rtx4000a4-s, Hourly: $2.96, Monthly: $1976.0
# Instance: g2-gpu-rtx4000a4-m, Hourly: $3.57, Monthly: $2384.0



# Recommendation:

# For cost-effectiveness, use RTX 6000 ($1.39 for 10 hours)
# For faster training, use A100 ($2.78 for 10 hours)