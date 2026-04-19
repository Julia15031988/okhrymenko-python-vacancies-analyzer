import pandas as pd
import matplotlib.pyplot as plt
import os
from config import TECHNOLOGIES, DATA_FILE


def analyze_technologies(level=None):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, DATA_FILE)

    if not os.path.exists(full_path):
        print(f"Error: File {full_path} not found!")
        return {tech: 0 for tech in TECHNOLOGIES}

    df = pd.read_csv(full_path)

    if level and level != "all":
        df = df[df['experience_level'] == level]

    results = {tech: 0 for tech in TECHNOLOGIES}

    for description in df['description']:
        desc_lower = str(description).lower()
        for tech in TECHNOLOGIES:
            if tech.lower() in desc_lower:
                results[tech] += 1

    return results


def create_chart(data, level_name="all"):
    filtered_data = {k: v for k, v in data.items() if v > 0}
    if not filtered_data:
        print(f"No data to visualize: {level_name}")
        return

    sorted_data = dict(sorted(filtered_data.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(12, 7))
    plt.bar(list(sorted_data.keys()), list(sorted_data.values()), color='skyblue')

    plt.xlabel('Technologies')
    plt.ylabel('Number of vacancies')
    plt.title(f'Popular technologies for the level: {level_name.upper()}')
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_filename = f"data/chart_{level_name}.png"
    plt.savefig(chart_filename)
    print(f"✅ The schedule is saved: {chart_filename}")

    plt.close()

