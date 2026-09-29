function copyPlan() {

    const plan = document.getElementById("plan");

    if (!plan) {
        return;
    }

    navigator.clipboard
        .writeText(plan.innerText)
        .then(() => {

            alert(
                "Plan copied to clipboard."
            );

        })
        .catch(() => {

            alert(
                "Copy failed. Select the plan manually."
            );

        });
}