function fillRandomRepos() {
    const samples = [
        {
            full_name: "pallets/flask",
            forks_count: 5800, size: 3200, has_issues: true, has_projects: false,
            has_downloads: true, has_wiki: true, has_pages: false, has_discussions: true, archived: false,
            open_issues_count: 30
        },
        {
            full_name: "psf/requests",
            forks_count: 9500, size: 2000, has_issues: true, has_projects: true,
            has_downloads: true, has_wiki: false, has_pages: false, has_discussions: true, archived: false,
            open_issues_count: 12
        },
        {
            full_name: "microsoft/vscode",
            forks_count: 24000, size: 120000,  has_issues: true, has_projects: true,
            has_downloads: false, has_wiki: false, has_pages: true, has_discussions: true, archived: false,
            open_issues_count: 5000
        },
        {
            full_name: "vercel/next.js",
            forks_count: 14000, size: 62000,  has_issues: true, has_projects: false,
            has_downloads: false, has_wiki: false, has_pages: true, has_discussions: false, archived: false,
            open_issues_count: 80
        },
        {
            full_name: "numpy/numpy",
            forks_count: 7200, size: 48000, has_issues: true, has_projects: false,
            has_downloads: true, has_wiki: true, has_pages: false, has_discussions: false, archived: false,
            open_issues_count: 40
        }
    ];

    samples.forEach((repo, i) => {
        for (const [key, value] of Object.entries(repo)) {
            const el = document.getElementById(`${key}_${i + 1}`);
            if (el) {
                if (el.type === "checkbox") {
                    el.checked = value;
                } else {
                    el.value = value;
                }
            }
        }
    });
}
