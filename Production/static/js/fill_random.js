function fillRandomRepos() {
    const samples = [
        {
            full_name: "mdeff/fma",
            forks_count: 447,
            size: 20019,
            has_issues: true,
            has_projects: true,
            has_downloads: true,
            has_wiki: true,
            has_pages: false,
            has_discussions: false,
            archived: false,
            open_issues_count: 1
        },
        {
            full_name: "donnemartin/system-design-primer",
            forks_count: 50000,
            size: 2000,
            has_issues: true,
            has_projects: true,
            has_downloads: true,
            has_wiki: true,
            has_pages: false,
            has_discussions: true,
            archived: false,
            open_issues_count: 238
        },
        {
            full_name: "jakevdp/PythonDataScienceHandbook",
            forks_count: 18300,
            size: 50000,
            has_issues: true,
            has_projects: false,
            has_downloads: true,
            has_wiki: false,
            has_pages: true,
            has_discussions: false,
            archived: false,
            open_issues_count: 121
        },
        {
            full_name: "ageron/handson-ml2",
            forks_count: 13000,
            size: 60000,
            has_issues: true,
            has_projects: true,
            has_downloads: true,
            has_wiki: false,
            has_pages: true,
            has_discussions: false,
            archived: false,
            open_issues_count: 19
        },
        {
            full_name: "danielgatis/rembg",
            forks_count: 2000,
            size: 12000,
            has_issues: true,
            has_projects: false,
            has_downloads: true,
            has_wiki: false,
            has_pages: false,
            has_discussions: true,
            archived: false,
            open_issues_count: 3
        },
        {
            full_name: "thomasnield/kotlin-statistics",
            forks_count: 320,
            size: 1800,
            has_issues: true,
            has_projects: false,
            has_downloads: true,
            has_wiki: true,
            has_pages: false,
            has_discussions: false,
            archived: false,
            open_issues_count: 0
        },
        {
            full_name: "huggingface/transformers",
            forks_count: 29100,
            size: 650000,
            has_issues: true,
            has_projects: true,
            has_downloads: true,
            has_wiki: false,
            has_pages: true,
            has_discussions: true,
            archived: false,
            open_issues_count: 1100
        },
        {
            full_name: "pytorch/ignite",
            forks_count: 4700,
            size: 28000,
            has_issues: true,
            has_projects: true,
            has_downloads: true,
            has_wiki: true,
            has_pages: true,
            has_discussions: true,
            archived: false,
            open_issues_count: 112
        },
        {
            full_name: "jwasham/coding-interview-university",
            forks_count: 78900,
            size: 4000,
            has_issues: true,
            has_projects: false,
            has_downloads: false,
            has_wiki: false,
            has_pages: false,
            has_discussions: true,
            archived: false,
            open_issues_count: 59
        },
        {
            full_name: "rwightman/pytorch-image-models",
            forks_count: 4900,
            size: 160000,
            has_issues: true,
            has_projects: true,
            has_downloads: true,
            has_wiki: false,
            has_pages: true,
            has_discussions: true,
            archived: false,
            open_issues_count: 49
        }
    ];

    // Select 5 random repositories
    const selected = samples.sort(() => 0.5 - Math.random()).slice(0, 5);

    selected.forEach((repo, i) => {
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
