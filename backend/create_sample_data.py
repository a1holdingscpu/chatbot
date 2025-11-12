import pandas as pd
import random

# Create sample real estate deals
deals = []

property_types = ['residential', 'commercial', 'land', 'rv_park', 'mobile_home_park']
addresses = [
    '123 Main St, Austin TX',
    '456 Oak Ave, Dallas TX',
    '789 Pine Rd, Houston TX',
    '321 Elm St, San Antonio TX',
    '654 Maple Dr, Fort Worth TX',
    '987 Cedar Ln, El Paso TX',
    '147 Birch Way, Arlington TX',
    '258 Walnut Ct, Plano TX',
    '369 Ash Blvd, Irving TX',
    '741 Spruce Pl, Garland TX'
]

for i in range(10):
    price = random.randint(150000, 800000)
    monthly_rent = price * random.uniform(0.006, 0.012)
    
    deal = {
        'address': addresses[i],
        'property_type': random.choice(property_types),
        'price': price,
        'monthly_rent': monthly_rent,
        'arv': price * random.uniform(1.1, 1.4),
        'estimated_rehab': price * random.uniform(0.05, 0.20),
        'beds': random.randint(2, 5),
        'baths': random.randint(1, 3),
        'sqft': random.randint(1000, 3000),
        'units': random.randint(1, 4),
        'occupancy_pct': random.uniform(75, 95),
        'lot_size_acres': random.uniform(0.1, 2.0),
        'taxes': price * 0.012,
        'insurance': price * 0.008,
        'assignment_allowed': random.choice([True, False]),
        'subject_to_possible': random.choice([True, False]),
        'seller_finance_available': random.choice([True, False]),
        'days_on_market': random.randint(5, 120)
    }
    deals.append(deal)

df = pd.DataFrame(deals)
df.to_excel('/app/data/sample_deals.xlsx', index=False)
print(f"Created sample data with {len(df)} deals")
print(df[['address', 'price', 'monthly_rent', 'property_type']].head())
