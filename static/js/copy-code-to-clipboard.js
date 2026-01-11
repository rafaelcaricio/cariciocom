// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const codeBlocks = document.querySelectorAll("pre code[data-lang]");

    for (const codeBlock of codeBlocks) {
        // Skip if button already exists
        const preElement = codeBlock.parentElement;
        if (preElement.querySelector('.copy-button')) {
            continue;
        }

        let content;
        if (preElement.hasAttribute("data-linenos")) {
            content = [...codeBlock.querySelectorAll("tr")]
                .map((row) => row.querySelector("td:last-child")?.innerText ?? "")
                .join("");
        } else {
            content = codeBlock.innerText.split("\n").filter(Boolean).join("\n");
        }

        if (navigator.clipboard !== undefined) {
            const copyButton = document.createElement("button");
            copyButton.classList.add("copy-button");
            copyButton.innerText = "Copy";

            copyButton.addEventListener("click", () => {
                copyButton.innerText = "Copied!";
                navigator.clipboard.writeText(content);
                setTimeout(() => copyButton.innerText = "Copy", 1000);
            });

            // Insert as first child of <pre> element for correct positioning
            preElement.insertBefore(copyButton, preElement.firstChild);
        }
    }
});
