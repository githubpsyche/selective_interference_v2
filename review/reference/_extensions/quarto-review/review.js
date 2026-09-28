/* Boundary elements allow overlapping comments without invalid HTML nesting. */
document.addEventListener("DOMContentLoaded", () => {
  const panel = document.getElementById("quarto-review");
  if (!panel) return;
  const active = new Map();
  const root = document.querySelector("main") || document.body;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  const threadIds = new Set([...panel.querySelectorAll(".qr-thread")].map(node => node.dataset.reviewId));
  for (const node of nodes) {
    if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains("qr-boundary")) {
      const {reviewKind: kind, reviewId: id, reviewEdge: edge} = node.dataset;
      const key = `${kind}:${id}`;
      if (edge === "S") {
        active.set(key, {kind, id});
        if (!document.getElementById(`qr-anchor-${id}`)) node.id = `qr-anchor-${id}`;
        if (kind === "C" && threadIds.has(id)) {
          const link = document.createElement("a");
          link.className = "qr-link";
          link.href = `#qr-thread-${id}`;
          link.textContent = id;
          link.setAttribute("aria-label", `Read comment ${id}`);
          node.after(link);
        }
      } else active.delete(key);
      continue;
    }
    const math = node.nodeType === Node.ELEMENT_NODE && node.classList.contains("math");
    const text = node.nodeType === Node.TEXT_NODE && node.textContent.length > 0;
    if ((!math && !text) || active.size === 0) continue;
    if (node.parentElement?.closest(".math,script,style,.qr-panel,.qr-controls")) continue;
    const span = document.createElement("span");
    const entries = [...active.values()];
    span.classList.add("qr-mark");
    if (entries.some(item => item.kind === "I")) span.classList.add("qr-insert");
    if (entries.some(item => item.kind === "D")) span.classList.add("qr-delete");
    if (entries.some(item => item.kind === "C")) span.classList.add("qr-comment");
    span.dataset.reviewIds = entries.map(item => item.id).join(" ");
    node.replaceWith(span);
    span.append(node);
  }
  for (const block of root.querySelectorAll("p,li,figcaption")) {
    if (block.closest(".qr-panel") || block.querySelector(".qr-link")) continue;
    const textWalker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
    const content = [];
    while (textWalker.nextNode()) {
      if (textWalker.currentNode.textContent.trim()) content.push(textWalker.currentNode);
    }
    if (!content.length && block.querySelector(".qr-boundary")) block.classList.add("qr-boundary-block");
    for (const kind of ["insert", "delete"]) {
      if (content.length && content.every(node => node.parentElement.closest(`.qr-${kind}`))) {
        block.classList.add(`qr-${kind}-block`);
      }
    }
  }
  const controls = panel.querySelector(".qr-controls");
  root.prepend(controls);
  const items = [...panel.querySelectorAll(".qr-thread,.qr-suggestion")];
  const threads = items.filter(node => node.classList.contains("qr-thread"));
  const view = controls.querySelector("#qr-view");
  const author = controls.querySelector("#qr-author");
  const status = controls.querySelector("#qr-status");
  function update() {
    document.body.dataset.reviewView = view.value;
    const visible = new Set();
    for (const item of items) {
      const match = (!author.value || item.dataset.author.split("\n").includes(author.value)) && (!status.value || status.value === item.dataset.status);
      item.hidden = !match;
      if (match) {
        visible.add(item.dataset.reviewId);
        if (item.dataset.anchorId) visible.add(item.dataset.anchorId);
      }
    }
    for (const mark of root.querySelectorAll(".qr-mark")) {
      mark.classList.toggle("qr-filtered", Boolean(author.value || status.value) && !mark.dataset.reviewIds.split(" ").some(id => visible.has(id)));
    }
    controls.querySelector("#qr-count").textContent = `${threads.filter(item => !item.hidden).length} comments shown`;
    current = -1;
  }
  let current = -1;
  function navigate(direction) {
    const available = threads.filter(item => !item.hidden);
    if (available.length === 0) return;
    current = current < 0 ? (direction > 0 ? 0 : available.length - 1)
      : (current + direction + available.length) % available.length;
    const id = available[current].dataset.reviewId;
    const anchor = document.getElementById(`qr-anchor-${id}`);
    (anchor || available[current]).scrollIntoView({block: "center"});
  }
  for (const element of [view, author, status]) element.addEventListener("change", update);
  controls.querySelector("#qr-next").addEventListener("click", () => navigate(1));
  controls.querySelector("#qr-previous").addEventListener("click", () => navigate(-1));
  update();
});
