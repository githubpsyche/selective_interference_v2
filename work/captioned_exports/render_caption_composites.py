from pathlib import Path
import textwrap

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = Path(__file__).resolve().parent
CAPTION_EXPORT_DIR = WORK_DIR

FIG_WIDTH = 10.8
TITLE_FONTSIZE = 13
BODY_FONTSIZE = 10.5
WRAP_WIDTH = 142
TITLE_GAP = 0.045
LINE_STEP = 0.030
TOP_CAPTION_GAP = 0.080

# Manuscript-facing figure font hierarchy:
# raw SVG schematics use 44 panel letters, 27-28 panel titles,
# 24 primary structural labels, 21 row/column/block labels, and
# 18 only for secondary subtitles that do not carry the main reading path.
# Row descriptions that define a condition should use 21. Matplotlib simulation figures use
# 16 panel letters, 13 panel titles, 11 axis/structural labels, and 10
# tick, legend, and phase-band labels.


CAPTIONED_FIGURES = [
    {
        "image": ROOT / "work" / "empirical_target" / "empirical_target_composite.png",
        "output": CAPTION_EXPORT_DIR / "empirical_target_composite_with_caption",
        "title": "Modeled trauma-film paradigm and schematic selective-interference pattern.",
        "body": (
            "(A) The modeled trauma-film paradigm includes film encoding, an intervening delay, a possible pre-task film reminder, "
            "an intervening task, a post-task delay, and a later test of unguided or deliberate film recall. "
            "(B) The qualitative pattern targeted by the recall simulations is summarized as an interaction among reminder condition, "
            "intervening task, and retrieval condition. "
            "Columns distinguish whether the task is preceded by a film reminder, rows distinguish unguided film recall from "
            "deliberate film recall, and paired bars compare film recall after a comparison/control condition versus a visuospatial task condition. "
            "The visuospatial task condition produces the largest reduction in unguided film recall when it follows a film reminder, "
            "whereas deliberate film recall shows a smaller reduction under the same conditions. "
            "Bars are schematic and do not plot empirical counts, fitted values, or model output."
        ),
    },
    {
        "image": ROOT / "work" / "retrieved_context_account" / "retrieved_context_encoding_associations_composite.png",
        "output": CAPTION_EXPORT_DIR / "retrieved_context_encoding_associations_composite_with_caption",
        "title": "Encoding and associative structure in the retrieved-context account.",
        "body": (
            "(A) The model stores bidirectional item-context associations. "
            "Context-to-feature associations cue candidate items from the current context, and feature-to-context associations "
            "reinstate context when an item is recalled or when a reminder or test cue is presented. "
            "(B) The interference manipulation changes which context states task items are linked to during encoding. "
            "Without a pre-task reminder, task items are encoded after context has drifted away from the film. "
            "With a pre-task film reminder, film-associated context is reinstated before task encoding, so task items are "
            "learned while that context remains active. "
            "Thus, the same context that can cue film items can also cue task competitors during later retrieval. "
            "When task encoding is strong, those task items become stronger competitors during later context-guided retrieval. "
            "Circles mark item features: F labels film items and T labels task items. "
            "Squares mark context states. "
            "Blue marks film items or film-linked context, orange marks task items or task-linked context, green marks reminder cues, "
            "and gray marks neutral, delay, comparison, or shared model structure."
        ),
    },
    {
        "image": ROOT / "work" / "retrieved_context_account" / "retrieved_context_retrieval_operations_composite.png",
        "output": CAPTION_EXPORT_DIR / "retrieved_context_retrieval_operations_composite_with_caption",
        "title": "Retrieval operations in the retrieved-context account.",
        "body": (
            "(A) The upper box represents stored film and task associations; the lower boxes compare the context state used to begin "
            "unguided retrieval and deliberate recall. "
            "Stored film and task associations can be sampled from different starting contexts. "
            "Unguided retrieval begins from ongoing context, which can support film and task candidates together. "
            "Deliberate recall can begin with start-of-film context reinstatement, which favors film candidates while leaving task "
            "candidates possible. "
            "(B) During context-to-feature sampling, ongoing context can support film items and task competitors, while a maintained "
            "film-category cue adds support only to film candidates. "
            "(C) Rows compare film recall, unmonitored task recall, and monitored task recall. "
            "Sampled outputs update the next retrieval context through feature-to-context memory. "
            "Recalling a film item keeps later search biased toward film candidates. "
            "Recalling a task item without monitoring can shift later context toward task candidates. "
            "With retrieval monitoring, the task-item update is dampened, preserving some film-candidate support. "
            "Blue marks film items, film-biased context, or stronger film support; orange marks task items, task-biased context, or "
            "stronger task support; gray marks shared context and associative operations. "
            "Dashed outlines or arrows mark weaker support or dampened updating, not unavailable candidates."
        ),
    },
    {
        "image": ROOT / "work" / "simulation1_unguided_cued" / "simulation1_unguided_cued_sequence_summary.png",
        "output": CAPTION_EXPORT_DIR / "simulation1_unguided_cued_sequence_summary_with_caption",
        "title": "Simulation 1: unguided film recall by reminder condition and task encoding strength.",
        "body": (
            "Reminder condition and task encoding strength were crossed while retrieval mode was held unguided; weak film cues were "
            "supplied periodically during recall in every condition. "
            "(A) Example generated recall sequences for each condition. Each row shows one simulated trial selected near the "
            "condition mean for the number of film items recalled; recalled items are ordered left to right by output position. Colors mark film items, task items, "
            "delay/filler items, and unfilled output positions. "
            "(B) Mean number of film items recalled across all simulated trials. "
            "Film recall was lowest when a film reminder preceded strong task encoding, isolating the unguided-retrieval "
            "component of the selective interference effect."
        ),
    },
    {
        "image": ROOT / "work" / "simulation1_unguided_cued" / "simulation1_unguided_cued_recall_distributions.png",
        "output": CAPTION_EXPORT_DIR / "simulation1_unguided_cued_recall_distributions_with_caption",
        "title": "Simulation 1: reminder-linked task encoding redistributes recall probability by encoded position.",
        "body": (
            "Reminder condition and task encoding strength were crossed while retrieval was held unguided; weak film cues were "
            "supplied periodically during recall in all conditions. "
            "(A) Without a pre-task film reminder, recall probability by encoded position changes only modestly when task encoding "
            "is strengthened. "
            "(B) With a pre-task film reminder, strong task encoding reduces recall from film positions and increases recall from "
            "task positions. Curves compare weak and strong task encoding; shaded bands mark film, break, task, and filler positions, "
            "and the green vertical line marks the pre-task film reminder. "
            "Task encoding strength therefore changes recall probability by encoded position most clearly when task encoding follows "
            "a film reminder."
        ),
    },
    {
        "image": ROOT / "work" / "simulation1_unguided_cued" / "simulation1_unguided_cued_context_overlap.png",
        "output": CAPTION_EXPORT_DIR / "simulation1_unguided_cued_context_overlap_with_caption",
        "title": "Simulation 1: reminder reinstatement increases similarity between film- and task-encoding contexts.",
        "body": (
            "Reminder condition was varied before task encoding while retrieval was held unguided. "
            "(A) Mean context similarity between each encoded film position and the task-encoding period, averaging across encoded "
            "task positions. "
            "(B) Full film-by-task context-similarity matrices for the same conditions; each cell compares the context state associated "
            "with one encoded film position to the context state active at one encoded task position. "
            "Brighter cells indicate greater context similarity. "
            "The film reminder increases similarity between film-encoding and task-encoding contexts, especially for later film positions "
            "and early task positions."
        ),
    },
    {
        "image": ROOT / "work" / "simulation2_control_cued_behavioral" / "simulation2_control_cued_behavioral.png",
        "output": CAPTION_EXPORT_DIR / "simulation2_control_cued_behavioral_with_caption",
        "title": "Simulation 2: deliberate film recall is protected from reminder-linked task interference.",
        "body": (
            "Reminder condition and task encoding strength were crossed as in Simulation 1 while retrieval mode was varied between "
            "unguided film recall and deliberate film recall. "
            "Deliberate film recall combined start-of-film context reinstatement, a maintained film-category cue, and retrieval monitoring. "
            "Weak film cues were supplied periodically during recall in all conditions. "
            "Rows compare retrieval modes, columns compare reminder conditions, and paired bars compare weak versus strong task "
            "encoding. "
            "Strong task encoding reduced film recall most clearly when it followed a film reminder, but this reduction was much "
            "larger under unguided film recall than under deliberate film recall. "
            "The model therefore simulates a selective interference effect: strong task encoding after a film reminder strongly "
            "reduces unguided film recall while leaving deliberate film recall relatively preserved."
        ),
    },
    {
        "image": ROOT / "work" / "simulation2_retrieval_control_decomposition" / "simulation2_retrieval_control_decomposition.png",
        "output": CAPTION_EXPORT_DIR / "simulation2_retrieval_control_decomposition_with_caption",
        "title": "Simulation 2: different retrieval controls preserve film recall to different degrees.",
        "body": (
            "Each control setting was evaluated in two conditions: a low-interference condition with no pre-task reminder and weak "
            "task encoding, and a high-interference condition with a pre-task film reminder and strong task encoding. "
            "Weak film cues were supplied periodically during recall in all conditions. "
            "Unguided film recall includes none of the three deliberate-control operations. "
            "Bars show mean number of film items recalled for each control setting in both conditions. "
            "Start-of-film reinstatement and retrieval monitoring increase film recall in some conditions, but the loss from the low- "
            "to high-interference condition is smallest when a maintained film-category cue is included."
        ),
    },
    {
        "image": ROOT / "work" / "simulation2_start_context_reinstatement" / "simulation2_start_context_reinstatement.png",
        "output": CAPTION_EXPORT_DIR / "simulation2_start_context_reinstatement_with_caption",
        "title": "Simulation 2: start-of-film context reinstatement protects early encoded film positions.",
        "body": (
            "Unguided recall was compared with start-of-film context reinstatement while the condition with a pre-task film reminder "
            "and strong task encoding was held fixed and retrieval monitoring was disabled. "
            "Start-of-film context reinstatement initializes retrieval by drifting the current context toward the state present at the "
            "start of film encoding. "
            "Weak film cues were supplied periodically during recall. "
            "Shaded bands mark film, break, task, and filler positions; the green line marks the reminder immediately before the "
            "task phase. "
            "(A) Item accessibility before the first recall attempt. "
            "Reinstatement increases accessibility most strongly for early encoded film positions. "
            "(B) First recall probability distribution. Reinstatement shifts recall initiation toward early film positions. "
            "(C) Full recall probability distribution. The early-film bias remains visible across the recall period, while later film "
            "positions remain more vulnerable when strong task encoding follows a film reminder. "
            "Start-of-film context reinstatement therefore protects early encoded film positions by shifting retrieval initiation toward "
            "the start of the film sequence."
        ),
    },
    {
        "image": ROOT / "work" / "simulation2_target_monitoring_diagnostic" / "simulation2_target_monitoring_diagnostic.png",
        "output": CAPTION_EXPORT_DIR / "simulation2_target_monitoring_diagnostic_with_caption",
        "title": "Simulation 2: retrieval monitoring supports return to film recall.",
        "body": (
            "The condition with a pre-task film reminder and strong task encoding was held fixed, start-of-film context reinstatement "
            "was present, and retrieval monitoring strength was varied. "
            "Retrieval monitoring dampens context updating after non-film samples during deliberate recall. "
            "Weak film cues were supplied periodically during recall. "
            "(A) Model-diagnostic probability that a non-film sample was followed by recall of a film item as retrieval monitoring increased. "
            "(B) Recall probability by encoded position with no retrieval monitoring versus the moderate retrieval-monitoring setting used "
            "in the Simulation 2 anchor figure. "
            "Shaded bands mark film, break, task, and filler positions; the green line marks the reminder immediately before the "
            "task phase. "
            "Retrieval monitoring therefore supports film recall after search is pulled away from the film sequence, increasing film "
            "recall probability when strong task encoding follows a film reminder."
        ),
    },
    {
        "image": ROOT / "work" / "simulation2_film_retrieval_goal_context_overlap" / "simulation2_film_retrieval_goal_context_overlap.png",
        "output": CAPTION_EXPORT_DIR / "simulation2_film_retrieval_goal_context_overlap_with_caption",
        "title": "Simulation 2: a maintained film-category cue makes film-directed retrieval cues less similar to task-encoding context.",
        "body": (
            "The high-interference condition was held fixed: a film reminder preceded strong task encoding, and weak film cues were "
            "supplied periodically during recall. "
            "A maintained film-category cue supports film items during deliberate recall and is distinct from the external film reminder "
            "and test-phase film cues. "
            "(A) Mean similarity between task-encoding contexts and film-directed retrieval cues, averaging across encoded task "
            "positions for each encoded film position. "
            "(B) Full similarity matrices for the same condition. "
            "The left matrix uses temporal context alone; the right matrix schematically adds the maintained film-category cue to "
            "the film-directed retrieval cue. "
            "Brighter cells indicate greater similarity to task-encoding context. "
            "Adding the maintained film-category cue reduces similarity between film-directed retrieval cues and task-encoding contexts, "
            "providing a route to film recall that depends less on temporal context remaining selective for film items."
        ),
    },
    {
        "image": ROOT / "work" / "simulation4_recognition_full_figure" / "item_context_recognition.png",
        "output": CAPTION_EXPORT_DIR / "item_context_recognition_with_caption",
        "title": "Item-to-context retrieval bypasses reminder-linked task interference.",
        "body": (
            "(A) CMR stores bidirectional associations between item features and context. "
            "Feature-to-context memory lets an item reinstate its associated context, whereas context-to-feature memory "
            "lets context cue candidate items. "
            "(B) When film-associated context cues items, film items and task items linked to that context can both receive support. "
            "When a film item reinstates context, retrieval targets context units instead, so task items are not competitors in that step. "
            "(C) In recognition, the test presents a candidate film item as the probe. The probe retrieves associated context, which is compared "
            "with ongoing test context; stronger matches provide stronger evidence that the item appeared in the film. "
            "(D) Old-film minus foil recognition evidence is plotted across the same reminder conditions and task encoding strengths used "
            "in the recall simulations. The measure subtracts mean evidence for film-source-matched foils from mean evidence for studied film probes. "
            "Strong task encoding after a film reminder does not produce a corresponding reduction in recognition-evidence separation."
        ),
        "top_caption_gap": 0.010,
    },
]


