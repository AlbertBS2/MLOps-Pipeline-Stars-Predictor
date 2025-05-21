function fillRandomRepos() {
    console.log("fill_random.js loaded!");

    const repos = [
        "pallets/flask",
        "psf/requests",
        "django/django",
        "tiangolo/fastapi",
        "numpy/numpy",
        "scikit-learn/scikit-learn",
        "huggingface/transformers",
        "torvalds/linux",
        "microsoft/vscode",
        "vercel/next.js"
    ];

    const selected = repos.sort(() => 0.5 - Math.random()).slice(0, 5);

    for (let i = 0; i < 5; i++) {
        const input = document.getElementById(`repo_${i + 1}`);
        if (input) {
            input.value = selected[i];
        }
    }
}
