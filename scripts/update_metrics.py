import os
import re
import json
import urllib.request

USERNAME = "Madhu-36"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def fetch_data():
    # 1. Fetch Streak Stats from demolab
    try:
        streak_req = urllib.request.Request(
            f"https://streak-stats.demolab.com?user={USERNAME}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        streak_html = urllib.request.urlopen(streak_req, timeout=15).read().decode("utf-8")
        numbers = re.findall(r'<text[^>]*>\s*([0-9,]+)\s*</text>', streak_html)
        total_contribs = numbers[0] if len(numbers) > 0 else "1,510"
        current_streak = numbers[1] if len(numbers) > 1 else "24"
        longest_streak = numbers[2] if len(numbers) > 2 else "35"
    except Exception as e:
        print(f"Warning fetching streak stats: {e}")
        total_contribs = "1,510"
        current_streak = "24"
        longest_streak = "35"

    # 2. Fetch Total Commits from GitHub API
    total_commits_raw = 1824
    try:
        headers = {
            "Accept": "application/vnd.github.cloak-preview",
            "User-Agent": "Mozilla/5.0"
        }
        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"
        
        commit_req = urllib.request.Request(
            f"https://api.github.com/search/commits?q=author:{USERNAME}",
            headers=headers
        )
        commit_data = json.loads(urllib.request.urlopen(commit_req, timeout=15).read().decode("utf-8"))
        if "total_count" in commit_data:
            total_commits_raw = commit_data["total_count"]
    except Exception as e:
        print(f"Warning fetching commits: {e}")

    total_commits_fmt = f"{total_commits_raw:,}"
    if total_commits_raw >= 1000:
        total_commits_short = f"{total_commits_raw / 1000:.1f}k+"
    else:
        total_commits_short = str(total_commits_raw)

    print(f"Live Metrics: Streak={current_streak}, Longest={longest_streak}, Contribs={total_contribs}, Commits={total_commits_raw} ({total_commits_short})")
    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_contribs": total_contribs,
        "total_commits_raw": total_commits_raw,
        "total_commits_fmt": total_commits_fmt,
        "total_commits_short": total_commits_short,
    }

def generate_badges(metrics):
    os.makedirs("dist", exist_ok=True)
    
    badges = {
        "dist/streak.json": {
            "schemaVersion": 1,
            "label": "Current Streak",
            "message": f"{metrics['current_streak']} Days 🔥",
            "color": "FF5722",
            "logo": "fire",
            "logoColor": "white"
        },
        "dist/longest_streak.json": {
            "schemaVersion": 1,
            "label": "Longest Streak",
            "message": f"{metrics['longest_streak']} Days ⚡",
            "color": "0A66C2",
            "logo": "speedtest",
            "logoColor": "white"
        },
        "dist/contributions.json": {
            "schemaVersion": 1,
            "label": "Total Contributions",
            "message": f"{metrics['total_contribs']} 🚀",
            "color": "7928CA",
            "logo": "github",
            "logoColor": "white"
        },
        "dist/commits.json": {
            "schemaVersion": 1,
            "label": "Total Commits",
            "message": f"{metrics['total_commits_short']} 💻",
            "color": "00C7B7",
            "logo": "git",
            "logoColor": "white"
        }
    }
    
    for path, data in badges.items():
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Wrote {path}")

def update_readme(metrics):
    if not os.path.exists("README.md"):
        return
        
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Update YAML identity block
    content = re.sub(
        r'current_streak:\s*"[^"]*"',
        f'current_streak: "{metrics["current_streak"]}+ Days (Active)"',
        content
    )
    content = re.sub(
        r'longest_streak:\s*"[^"]*"',
        f'longest_streak: "{metrics["longest_streak"]} Days"',
        content
    )
    content = re.sub(
        r'total_contributions:\s*"[^"]*"',
        f'total_contributions: "{metrics["total_contribs"]}+"',
        content
    )
    content = re.sub(
        r'total_commits:\s*"[^"]*"',
        f'total_commits: "{metrics["total_commits_fmt"]} ({metrics["total_commits_short"]})"',
        content
    )

    # Update Table rows
    content = re.sub(
        r'(\|\s*🔥\s*\*\*Current Active Streak\*\*\s*\|\s*\*\*)[^*]*(\*\*)',
        f'\\g<1>{metrics["current_streak"]}+ Days\\g<2>',
        content
    )
    content = re.sub(
        r'(\|\s*⚡\s*\*\*Longest Streak\*\*\s*\|\s*\*\*)[^*]*(\*\*)',
        f'\\g<1>{metrics["longest_streak"]} Days\\g<2>',
        content
    )
    content = re.sub(
        r'(\|\s*📈\s*\*\*Total Contributions\*\*\s*\|\s*\*\*)[^*]*(\*\*)',
        f'\\g<1>{metrics["total_contribs"]}+\\g<2>',
        content
    )
    content = re.sub(
        r'(\|\s*💻\s*\*\*Total Git Commits\*\*\s*\|\s*\*\*)[^*]*(\*\*)',
        f'\\g<1>{metrics["total_commits_fmt"]} ({metrics["total_commits_short"]})\\g<2>',
        content
    )
        
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("README.md updated with live metric values")

if __name__ == "__main__":
    m = fetch_data()
    generate_badges(m)
    update_readme(m)