def save_caption_composite(image_path, output_base, title, body, top_caption_gap=TOP_CAPTION_GAP):
    image = plt.imread(str(image_path))
    image_aspect = image.shape[0] / image.shape[1]
    image_height = FIG_WIDTH * image_aspect
    body_lines = textwrap.wrap(body, width=WRAP_WIDTH)
    caption_height = 0.55 + 0.22 * max(1, len(body_lines))
    fig = plt.figure(figsize=(FIG_WIDTH, image_height + caption_height))
    image_bottom = caption_height / (image_height + caption_height)

    axis = fig.add_axes([0.0, image_bottom, 1.0, 1.0 - image_bottom])
    axis.imshow(image)
    axis.axis("off")

    y = image_bottom - top_caption_gap
    fig.text(0.02, y, title, fontsize=TITLE_FONTSIZE, fontweight="bold", ha="left", va="top")
    y -= TITLE_GAP
    for line in body_lines:
        fig.text(0.02, y, line, fontsize=BODY_FONTSIZE, ha="left", va="top")
        y -= LINE_STEP

    fig.savefig(f"{output_base}.png", bbox_inches="tight", dpi=600)
    fig.savefig(f"{output_base}.svg", bbox_inches="tight")
    plt.close(fig)


def main():
    CAPTION_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for item in CAPTIONED_FIGURES:
        save_caption_composite(
            item["image"],
            item["output"],
            item["title"],
            item["body"],
            item.get("top_caption_gap", TOP_CAPTION_GAP),
        )
        print(item["output"])


if __name__ == "__main__":
    main()
