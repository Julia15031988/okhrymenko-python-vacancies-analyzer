from scraper.parser import get_vacancy_links, get_vacancy_description, save_to_csv, determine_experience
from analysis.analyzer import analyze_technologies, create_chart
import time


def main():
    print("--- Starting getting the data ---")
    links = get_vacancy_links(max_pages=20)
    scraped_data = []

    for index, link in enumerate(links):
        print(f"[{index + 1}/{len(links)}] processing : {link}")
        desc = get_vacancy_description(link)

        if desc:
            level = determine_experience(desc)

            scraped_data.append({
                'url': link,
                'description': desc,
                'experience_level': level
            })

        time.sleep(1)

    save_to_csv(scraped_data)

    print("\n--- Starting analysis ---")
    levels = ["junior", "middle", "senior", "unknown"]

    for lvl in levels:
        print(f"calculating statistics for: {lvl}")
        stats = analyze_technologies(level=lvl)
        if any(stats.values()):
            create_chart(stats, level_name=lvl)
        else:
            print(f"For level {lvl} not enough data for the graph.")


if __name__ == "__main__":
    main()
